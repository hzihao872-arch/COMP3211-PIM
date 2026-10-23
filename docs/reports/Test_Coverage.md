# Model Test Coverage Report - COMP3211 PIM

**Group:** 89. **Revision:** independent review, 2026-10-23.
**Delivery:** current candidate files identified by the manifest. Application fixes and tests are included; the old source commit is not the complete delivery.

## 1. Reproduce the full suite

From the submitted `03_Implementation` folder in PowerShell:

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m unittest discover -s tests -t . -v
python tools/model_coverage.py
```

The independent revision passed **51 test methods, zero failures and errors**, on Python **3.11.9, 3.12.3 and 3.13.5**. These comprise 25 model, 13 controller, 7 storage, 4 real-process acceptance and 2 measurement-tool tests. `subTest` cases are included within method counts. All original 45 methods remain; this review added four application tests and two tool tests.

Host: Windows 11, build 26200, confirmed using the operating-system record. Python 3.11's `platform.release()` reports Windows 10 on this host; that interpreter label in raw logs does not identify a second machine. The 3.11.9 runtime is an official standalone embeddable distribution configured for normal imports. A separate **51-test run with `-S` (site packages disabled)** also passed. No third-party runtime dependency is required or bundled.

Raw logs are `independent-verification-2026-10-23-python311.txt`, `independent-verification-2026-10-23-python312.txt` and `independent-verification-2026-10-23-python313.txt`. Coverage uses the same suffixes after `independent-model-coverage-2026-10-23-`. Repository logs are in `docs/reports/`; candidate copies are in `03_Implementation/evidence/`.

## 2. Model source-line coverage

The full 51-test suite achieved **416/421 model source lines (98.81%)** on each of the three interpreters. The numerator and denominator include only `src/model/*.py`. Controller, storage, tests and tools are not included as measured source. CLI subprocess execution is outside the parent trace session.

| Model module | Covered / executable source lines | Coverage |
|---|---:|---:|
| `model/__init__.py` | 0/0 | n/a |
| `model/errors.py` | 4/4 | 100.00% |
| `model/manager.py` | 95/95 | 100.00% |
| `model/records.py` | 57/57 | 100.00% |
| `model/search.py` | 226/231 | 97.84% |
| `model/validation.py` | 34/34 | 100.00% |
| **Total model** | **416/421** | **98.81%** |

The tool uses standard-library `trace` to collect executed lines and its private `_find_executable_linenos` helper to identify candidate executable lines. It now excludes nonpositive/noninteger entries (`0` and `None`), which refer to interpreter bookkeeping, not source lines. It prints excluded-entry counts and actual missing source lines for each module. This private CPython helper is version-dependent, so results name the measured interpreter and are not a promise for future releases.

The prior Python 3.13 report counted 416/430 (96.74%); nine denominator entries were `0` or `None`. Removing these produces 416/421 without changing the numerator or model code. On Python 3.11 six such entries were removed from 427. The increase is **a corrected measurement, not newly covered model behavior**. The remaining five real lines, `search.py` 205-209, belong to the unused `_Parser._accept` helper. They remain in the denominator; dead code was not deleted or artificially called to inflate coverage.

Two fixture-based regressions first failed against the old tool and passed after correction: a docstring-only module has 0/0 executable source lines, and an uncalled real function body remains in the denominator and is listed as missing. Nested tracing restores the previous tracer after each fixture run.

## 3. Model unit tests alone

To distinguish model unit evidence from the full suite, a separate Python 3.11.9 run executed only the **25 model unit methods**, using the same coverage algorithm. It covered **415/421 lines (98.57%)**. The extra missing line is `manager.py` 22, the invalid record-type branch exercised through the boundary tests in the full suite. Other module counts are unchanged.

Reproduce this narrower check from the same folder:

```powershell
$check = "from tools import model_coverage as c; c.TESTS /= 'model'; "
$check += "raise SystemExit(c.main())"
python -c $check
```

The resulting log is `independent-model-units-only-2026-10-23.txt`. Its runner prints the default tool command in the header; the command above is the actual narrower invocation. The full-suite percentage must not be described as coverage produced only by model unit tests.

## 4. Assertion quality and limits

Existing assertions cover all four PIR types, nine mutable fields, five text-search fields, three time fields and all three time comparisons, invalid inputs, immutable replacement, stable IDs, complete snapshot validation and failure atomicity. This review added an independent truth-table oracle for six three-atom Boolean compositions over all eight assignments (48 subcases), rather than assertions derived from the parser's own output.

Two fixes have observed failing-then-passing regressions: deeply nested malformed JSON is converted to a FORMAT error with the old state and next ID preserved, and a line-buffered terminal receives each prompt before input blocks. The nesting failure was reproduced on Python 3.11; the same sample takes a different rejection path on newer interpreters. A 40-import AST audit and the `-S` test run support the standard-library restriction.

This is source-line coverage, not branch, condition, mutation or exhaustive requirements coverage. No course minimum coverage percentage is specified. NFR-01's exact network-disabled/no-graphical-session environment remains untested. Human recordings, genuine identities and the official declaration remain separate deliverables. The final candidate's clean-extraction log records verification of the actual ZIP contents.
