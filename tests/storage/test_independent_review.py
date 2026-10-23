"""Independent malformed-file regression checks (US11, FR-44/47/49)."""

import io
import tempfile
import unittest
from pathlib import Path

from controller.cli import CommandController
from model.manager import PIMManager
from storage.pim_file import PersistenceError, load_pim


class MalformedSnapshotTests(unittest.TestCase):
    def test_excessive_json_nesting_reports_format_error(self):
        """An invalid nested snapshot must fail through the storage API contract."""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nested.pim"
            path.write_text("[" * 2000 + "0" + "]" * 2000, encoding="utf-8")
            with self.assertRaises(PersistenceError) as error:
                load_pim(path, 1)
            self.assertEqual(error.exception.category, "FORMAT")

    def test_excessive_nesting_preserves_state_and_session(self):
        """Rejected load retains the manager and permits show/add after the error."""
        with tempfile.TemporaryDirectory() as directory:
            cwd = Path(directory)
            (cwd / "nested.pim").write_text("[" * 2000 + "0" + "]" * 2000,
                                           encoding="utf-8")
            manager = PIMManager()
            original = manager.create_note("keep")
            controller = CommandController(manager, cwd)
            output = io.StringIO()
            controller.run(io.StringIO('load "nested.pim"\nshow 1\nadd note after\nexit\n'),
                           output)
            self.assertEqual(output.getvalue().count("Error: FORMAT:"), 1)
            self.assertIn("text: keep", output.getvalue())
            self.assertIn("Created note 2", output.getvalue())
            self.assertIs(controller._manager, manager)
            self.assertIs(manager.get(1), original)
            self.assertEqual(manager.get(2).text, "after")
            self.assertEqual(manager.next_id, 3)
