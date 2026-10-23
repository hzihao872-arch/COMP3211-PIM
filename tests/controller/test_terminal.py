"""Peer-inspired regressions for safe output without changing stored data."""

import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from controller.cli import CommandController
from model.manager import PIMManager
from storage.pim_file import load_pim


class TerminalOutputTests(unittest.TestCase):
    def test_record_controls_are_visible_and_round_trip_unchanged(self):
        with tempfile.TemporaryDirectory() as directory:
            manager = PIMManager()
            original = "memo\x1b[2J\x00\b\x7f\x9b31m"
            manager.create_note(original)
            controller = CommandController(manager, Path(directory))
            output = io.StringIO()
            controller.run(io.StringIO('list\nshow all\nsearch type = "note"\n'
                                       'save "records.pim"\nexit\n'), output)
            rendered = output.getvalue()
            for char in ("\x1b", "\x00", "\b", "\x7f", "\x9b"):
                self.assertNotIn(char, rendered)
                self.assertIn(f"\\x{ord(char):02x}", rendered)
            self.assertEqual(load_pim(Path(directory) / "records.pim", 1).get(1).text,
                             original)

    def test_io_error_messages_cannot_emit_terminal_controls(self):
        controller = CommandController(PIMManager(), Path.cwd())
        output = io.StringIO()
        with patch("storage.pim_file.os.replace", side_effect=OSError("disk\x1b[31m\r\b")):
            with tempfile.TemporaryDirectory() as directory:
                controller = CommandController(PIMManager(), Path(directory))
                controller.run(io.StringIO('save "x.pim"\nadd note after\nexit\n'), output)
        self.assertNotIn("\x1b", output.getvalue())
        self.assertNotIn("\r", output.getvalue())
        self.assertNotIn("\b", output.getvalue())
        self.assertIn(r"disk\x1b[31m\x0d\x08", output.getvalue())
        self.assertIn("Created note 1", output.getvalue())

    def test_ascii_output_escapes_unicode_without_losing_the_record(self):
        manager = PIMManager()
        manager.create_note("中文 café 😀")
        raw = io.BytesIO()
        output = io.TextIOWrapper(raw, encoding="ascii", errors="strict")
        self.addCleanup(output.close)
        controller = CommandController(manager, Path.cwd())
        try:
            controller.run(io.StringIO("show 1\nadd note after\nexit\n"), output)
        except UnicodeEncodeError as error:
            self.fail(f"display encoding terminated the command session: {error}")
        output.flush()
        self.assertIn(br"\u4e2d\u6587 caf\xe9 \U0001f600", raw.getvalue())
        self.assertIn(b"Created note 2", raw.getvalue())
        self.assertEqual(manager.get(1).text, "中文 café 😀")

    def test_unicode_output_preserves_ordinary_text_and_prompt_flush(self):
        manager = PIMManager()
        manager.create_note("中文 café 😀")
        output = io.StringIO()
        CommandController(manager, Path.cwd()).run(io.StringIO("show 1\nexit\n"), output)
        self.assertEqual(output.getvalue(), 'pim> id: 1\ntype: note\ntext: 中文 café 😀\npim> Warning: unsaved changes will be lost; use save "PATH.pim" before exiting.\n')
