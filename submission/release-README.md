# COMP3211 PIM — Group 89

This is the source-code root of the submitted command-line PIM. It contains the reviewed Python application, tests, coverage tool, and the four implementation documents. No Git checkout, network connection, or third-party Python runtime package is needed to run the product.

## Start from the extracted ZIP

Open PowerShell in this `03_Implementation` folder. Use Python 3.11.9, 3.12.3 or 3.13.5 on Windows 11, the versions verified during the project:

```powershell
python --version
python src/main.py
```

At the `pim> ` prompt, type `help`. One short session is:

```text
add note "memo"
show 1
save "records.pim"
exit
```

Start `python src/main.py` again **from the same folder**, then use `load "records.pim"` and `show all`. The program starts empty on each run and does not save on exit. `records.pim` is written in the current working directory.

## Tests and model line coverage

From this folder in PowerShell:

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m unittest discover -s tests -t . -v
python tools/model_coverage.py
python -m compileall -q src tests tools
```

On 2026-10-23, 51 tests passed on Python 3.11.9, 3.12.3 and 3.13.5. Model line coverage on Python 3.13.5 was 416/421 (98.81%) using trace with non-source 0/None entries excluded. These results apply to those measured versions and runs.

## Documents and provenance

- `Developer_Manual.pdf` gives setup, debugging, and coverage instructions.
- `User_Manual.pdf` explains every command, field format, search expression, error, and output.
- `Requirements_Coverage.pdf` maps US1–US11 and every SRS FR/NFR to source and evidence.
- `Test_Coverage.pdf` explains the model-only coverage method and result.

The two coverage reports are placed directly in this source-code root as the course requires. The accompanying manifest identifies the current files, including prompt-flush and malformed-JSON recovery fixes and the corrected coverage tool. The suite contains 51 methods. The `evidence/` folder contains fresh test, coverage and import-audit logs. Group member identities, contribution percentages, signed declaration, and the two human recordings must be reviewed before final submission.
