"""Measure local search/save/load timings while verifying actual results."""

import argparse
from pathlib import Path
import platform
import statistics
import sys
import tempfile
import time


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from model.manager import PIMManager
from model.search import parse_criterion
from storage.pim_file import load_pim, save_pim


def measure(records: int, runs: int) -> list[str]:
    if records <= 0 or records % 4 or runs <= 0:
        raise ValueError("records must be a positive multiple of 4; runs must be positive")
    manager = PIMManager()
    for number in range(records // 4):
        manager.create_note(f"benchmark note {number}")
        manager.create_task(f"benchmark task {number}", "2026-01-01 09:00")
        manager.create_event(f"benchmark event {number}", "2026-01-02 10:00", "2026-01-02 09:00")
        manager.create_contact(f"Contact {number}", "Room 1", f"+00{number:05d}")
    criterion = parse_criterion('(type = "task" && deadline < "2026-01-02 00:00") || text contains "benchmark"')
    expected_ids = tuple(number for number in range(1, records + 1) if number % 4 in (1, 2))
    original = manager.list_all()
    lines = ["Local performance observations (not a course requirement or a timing guarantee)",
             f"Python: {platform.python_version()}", f"Platform: {platform.platform()}",
             f"Records: {records} ({records // 4} of each type); runs: {runs}",
             "Milliseconds: median / min / max; validation excluded from timed interval.",
             "Search excludes parsing; file writes include atomic replacement, not an fsync durability guarantee."]
    with tempfile.TemporaryDirectory(prefix="pim-benchmark-") as directory:
        path = Path(directory) / "benchmark.pim"
        for name, operation in (("search", lambda: manager.search(criterion)),
                                ("save", lambda: save_pim(manager, path)),
                                ("load", lambda: load_pim(path, 1))):
            timings = []
            for _ in range(runs):
                started = time.perf_counter()
                result = operation()
                timings.append((time.perf_counter() - started) * 1000)
                if name == "search":
                    if tuple(record.id for record in result) != expected_ids:
                        raise ValueError("search result IDs differ from the expected mixed dataset")
                else:
                    restored = load_pim(path, 1) if name == "save" else result
                    if restored.list_all() != original or restored.next_id != records + 1:
                        raise ValueError(f"{name} did not preserve every record field and next ID")
            lines.append(f"{name}: {statistics.median(timings):.3f} / {min(timings):.3f} / {max(timings):.3f} ms")
    lines.append("PASS: search IDs and all loaded fields/counters verified")
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--records", type=int, default=1000)
    parser.add_argument("--runs", type=int, default=5)
    args = parser.parse_args()
    try:
        lines = measure(args.records, args.runs)
    except ValueError as error:
        parser.error(str(error))
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
