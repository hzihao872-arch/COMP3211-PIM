"""Versioned .pim round trips and failure atomicity (US10/US11)."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from model.manager import PIMManager
from storage.pim_file import PersistenceError, load_pim, save_pim


class PersistenceTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "records.pim"

    def test_round_trip_four_types_and_preserve_higher_counter(self):
        manager = PIMManager()
        manager.create_note("memo")
        manager.create_task("task", "2026-10-01 09:00")
        manager.create_event("event", "2026-10-02 10:00", "2026-10-01 08:00")
        manager.create_contact("Li", "Room 1", "+00123")
        save_pim(manager, self.path)
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertEqual(set(raw), {"format", "version", "next_id", "records"})
        self.assertEqual(raw["format"], "COMP3211-PIM")
        self.assertEqual(raw["version"], 1)
        self.assertEqual(raw["records"][2]["start_time"], "2026-10-02 10:00")
        restored = load_pim(self.path, 10)
        self.assertEqual(restored.list_all(), manager.list_all())
        self.assertEqual(restored.next_id, 10)
        self.assertEqual(manager.next_id, 5)

    def test_reject_missing_invalid_and_duplicate_json(self):
        with self.assertRaises(PersistenceError) as error:
            load_pim(self.path, 1)
        self.assertEqual(error.exception.category, "IO")
        samples = (
            '{',
            '{"format":"COMP3211-PIM","format":"COMP3211-PIM","version":1,"next_id":1,"records":[]}',
            '{"format":"COMP3211-PIM","version":1,"next_id":NaN,"records":[]}',
            '{"format":"COMP3211-PIM","version":2,"next_id":1,"records":[]}',
            '{"format":"COMP3211-PIM","version":true,"next_id":1,"records":[]}',
            '{"format":"COMP3211-PIM","version":1,"next_id":2,"records":[{"id":1,"type":"task","description":"x","deadline":"bad"}]}',
            '{"format":"COMP3211-PIM","version":1,"next_id":2,"records":[{"id":1,"type":"note","text":"x"},{"id":1,"type":"note","text":"y"}]}',
            '{"format":"COMP3211-PIM","version":1,"next_id":1,"records":[{"id":1,"type":"note","text":"x"}]}',
        )
        for sample in samples:
            with self.subTest(sample=sample):
                self.path.write_text(sample, encoding="utf-8")
                with self.assertRaises(PersistenceError) as error:
                    load_pim(self.path, 1)
                self.assertEqual(error.exception.category, "FORMAT")

    def test_wrong_extension_and_failed_save_preserve_existing_bytes(self):
        manager = PIMManager()
        manager.create_note("memo")
        with self.assertRaises(PersistenceError) as error:
            save_pim(manager, self.path.with_suffix(".PIM"))
        self.assertEqual(error.exception.category, "PATH")
        self.path.write_bytes(b"original")
        with patch("storage.pim_file.os.replace", side_effect=OSError("denied")):
            with self.assertRaises(PersistenceError) as error:
                save_pim(manager, self.path)
        self.assertEqual(error.exception.category, "IO")
        self.assertEqual(self.path.read_bytes(), b"original")
        self.assertEqual(list(self.path.parent.glob("*.tmp")), [])


if __name__ == "__main__":
    unittest.main()
