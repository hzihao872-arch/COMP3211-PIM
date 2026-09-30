# COMP3211 Personal Information Management System

Group repository for the Fall 2026 COMP3211 Software Engineering course project.

The project is a command-line Personal Information Management (PIM) system. It manages notes, tasks, events, and contacts; supports modification, deletion, printing, compound search conditions, and `.pim` file persistence.

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

```powershell
git clone https://github.com/hzihao872-arch/COMP3211-PIM.git
cd COMP3211-PIM
python --version
```

The implementation must use only the Python standard library.

## Run commands

Run the local CLI from the repository root:

```powershell
python src/main.py
$env:PYTHONPATH = "$PWD\src"
python -m unittest discover -s tests -t . -v
```

Type `help` for every command form, field order, quoting rule, and search syntax. For example:

```text
add task "Prepare demo" "2026-10-01 09:00"
search type = "task" && deadline < "2026-11-01 00:00"
save "records.pim"
exit
```

The program starts with an empty collection. Use `load "records.pim"` in a later session to restore a saved snapshot. The `.pim` suffix must be lowercase. Dates use local `YYYY-MM-DD HH:mm` format. A failed command reports an error and returns to the prompt.

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
