"""Real-process CLI paths covering all official US1–US11 and recovery."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


_MAIN = Path(__file__).resolve().parents[1] / "src" / "main.py"


def run_cli(commands: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(_MAIN)], input=commands, text=True,
                          capture_output=True, cwd=cwd, timeout=10, check=False)


class AcceptanceTests(unittest.TestCase):
    def test_all_stories_across_save_and_restart(self):
        with tempfile.TemporaryDirectory() as directory:
            cwd = Path(directory)
            first = run_cli(
                'add note "memo"\nadd task "team task" "2026-10-01 09:00"\n'
                'add event "meeting" "2026-10-02 10:00" "2026-10-01 08:00"\n'
                'add contact "Li" "Room 1" "+00123"\n'
                'search (type = "task" && deadline < "2026-10-02 09:00") || !name contains "Li"\n'
                'show 2\nupdate 2 description "revised task"\nshow all\ndelete 1\n'
                'save "snapshot.pim"\nexit\n', cwd)
            self.assertEqual(first.returncode, 0, first.stderr)
            for fragment in ('Created note 1', 'Created task 2', 'Created event 3',
                             'Created contact 4', '2 | task | team task',
                             'description: revised task', 'Deleted 1', 'Saved 3 PIR(s)'):
                self.assertIn(fragment, first.stdout)
            self.assertTrue((cwd / 'snapshot.pim').exists())
            second = run_cli('load "snapshot.pim"\nlist\nshow 4\nexit\n', cwd)
            self.assertEqual(second.returncode, 0, second.stderr)
            for fragment in ('Loaded 3 PIR(s)', '2 | task | revised task',
                             '3 | event | meeting', '4 | contact | Li', 'mobile_number: +00123'):
                self.assertIn(fragment, second.stdout)

    def test_invalid_input_recovers_in_real_process(self):
        with tempfile.TemporaryDirectory() as directory:
            result = run_cli('add note "keep"\nupdate 1 text ""\nsearch bad = "x"\n'
                             'load "missing.pim"\nshow 1\nexit\n', Path(directory))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('Error: VALIDATION:', result.stdout)
            self.assertIn('Error: SEARCH:', result.stdout)
            self.assertIn('Error: IO:', result.stdout)
            self.assertIn('text: keep', result.stdout)


if __name__ == '__main__':
    unittest.main()
