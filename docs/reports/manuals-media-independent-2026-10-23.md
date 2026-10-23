# Independent manuals and media review - 2026-10-23

## Scope and authority

This review used the current working files in `COMP3211-PIM`, including existing uncommitted changes. It did not reset the repository or treat an earlier commit as the complete delivery. The review read all four pages of the original Project Description, ran the documented commands independently, extracted the editable PPTX text, and rendered every page of the six existing document PDFs and the presentation PDF.

Official requirements relevant here are Project Description p. 2, Deliverable 3.b-c (development version, IDE, build/debug instructions, complete user commands and error/output explanations), p. 2, 3.d (MP4 system demo at most four minutes), and p. 3, Deliverable 5 (PDF slides, MP4 presentation at most five minutes, each member at least one minute, real student card and face at the start and current speaker's face always visible). Presentation content must cover creation, criterion definition, searching, architecture/main components, and one lesson about requirements engineering, API design or unit testing. The official deadline is 20:00, 20 November 2026. Course PDF p. 3 requires accurate GenAI acknowledgement and the official Honour Declaration; this review cannot supply human signatures or contribution consensus.

No local workflow preference, optional IDE, demonstration filename, slide count, planned speaking window or coverage percentage is a new course requirement.

## Findings and corrections

| Severity | Finding and evidence | Correction and verification |
|---|---|---|
| Medium | User Manual still described WP04/WP05, a frozen commit and untested Python 3.11; Developer Manual and demo checklist incorrectly required source/tool files to match an earlier commit. Current files and this review's version commands contradict those descriptions. | Updated `README.md`, both manuals, demo script/checklist and presentation script to identify the current candidate by manifest. Removed the stale source freeze requirement and referred changing test details to the current coverage report. |
| Medium | User Manual and README assumed a repository checkout, while the submitted source lives under `03_Implementation`. A ZIP reader following `python src/main.py` from the archive root would fail. | Both explicitly distinguish the extracted `03_Implementation` folder from the repository root. Developer Manual already explained the extracted folder; this was preserved. The main review separately verifies the assembled ZIP in a clean extraction. |
| Medium | Developer Manual gave debugger configuration but no complete terminal debugging sequence a reader could reproduce without configuring an IDE. | Added standard-library `python -m pdb src/main.py`, `b main`, `c`, `c`, application `exit`, debugger `q`. The exact sequence stopped at `main`, reached `pim>` and exited 0. VS Code remains the documented IDE; this review did not claim to launch VS Code. |
| Medium | Demo expected output embedded a private old absolute directory and the script described 30 September output as the release reference. | Reran both sessions in a new temporary directory using current source. Replaced the expected output with observed output, normalizing only the directory to `<DEMO_DIR>` and prompt trailing spaces. The script explains the placeholder. Both processes exited 0, the snapshot existed, records 2-4 were restored and the next record was 5. |
| Medium | Presentation/testing material repeated 45 tests and the old trace denominator, even after the review added regressions and corrected measurement. | Updated presentation draft/checklist to the independently rerun suite and corrected model source-line coverage; the authoritative report and slide 6 must match before recording. Coverage means model lines, excludes non-source 0/None entries and is not branch or whole-project coverage. |
| Low | Windows users could plausibly paste a quoted path with ordinary backslashes and trigger the documented escape parser; no concrete path example clarified this. | User Manual now gives forward-slash and doubled-backslash examples and states that the parent directory must exist. A path containing spaces successfully saved and loaded through both forms in a real process. |
| Low | Presentation p. 2 showed `Created task 2` without displaying its prerequisite note; p. 1/2 used frozen-version labels. Slide 5's architecture diagram was small and the generic pattern was not named in its text. | Sent exact slide changes to the main reviewer: prerequisite note, current-candidate wording, explicit layered/MVC-style separation, and larger architecture illustration. Only the main reviewer edits/export-checks the PPTX and PDF. |

## Independent execution evidence

Commands were run on Windows 11. `python --version`, `py -3.12 --version` and the available standalone Python version command actually returned 3.13.5, 3.12.3 and 3.11.9 respectively. This subreview's command transcripts use Python 3.13.5; interpreter-wide suite evidence is handled by the main review.

| Check | Observed outcome |
|---|---|
| README creation/search/save sequence | Exit 0; task created and matched the deadline criterion; snapshot written. |
| Developer Manual help/create/show/save then new-process load/show | Both exit 0; persisted note shown after restart. |
| User Manual empty note, ID 0 and missing ID 99 | Exact documented VALIDATION, COMMAND and NOT_FOUND errors; following valid creation returned ID 1. |
| User Manual section 8, both code blocks | Both exit 0; actual output equals the printed output after replacing only temporary directory and removing invisible prompt trailing spaces. |
| Demo command file, two separate processes | Both exit 0, no `Error:`, expected records and next ID; snapshot verified on disk. |
| Quoted `my records/snapshot.pim` and `my records\\snapshot.pim` | Both accepted; save/load selected the same file. |
| `python -m pdb src/main.py` | Breakpoint established at `main`, CLI reached, `exit` and debugger `q` completed with exit 0. |
| `$env:PYTHONPATH = "$PWD\src"`; `python -m unittest discover -s tests -t . -v` | Current observed suite: 51 tests, zero failures/errors, exit 0. |
| `python tools/model_coverage.py` | 51 tests passed; model source-line coverage 416/421 (98.81%); excluded nine non-source entries; unexecuted source lines 205-209 in `model/search.py` remain in the denominator. |
| `python -m compileall -q src tests tools` | Exit 0. Generated caches are development output and must be omitted from the ZIP. |

The helper compared User Manual section 8's actual output with its literal code blocks, rather than merely checking that a process ran. The demo check asserted absence of errors, snapshot existence, successful return codes, and deterministic record IDs. Local raw transcripts are in `D:\comp3211\tmp\independent-review\manual-command-evidence.txt`; the corrected, portable demo transcript is delivered as `media/demo/demo-expected-output.txt`. The main coverage report records the final complete version's suite results if later test changes occur.

During parallel development a transient run encountered the two newly added coverage-tool regressions before their implementation fix; that was not recorded as a passing result. After the tool fix, the complete commands above passed. No disconnected-network/no-graphical-session environment was exercised by this subreview; NFR-01's precise environment remains unverified unless separately established.

## Existing PDF and PPTX review

The initial six document PDFs contained 33 pages: Design 9, Developer Manual 2, Requirements Coverage 8, SRS 8, Test Coverage 2, User Manual 4. The presentation had six pages. All 39 pages were rendered and visually inspected in page sheets; PPTX text was independently extracted from all six native slide XML files. This is not a claim that the deck was opened in PowerPoint, nor that page thumbnails prove every small glyph legible at presentation distance.

No obvious clipped blocks, overlapping text, broken tables or missing glyphs were observed in the initial rendering. Several layout weaknesses were reported for the main re-export: Design p. 3 and p. 9 were sparse, SRS p. 8 contained only the last two rationale rows, and Requirements Coverage p. 8 contained only its short final evidence section. These are readability/pagination improvements, not separate official noncompliances. Slide 5's architecture image needed enlargement for presentation viewing; report code/signature tables needed full-size zoom to read comfortably.

Required content was present in the six-slide narrative: FR-03 creation, FR-26 criterion definition, FR-27/FR-39 search, architecture/components and the documented deep-expression unit-testing lesson. The lesson's historical basis is `docs/reports/integration-test-log.md`; this review did not falsely present that old failure as a newly discovered defect. Both script and checklist require speakers to understand the AI-assisted example and adapt statements to their actual involvement.

Final revised document/slide PDF rendering is coordinated by the main reviewer after this source handoff. The main independent report records completion of that export check and the clean ZIP verification.

## Human closeout

- Supply and verify the four real members' names and IDs; do not replace placeholders with inferred identities.
- Review and understand the AI-assisted implementation, review changes and testing lesson; acknowledge actual GenAI assistance accurately.
- Agree contribution percentages and complete/sign the official Honour Declaration using real group decisions.
- Rehearse and record both real MP4s. The speaking windows are plans, not evidence of duration. Measure each member's actual speaking time and the exported recordings; check real faces/cards and continuous current-speaker visibility.
- Review the final candidate and submit it through the official course process. This work neither submits the project nor claims a submission receipt.

This subreview changed README, manual sources, demo sources/output and presentation script/checklist only, plus this report. It did not modify application code, tests, the coverage tool, PDFs, PPTX, submission documents, recordings or the ZIP.
