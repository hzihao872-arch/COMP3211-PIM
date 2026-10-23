# Independent requirements and design review — Group 89

Date: 2026-10-23. Scope: current working tree in `COMP3211-PIM`, including pre-existing local changes; no checkout, reset or reconstruction from an older commit. This is an AI-assisted review for human group consideration, not evidence of a group meeting, vote or sign-off. The package remains a candidate pending human materials.

## Sources and method

Read all four pages of **Project Description - 2026.pdf** via the fresh page-labelled extraction, including the complete Appendix A rubric and Appendix B stories. Read Lecture 04's natural-language guidance (pp. 26–27), definition of SRS as WHAT rather than HOW (p. 30), and structure tables (pp. 31–32). These source documents govern the review; prior reports were used only to locate files.

Independently read `src/main.py`, the controller and storage modules, and the model's validation, record, manager and search interfaces. Compared their fields, call directions, argument and return contracts, validation and exceptions with the SRS, 55-row requirements catalogue, Design Document, Technical Contract and all three Mermaid sources. Visually inspected all three existing PNG diagram renditions. Ran fresh model probes and structural consistency checks described below. Final PDF rendering and package verification are recorded by the overall independent review, not claimed by this subreview.

The official deliverables require all Appendix B stories, valid/consistent/complete/realistic/verifiable requirements, the Lecture 04 SRS structure with four exemptions, and architectural/component/example-use diagrams with explanation. They do **not** prescribe this group's ID algorithm, field trimming, exact search grammar, case behavior, minute precision, atomic replacement mechanism, JSON format, Python minimum, or a numerical coverage threshold. Those choices remain explicitly labelled group decisions.

## Findings and applied changes

Severity describes delivery impact, not a claimed mark deduction.

| Severity / ID | Finding and evidence | Basis | Applied change and verification |
|---|---|---|---|
| Medium RD-01 | FR-06 said every accepted field was trimmed. `validate_text` trims text, while `parse_local_time` rejects a padded time through exact round-trip comparison. The blanket wording obscured which padded fields should be accepted. | Official p. 1: consistency/verifiability; Lecture 04 pp. 26–27: avoid ambiguous quantifiers and use uniform requirements. | SRS FR-06 and matching catalogue row now distinguish accepted text trimming from exact FR-07 time syntax. Fresh probe accepted `"  alpha  "` as `"alpha"`, rejected `" 2026-10-01 09:00 "`, and asserted records/counter unchanged. Product decision clarification delegated to overall review owner. |
| Medium RD-02 | SRS/Design/Technical Contract called the current product a frozen SHA, and the contract still referred to a Python 3.11 evidence gap. Neither identifies the local candidate being reviewed, which now includes genuine application fixes. | Official pp. 1–2: document quality and accurate implementation explanation; Lecture p. 31: meaningful version history. | Replaced current freeze claims with candidate-working-tree wording and manifest references; retained SHA only as history; moved current test counts/versions to coverage-report references. Corrected chronology and marked historical pending evidence as historical. |
| Low RD-03 | FR-09 could be read as global ID non-reuse across independent processes. Each new `PIMManager` starts at 1; load preserves only the greater in-session/file counter. | Group ID choice, not an Appendix B requirement; realistic, unambiguous scope is required. | SRS FR-09, persistence explanation and catalogue now explicitly state session scope and loaded-file counter. Probe verified deletion does not reuse IDs, older snapshot load preserves the greater counter, and a new session starts at 1. |
| Low RD-04 | FR-43 specified a temporary sibling file in a functional requirement, conflating the required observable outcome with its implementation mechanism. | Lecture 04 p. 30: describe WHAT, as far as possible, rather than HOW. | FR-43 now states complete replacement after a successful write and preservation of prior destination bytes on failure. The existing temporary sibling / `os.replace` strategy remains fully documented in design and contract. No behavior or requirement ID changed. |
| Low RD-05 | FR-49 broadly promised prompt recovery from any I/O failure, whereas `run` deliberately allows stream I/O errors to propagate. A failed terminal cannot reliably display a new prompt. | Official p. 1: realistic/verifiable requirements; design signature already documented stream errors. | FR-49 now says file I/O failure; nearby prose states the usable input/output stream assumption. This does not excuse invalid-input/file failures; those still require recovery. Catalogue synchronized. |
| Low RD-06 | Technical Contract said `contains` had a fixed spelling, although `_Parser._take` compares words with `casefold()`. | Official p. 2: design must describe actual interfaces. | Contract now explicitly documents the case-insensitive keyword. Fresh `TEXT CONTAINS "ALP"` probe matched the note. No new command syntax was introduced. |
| Low RD-07 | Diagram arrows mix dependencies and data exchanges. The storage-to-model arrow labelled “validated replacement manager” could be mistaken for a returned manager going to the model rather than controller. | Official pp. 1–2 / Appendix A: diagram understanding and explanatory text. | Figure 1 prose now explicitly defines that edge as construction/validation dependency and explains that the returned manager goes to the controller. The MMD/SVG/PNG sources remain unchanged and mutually consistent; no new drawing was claimed. |
| Low RD-08 | Main design signatures used `Record`, `RecordType`, `TextField`, `TimeField` aliases without defining their exact domains in that document; the private `_print_records` table omitted the input collection type. | Official p. 2: names, arguments/types, returns and possible exceptions. | Added alias domains, the current tuple-of-records caller contract (labelled as documentation for an unannotated parameter), and controller syntax exception description. Added UTF-8 text constraint already present in model validation. AST name check confirmed every public top-level class/function and public method in `src` is represented in the document; signatures were manually compared with code. |
| Medium RD-09, implementation-owned | Deep JSON parsing on Python 3.11 can raise `RecursionError`, bypassing the old file error conversion. The implementation reviewer independently reproduced and repaired it. | FR-44/47/49 and official reliability/error-handling rubric. | Design/contract now describe parser-depth errors converted to `PersistenceError(FORMAT)` before controller recovery. Source/test changes and cross-version evidence belong to the overall implementation review. No public signature changed. |
| Medium RD-10, implementation-owned | A prompt written to a line-buffered stream without a newline may remain invisible until after blocking input. The implementation reviewer added a flush-before-read regression and fix. | Usable local CLI and correct prompt interaction. | Design/contract now explicitly state prompt is written and flushed before reading. Source/test evidence belongs to the overall implementation review. |

## Completeness and correspondence checks

The SRS retains exactly the six non-exempt chapters: Preface, Introduction, Glossary, User requirements definition, System architecture, and System requirements specification. The official p. 1 exemption covers System models, System evolution, Appendix and Index. Their absence is not a defect. Preface includes readership and version rationale; user requirements include services and quality/standard constraints; architecture states responsibility allocation without fixing classes; detailed FR/NFR sections use numbered **shall** statements, verification ideas and rationale groups.

| Official story | Independently inspected implementation and specification correspondence |
|---|---|
| US1 | Four record dataclasses share one manager collection; FR-01 and the ID/duplicate-value rules describe the group interaction choice. |
| US2 | `Note.text`, `create_note`, add/show path; FR-02/06/14. |
| US3 | `Task.description/deadline`, exact time parsing, create and update; FR-03/06/07/14. |
| US4 | `Event.description/start_time/alarm_time`; FR-04/06/07/14. The group scope stores alarm data and does not promise notification delivery. Appendix B does not explicitly require a notification mechanism. |
| US5 | `Contact.name/address/mobile_number`; FR-05/06/08/14. Mobile values remain strings. |
| US6 | `PIMManager.update` validates one replacement field before assignment; FR-16/17/23. Every data field is reachable by the CLI field name. |
| US7 | Type, all five text fields, all three time fields with `<`, `>`, `=`, Boolean nodes and explicit-stack parsing/evaluation; FR-26–40. Parentheses and `!`, `&&`, `||` precedence are group choices, not invented course wording. |
| US8 | `show ID` and `show all` expose all data; list/search summaries are additional selection support and do not replace detailed display; FR-18–21/23. |
| US9 | Manager deletes only the selected existing record; FR-22/23. |
| US10 | Complete `.pim` snapshot save and replacement behavior; FR-41–43/48. |
| US11 | Full-file validation and replacement manager with preserved greater counter; FR-44–48. |

All 50 FR and 5 NFR identifiers remain unchanged. The source labels and verification ideas in `requirements-catalog.csv` remain aligned with SRS. The catalogue preserves its UTF-8 BOM and CSV quoting. Only FR-06, FR-09, FR-43 and FR-49 statements changed in this subreview; verification ideas for FR-06/09/43 changed accordingly. Coverage tables should retain these IDs and use the updated statements rather than duplicate stale text.

The design explains the selected layered/MVC-style separation, group instantiation, alternatives and costs, immutable replacement, model independence from terminal/files, and storage as an adapter. The architecture and components diagrams show the main dependencies; the search/update sequence follows actual controller → parser → manager → criterion calls, selection with `show`, and validated update. The sequence is explicitly a successful example, with failure paths explained in prose; the assignment does not require every error branch in that example diagram. Existing PNGs are legible without truncation when inspected at full image size. Page-scale readability must still be checked in the newly exported Design PDF by the overall reviewer.

## Fresh verification in this subreview

Executed with `D:/conda/python.exe` against the current repository source; paths are review-environment evidence, not required user commands:

1. Regex-parsed all numbered SRS requirements and CSV-decoded all rows: **55 unique IDs, exact statement and verification-idea equality**.
2. Asserted all six required chapter headings and US1–US11 table rows exist.
3. Executed and asserted text normalization, padded-time rejection with unchanged records/counter, uppercase `CONTAINS`, and absent-field negation.
4. Executed and asserted session-local monotonic IDs, older-snapshot counter preservation, and independent new-session counter initialization.
5. AST-enumerated all public top-level classes/functions and public methods in `src`, then checked their names occur in Design Document; manually compared interface fields, argument names/types, return contracts and exception categories.
6. `git diff --check -- docs/srs docs/design` returned no whitespace errors.
7. Read all three Mermaid files and inspected all three PNG renders. No diagram source was modified, so no SVG/PNG regeneration was needed.

These are focused review probes, not additions to the project's automated test count or claims of a new coverage percentage. Full suite, line-coverage measurement, PDF rendering and clean-extraction verification are reported by the overall review.

## Remaining responsibilities

- Overall reviewer: regenerate SRS and Design PDFs from these sources, inspect every rendered page including diagrams/tables, reconcile coverage table wording and `decisions.md`, and package the updated source plus verification reports.
- Human group: provide genuine names/IDs, review the group choices and AI-assisted changes, supply the required videos and truthful signed declaration/contribution agreement. This review does not represent human consensus.
- NFR-01's exact disconnected and no-graphical-session environment check remains unproven unless separately executed; a standard-library import audit is not substituted for it.
