# COMP3211 Personal Information Management System

Group repository for the Fall 2026 COMP3211 Software Engineering course project.

The project is a command-line Personal Information Management (PIM) system. It manages notes, tasks, events, and contacts; supports modification, deletion, printing, compound search conditions, and `.pim` file persistence.

## Current source revision

The usability release preserves this PIM mainline and adds unsaved-load protection, `help COMMAND`, and positioned search/quoting diagnostics. It also includes terminal escaping, limited-encoding output, Ctrl+C/closed-pipe handling and reproducible demo/performance tools. All 86 tests pass on Python 3.11.9, 3.12.3 and 3.13.5. The six document PDFs and presentation match this revision; see [current verification](docs/reports/usability-release-2026-10-23.md).

## Latest packaged usability candidate

The latest reviewed package is `output/COMP3211_Group_Project-usability-2026-10-23.zip`. Its file hashes are in [the current manifest](submission/manifest.md); findings and verification are in [the usability release report](docs/reports/usability-release-2026-10-23.md). Earlier ZIPs and dated reports are historical. The candidate still requires the two real recordings, the official declaration, and human group review before submission.

Download the verified ZIP from the [usability release](https://github.com/hzihao872-arch/COMP3211-PIM/releases/tag/usability-2026-10-23). The release is marked as a prerelease because the human deliverables above remain pending.

## Important dates

- Group registration: **2026-09-28 09:00**
- Final submission: **2026-11-20 20:00**

## Repository map

| Path | Purpose |
|---|---|
| `src/model/` | Required model package containing PIR data and business rules |
| `src/controller/` | Command parsing and application coordination |
| `src/storage/` | `.pim` file save/load code |
| `tests/model/` | Automatically executable model unit tests |
| `docs/srs/` | Software Requirements Specification source |
| `docs/design/` | Architecture, component, and sequence/activity design source |
| `docs/manuals/` | Developer and user manuals |
| `docs/reports/` | Requirements and test coverage reports |
| `media/` | Demo and presentation plans or recordings |
| `submission/` | Final ZIP checklist and Honour Declaration placeholder |

## First-time setup

For a supplied candidate ZIP, extract it and open PowerShell in `03_Implementation`, the folder containing `src`, `tests` and `tools`. No Git clone is required. Use Python 3.11.9, 3.12.3 or 3.13.5; see the supplied Developer Manual and Test Coverage report for the verified environments.

For a fresh repository checkout only:

```powershell
git clone https://github.com/hzihao872-arch/COMP3211-PIM.git
cd COMP3211-PIM
python --version
```

The implementation must use only the Python standard library.

## Run commands

Run the local CLI from the repository root, or from `03_Implementation` in an extracted candidate:

```powershell
python src/main.py
$env:PYTHONPATH = "$PWD\src"
python -m unittest discover -s tests -t . -v
python tools/model_coverage.py
python tools/verify_demo.py
python tools/benchmark.py
```

Type `help` for every command form, field order, quoting rule, and search syntax. For example:

```text
add task "Prepare demo" "2026-10-01 09:00"
search type = "task" && deadline < "2026-11-01 00:00"
save "records.pim"
exit
```

The program starts with an empty collection. Use `load "records.pim"` in a later session to restore a saved snapshot. The `.pim` suffix must be lowercase. Dates use local `YYYY-MM-DD HH:mm` format. A failed command reports an error and returns to the prompt.

The last two verification commands are available in the current source revision. They use temporary directories and never replace your snapshots. Keep `media/demo/demo-commands.txt` and `media/demo/demo-expected-output.txt` alongside `src`, `tests` and `tools` when copying it. Benchmark timings are local observations, not pass/fail performance requirements.

## Candidate status

The current manifest in `submission/manifest.md` identifies the candidate files. Source, tests and reports may include reviewed changes after the earlier source baseline; use the manifest and current test results instead of an old commit label. The two real MP4 recordings, verified member details, contribution consensus and signed official Honour Declaration remain human closeout work. This repository does not establish that the project has been submitted.

## Start a task

```powershell
git switch main
git pull
git switch -c feature/short-task-name
```

After completing and testing the task:

```powershell
git add <changed-files>
git commit -m "feat: describe the change"
git push -u origin feature/short-task-name
```

Open a pull request on GitHub and ask at least one teammate to review it before merging.

## Current planning files

- [End-to-end delivery plan](docs/plans/2026-09-30-project-master-plan.md)
- [New-conversation work packages](docs/plans/work-packages/README.md)
- [Requirements checklist](requirements-checklist.md)
- [Team decisions](decisions.md)
- [Task board](tasks.md)
- [Contribution guide](CONTRIBUTING.md)
