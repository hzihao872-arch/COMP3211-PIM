"""Exhaustion snapshots, BOM input and durable-write failure behavior."""

import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from controller.cli import CommandController
from model.manager import PIMManager
from model.schema import MAX_NEXT_ID, MAX_RECORD_ID
from storage.pim_file import PersistenceError, load_pim, save_pim


class StorageHardeningTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.cwd = Path(temp.name)
        self.path = self.cwd / "records.pim"

    def test_exhaustion_round_trip_and_restart_do_not_reuse_ids(self):
        """US10/11: the exhausted counter remains valid persisted state."""
        manager = PIMManager.from_rows([], MAX_RECORD_ID, 1)
        manager.create_note("last")
        save_pim(manager, self.path)
        restored = load_pim(self.path, 1)
        self.assertEqual(restored.next_id, MAX_NEXT_ID)
        self.assertEqual(restored.list_all(), manager.list_all())
        output = io.StringIO()
        CommandController(PIMManager(), self.cwd).run(
            io.StringIO('load "records.pim"\nadd note rejected\nshow all\nsave "copy.pim"\nexit\n'), output)
        self.assertIn("Error: VALIDATION: record IDs are exhausted", output.getvalue())
        self.assertIn("text: last", output.getvalue())
        self.assertNotIn("Warning:", output.getvalue())
        self.assertEqual(load_pim(self.cwd / "copy.pim", 1).next_id, MAX_NEXT_ID)

    def test_huge_counter_load_is_bounded_and_preserves_dirty_state(self):
        """The former 4,300-nine crash is rejected before swapping the manager."""
        self.path.write_text('{"format":"COMP3211-PIM","version":1,"next_id":'
                             + "9" * 4300 + ',"records":[]}', encoding="utf-8")
        manager = PIMManager()
        manager.create_note("keep")
        controller = CommandController(manager, self.cwd)
        output = io.StringIO()
        controller.run(io.StringIO('load "records.pim" force=true\nshow 1\nadd note after\nexit\n'), output)
        self.assertIn("Error: FORMAT:", output.getvalue())
        self.assertIn("text: keep", output.getvalue())
        self.assertIn("Created note 2", output.getvalue())
        self.assertIn("Warning:", output.getvalue())
        self.assertLess(len(output.getvalue()), 1600)
        self.assertIs(controller._manager, manager)

    def test_bom_is_accepted_and_writes_remain_without_bom(self):
        manager = PIMManager()
        manager.create_note("memo")
        save_pim(manager, self.path)
        original = self.path.read_bytes()
        self.assertFalse(original.startswith(b"\xef\xbb\xbf"))
        self.path.write_bytes(b"\xef\xbb\xbf" + original)
        self.assertEqual(load_pim(self.path, 1).list_all(), manager.list_all())
        self.path.write_bytes(b"\xff")
        with self.assertRaises(PersistenceError) as error:
            load_pim(self.path, 1)
        self.assertEqual(error.exception.category, "FORMAT")

    def test_record_errors_include_path_and_index_root_errors_do_not(self):
        root = {"format": "COMP3211-PIM", "version": 1, "next_id": 3,
                "records": [{"id": 1, "type": "note", "text": "valid"},
                            {"id": 2, "type": "note", "text": ""}]}
        for records, fragment in ((root["records"], "record #2"), (None, "records must be an array")):
            root["records"] = records
            self.path.write_text(json.dumps(root), encoding="utf-8")
            with self.assertRaises(PersistenceError) as error:
                load_pim(self.path, 1)
            self.assertIn("records.pim", str(error.exception))
            self.assertIn(fragment, str(error.exception))
            if records is None:
                self.assertNotIn("record #", str(error.exception))

    def test_flush_and_fsync_happen_before_replace(self):
        """US10: fsync sees the completed file before it is atomically published."""
        import os
        real_fsync, real_replace = os.fsync, os.replace
        order = []

        def fsync(descriptor):
            temporary, = self.cwd.glob(".pim-*.tmp")
            self.assertEqual(json.loads(temporary.read_text(encoding="utf-8"))["records"], [])
            self.assertFalse(self.path.exists())
            order.append("fsync")
            real_fsync(descriptor)

        def replace(source, destination):
            order.append("replace")
            real_replace(source, destination)

        with patch("storage.pim_file.os.fsync", side_effect=fsync), \
                patch("storage.pim_file.os.replace", side_effect=replace):
            save_pim(PIMManager(), self.path)
        self.assertEqual(order, ["fsync", "replace"])

    def test_fsync_failure_preserves_file_collection_and_dirty_flag(self):
        self.path.write_bytes(b"previous")
        manager = PIMManager()
        manager.create_note("keep")
        controller = CommandController(manager, self.cwd)
        before = manager.list_all(), manager.next_id
        output = io.StringIO()
        with patch("storage.pim_file.os.fsync", side_effect=OSError("sync failed")), \
                patch("storage.pim_file.os.replace") as replace:
            controller.run(io.StringIO('save "records.pim"\nload "records.pim"\nshow 1\nexit\n'), output)
        replace.assert_not_called()
        self.assertEqual(self.path.read_bytes(), b"previous")
        self.assertEqual((manager.list_all(), manager.next_id), before)
        self.assertEqual(list(self.cwd.glob(".pim-*.tmp")), [])
        self.assertIn("Error: IO:", output.getvalue())
        self.assertIn("unsaved changes", output.getvalue())
