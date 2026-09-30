# WP07 Independent Cross-Artifact Audit

**Group:** 89. **Audit date:** 2026-09-30. **Input main commit:** `aa64375f84b1e789e939f74676f2762b25e6b99e` (WP06 PR #8 merge). **Frozen product:** `4d3508db0447a3ac6346a2a2789da89208f88fd5`.

## Authority and scope

The local official `D:\comp3211\Project Description - 2026.pdf` has four pages and SHA-256 `28db75767dfec9832f8080f83d2ce3537a36c26dcfb1c28626be08e9fc25b881`. It was checked against the official requirements matrix, SRS, design and technical contract, frozen `src/tests/tools`, WP04 raw results, six WP05 Markdown/PDF documents, WP06 slides/PDF, scripts, commands, and observed two-process output. Three read-only auditors separately checked requirement traceability, code/tests/manuals, and submission/presentation. The primary Agent reproduced accepted findings and made the repairs.

The full Python 3.13.5 suite ran 33 tests with zero failures/errors. Python 3.12.3 also ran 33 tests with zero failures/errors. The model coverage tool reported 411/430 executable lines (95.58%) on Python 3.13.5, matching WP04 raw output and the Test Coverage Report. All seven delivery PDFs rendered (36 pages total); the six-slide presentation and its editable PPTX were checked. The WP06 demo ran in two separate processes with exit code 0, search/update/save/load behavior, and next ID 5. Source, tests, and coverage tool have no diff against the frozen SHA.

## Accepted findings

| ID / severity | Exact location | Violated requirement or evidence | Reproduction | Repair or disposition |
|---|---|---|---|---|
| A-01 / high | `docs/manuals/Developer_Manual.md` §1, original lines 8–22; `artifacts/documents/Developer_Manual.pdf` p. 1 | Official PDF p. 2 asks for usable developer instructions; WP08 requires reproduction from the extracted source-code root. The original setup depended on a private Git clone and `.git` metadata that the release tree does not contain. | Copy `src`, `tests`, `tools` into an isolated `03_Implementation`; `git rev-parse HEAD` fails there, and private Git access cannot be assumed. | Added an explicit extracted-ZIP route and identified `03_Implementation` as the working directory throughout the manual. Kept the Git route as an optional provenance check. Regenerated the PDF. Reproduced tests, coverage, CLI smoke flow, and compile check from a new copy with no `.git`. |
| A-02 / medium | `submission/README.md` original line 12 | WP08 assembly layout and `docs/plans/deliverables-matrix.md` use `03_Implementation/src/` with `tools/`; the old sketch said `source/`. | Compare the two trees. | Updated the sketch to `src/`, `tests/`, `tools/`, and `README.md`. |
| A-03 / medium | Root `README.md` repository map and Git workflow; WP08 `03_Implementation/README.md` planned copy | A raw copy would point to repository-only `docs/`, `media/`, and `submission/` paths, and to a private clone. | Copy only planned implementation files and read the root README in that copy. | WP08 must supply a committed release-specific README when assembling `03_Implementation`. This is an assembly task, not a frozen-source defect. G7 accepts it only with that explicit G8 check. |

## Cross-artifact checks and remaining evidence

- Official Appendix B US1–US11 map to the SRS, frozen code, and Requirements Coverage Report. FR-01–FR-50 and NFR-01–NFR-05 are present in the SRS and coverage report; referenced classes, methods, and test methods were checked against source. No new product behavior defect was confirmed.
- Design architecture, component, and search-update diagrams agree with the model/controller/storage structure and documented public interfaces. The CLI examples and WP06 two-process command sequence run against frozen code. The coverage numerator, denominator, interpreter, and model-only scope agree with raw output.
- The 12 FR rows already labelled “Implemented; evidence gap” in `docs/reports/Requirements_Coverage.md` remain targeted test gaps, not evidence of observed failures: FR-04, FR-07, FR-13, FR-15, FR-16, FR-19, FR-21, FR-32, FR-33, FR-34, FR-45, and FR-50. NFR-01's network-disabled/no-GUI condition was not independently run. Their statuses are accurately disclosed, so G7 accepts these lower-severity verification limits. They must not be described as separately passed checks.
- NFR-02's Python 3.11 target remains **unverified**: `py -3.11 --version` reported no suitable runtime. The 3.12.3 and 3.13.5 results do not establish 3.11 compatibility. No document was changed to claim otherwise.
- The member names, student IDs, contribution percentages, signed official Honour Declaration, `System_Demo.mp4`, and `Presentation_Recording.mp4` are absent. The scripts correctly distinguish planned speaking windows from measured durations and require ID/face review. They are human closeout items, not WP07 passes.
- The requirements and model coverage PDFs must be placed in the **source-code root** at WP08. The official signed declaration must be in the final ZIP root. Neither placement can be called verified before assembly.

`rg -n "TODO|TBD|PLACEHOLDER|MEMBER_[A-Z]|example student|230[0-9]+" .` was run. Binary PDF/SVG matches are not meaningful text findings; text-file matches are plan instructions, old templates, and `MEMBER_A`–`MEMBER_D` explicitly marked for real human replacement. `rg -n "^\s*(from|import)\s+" src tests tools` found only standard-library and local source imports. The product does not use a third-party runtime package.

The repair evidence, document hashes, and G7 decision are in [final-audit-resolution.md](final-audit-resolution.md).
