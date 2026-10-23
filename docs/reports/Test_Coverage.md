# Test Coverage Report - COMP3211 PIM

**Group:** 89; genuine member details pending. **Revision:** Usability release, 2026-10-23.
**Environment:** Windows 11; Python 3.11.9, 3.12.3 and 3.13.5. Current payload hashes are in the candidate manifest. Earlier reports and archives are historical.

## 1. Test execution and scope

All **86 test methods** passed with zero failures/errors on each interpreter. Subtests are not separate methods. The suite covers model rules, controller behavior, storage validation/atomicity, actual CLI processes and evidence-tool failure detection. All 86 also pass with site packages disabled using `-S`. This demonstrates the tested environments, not every future Python version or every possible input. `compileall`, the two-process demo checker and the 1,000-record/five-run search/save/load benchmark also pass on all three versions.

Run from the repository root or the ZIP's `03_Implementation` folder:

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m unittest discover -s tests -t . -v
python tools/model_coverage.py
python tools/verify_demo.py
python tools/benchmark.py
python -S -m unittest discover -s tests -t .
python -m compileall -q src tests tools
```

The evidence directory contains `usability-verification`, `usability-coverage`, `usability-model-only`, `usability-stdlib`, `usability-demo`, `usability-benchmark` and `usability-compile` logs, each suffixed `-2026-10-23-python311.txt`, `python312.txt` or `python313.txt`. Each log records the executable, arguments and exit code. Evidence is in repository `docs/reports/` and packaged `evidence/`.

| Test file | Methods |
|---|---:|
| `tests/controller/test_cli.py` | 7 |
| `tests/controller/test_independent_review.py` | 1 |
| `tests/controller/test_requirement_edges.py` | 5 |
| `tests/controller/test_terminal.py` | 4 |
| `tests/controller/test_usability.py` | 13 |
| `tests/model/test_independent_review.py` | 1 |
| `tests/model/test_manager.py` | 5 |
| `tests/model/test_records.py` | 5 |
| `tests/model/test_requirement_edges.py` | 6 |
| `tests/model/test_search.py` | 7 |
| `tests/model/test_search_integration.py` | 1 |
| `tests/model/test_search_positions.py` | 7 |
| `tests/storage/test_independent_review.py` | 2 |
| `tests/storage/test_pim_file.py` | 4 |
| `tests/storage/test_requirement_edges.py` | 1 |
| `tests/test_acceptance.py` | 6 |
| `tests/test_process_boundaries.py` | 5 |
| `tests/tools/test_evidence.py` | 4 |
| `tests/tools/test_model_coverage.py` | 2 |
| **Total** | **86** |

## 2. Model source-line coverage

The full suite covers **431/436 model source lines (98.85%)**, identically on all three interpreters. Measured source is only `src/model/*.py`; controller, storage, tests and tools are excluded from the denominator. CLI subprocess execution is outside the parent tracer.

| Model module | Full-suite covered / executable | Model units alone |
|---|---:|---:|
| `__init__.py` | 0/0 (n/a) | 0/0 (n/a) |
| `errors.py` | 7/7 | 7/7 |
| `manager.py` | 95/95 | 94/95 |
| `records.py` | 57/57 | 57/57 |
| `search.py` | 238/243 | 238/243 |
| `validation.py` | 34/34 | 34/34 |
| **Total** | **431/436 (98.85%)** | **430/436 (98.62%)** |

The standard-library `trace` collector records executed lines. Its private `_find_executable_linenos` helper supplies executable source candidates; noninteger/nonpositive bookkeeping entries such as `0` and `None` are excluded. Missing real lines remain in the denominator. This is source-line coverage, not branch coverage. The private helper is interpreter dependent, so versions are named explicitly. Measurement-tool fixture tests check both a docstring-only module and an unexecuted function body.

The five full-suite missing lines are `model/search.py` 209–213, the unused `_Parser._accept` helper. They were not artificially executed or deleted to raise the result. Model-unit-only measurement also misses `model/manager.py` 22, an invalid record-type branch covered by boundary tests in the full suite. The source changed to support positions, so older 416/421 figures are not the denominator for this revision.

## 3. Model unit tests alone

The narrower run selects **32 model unit methods** and covers **430/436 lines (98.62%)** on each listed interpreter, using the same algorithm. Reproduce it with:

```powershell
$check = "from tools import model_coverage as c; c.TESTS /= 'model'; "
$check += "raise SystemExit(c.main())"
python -c $check
```

The tool prints its default command header; the saved model-only log records the actual narrower invocation. Do not describe the full-suite percentage as coverage produced only by model unit tests.

## 4. Assertions and limitations

The 22 added methods cover dirty-state transitions, protected/forced load and failure preservation, all ten help topics, wrong topic/count recovery, quoted-command offsets, lexical/syntactic/semantic search offsets, Unicode and EOF positions, plus two real-process acceptance scenarios. Existing malformed-file tests explicitly use `force=true` when necessary to reach their original storage checks. Their record/counter preservation assertions remain. The initial 19-method red run failed before implementation; the final suite is green.

Earlier coverage remains for four record schemas, all editable fields, all search field/operator categories, Boolean truth tables, precedence, missing-field semantics, deep iterative parsing/evaluation, stable IDs, complete snapshot validation and save atomicity. Terminal tests check display controls and limited encodings; process tests distinguish closed output pipes from input/device failures. Evidence tools compare complete transcripts, search IDs and full persisted data/counters, not merely process success.

An independent read-only code reviewer reported no actionable findings, after rerunning 86 tests and additional random/deep-expression probes. These are review observations, not added unit methods. The AST import audit found 49 standard-library/local import references and no external dependency. NFR-01's exact network-disabled/no-graphical-session environment was not independently recorded. Real recordings, genuine member details, contribution agreement and the official declaration remain pending.
