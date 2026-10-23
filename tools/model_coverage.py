"""Run the full unittest suite and report standard-library trace line coverage for model."""

from __future__ import annotations

import platform
import sys
import trace
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src"
TESTS = ROOT / "tests"
MODEL = SOURCE / "model"


def _run_suite() -> unittest.result.TestResult:
    suite = unittest.defaultTestLoader.discover(
        start_dir=str(TESTS), top_level_dir=str(ROOT)
    )
    return unittest.TextTestRunner(verbosity=1).run(suite)


def main() -> int:
    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(SOURCE))

    tracer = trace.Trace(count=True, trace=False)
    previous_trace = sys.gettrace()
    try:
        result = tracer.runfunc(_run_suite)
    finally:
        sys.settrace(previous_trace)
    counts = tracer.results().counts
    executed: dict[Path, set[int]] = {}
    for (filename, line_number), count in counts.items():
        if count:
            executed.setdefault(Path(filename).resolve(), set()).add(line_number)

    print("Model line coverage (Python standard-library trace)")
    print(f"Python: {platform.python_version()}")
    print(f"OS: {platform.system()} {platform.release()}")
    print("Command: python tools/model_coverage.py")
    print(f"Tests: {result.testsRun}; failures: {len(result.failures)}; errors: {len(result.errors)}")
    print("Scope: src/model/*.py; subprocess CLI execution is outside trace scope")
    print("Method: trace executable source lines; non-source 0/None entries excluded")

    covered_total = 0
    executable_total = 0
    for source_file in sorted(MODEL.glob("*.py")):
        # CPython can emit 0/None bookkeeping entries. They are not source
        # lines, and cannot belong in a source-line coverage denominator.
        raw_lines = set(trace._find_executable_linenos(str(source_file)))
        executable = {line for line in raw_lines if isinstance(line, int) and line > 0}
        covered = len(executable & executed.get(source_file.resolve(), set()))
        covered_total += covered
        executable_total += len(executable)
        percentage = f"{covered / len(executable):.2%}" if executable else "n/a"
        print(f"{source_file.relative_to(SOURCE).as_posix()}: {covered}/{len(executable)} ({percentage})")
        missing = sorted(executable - executed.get(source_file.resolve(), set()))
        print("  Missing source lines: " + (", ".join(map(str, missing)) or "none"))
        print(f"  Excluded non-source entries: {len(raw_lines - executable)}")
    total_percentage = f"{covered_total / executable_total:.2%}" if executable_total else "n/a"
    print(f"TOTAL model: {covered_total}/{executable_total} ({total_percentage})")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
