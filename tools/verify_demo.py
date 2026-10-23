"""Verify the maintained two-process demo without touching a user's snapshots."""

import argparse
import difflib
import os
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]


def verify_demo(commands: Path, expected: Path) -> str:
    sessions: list[list[str]] = []
    for line in commands.read_text(encoding="utf-8-sig").splitlines():
        if line.startswith("# SESSION"):
            sessions.append([])
        elif line.strip() and not line.lstrip().startswith("#"):
            if not sessions:
                raise ValueError("commands must begin with a # SESSION marker")
            sessions[-1].append(line)
    if len(sessions) != 2 or any(not block or block[-1] != "exit" for block in sessions):
        raise ValueError("demo must contain two sessions, each ending with exit")

    with tempfile.TemporaryDirectory(prefix="pim-demo-") as directory:
        outputs = []
        for number, block in enumerate(sessions, 1):
            result = subprocess.run(
                [sys.executable, str(ROOT / "src/main.py")], cwd=directory,
                input="\n".join(block) + "\n", capture_output=True, text=True,
                encoding="utf-8", env={**os.environ, "PYTHONIOENCODING": "utf-8"}, timeout=30,
            )
            if result.returncode or result.stderr or "Error:" in result.stdout:
                raise ValueError(f"session {number}: command failed\n{result.stderr}{result.stdout}")
            outputs.append(f"SESSION {number} exit={result.returncode}\n{result.stdout}")
        actual = "\n".join(outputs).replace(directory, "<DEMO_DIR>")
    # Platform path separator and trailing prompt spaces are presentation-only.
    def normalize(text: str) -> str:
        return "\n".join(line.rstrip() for line in text.replace("<DEMO_DIR>/", "<DEMO_DIR>\\").splitlines()).strip()

    wanted = normalize(expected.read_text(encoding="utf-8-sig"))
    actual = normalize(actual)
    if actual != wanted:
        diff = "\n".join(difflib.unified_diff(wanted.splitlines(), actual.splitlines(),
                                            fromfile="expected", tofile="actual", lineterm=""))
        raise ValueError(f"transcript mismatch\n{diff}")
    return actual


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commands", type=Path, default=ROOT / "media/demo/demo-commands.txt")
    parser.add_argument("--expected", type=Path, default=ROOT / "media/demo/demo-expected-output.txt")
    args = parser.parse_args()
    try:
        transcript = verify_demo(args.commands, args.expected)
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(transcript)
    print("PASS: 2 fresh CLI processes match the complete expected transcript")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
