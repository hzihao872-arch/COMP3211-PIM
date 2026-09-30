"""Exact command forms, output, quoting, and recovery (FR-12–FR-25, FR-49)."""

import io
import tempfile
import unittest
from pathlib import Path

from controller.cli import CommandController
from model.errors import ValidationError
from model.manager import PIMManager


class CLITests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.cwd = Path(self.directory.name)
        self.controller = CommandController(PIMManager(), self.cwd)

    def session(self, commands):
        output = io.StringIO()
        self.controller.run(io.StringIO(commands), output)
        return output.getvalue()

    def test_add_list_show_update_delete_and_help(self):
        output = self.session(
            'help\nADD NoTe "  hello world  "\nadd TASK "work" "2026-10-01 09:00"\n'
            'add event "meet" "2026-10-02 10:00" "2026-10-01 08:00"\n'
            'add contact "Li" "Room 1" "+00123"\nlist\nlist TASK\nshow 4\n'
            'update 2 DESCRIPTION "revised work"\nshow all\ndelete 1\nlist\nexit\n'
        )
        for expected in ('add TYPE', 'search EXPR', 'Created note 1', 'Created contact 4',
                         '1 | note | hello world', '2 | task | work', 'mobile_number: +00123',
                         'Updated 2', 'description: revised work', 'Deleted 1'):
            self.assertIn(expected, output)
        self.assertEqual([r.id for r in self.controller._manager.list_all()], [2, 3, 4])

    def test_search_compound_and_no_matches(self):
        output = self.session(
            'add note "memo"\nadd task "work" "2026-10-01 09:00"\n'
            'search (type = "task" && deadline < "2026-10-02 09:00") || text contains "memo"\n'
            'search type = "contact"\nexit\n'
        )
        self.assertIn('1 | note | memo', output)
        self.assertIn('2 | task | work', output)
        self.assertIn('No matching PIRs.', output)

    def test_errors_do_not_mutate_and_next_command_runs(self):
        output = self.session(
            'add note "good"\nupdate 1 text ""\nshow 1\n'
            'search type = "bad"\nshow 1\nshow 999\nadd note "bad\\n"\n'
            'unknown\nadd note "after"\nlist\nexit\n'
        )
        for category in ('VALIDATION', 'SEARCH', 'NOT_FOUND', 'COMMAND'):
            self.assertIn(f'Error: {category}:', output)
        self.assertEqual(self.controller._manager.get(1).text, 'good')
        self.assertEqual(self.controller._manager.get(2).text, 'after')
        self.assertEqual(output.count('text: good'), 2)

    def test_quote_escapes_argument_counts_ids_and_eof(self):
        output = self.session('add note "a \\"quote\\" and \\\\ slash"\nadd note one two\nshow 0\nlist badtype\n')
        self.assertEqual(self.controller._manager.get(1).text, 'a "quote" and \\ slash')
        self.assertIn('Error: COMMAND:', output)
        self.assertIn('Error: VALIDATION:', output)
        self.assertTrue(output.endswith('pim> '))

    def test_tab_separated_search_and_invalid_path_recover(self):
        output = self.session('add note memo\nsearch\ttype = "note"\nsave "bad\x00.pim"\nshow 1\nexit\n')
        self.assertIn('1 | note | memo', output)
        self.assertIn('Error: PATH:', output)
        self.assertIn('text: memo', output)

    def test_save_load_swap_and_failure_preserves_active_manager(self):
        output = self.session(
            'add note "old"\nsave "file.pim"\nadd note "new"\n'
            'load "missing.pim"\nlist\nload "file.pim"\nlist\n'
            'add note "after reload"\nshow 3\nexit\n'
        )
        self.assertIn('Saved 1 PIR(s)', output)
        self.assertIn('Error: IO:', output)
        self.assertIn('2 | note | new', output)
        self.assertIn('Loaded 1 PIR(s)', output)
        self.assertIn('text: after reload', output)
        self.assertEqual([r.id for r in self.controller._manager.list_all()], [1, 3])
        self.assertTrue((self.cwd / 'file.pim').exists())

    def test_constructor_rejects_invalid_dependencies(self):
        with self.assertRaises(ValidationError):
            CommandController(object(), self.cwd)
        with self.assertRaises(ValidationError):
            CommandController(PIMManager(), str(self.cwd))


if __name__ == '__main__':
    unittest.main()
