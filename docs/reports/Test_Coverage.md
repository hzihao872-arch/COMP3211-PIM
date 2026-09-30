# Model Test Coverage Report — COMP3211 PIM

**Group:** 89; member names and student IDs await human input.

**Frozen product and test commit:** `4d3508db0447a3ac6346a2a2789da89208f88fd5` (2026-09-30).
**Evidence:** `docs/reports/model-coverage-raw.txt`, `docs/reports/code-freeze.md`, and `docs/reports/integration-test-log.md`. The course requires a separate model line-coverage report in the submitted source-code root; WP08 must place the final PDF there. This Markdown is the maintained report source.

## 1. Environment and method

WP04 ran on Windows 11 with Python 3.13.5 and 3.12.3. The test framework is Python's standard-library `unittest`. The coverage tool is `tools/model_coverage.py`, using the standard-library `trace` module. Python 3.11 was unavailable and remains unverified.

From the repository root, WP04 used:

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m unittest discover -s tests -t . -v
py -3.12 -m unittest discover -s tests -t . -q
python tools/model_coverage.py
python -m compileall -q src tests tools
```

The explicit `-t .` prevents `tests/model` from shadowing `src/model`. `tools/model_coverage.py` discovers and runs the full suite under `trace`, intersects traced line numbers with `trace._find_executable_linenos` for every `src/model/*.py` file, and prints covered/executable counts and percentages. No third-party coverage package or IDE coverage view generated the submitted figures.

## 2. Observed WP04 results

| Check | Observed result |
|---|---|
| Python 3.13.5 full suite | 33 tests; 0 failures; 0 errors. |
| Python 3.12.3 full suite | 33 tests; 0 failures; 0 errors. |
| Python 3.13.5 model line coverage | 411/430 executable lines; 95.58%. |
| Compile check | Exit code 0. |
| Manual CLI acceptance | Two separate processes created, searched, updated, deleted, saved, loaded, and continued with next ID 5; both exit codes 0. |

The raw coverage output reports:

| Model module | Covered/executable lines | Line coverage | Uncovered entries |
|---|---:|---:|---:|
| `model/__init__.py` | 0/1 | 0.00% | 1 |
| `model/errors.py` | 4/5 | 80.00% | 1 |
| `model/manager.py` | 92/97 | 94.85% | 5 |
| `model/records.py` | 57/58 | 98.28% | 1 |
| `model/search.py` | 224/233 | 96.14% | 9 |
| `model/validation.py` | 34/36 | 94.44% | 2 |
| **Total model** | **411/430** | **95.58%** | **19** |

The full raw text is retained in `docs/reports/model-coverage-raw.txt`; these values are copied exactly, without replacing the tool's denominator or rounding its module percentages. The reported coverage is **model-only**. The suite also contains controller, storage, and real-process acceptance tests, but those packages are outside the model numerator and denominator. The acceptance tests launch a new CLI subprocess, whose executed lines are outside the parent `trace` session. Thus this report does not claim controller, storage, subprocess CLI, branch, condition, or mutation coverage.

## 3. Uncovered-line explanation

A read-only repeat of the frozen tool's line accounting showed the 19 unexecuted entries below. Python's `trace._find_executable_linenos` includes bookkeeping keys `0` or `None` in these files; they have no corresponding executable source statement. They account for nine denominator entries: one each in `model/__init__.py`, `errors.py`, and `records.py`, and two each in `manager.py`, `search.py`, and `validation.py`. The `model/__init__.py` file contains only a docstring, so its single counted entry is untraced. These entries are retained because WP04's raw calculation includes them.

The remaining ten entries correspond to actual frozen source lines:

| Source | Untraced line(s) | Explanation |
|---|---|---|
| `model/manager.py::PIMManager.update` | 70 | The `field_name` non-string rejection branch was not reached by the 33 tests; CLI fields arrive as strings. |
| `model/manager.py::PIMManager.from_rows` | 95 | Direct non-array `rows` input to the model constructor was not exercised; file loading checks for an array in `storage/pim_file.py::load_pim` first. |
| `model/manager.py::PIMManager.from_rows` | 101 | Direct non-mapping record input was not exercised; the tests use malformed mappings and other file errors. |
| `model/search.py::OrCriterion.__post_init__` | 98 | The tests construct a valid `OrCriterion`, but do not pass it a non-criterion operand. |
| `model/search.py::_tokenize` | 185 | The invalid-character branch was not reached by the sampled malformed search expressions. |
| `model/search.py::_Parser._accept` | 205–209 | This helper is present in the frozen parser but the iterative parse path never calls it; all five counted lines remain untraced. |

The source-line numbers above are from freeze commit `4d3508d`; line numbers in a later edited source could differ. The untraced branches show limits of the automated suite, not observed failures of those behaviors. The `_accept` helper is unused in the frozen product path. No official minimum coverage percentage is specified in the Project Description PDF.

## 4. Test scope and remaining verification

The 33-test suite includes `tests/model/test_records.py`, `test_manager.py`, `test_search.py`, and `test_search_integration.py`; it also includes controller, storage, and real-process acceptance tests. WP04's two-process manual session independently exercised the user-facing path, and its import audit found only standard-library or local source imports. `docs/reports/Requirements_Coverage.md` records requirement-level tests and direct-check gaps. Python 3.11 remains a requirement target without a passing run; neither the 3.12.3 nor the 3.13.5 result proves it.
