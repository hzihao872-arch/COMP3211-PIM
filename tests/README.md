# Testing Guide

Use the Python standard-library `unittest` framework. Model tests belong in `tests/model/` and mirror their corresponding module names, for example:

```text
src/model/records.py -> tests/model/test_records.py
src/model/search.py  -> tests/model/test_search.py
```

Each test should make its exercised behavior and expected result clear through its name, short comments or docstring where useful, and assertions.

Run all tests from the repository root:

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m unittest discover -s tests -t . -v
```

The explicit `-t .` keeps `tests/model` from shadowing `src/model`. Storage and controller tests live in their own subdirectories; `tests/test_acceptance.py` runs the actual CLI process. The final submission also needs a separate line-coverage report for the `model` package.

The earlier usability revision had 86 methods. The current source adds hardening cases in `tests/model/test_hardening.py`, `tests/storage/test_hardening.py`, `tests/controller/test_hardening.py` and `tests/test_process_boundaries.py`; see the current source hardening report for counts and execution results. `tests/controller/test_usability.py` covers unsaved protection and focused help; `tests/model/test_search_positions.py` covers positioned search failures. `tests/controller/test_terminal.py` covers display controls and encodings, `tests/test_process_boundaries.py` exercises actual subprocess exits, and `tests/tools/test_evidence.py` ensures incorrect evidence fails. Include the maintained `media/demo` text files when copying the source; the demo tool and its tests use them. Reproduce the walkthrough with `python tools/verify_demo.py` and measured mixed-record timings with `python tools/benchmark.py`.

`tests/controller/test_input_failures.py` verifies no retry/state change and best-effort warnings. `tests/test_input_failures.py` checks real stdin decoding failure, bounded stderr, nonzero status and unavailable output pipes. The input error check in `test_process_boundaries.py` also forbids a traceback. Current execution results are in `docs/reports/input-io-fix-2026-10-23.md`.
