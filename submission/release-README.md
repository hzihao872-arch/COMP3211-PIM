# COMP3211 PIM - Usability release candidate

Group 89, 2026-10-23. Open a terminal in this `03_Implementation` folder. Use Python 3.11.9, 3.12.3 or 3.13.5. The application and tests use only the standard library; no package installation is needed.

```powershell
python src/main.py
$env:PYTHONPATH = "$PWD\src"
python -m unittest discover -s tests -t . -v
python tools/model_coverage.py
python tools/verify_demo.py
python tools/benchmark.py
```

Type `help` or `help search` for syntax/examples. Unsaved edits block load unless you explicitly append `force=true`; failed loads preserve your data. Exit/EOF warns once and terminates without saving. Save first to retain changes. Search errors identify one-based positions within the expression; quoted-command errors use positions in the complete line.

All 86 tests pass on the listed Python versions. Model source-line coverage from the full suite is 431/436 (98.85%); model units alone cover 430/436 (98.62%). See the two coverage PDFs directly in this folder and the fresh logs in `evidence/`. Demo text inputs are included under `media/demo/`; tools use temporary directories and do not modify your own snapshots. The editable presentation is next to its PDF in `05_Presentation`.

This is a review candidate. The two real videos, genuine member details/contributions and official Honour Declaration still require the group. The archive root README and SHA256SUMS identify the payload. No video or signature has been fabricated.
