"""Fatal input failures preserve records and do not retry an unusable stream."""

import io
from pathlib import Path
import unittest

from controller.cli import CommandController, InputReadError
from model.manager import PIMManager


class InputFailureTests(unittest.TestCase):
    def test_read_failures_preserve_state_and_stop_reading(self):
        for error in (OSError("input failed"), UnicodeDecodeError("utf-8", b"\xff", 0, 1, "invalid")):
            with self.subTest(error=type(error).__name__):
                manager = PIMManager()
                manager.create_note("keep")
                before = manager.list_all(), manager.next_id
                controller = CommandController(manager, Path.cwd())

                class FailedInput:
                    calls = 0

                    def readline(self):
                        self.calls += 1
                        raise error

                source = FailedInput()
                output = io.StringIO()
                with self.assertRaises(InputReadError) as failure:
                    controller.run(source, output)
                self.assertEqual(source.calls, 1)
                self.assertIs(failure.exception.__cause__, error)
                self.assertEqual((manager.list_all(), manager.next_id), before)
                self.assertTrue(controller._dirty)
                self.assertEqual(output.getvalue().count("Warning: unsaved changes"), 1)

    def test_clean_read_failure_has_no_dirty_warning(self):
        class FailedInput:
            def readline(self):
                raise OSError("input failed")

        output = io.StringIO()
        with self.assertRaisesRegex(InputReadError, "cannot read input"):
            CommandController(PIMManager(), Path.cwd()).run(FailedInput(), output)
        self.assertNotIn("Warning:", output.getvalue())

    def test_warning_failure_cannot_mask_input_failure(self):
        class FailedInput:
            def readline(self):
                raise OSError("original input failure")

        for warning_error in (OSError("output failed"), UnicodeEncodeError("ascii", "中", 0, 1, "invalid")):
            class FailedWarning(io.StringIO):
                def write(self, text):
                    if text.startswith("Warning:"):
                        raise warning_error
                    return super().write(text)

            manager = PIMManager()
            manager.create_note("keep")
            with self.assertRaisesRegex(InputReadError, "original input failure"):
                CommandController(manager, Path.cwd()).run(FailedInput(), FailedWarning())

    def test_unexpected_read_exception_still_propagates(self):
        class DefectiveInput:
            def readline(self):
                raise RuntimeError("programming defect")

        with self.assertRaisesRegex(RuntimeError, "programming defect"):
            CommandController(PIMManager(), Path.cwd()).run(DefectiveInput(), io.StringIO())
