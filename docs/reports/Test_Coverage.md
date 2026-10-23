# Test Coverage Report - COMP3211 PIM

**Revision:** Input-read correction, 2026-10-23. **Platform:** Windows 11.

## 1. Execution results

All **112 test methods** passed with zero failures/errors on Python **3.11.9**, **3.12.14** and **3.13.0**. The earlier 19 hardening methods cover ID/counter bounds and exhaustion, bounded errors, file/row context, complete megabyte field output, BOM input, flush/fsync sequencing and failure preservation, common expected-error handling, and dirty Ctrl+C with closed stdout. Seven further methods verify fatal input errors, preserved state/no retry, best-effort dirty warnings, invalid stdin bytes, bounded stderr and unavailable output pipes. Subtests are not counted separately.

Python 3.11.9 was freshly verified using the official Windows embeddable package in `tmp/python311`, without a system installation. Its `_pth` override was disabled for ordinary script/PYTHONPATH and stream-encoding behavior; the runtime has no installed third-party packages. Earlier usability and hardening logs remain historical snapshots.

Current evidence is `input-io-coverage-2026-10-23-python311.txt`, `python312.txt` and `python313.txt` (same prefix), plus matching `input-io-demo` logs. The narrower fresh 3.11 run is `input-io-model-only-2026-10-23-python311.txt`. The current source audit is `input-io-import-audit-2026-10-23.txt`. The audit and model-unit code are unchanged from the previous 3.12/3.13 measurements.

Prior hardening evidence logs: `hardening-coverage-2026-10-23-python312.txt`, `python313.txt` (same prefix); `hardening-model-only`, `hardening-demo` and `hardening-benchmark` use the same date/version suffixes. Each current execution log records Python version, executable, arguments and exit code. The import/syntax audit is `hardening-import-audit-2026-10-23.txt`.

| Test file | Methods |
|---|---:|
| `tests/controller/test_cli.py` | 7 |
| `tests/controller/test_hardening.py` | 7 |
| `tests/controller/test_independent_review.py` | 1 |
| `tests/controller/test_input_failures.py` | 4 |
| `tests/controller/test_requirement_edges.py` | 5 |
| `tests/controller/test_terminal.py` | 4 |
| `tests/controller/test_usability.py` | 13 |
| `tests/model/test_hardening.py` | 5 |
| `tests/model/test_independent_review.py` | 1 |
| `tests/model/test_manager.py` | 5 |
| `tests/model/test_records.py` | 5 |
| `tests/model/test_requirement_edges.py` | 6 |
| `tests/model/test_search.py` | 7 |
| `tests/model/test_search_integration.py` | 1 |
| `tests/model/test_search_positions.py` | 7 |
| `tests/storage/test_hardening.py` | 6 |
| `tests/storage/test_independent_review.py` | 2 |
| `tests/storage/test_pim_file.py` | 4 |
| `tests/storage/test_requirement_edges.py` | 1 |
| `tests/test_acceptance.py` | 6 |
| `tests/test_input_failures.py` | 3 |
| `tests/test_process_boundaries.py` | 6 |
| `tests/tools/test_evidence.py` | 4 |
| `tests/tools/test_model_coverage.py` | 2 |
| **Total** | **112** |

## 2. Model source-line coverage

| Model module | Full suite | Model units alone |
|---|---:|---:|
| `__init__.py` | 0/0 | 0/0 |
| `diagnostics.py` | 32/32 | 32/32 |
| `errors.py` | 15/15 | 15/15 |
| `manager.py` | 97/97 | 96/97 |
| `records.py` | 57/57 | 57/57 |
| `schema.py` | 11/11 | 11/11 |
| `search.py` | 236/236 | 236/236 |
| `validation.py` | 40/40 | 40/40 |
| **Total** | **488/488 (100.00%)** | **487/488 (99.80%)** |

All three measured interpreters produce the full-suite result. The model-only result was freshly reproduced on 3.11.9; the unchanged model code and tests retain the earlier 3.12.14/3.13.0 measurements. Coverage denominators include only `src/model/*.py`; controller, storage, tools and tests are not in the denominator. The full suite includes 112 methods; the narrower run selects 37 model unit methods. CLI subprocess execution is outside the parent trace. The model-unit-only run misses `manager.py:18`, the invalid record-type branch exercised by the full suite.

The existing standard-library trace algorithm is unchanged: executable source candidates come from `trace._find_executable_linenos`, excluding noninteger/nonpositive bookkeeping entries. This measures lines, not branches, and relies on a private interpreter API. The fixture regressions still verify that docstring-only modules have no executable lines and that genuinely unexecuted lines remain in the denominator. Percentages are not directly comparable with AST statement-start measurements in other projects.

The former unused `_Parser._accept` body was removed as dead code, not exercised merely to improve the number. The baseline was 431/436 full-suite lines and 430/436 model-unit-only lines. New schema/diagnostic code and changed validation produce a new denominator.

## 3. Reproduction

Run in the repository root with a writable system temporary directory:

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m unittest discover -s tests -t . -v
python -m unittest discover -s tests/model -t . -v
python tools/model_coverage.py
python -c "from tools import model_coverage as c; c.TESTS /= 'model'; raise SystemExit(c.main())"
python tools/verify_demo.py
python tools/benchmark.py --records 1000 --runs 5
```

This sandbox used `tmp/hardening-tests` as TEMP/TMP because its default temporary-directory permissions are restricted. Evidence logs preserve the real execution commands. Benchmark results include flush, fsync and atomic replacement; they are local observations, not response-time or power-loss guarantees.

## 4. Limits and release status

100% line coverage does not establish complete branch/input coverage. No new independent human/subagent review is claimed. The exact network-disabled/no-graphical-session scenario for NFR-01 remains unrecorded. Product import audit found only local and standard-library imports and no model dependencies on controller/storage.

Current Markdown source documentation is updated. Existing PDF exports, presentation and candidate ZIPs are the historical usability release; their file hashes do not describe this modified working tree. See [latest input-read verification](input-io-fix-2026-10-23.md) and [prior source hardening details](source-hardening-2026-10-23.md). Human group review and final recordings/declaration remain separate closeout items.
