# Official Requirements Matrix — 2026 Course Project

Source: the four-page PDF identified in [references/README.md](../../references/README.md). Page numbers are the printed PDF pages. “Official” means the PDF states the rule; “Group choice” is a concrete project convention, not an additional teacher requirement. The planned evidence is a future check, not a claim that an artifact already exists.

| ID | PDF page | Requirement summary | Official/group choice | Planned evidence |
|---|---:|---|---|---|
| ADM-01 | 1 | Develop one command-line PIM. | Official | CLI acceptance run, SRS, user manual. |
| ADM-02 | 1 | Form a group of 3–4 on Canvas by 2026-09-28 09:00; ungrouped students are randomly assigned afterward. | Official; user confirmed group formed with 4 current members on 2026-09-30 | Human report recorded in task register. |
| ADM-03 | 1 | Late group changes need written agreement of all affected group members before 2026-10-12 09:00. | Official | Human review if a change occurred. |
| ADM-04 | 1 | Java or Python is permitted; another language needs instructor consultation. | Official; Python is group choice | Source and developer manual. |
| ADM-05 | 1 | Submit all deliverables in one ZIP by 2026-11-20 20:00. | Official | Final ZIP manifest and human upload confirmation. |
| ADM-06 | 1 | Documents are DOC, DOCX, or PDF unless specified otherwise. | Official; final documents use PDF by group choice | ZIP file type inspection. |
| SRS-01 | 1 | SRS is worth 6 points; cover all Appendix B stories with valid, consistent, complete, realistic, verifiable requirements. | Official | SRS review and US traceability. |
| SRS-02 | 1 | Follow Lecture 04 SRS structure, omitting System models, System evolution, Appendix, and Index. | Official | Structure review against the actual slides at WP01. |
| SRS-03 | 1 | Include important functional and non-functional requirements. | Official | SRS requirement catalog. |
| SRS-04 | 1–2 | Put all model code in a separate package named `model`. | Official | Package inspection and model tests. |
| SRS-05 | 1 | Additional features such as GUI/online use are not recommended and earn no extra credit. | Official advice, not a prohibition; narrow CLI scope is group choice | Scope review. |
| DES-01 | 1–2 | Design document is worth 5 points; provide architecture diagram, main-component structure/relationship diagrams, and a search-then-update example process diagram. | Official | Design diagram inventory and rendered document. |
| DES-02 | 1–2 | Explain architectural pattern choice, reasons, and how its components appear in this PIM. | Official | Design text and architecture diagram review. |
| DES-03 | 2 | Explain classes, fields, public/protected methods if OO; or data types/functions if procedural. Give each method/function return type, name, argument names/types, possible exceptions, and component relationships. | Official; OO is a recommendation, not a mandate | Design/API review against source. |
| DES-04 | 2 | Use a sequence or activity diagram for example collaboration; accompany every diagram with necessary explanation. | Official | Diagram and caption review. |
| IMP-01 | 2 | Implementation is worth 6 points; include complete source, developer manual, user manual, short system demo, and requirements coverage report. | Official | Release manifest. |
| IMP-02 | 2 | Only invoke selected language's standard libraries; keep `model` separate and other major components identifiable. | Official; `controller`/`storage` names are group choices | Import audit and package inspection. |
| IMP-03 | 2 | Developer manual identifies actual development JDK/Python version, IDE, build commands/parameters and/or debugging launch for one platform. | Official | Execute documented commands from clean checkout. |
| IMP-04 | 2 | User manual explains commands, formats, invalid command behavior, and output interpretation. | Official | Manual-to-CLI reconciliation. |
| IMP-05 | 2 | System demo is MP4, no more than 4 minutes, demonstrating important features. | Official | MP4 metadata check and viewing. |
| IMP-06 | 2 | Requirements coverage table states which Appendix B stories and SRS requirements are/are not implemented; place it in source-code root. | Official | Root-location and content check. |
| TST-01 | 2–3 | Model unit tests are worth 4 points, identify exercised behavior and expected result, execute automatically, and pass. | Official; `unittest` is group choice | Test command output and test review. |
| TST-02 | 3 | Report model **line** coverage separately in source-code root. | Official; no minimum percentage stated | Coverage tool output and root report. |
| PRE-01 | 3 | Presentation is worth 4 points, is at most 5 minutes; slides PDF, recording MP4. | Official | PDF/MP4 inspection and duration check. |
| PRE-02 | 3 | Every member presents at least 1 minute; each presenter shows student ID card and face at the beginning of their presentation, and the current speaker's face remains visible. Missing card or face halves that member's presentation marks. | Official | Human timed viewing against real member roster. |
| PRE-03 | 3 | Present three requirements: PIR creation, criterion definition, and search; overall design from architecture plus component structure; one lesson from requirements engineering, API design, or unit testing. | Official | Slide and recording content checklist. |
| PRE-04 | 3 | System snapshots or short clips may appear in the presentation but should not dominate its limited time. | Official guidance | Human slide and recording review. |
| DEC-01 | 3 | Declare GenAI-assisted content properly. Honour Declaration is required even without GenAI and belongs in ZIP root; missing or false declaration can cost up to 30% of total points. | Official | Real signed form, AI-use log, ZIP-root check. |
| DEC-02 | 3 | Members agree actual contribution percentages and state them in the declaration; individual score is min(group score × member count × contribution share, group score). If consensus fails, submit other items and report to instructor before deadline. | Official | Human-confirmed contributions and declaration. |
| GRADE-01 | 4 | Appendix A grades SRS completeness, document quality, and requirements quality. | Official criteria | SRS review. |
| GRADE-02 | 4 | Appendix A grades design completeness, document/design quality, and diagram quality. | Official criteria | Design review. |
| GRADE-03 | 4 | Appendix A grades implementation completeness, document/code quality, and requirements coverage. | Official criteria | Integration audit. |
| GRADE-04 | 4 | Appendix A grades test completeness, test quality, and test coverage. | Official criteria | Test and coverage audit. |
| GRADE-05 | 4 | Appendix A grades presentation completeness, content, delivery, and timing. | Official criteria | Human recording review. |
| US1 | 4 | Create different PIR types and manage them in one PIM. | Official | Four-type CLI acceptance and SRS coverage. |
| US2 | 4 | Create plain-text note PIRs. | Official | Note creation test and demo. |
| US3 | 4 | Create task PIRs with description and deadline. | Official | Task creation test. |
| US4 | 4 | Create event PIRs with description, starting time, and alarm. | Official | Event creation test. |
| US5 | 4 | Create contact PIRs with name, address, and mobile number. | Official | Contact creation test. |
| US6 | 4 | Modify data in existing PIRs. | Official | Update test and search-update scenario. |
| US7 | 4 | Search type and field data: text containment in note/description/name/address/mobile; time `<`, `>`, `=` on deadline/start/alarm; `&&`, OR (&#124;&#124;), `!` combinations. | Official; parser details in `decisions.md` are group choices | Positive/negative search tests for every field, operator, and combination. |
| US8 | 4 | Print detailed information for a selected PIR or all PIRs. | Official | CLI display acceptance. |
| US9 | 4 | Delete a specified PIR. | Official | Delete test. |
| US10 | 4 | Store PIRs in a `.pim` file. | Official; JSON interior is group choice | Four-type round-trip test. |
| US11 | 4 | Load PIRs from a `.pim` file. | Official; replace/validation semantics are group choices | Load and corrupt-file preservation tests. |

**Interpretation guardrails:** The PDF suggests object orientation and a test framework but does not require either. It does not mandate Python 3.11, `unittest`, internal JSON, a command vocabulary, a coverage threshold, or the numbered ZIP folders in the project plan.
