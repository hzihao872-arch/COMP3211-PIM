"""Real-process error status, safe stderr and shutdown with unavailable outputs."""

import os
from pathlib import Path
import subprocess
import sys
import unittest


MAIN = Path(__file__).resolve().parents[1] / "src" / "main.py"


class InputFailureProcessTests(unittest.TestCase):
    def run_failed_input(self, exception, close=()):
        script = (
            "import os, runpy, sys\n"
            "class FailedInput:\n"
            "    first = True\n"
            "    def readline(self):\n"
            "        if self.first:\n"
            "            self.first = False\n"
            "            return 'add note unsaved\\n'\n"
            f"        for name in {close!r}:\n"
            "            reader, writer = os.pipe()\n"
            "            os.close(reader)\n"
            "            os.dup2(writer, getattr(sys, name).fileno())\n"
            "            os.close(writer)\n"
            f"        raise {exception}\n"
            "sys.stdin = FailedInput()\n"
            f"sys.path.insert(0, {str(MAIN.parent)!r})\n"
            f"runpy.run_path({str(MAIN)!r}, run_name='__main__')\n"
        )
        return subprocess.run([sys.executable, "-c", script], capture_output=True, timeout=15,
                              env={**os.environ, "PYTHONIOENCODING": "ascii:strict"})

    def test_invalid_utf8_input_returns_one_without_traceback(self):
        result = subprocess.run([sys.executable, str(MAIN)], input=b"\xff\n", capture_output=True,
                                timeout=15, env={**os.environ, "PYTHONIOENCODING": "utf-8:strict"})
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn(b"Error: IO: cannot read input:", result.stderr)
        self.assertNotIn(b"Traceback", result.stderr)
        self.assertNotIn(b"Warning:", result.stdout)

    def test_dirty_read_errors_are_bounded_and_warn_once(self):
        for exception in ("OSError('device\\x1b' + '\\U0001f600' * 10**6)",
                          "UnicodeDecodeError('utf-8', b'\\xff', 0, 1, 'invalid')"):
            with self.subTest(exception=exception[:30]):
                result = self.run_failed_input(exception)
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn(b"Created note 1", result.stdout)
                self.assertEqual(result.stdout.count(b"Warning: unsaved changes"), 1)
                self.assertNotIn(b"Error:", result.stdout)
                self.assertIn(b"Error: IO: cannot read input:", result.stderr)
                self.assertNotIn(b"Traceback", result.stderr)
                self.assertNotIn(b"\x1b", result.stderr)
                self.assertLess(len(result.stderr), 1100)

    def test_unavailable_outputs_preserve_input_failure_exit_status(self):
        for close in (("stdout",), ("stderr",), ("stdout", "stderr")):
            with self.subTest(close=close):
                result = self.run_failed_input("OSError('input failed')", close)
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertNotIn(b"Traceback", result.stderr)
                self.assertNotIn(b"Exception ignored", result.stderr)
                if "stderr" not in close:
                    self.assertIn(b"Error: IO: cannot read input:", result.stderr)
