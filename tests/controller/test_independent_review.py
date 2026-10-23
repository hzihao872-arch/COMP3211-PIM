"""Prompt visibility at the stream boundary, independently of StringIO tests."""

import io
import unittest
from pathlib import Path

from controller.cli import CommandController
from model.manager import PIMManager


class PromptVisibilityTests(unittest.TestCase):
    def test_prompt_is_visible_before_waiting_for_each_command(self):
        """A line-buffered terminal must receive its prompt before input blocks."""
        raw_output = io.BytesIO()
        output = io.TextIOWrapper(raw_output, encoding="utf-8", line_buffering=True)
        self.addCleanup(output.close)
        testcase = self

        class CheckingInput(io.StringIO):
            def readline(self, *args):
                testcase.assertTrue(raw_output.getvalue().endswith(b"pim> "),
                                    "prompt must be flushed before reading input")
                return super().readline(*args)

        controller = CommandController(PIMManager(), Path.cwd())
        controller.run(CheckingInput('unknown\nadd note kept\nexit\n'), output)
        self.assertEqual(raw_output.getvalue().count(b"pim> "), 3)
        self.assertIn(b"Error: COMMAND:", raw_output.getvalue())
        self.assertEqual(controller._manager.get(1).text, "kept")
