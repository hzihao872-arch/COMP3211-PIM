"""Evidence tools must reject mismatches rather than report a false pass."""

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]


class EvidenceToolTests(unittest.TestCase):
    def run_tool(self, name, cwd, *args):
        return subprocess.run([sys.executable, str(ROOT / "tools" / name), *args],
                              cwd=cwd, capture_output=True, text=True, encoding="utf-8",
                              env={**os.environ, "PYTHONIOENCODING": "utf-8"}, timeout=30)

    def test_demo_runs_from_another_directory_without_leaving_a_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            sentinel = Path(directory) / "snapshot.pim"
            sentinel.write_bytes(b"keep user data")
            result = self.run_tool("verify_demo.py", directory)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("PASS: 2 fresh CLI processes match the complete expected transcript", result.stdout)
            self.assertEqual(sentinel.read_bytes(), b"keep user data")
            self.assertEqual(list(Path(directory).iterdir()), [sentinel])

    def test_demo_rejects_incorrect_expected_output(self):
        with tempfile.TemporaryDirectory() as directory:
            expected = Path(directory) / "expected.txt"
            original = (ROOT / "media/demo/demo-expected-output.txt").read_text(encoding="utf-8")
            expected.write_text(original.replace("Created note 5", "Created note 999"), encoding="utf-8")
            result = self.run_tool("verify_demo.py", directory, "--expected", str(expected))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("transcript mismatch", result.stderr)
            self.assertNotIn("PASS:", result.stdout)

    def test_demo_rejects_invalid_command(self):
        with tempfile.TemporaryDirectory() as directory:
            commands = Path(directory) / "commands.txt"
            original = (ROOT / "media/demo/demo-commands.txt").read_text(encoding="utf-8")
            commands.write_text(original.replace('add note "memo"', "not-a-command"), encoding="utf-8")
            result = self.run_tool("verify_demo.py", directory, "--commands", str(commands))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("command failed", result.stderr)

    def test_benchmark_checks_mixed_data_and_rejects_invalid_sizes(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_tool("benchmark.py", directory, "--records", "20", "--runs", "2")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Records: 20 (5 of each type); runs: 2", result.stdout)
            self.assertIn("PASS: search IDs and all loaded fields/counters verified", result.stdout)
            self.assertEqual(list(Path(directory).iterdir()), [])
            for count in ("0", "3", "-4"):
                with self.subTest(count=count):
                    invalid = self.run_tool("benchmark.py", directory, "--records", count)
                    self.assertNotEqual(invalid.returncode, 0)
                    self.assertNotIn("PASS:", invalid.stdout)
