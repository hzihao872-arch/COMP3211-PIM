# Project Tasks

The execution source is [the end-to-end delivery plan](docs/plans/2026-09-30-project-master-plan.md). A work package is complete only when its gate passes and its branch is reviewed and merged. Blank human ownership has not been inferred.

## Immediate setup and WP00

| Task | Owner | Target | Status |
|---|---|---|---|
| Confirm actual 3–4-member Canvas group status and count | User | WP00 | User confirmed on 2026-09-30: Canvas group formed, current count 4. |
| Record Canvas group number | User | WP04 | User supplied group number 89 on 2026-09-30; member names and student IDs will be supplied later. |
| Restore and verify official Project Description PDF | WP00 primary Agent | Immediate | Verified locally: 4 pages, 233333 bytes, SHA-256 in `references/README.md`. |
| Review official requirements and all US1–US11 | WP00 primary Agent plus three read-only AI auditors | WP00 | Draft matrices completed; see workshop note. |
| Close technical product-rule gaps | WP00 primary Agent | WP00 | Working choices recorded in `decisions.md`; human group may amend before WP01. |
| Record G0 | WP00 primary Agent | Before WP01 | Passed on 2026-09-30 after human Canvas status/count and WP00 verification. |
| Add every real member as repository collaborator | Leader | Group scheduling | Human action; status unverified. |
| Assign work-package owners and reviewers | Human group | Before work starts | Not yet provided. |
| Obtain or independently verify Lecture 04 SRS structure slides | WP00 primary Agent | Before G1 | Verified local Lecture 04 PDF, pages 31–32; source and SHA-256 in `references/README.md`. |

## Suggested milestones

| Milestone | Required result | Owner | Target | Status |
|---|---|---|---|---|
| WP01 requirements baseline | Reviewed SRS, stable FR/NFR IDs | WP01 primary Agent plus three read-only AI reviewers | 2026-10-05 | G1 passed; PR #3 merged into `main` on 2026-09-30. Human group review remains pending. |
| WP02 design baseline | Architecture, contract, three required diagrams | WP02 primary Agent plus two read-only AI reviewers | 2026-10-08 | G2 passed; PR #4 merged into `main` on 2026-09-30. Human group review remains pending. |
| WP03 complete implementation | US1–US11, CLI, model tests | Codex single modifying Agent | 2026-10-20 | G3 implementation checks passed and PR #5 merged on 2026-09-30. WP04 found and fixed additional edge cases. Python 3.11 runtime verification and human group review remain pending. |
| WP04 code freeze | Integration evidence and real model coverage | Codex primary Agent plus three read-only auditors | 2026-10-25 | G4 checks on 2026-09-30: 33 tests passed on Python 3.13.5 and 3.12.3; clean-copy CLI and tests passed; standard-library trace model coverage recorded. PR #6 merged into `main` on 2026-09-30. Python 3.11 runtime verification remains pending. |
| WP05 document freeze | Six reviewed final PDFs | Codex primary Agent plus three disjoint document Agents | 2026-11-04 | G5 checks passed on 2026-09-30: six PDFs generated and visually checked page by page; freeze SHA, requirement IDs, source symbols, test names, and coverage figures audited. PR #7 merged into `main` on 2026-09-30. Human group review and Python 3.11 runtime verification remain pending. |
| WP06 presentation assets | Presentation PDF and two recording scripts | Codex primary Agent | 2026-11-10 | G6 document and demo checks passed on 2026-09-30: six-slide editable PPTX and PDF validated and visually checked; fixed two-process demo commands ran against frozen code with exit code 0; recording scripts and timing/identity checklists prepared. PR #8 merged into `main` on 2026-09-30. Real member details, human rehearsal and MP4 recordings remain pending. |
| WP07 audit | No unresolved blocking/high finding | Codex primary Agent plus three read-only auditors | 2026-11-13 | G7 passed on 2026-09-30; extracted implementation reproduced 33 tests and 411/430 model line coverage. See `docs/reports/final-audit.md` and `final-audit-resolution.md`; PR #9 merged into `main` on 2026-09-30. |
| WP08 release candidate | Clean reproduction and complete manifest | Codex primary Agent | 2026-11-16 | Local G8 candidate checks passed on 2026-09-30: 32-file pre-video ZIP matched the directory and manifest; clean extraction ran 33 tests, 411/430 model coverage, and the CLI workflow; seven PDFs rendered. PR and merge pending. |
| Human closeout | Real videos, signed declaration, final clean check | Human group | 2026-11-19 | Waiting for real names/IDs, agreed contributions, two timed MP4s, official signed declaration, final ZIP check, and upload. See `submission/human-closeout-checklist.md`. |

## Task template

```text
Title:
Owner:
User story / requirement:
Files expected to change:
Acceptance checks:
Reviewer:
```
