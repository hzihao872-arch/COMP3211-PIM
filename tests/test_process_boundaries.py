"""Real process exit and encoding checks, including Windows pipe behavior."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


MAIN = Path(__file__).resolve().parents[1] / "src" / "main.py"


class ProcessBoundaryTests(unittest.TestCase):
    def test_loaded_unicode_can_be_displayed_on_ascii_stdout(self):
        with tempfile.TemporaryDirectory() as directory:
            data = {"format": "COMP3211-PIM", "version": 1, "next_id": 2,
                    "records": [{"id": 1, "type": "note", "text": "中文 😀"}]}
            Path(directory, "unicode.pim").write_text(json.dumps(data), encoding="utf-8")
            result = subprocess.run([sys.executable, str(MAIN)], cwd=directory,
                                    input=b'load "unicode.pim"\nshow 1\nadd note after\nexit\n',
                                    env={**os.environ, "PYTHONIOENCODING": "ascii:strict"},
                                    capture_output=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stderr, b"")
            self.assertIn(br"\u4e2d\u6587 \U0001f600", result.stdout)
            self.assertIn(b"Created note 2", result.stdout)

    def test_keyboard_interrupt_exits_without_traceback(self):
        # Inject at readline in a real process: sending Windows console events
        # would also interrupt the parent test runner's console group.
        script = (
            "import runpy, sys\n"
            "class InterruptedInput:\n"
            "    def readline(self): raise KeyboardInterrupt\n"
            "sys.stdin = InterruptedInput()\n"
            f"sys.path.insert(0, {str(MAIN.parent)!r})\n"
            f"runpy.run_path({str(MAIN)!r}, run_name='__main__')\n"
        )
        result = subprocess.run([sys.executable, "-c", script], capture_output=True, timeout=15)
        self.assertEqual(result.returncode, 130, result.stderr)
        self.assertNotIn(b"Traceback", result.stderr)

    def test_closed_stdout_pipe_exits_without_traceback(self):
        with tempfile.TemporaryFile(mode="w+b") as commands:
            commands.write(b"help\n" * 1000)
            commands.seek(0)
            process = subprocess.Popen([sys.executable, "-u", str(MAIN)], stdin=commands,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process.stdout.close()
            try:
                status = process.wait(timeout=15)
                errors = process.stderr.read()
            finally:
                if process.poll() is None:
                    process.kill()
                    process.wait()
                process.stderr.close()
            self.assertEqual(status, 0, errors)
            self.assertEqual(errors, b"")

    def test_unrelated_output_error_is_not_silently_swallowed(self):
        script = (
            "import runpy, sys\n"
            "class FailedOutput:\n"
            "    def write(self, text): raise OSError(5, 'unrelated device failure')\n"
            "    def flush(self): pass\n"
            "sys.stdout = FailedOutput()\n"
            f"sys.path.insert(0, {str(MAIN.parent)!r})\n"
            f"runpy.run_path({str(MAIN)!r}, run_name='__main__')\n"
        )
        result = subprocess.run([sys.executable, "-c", script], capture_output=True, timeout=15)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b"unrelated device failure", result.stderr)

    def test_input_error_is_not_mistaken_for_a_closed_output_pipe(self):
        script = (
            "import errno, runpy, sys\n"
            "class FailedInput:\n"
            "    def readline(self): raise OSError(errno.EINVAL, 'unrelated input device failure')\n"
            "sys.stdin = FailedInput()\n"
            f"sys.path.insert(0, {str(MAIN.parent)!r})\n"
            f"runpy.run_path({str(MAIN)!r}, run_name='__main__')\n"
        )
        result = subprocess.run([sys.executable, "-c", script], capture_output=True, timeout=15)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b"unrelated input device failure", result.stderr)
