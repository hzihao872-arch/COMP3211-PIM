"""Direct command-level SRS checks, with state and recovery assertions."""

import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from controller.cli import CommandController
from model.manager import PIMManager


class CLIRequirementTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.cwd = Path(directory.name)
        self.controller = CommandController(PIMManager(), self.cwd)

    def session(self, commands):
        output = io.StringIO()
        self.controller.run(io.StringIO(commands), output)
        return output.getvalue()

    def test_all_command_forms_accept_mixed_case(self):
        """FR-13: every command and all types accept case variations; values retain case."""
        output = self.session(
            'HeLp\nAdD NoTe "MiXeD"\nAdD TaSk "Task" "2026-01-01 00:00"\n'
            'AdD EvEnT "Event" "2026-01-01 00:00" "2026-01-02 00:00"\n'
            'AdD CoNtAcT "Name" "Road" "+001"\nLiSt\nLiSt NoTe\nShOw 1\n'
            'ShOw AlL\nUpDaTe 1 TeXt "Changed"\nSeArCh TyPe = "NoTe"\n'
            'SaVe "Case.pim"\nDeLeTe 1\nLoAd "Case.pim" FoRcE=TrUe\nExIt\n'
            'add note "must not execute"\n'
        )
        self.assertNotIn("Error:", output)
        for expected in ("add TYPE", "Created note 1", "Created task 2", "Created event 3",
                         "Created contact 4", "text: MiXeD", "Updated 1", "1 | note | Changed",
                         "Saved 4 PIR(s)", "Deleted 1", "Loaded 4 PIR(s)"):
            self.assertIn(expected, output)
        self.assertEqual(self.controller._manager.get(1).text, "Changed")
        self.assertEqual(self.controller._manager.next_id, 5)
        self.assertTrue((self.cwd / "Case.pim").is_file())

    def test_bad_quoting_and_escapes_recover_without_mutation(self):
        """FR-15: unmatched quotes and unsupported escapes reject the entire command."""
        self.session('add note "keep"\n')
        before = self.controller._manager.list_all(), self.controller._manager.next_id
        for bad in ('add note "unterminated', r'add note "bad\q"', r'update 1 text "bad\n"'):
            with self.subTest(command=bad):
                output = self.session(bad + '\nshow 1\n')
                self.assertEqual(output.count("Error: COMMAND:"), 1)
                self.assertIn("text: keep", output)
                self.assertEqual((self.controller._manager.list_all(), self.controller._manager.next_id), before)

    def test_show_each_type_prints_all_details(self):
        """FR-19: show ID exposes every stored field for each of the four types."""
        self.session('add note "memo"\nadd task "work" "2026-01-01 09:00"\n'
                     'add event "meet" "2026-01-02 10:00" "2026-01-01 08:00"\n'
                     'add contact "Li" "Room 1" "+00123"\n')
        expected = (
            "id: 1\ntype: note\ntext: memo",
            "id: 2\ntype: task\ndescription: work\ndeadline: 2026-01-01 09:00",
            "id: 3\ntype: event\ndescription: meet\nstart_time: 2026-01-02 10:00\nalarm_time: 2026-01-01 08:00",
            "id: 4\ntype: contact\nname: Li\naddress: Room 1\nmobile_number: +00123",
        )
        for record_id, details in enumerate(expected, 1):
            with self.subTest(record_id=record_id):
                self.assertEqual(self.session(f"show {record_id}\n"), f'pim> {details}\npim> Warning: unsaved changes will be lost; use save "PATH.pim" before exiting.\n')

    def test_empty_list_filter_and_show_all_have_clear_output(self):
        """FR-21: empty display paths produce an explicit message, without errors."""
        for command in ("list", "list task", "show all"):
            with self.subTest(command=command):
                self.assertEqual(self.session(command + "\n"), "pim> No PIRs.\npim> ")
        self.session('add note "memo"\n')
        self.assertEqual(self.session("list contact\n"), 'pim> No PIRs.\npim> Warning: unsaved changes will be lost; use save "PATH.pim" before exiting.\n')

    def test_each_failed_operation_preserves_state_and_returns_to_prompt(self):
        """FR-50/49: create/update/delete/search/save/load failures are atomic and recover."""
        self.session('add note "keep"\n')
        (self.cwd / "broken.pim").write_text("{", encoding="utf-8")
        (self.cwd / "keep.pim").write_bytes(b"original destination")
        before = self.controller._manager.list_all(), self.controller._manager.next_id
        for command, category in (
            ('add task "bad" "not a date"', "VALIDATION"),
            ('update 1 text ""', "VALIDATION"), ('delete 999', "NOT_FOUND"),
            ('search text contains "keep" &&', "SEARCH"), ('save "bad.txt"', "PATH"),
            ('save "missing/records.pim"', "IO"), ('load "missing.pim" force=true', "IO"),
            ('load "broken.pim" force=true', "FORMAT"), ('unknown', "COMMAND"),
        ):
            with self.subTest(command=command):
                output = self.session(command + '\nshow 1\n')
                self.assertEqual(output.count(f"Error: {category}:"), 1)
                self.assertIn("text: keep", output)
                self.assertEqual((self.controller._manager.list_all(), self.controller._manager.next_id), before)
        with patch("storage.pim_file.os.replace", side_effect=OSError("simulated disk failure")):
            output = self.session('save "keep.pim"\nshow 1\n')
        self.assertIn("Error: IO:", output)
        self.assertIn("text: keep", output)
        self.assertEqual((self.controller._manager.list_all(), self.controller._manager.next_id), before)
        self.assertEqual((self.cwd / "keep.pim").read_bytes(), b"original destination")
        self.assertEqual(list(self.cwd.glob("*.tmp")), [])
