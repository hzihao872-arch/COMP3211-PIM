# WP04 Integration Test Log

**Date:** 2026-09-30

**Group:** 89 (number supplied by the user; member identities pending)

**Baseline:** WP03 PR #5 merge commit `9913b783531fa4cf67eede2329fea1a66a86c5e1`
**Frozen source and test commit:** `4d3508db0447a3ac6346a2a2789da89208f88fd5`

## Independent read-only audit and resolutions

Three read-only agents examined the official requirements matrix, SRS, decisions, technical contract, source, and tests. The primary Agent reproduced each reported defect before modifying code. The model/API auditor found no reproduced boundary or third-party-import defect.

| Finding and observed failure before fix | Root cause | Regression and resolution |
|---|---|---|
| A 5,000-digit `show` ID ended the CLI with `ValueError`; the following command was skipped. | `int()` conversion in `_id` could raise outside the controller's command-error boundary. | `test_very_long_id_is_reported_and_session_continues` failed before the fix, then passed after conversion errors became `CommandSyntaxError`. |
| 1,200 `!` operators or nested parentheses failed during recursive parsing; a 1,200-atom `&&` chain failed during recursive evaluation. | The parser and Boolean criterion evaluator used the Python call stack for expression depth. | `test_deep_valid_expressions_evaluate_without_recursion` and `test_deep_compound_search_and_following_command` exposed the failures. Iterative precedence parsing and stack evaluation now handle these cases; the full suite passed. |
| A note containing U+0085, U+2028, U+2029, vertical tab, or form feed was accepted as single-line text. | Text validation excluded only CR and LF. | `test_unicode_line_separators_are_not_single_line_text` failed before and passed after the shared model validator rejected Unicode line boundaries. |
| A `.pim` file containing an escaped lone surrogate loaded successfully, then could not be saved as UTF-8. | Model text validation accepted strings that UTF-8 cannot encode. | `test_lone_surrogate_is_not_valid_text` and `test_load_rejects_text_that_cannot_be_saved_as_utf8` failed before and passed after validation rejected unencodable text. Load now returns a `FORMAT` error without replacing the active manager. |

## Requirement and integration checks

| Check | Evidence |
|---|---|
| US1–US11 end-to-end paths | `tests/test_acceptance.py::test_all_stories_across_save_and_restart` runs the CLI in two processes. |
| Four record types and ID preservation | Model and storage tests round-trip every type and retain the higher post-load counter; the manual session below creates ID 5 after reloading IDs 2–4. |
| Failed operations preserve data and prompt | Model, CLI, storage, and real-process tests cover failed update, search, load, invalid commands and the long-ID regression. |
| Search operators and grouping | `tests/model/test_search.py` exercises type, all five text fields, all nine time-field/comparator pairs, `&&`, `||`, `!`, precedence, parentheses, and deep expressions. |
| Model isolation and runtime imports | AST import audit: 40 source imports, all standard-library or local package; no `model` import from `controller` or `storage`. |
| Clean-copy reproduction | Local clone of freeze commit `4d3508d` into a new directory; README `python src/main.py` help/add/show/exit worked and its `unittest` command ran 33 tests with zero failures/errors. |

## Automated verification

From the repository root with `PYTHONPATH` set to `src`:

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m unittest discover -s tests -t . -v
py -3.12 -m unittest discover -s tests -t . -q
python tools/model_coverage.py
python -m compileall -q src tests tools
git diff --check
```

- Python 3.13.5 on Windows 11: **33 tests, OK**.
- Python 3.12.3 on Windows 11: **33 tests, OK**.
- Standard-library `trace` model-only coverage on Python 3.13.5: **411/430 executable lines, 95.58%**. Per-module raw output is in [model-coverage-raw.txt](model-coverage-raw.txt). The docstring-only `model/__init__.py` is counted by `trace` as one executable line but does not receive a trace event (0/1); it is retained in the denominator rather than silently excluded. Subprocess CLI execution is outside this coverage trace.
- `compileall` and `git diff --check`: exit code 0.
- `rg -n "eval\(|TODO|TBD|PLACEHOLDER" src tests tools`: no matches (exit code 1).

## Manual CLI acceptance transcript

This was run in two fresh Python processes from one temporary working directory. The transient absolute directory has been replaced with `<TEMP_DIR>` in the displayed output; commands and other output are unchanged. Both processes returned code 0, the `.pim` file existed, and the second process assigned ID 5 after loading.

```text
Session 1 input:
add note "memo"
add task "draft" "2026-10-01 09:00"
add event "meeting" "2026-10-02 10:00" "2026-10-01 08:00"
add contact "Li" "Room 1" "+00123"
list
search (type = "task" && deadline < "2026-10-02 00:00") || text contains "memo"
update 2 description "revised"
delete 1
save "snapshot.pim"
exit

Session 1 output:
pim> Created note 1
pim> Created task 2
pim> Created event 3
pim> Created contact 4
pim> 1 | note | memo
2 | task | draft
3 | event | meeting
4 | contact | Li
pim> 1 | note | memo
2 | task | draft
pim> Updated 2
pim> Deleted 1
pim> Saved 3 PIR(s) to <TEMP_DIR>\snapshot.pim
pim>

Session 2 input:
load "snapshot.pim"
show all
add note "after load"
show 5
exit

Session 2 output:
pim> Loaded 3 PIR(s) from <TEMP_DIR>\snapshot.pim
pim> id: 2
type: task
description: revised
deadline: 2026-10-01 09:00

id: 3
type: event
description: meeting
start_time: 2026-10-02 10:00
alarm_time: 2026-10-01 08:00

id: 4
type: contact
name: Li
address: Room 1
mobile_number: +00123
pim> Created note 5
pim> id: 5
type: note
text: after load
pim>
```

## Remaining evidence gap

The chosen runtime baseline includes Python 3.11, but no Python 3.11 interpreter was available on this machine (`py -3.11 --version` found none). Python 3.11 compatibility is **unverified**, not reported as a passing test or a demonstrated defect. Group review of AI-assisted choices and real member identities also remains pending for later deliverables.
