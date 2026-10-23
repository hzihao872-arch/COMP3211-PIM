"""Unsaved-data protection, focused help and recoverable command diagnostics."""

import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from controller.cli import CommandController
from model.manager import PIMManager
from storage.pim_file import save_pim


class UsabilityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.cwd = Path(self.temp.name)
        saved = PIMManager()
        saved.create_note("saved")
        save_pim(saved, self.cwd / "saved.pim")
        self.controller = CommandController(PIMManager(), self.cwd)

    def session(self, commands):
        output = io.StringIO()
        self.controller.run(io.StringIO(commands), output)
        return output.getvalue()

    def test_dirty_load_is_refused_and_record_remains_editable(self):
        output = self.session('add note unsaved\nload "saved.pim"\nshow 1\nupdate 1 text kept\n')
        self.assertIn("unsaved changes", output)
        self.assertIn("force=true", output)
        self.assertIn("text: unsaved", output)
        self.assertEqual(self.controller._manager.get(1).text, "kept")

    def test_forced_load_replaces_and_preserves_high_id_counter(self):
        output = self.session('add note first\nadd note second\nload "saved.pim" force=true\nshow all\nexit\n')
        self.assertNotIn("Error:", output)
        self.assertIn("text: saved", output)
        self.assertNotIn("Warning:", output)
        self.assertEqual(self.controller._manager.next_id, 3)

    def test_successful_save_clears_dirty_state(self):
        output = self.session('add note unsaved\nsave "new.pim"\nload "saved.pim"\nexit\n')
        self.assertNotIn("Error:", output)
        self.assertNotIn("Warning:", output)
        self.assertEqual(self.controller._manager.get(1).text, "saved")

    def test_failed_save_keeps_unsaved_protection(self):
        with patch("storage.pim_file.os.replace", side_effect=PermissionError("denied")):
            output = self.session('add note keep\nsave "new.pim"\nload "saved.pim"\n')
        self.assertIn("Error: IO:", output)
        self.assertIn("unsaved changes", output)
        self.assertEqual(self.controller._manager.get(1).text, "keep")

    def test_failed_forced_load_keeps_state_counter_and_dirty_flag(self):
        output = self.session('add note keep\nload "missing.pim" force=true\nload "saved.pim"\n')
        self.assertIn("Error: IO:", output)
        self.assertIn("unsaved changes", output)
        self.assertEqual(self.controller._manager.get(1).text, "keep")
        self.assertEqual(self.controller._manager.next_id, 2)

    def test_failed_mutations_and_read_commands_do_not_dirty_a_loaded_session(self):
        output = self.session('load "saved.pim"\nupdate 1 text ""\ndelete 999\n'
                              'add task bad nope\nhelp search\nshow all\nsearch type = "note"\nexit\n')
        self.assertNotIn("Warning:", output)
        self.assertEqual(output.count("Error:"), 3)

    def test_update_and_delete_each_mark_the_session_dirty(self):
        for mutation in ('update 1 text changed', 'delete 1'):
            with self.subTest(mutation=mutation):
                self.controller = CommandController(PIMManager(), self.cwd)
                output = self.session(f'load "saved.pim"\n{mutation}\nload "saved.pim"\n')
                self.assertIn("unsaved changes", output)
                self.assertIn("Error: COMMAND:", output)

    def test_invalid_force_options_do_not_bypass_protection(self):
        self.session('add note keep\n')
        for option in ('force=yes', 'force=true extra', 'force=true force=true', 'other=true'):
            with self.subTest(option=option):
                output = self.session(f'load "saved.pim" {option}\n')
                self.assertIn("Error: COMMAND:", output)
                self.assertEqual(self.controller._manager.get(1).text, "keep")
        self.assertIn("unsaved changes", self.session('load "saved.pim" force=false\n'))

    def test_exit_and_eof_warn_once_without_saving_or_blocking(self):
        for ending in ('exit\nadd note never\n', ''):
            with self.subTest(ending=ending):
                self.controller = CommandController(PIMManager(), self.cwd)
                output = self.session('add note keep\n' + ending)
                self.assertEqual(output.count("Warning: unsaved changes"), 1)
                self.assertEqual(len(self.controller._manager.list_all()), 1)
                self.assertFalse((self.cwd / "new.pim").exists())

    def test_help_topics_cover_every_command_without_mutation(self):
        for topic in ('help','add','list','show','update','delete','search','save','load','exit'):
            with self.subTest(topic=topic):
                output = self.session(f'HeLp {topic.upper()}\n')
                self.assertNotIn("Error:", output)
                self.assertIn("Usage:", output)
                self.assertIn("Example:", output)
                self.assertIn(topic, output.lower())
        self.assertEqual(self.controller._manager.next_id, 1)

    def test_help_and_wrong_arguments_offer_a_recovery_path(self):
        output = self.session('help nonexistent\nupdate 1\nhelp load\n')
        self.assertEqual(output.count("Error: COMMAND:"), 2)
        self.assertIn('update ID FIELD "VALUE"', output)
        self.assertIn("force=true", output)
        self.assertIn("help", output)

    def test_bad_command_quote_has_one_based_position(self):
        for prefix in ('', '  '):
            output = self.session(prefix + 'add note "unclosed\nhelp add\n')
            self.assertIn(f"character {10 + len(prefix)}", output)
            self.assertIn("Usage:", output)

    def test_clean_load_accepts_false_and_force_flags_ignore_case(self):
        output = self.session('load "saved.pim" force=false\nupdate 1 text changed\n'
                              'load "saved.pim" FoRcE=TrUe\nexit\n')
        self.assertNotIn("Error:", output)
        self.assertNotIn("Warning:", output)
        self.assertEqual(self.controller._manager.get(1).text, "saved")
