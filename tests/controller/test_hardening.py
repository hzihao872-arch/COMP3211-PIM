"""Bounded errors, complete data output and dirty interruption behavior."""

import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from controller.cli import CommandController
from controller.output import ClosedOutputPipe
from model.errors import PIMError
from model.manager import PIMManager
from model.schema import MAX_NEXT_ID, MAX_RECORD_ID
from storage.pim_file import PersistenceError
import main


class ControllerHardeningTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.cwd = Path(directory.name)

    def test_megabyte_invalid_inputs_are_bounded_and_session_recovers(self):
        """FR-49/50: errors do not echo entire tokens or mutate valid data."""
        huge = "x" * 10**6
        commands = (huge, "add " + huge, "show " + huge, "save " + huge,
                    'search type = "' + huge + '"', 'search "' + huge + '"',
                    "search " + huge + ' = "note"', 'update 1 ' + huge + ' value',
                    'search deadline < "' + huge + '"')
        for command in commands:
            with self.subTest(prefix=command[:20]):
                manager = PIMManager()
                manager.create_note("keep")
                output = io.StringIO()
                CommandController(manager, self.cwd).run(io.StringIO(command + '\nshow 1\nexit\n'), output)
                self.assertEqual(output.getvalue().count("Error:"), 1)
                self.assertLess(len(output.getvalue()), 1500)
                self.assertIn("text: keep", output.getvalue())
                self.assertEqual(manager.next_id, 2)
                if command.startswith("search"):
                    self.assertIn("at character", output.getvalue())

    def test_megabyte_os_error_is_safe_on_ascii_stdout(self):
        raw = io.BytesIO()
        output = io.TextIOWrapper(raw, encoding="ascii")
        self.addCleanup(output.close)
        with patch("storage.pim_file.Path.read_text", side_effect=OSError("\x1b\U0001f600" * 10**6)):
            CommandController(PIMManager(), self.cwd).run(
                io.StringIO('load "missing.pim"\nadd note after\nexit\n'), output)
        output.flush()
        self.assertLess(len(raw.getvalue()), 1500)
        self.assertNotIn(b"\x1b", raw.getvalue())
        self.assertIn(b"Created note 1", raw.getvalue())

    def test_full_megabyte_fields_remain_available_in_list_search_and_show(self):
        """FR-18/19/39: only diagnostics are abbreviated, never stored fields."""
        text = "z" * 10**6
        manager = PIMManager()
        manager.create_note(text)
        output = io.StringIO()
        CommandController(manager, self.cwd).run(io.StringIO('list\nsearch type = "note"\nshow 1\nexit\n'), output)
        self.assertEqual(output.getvalue().count(text), 3)

    def test_cli_ids_accept_last_id_reject_counter_marker_and_allow_leading_zeroes(self):
        manager = PIMManager.from_rows([{"id": MAX_RECORD_ID, "type": "note", "text": "last"}], MAX_NEXT_ID, 1)
        output = io.StringIO()
        CommandController(manager, self.cwd).run(
            io.StringIO(f'show {MAX_RECORD_ID}\nshow {MAX_NEXT_ID}\nshow ' + '9' * 5000
                        + '\nshow ' + '0' * 5000 + str(MAX_RECORD_ID) + '\nexit\n'), output)
        self.assertEqual(output.getvalue().count("text: last"), 2)
        self.assertEqual(output.getvalue().count("Error: COMMAND:"), 2)

    def test_expected_error_subclasses_share_category_handling(self):
        class NewExpectedError(PIMError):
            pass

        for error, category in ((NewExpectedError("new failure"), "APPLICATION"),
                                (PersistenceError("IO", "disk"), "IO")):
            output = io.StringIO()
            controller = CommandController(PIMManager(), self.cwd)
            with patch.object(controller, "_dispatch", side_effect=[error, True]):
                controller.run(io.StringIO("first\nexit\n"), output)
            self.assertIn(f"Error: {category}:", output.getvalue())

    def interrupt_session(self, commands, output):
        class InterruptedInput(io.StringIO):
            def readline(self):
                line = super().readline()
                if not line:
                    raise KeyboardInterrupt
                return line

        with patch("sys.stdin", InterruptedInput(commands)), patch("sys.stdout", output):
            return main.cli()

    def test_interrupt_warns_once_when_dirty_and_retains_exit_130(self):
        for commands, warnings in (("", 0), ("add note unsaved\n", 1)):
            output = io.StringIO()
            self.assertEqual(self.interrupt_session(commands, output), 130)
            self.assertEqual(output.getvalue().count("Warning: unsaved changes"), warnings)

    def test_interrupt_warning_handles_a_closed_output_pipe(self):
        class ClosedWarningOutput(io.StringIO):
            def write(self, text):
                if text.startswith("Warning:"):
                    raise ClosedOutputPipe("consumer closed")
                return super().write(text)

        self.assertEqual(self.interrupt_session("add note unsaved\n", ClosedWarningOutput()), 130)
