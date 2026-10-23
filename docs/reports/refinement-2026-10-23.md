# Verification and document refinement - 2026-10-23

## Scope and provenance

The user asked the assistant to do as much of the remaining improvement work as possible so the four members could review and improve a stronger starting version. Application `src/` and `tools/model_coverage.py` remain byte-equivalent to commit `4d3508db0447a3ac6346a2a2789da89208f88fd5`. Twelve targeted test methods were added in three files; documents and slide evidence were revised. This is a local group-review candidate, not a new Git commit or a final submission.

Lecture 04 pp. 31-32 was re-extracted and compared with SRS chapter headings. All six required chapters are present. Page 27 motivates the added requirement-rationale table. The official assignment waives the other four chapters. Design additions explain alternatives, immutability trade-offs and unsuccessful interactions without changing architecture or interfaces.

## Observed checks

| Check | Observed result |
|---|---|
| Python 3.11.9 | 45 tests, zero failures/errors; includes CLI subprocess and restart acceptance |
| Python 3.12.3 | 45 tests, zero failures/errors |
| Python 3.13.5 | 45 tests, zero failures/errors |
| Model coverage, Python 3.13.5 | 416/430 (96.74%); unchanged coverage algorithm |
| Model coverage, Python 3.11.9 | 416/427 (97.42%); recorded separately due to interpreter line-count differences |
| Source compile | `python -m compileall -q src tests tools`, exit 0 |
| Product preservation | `git diff 4d3508d -- src tools` empty |
| Functional traceability | Dedicated passing assertions added for FR-04, 07, 13, 15, 16, 19, 21, 32, 33, 34, 45, 50 |

Raw interpreter and coverage logs are stored alongside this report. The 3.11.9 interpreter came from the official `python-3.11.9-embed-amd64.zip` distribution at python.org and resides outside the repository in the workspace temporary directory. Its `_pth` file was renamed to allow normal project imports; no pip packages were installed. Python 3.11's platform label reports Windows 10 while Python 3.13 reports Windows 11 on this same host; the raw outputs are preserved without relabelling.

## Limits and human review

NFR-01's exact network-disabled/no-graphical-session environmental check is still outstanding. Current evidence consists of a local CLI, reviewed standard-library imports and successful independent-interpreter execution. Test success does not prove every input or future Python version works.

The model coverage denominator retains the original tool's bookkeeping entries; the percentage is not whole-project or branch coverage. The previous audit/freeze records describe their dated baselines and are retained as history. Use the current Requirements/Test Coverage reports and release manifest for this candidate.

Two MP4s, real group identities and agreed contributions, the completed official declaration, human review and upload remain pending. Presentation text now refers to AI-assisted development explicitly; members should adapt the lesson after understanding and verifying it themselves.

## Release verification

The revised delivery PDFs and presentation were rendered and visually inspected. Text bounding boxes stayed within page bounds. A fresh ZIP extraction ran 45 tests successfully on all three interpreters and reproduced 416/430 coverage on Python 3.13.5. All 35 ZIP entries matched the assembly byte for byte. Current ZIP SHA-256: `9e5c0a3875eaa803650334278437b90fb9a8dbac9aeff5115e3c6c16192e8e92`. See `submission/manifest.md` for all file hashes.
