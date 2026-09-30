# AI-assisted requirements workshop — WP00

**Date:** 2026-09-30

**Participants:** primary Codex Agent and three read-only AI subagents: official-requirements auditor, user/API analyst, grader/test analyst. No human group meeting or member vote is represented by this note.

**Source:** verified four-page 2026 Project Description PDF, SHA-256 in [source register](../../references/README.md); master plan, WP00, existing checklist, decisions, and tasks.

## Independent review and reconciliation

| Reviewer | Main finding | Primary Agent resolution |
|---|---|---|
| Official-requirements auditor | US1–US11 were broadly present, but the checklist omitted many page 1–3 specifics: group/date rules, SRS structure, design interface details, manuals, presentation identity rules, declaration. | Added explicit rows to the requirements and deliverables matrices and expanded the checklist. |
| User/API analyst | The PDF leaves command syntax, IDs, date format, query grammar, absent-field behavior, storage interior, load semantics, and error recovery to the group. | Recorded a deterministic WP00 working baseline in `decisions.md`; labelled each as a group choice. |
| Grader/test analyst | Requirements coverage must include both user stories and SRS requirements; line coverage is a separate model report in the source-code root. Presentation and declaration conditions are likely grading losses. No minimum line-coverage percentage is stated. | Added location/content checks and future evidence for these points without inventing test or coverage results. |

## Product decisions made for the working baseline

The primary Agent applied WP00's recommended choices where the PDF did not conflict and resolved additional ambiguity in [decisions.md](../../decisions.md). The baseline uses Python 3.11+, four exact record schemas, monotonic IDs, a quoted single-line CLI, minute-precision local date/time, an explicit search grammar, UTF-8 JSON within `.pim`, validated replacement on load, and data-preserving error handling. These choices are **not** official requirements or proof of human team consensus.

Examples that WP01 should convert into acceptance requirements:

1. `type = "task" && deadline < "2026-11-20 20:00"` finds matching task PIRs; it does not treat an event without `deadline` as a match.
2. `!(description contains "urgent")` evaluates true for a contact without `description`, because the absent-field atom is false.
3. `text contains "Lab" || name contains "Lab" && type = "contact"` applies `&&` before `||`; parentheses can override it.
4. A failed `load "damaged.pim"` leaves current records and next ID unchanged.
5. A time comparison uses minute precision; impossible dates and malformed quotes fail with an error rather than silently matching nothing.

## Open human facts and handoff

- The user subsequently confirmed on 2026-09-30: **Canvas group formed; current member count 4**. The official registration deadline remains recorded in the matrix.
- The local Lecture 04 PDF was verified after G0: pages 31–32 contain the two SRS structure slides needed for WP01. See the source register.
- Real member identities, student IDs, contribution percentages, signatures, and video facts belong to later human evidence. The workshop did not infer them.
- Human group members should review this working product baseline and record any changes before WP01 approval. This note does not claim they already agreed.

## G0 audit state

**G0 passed on 2026-09-30.** The official PDF was checked page by page; the matrix covers all 11 user stories and the deliverables matrix lists the required artifacts. Official rules and group choices are separated, product rules have a concrete working choice, the AI-use log has begun, and the user supplied the Canvas group status and count. WP01's Lecture 04 prerequisite was verified afterward.
