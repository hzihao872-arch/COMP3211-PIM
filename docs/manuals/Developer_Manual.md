# Developer Manual — COMP3211 PIM

**Group:** 89. Member names and student IDs: pending human input.

**Product baseline:** frozen source, tests, and coverage tool at commit `4d3508db0447a3ac6346a2a2789da89208f88fd5` (2026-09-30). This manual documents that build.
**Platform:** Windows 11 with PowerShell. **Verified Python versions:** 3.13.5 and 3.12.3. Python 3.11 is a requirements target but was not installed in the WP04 environment and remains unverified. No third-party runtime or test package is needed.

## 1. Open the extracted submission or a clean checkout

For the submitted ZIP, extract it and open PowerShell in the directory containing `COMP3211_Group_Project`. Enter its source-code root:

```powershell
Set-Location .\COMP3211_Group_Project\03_Implementation
Get-ChildItem src, tests, tools
python --version
```

This folder contains `src/main.py`, the tests, `tools/model_coverage.py`, and this manual. It needs no Git metadata or access to the group's private repository. Run the commands in §3 from this folder. The release manifest records the hashes of the copied files; it does not itself establish a new product freeze.

To reproduce the original WP04 commit from a Git checkout **if repository access is available**, use:

```powershell
git clone https://github.com/hzihao872-arch/COMP3211-PIM.git
Set-Location COMP3211-PIM
git switch --detach 4d3508db0447a3ac6346a2a2789da89208f88fd5
git rev-parse HEAD
python --version
```

In the Git path, `git rev-parse HEAD` must print the full freeze SHA above. In either path, `python --version` identifies the interpreter used for the following commands. WP04 ran the application and suite with Python 3.13.5 and 3.12.3 on Windows 11. Python 3.11 remains unverified. A Python virtual environment is optional; all product imports are from the standard library or the delivered source.

## 2. IDE guidance and project layout

Visual Studio Code with a Python extension is a suitable editor on Windows 11; no specific IDE version was part of WP04 verification. Open the **`03_Implementation` folder or repository root**, select the installed Python 3.13.5 or 3.12.3 interpreter, and use its integrated PowerShell terminal for the commands below. The terminal commands are authoritative for reproduction; an IDE-specific test or coverage display was not used to obtain the report.

| Path | Responsibility |
|---|---|
| `src/main.py` | Composition root; creates a `PIMManager` and starts `CommandController`. |
| `src/model/records.py` | Immutable `Note`, `Task`, `Event`, and `Contact` records. |
| `src/model/validation.py`, `errors.py` | Model value rules and domain errors. |
| `src/model/manager.py` | Current collection, IDs, create/get/list/update/delete/search, validated snapshot reconstruction. |
| `src/model/search.py` | Search atoms, Boolean criteria, tokenizer, parser, and evaluator. |
| `src/controller/cli.py` | Command tokenization, dispatch, formatting, and recoverable error messages. |
| `src/storage/pim_file.py` | Version 1 UTF-8 JSON `.pim` save/load and validation. |
| `tests/model/`, `tests/controller/`, `tests/storage/`, `tests/test_acceptance.py` | Model unit, controller, persistence, and real-process acceptance tests. |
| `tools/model_coverage.py` | Standard-library `trace` runner for the model line-coverage report. |

The model package has no dependency on `controller` or `storage`. The controller imports the model and storage boundary. `src/main.py` is the only process entry point.

## 3. Run, test, and inspect coverage

Execute each block from the source-code root: `03_Implementation` in the extracted submission or the repository root in a Git checkout. The program launches with an empty in-memory collection:

```powershell
python src/main.py
```

At the `pim> ` prompt, type `help` for the full command grammar, then `exit` to end the session. A short smoke session is `help`, `add note "memo"`, `show 1`, `exit`. Data is not saved automatically; use `save "records.pim"` and later `load "records.pim"` when persistence is wanted.

Run the automatically discovered suite:

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m unittest discover -s tests -t . -v
```

The explicit `-t .` prevents `tests/model` from shadowing `src/model`. WP04 observed **33 tests, zero failures, zero errors** on both verified interpreters. Its Python 3.12.3 run selected that interpreter with `py -3.12 -m unittest discover -s tests -t . -q` after setting the same `PYTHONPATH`. The local fresh-clone check at the freeze SHA also ran the CLI and 33 tests successfully. Test elapsed time varies by machine.

Generate the submitted model-only line-coverage numbers:

```powershell
python tools/model_coverage.py
```

This tool discovers and runs the same 33 tests under Python's standard-library `trace` module. The WP04 Python 3.13.5 report was **411/430 executable model lines (95.58%)**. It covers `src/model/*.py`; subprocess executions of `src/main.py` in acceptance tests are outside the trace scope. The exact per-module figures and method appear in `Test_Coverage.pdf` beside this manual; the raw WP04 output is also retained at `docs/reports/model-coverage-raw.txt` in the repository.

Check that source, tests, and the coverage tool compile:

```powershell
python -m compileall -q src tests tools
```

Successful `compileall` produces no output and exits with code 0. It creates ignored bytecode cache folders.

## 4. Debug a command

Set the IDE's working directory to the source-code root identified in §3, program to `src/main.py`, interpreter to the verified Python selected above, and use an integrated terminal so you can type CLI commands. No command-line arguments are required. If the IDE needs an import path for direct test debugging, set `PYTHONPATH` to that root's `src` folder; launching `src/main.py` directly already puts `src` on Python's import path.

Useful breakpoints in the frozen code are `src/main.py::main`, `src/controller/cli.py::CommandController._dispatch` and `.run`, `src/model/manager.py::PIMManager.update` or `.search`, `src/model/search.py::parse_criterion`, and `src/storage/pim_file.py::save_pim` or `load_pim`. For a failed search, follow `parse_criterion` into `_Parser.parse`, then inspect `SearchSyntaxError` handling in `CommandController.run`. For a failed load, inspect `load_pim` before the controller replaces its active manager. The controller prints expected failures with `Error: SEARCH`, `NOT_FOUND`, `VALIDATION`, `PATH`, `FORMAT`, `IO`, or `COMMAND` and returns to the next prompt.

## 5. Evidence boundary

The course's NFR-02 includes Python 3.11. `py -3.11 --version` found no suitable runtime during WP04 and the WP05 clean-checkout check, so this manual does not claim Python 3.11 compatibility has been verified. IDE guidance is a setup recommendation; WP04 evidence came from PowerShell commands. Group 89 is confirmed, while member identity fields remain for human completion.
