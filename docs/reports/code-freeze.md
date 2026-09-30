# WP04 Code Freeze

**Group:** 89 (user-provided number; member names and student IDs pending)  
**Freeze date:** 2026-09-30  
**Frozen source, tests, and coverage tool commit:** `4d3508db0447a3ac6346a2a2789da89208f88fd5`  
**Branch:** `work/wp04-qa-freeze`

This SHA identifies the exact product source, automated tests, and `tools/model_coverage.py` used for WP04 verification. Later WP04 evidence-document commits do not alter those files. Any later product behavior change requires repeating WP04 checks and recording a new freeze SHA.

## Environment and commands

- OS: Windows 11.
- Verified Python interpreters: 3.13.5 and 3.12.3. Python 3.11 was unavailable and remains unverified.
- Launch: `python src/main.py` from the repository root.
- Unit/acceptance tests: set `$env:PYTHONPATH = "$PWD\src"`, then run `python -m unittest discover -s tests -t . -v`.
- Model line coverage: `python tools/model_coverage.py`.
- Compile check: `python -m compileall -q src tests tools`.

## Results

| Check | Observed result |
|---|---|
| Python 3.13.5 full suite | 33 tests; 0 failures; 0 errors. |
| Python 3.12.3 full suite | 33 tests; 0 failures; 0 errors. |
| Model line coverage, Python 3.13.5 | 411/430 executable lines, 95.58%; see [raw report](model-coverage-raw.txt). |
| Clean-copy README commands | Fresh local clone of this freeze commit ran CLI help/add/show/exit and 33 tests successfully. |
| Manual CLI acceptance | Two-process create/list/compound-search/update/delete/save/restart/load/show session passed; see the [transcript](integration-test-log.md#manual-cli-acceptance-transcript). |
| Model boundary and imports | 40 source imports audited; all standard-library or local, with no `model` dependency on `controller` or `storage`. |

`python tools/model_coverage.py` produced these per-model figures on Python 3.13.5:

| Model module | Covered/executable lines | Coverage |
|---|---:|---:|
| `model/__init__.py` | 0/1 | 0.00% |
| `model/errors.py` | 4/5 | 80.00% |
| `model/manager.py` | 92/97 | 94.85% |
| `model/records.py` | 57/58 | 98.28% |
| `model/search.py` | 224/233 | 96.14% |
| `model/validation.py` | 34/36 | 94.44% |
| **Total** | **411/430** | **95.58%** |

The 0/1 line in `model/__init__.py` is a docstring-only package file counted by standard-library `trace`; it remains in the total denominator. Subprocess CLI code is outside the model trace scope.

## Manual CLI transcript

The [full input and output transcript](integration-test-log.md#manual-cli-acceptance-transcript) records two separate Python processes. The first created all four PIR types, listed them, ran a compound search, updated ID 2, deleted ID 1, and saved a snapshot. The second loaded that snapshot, showed IDs 2–4, created the next record as ID 5, and displayed it. Both processes exited with code 0 and the snapshot file existed. The displayed absolute temporary directory is normalized as `<TEMP_DIR>` in the transcript.

## Known limitations and pending human evidence

- NFR-02's Python 3.11 target has not been run because that interpreter was not installed on this machine. This is an evidence gap; compatibility is not claimed.
- The group has supplied number 89 but not real member names, student IDs, agreed contribution percentages, signatures, or the two recorded videos. These are later human inputs and are not represented as complete here.
- Group review of the AI-assisted SRS and design choices remains pending.
