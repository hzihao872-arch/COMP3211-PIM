# Project Requirements Checklist

Source: verified 2026 Course Project Description PDF, pages 1–4; see [official requirements matrix](docs/plans/official-requirements-matrix.md). Unchecked boxes track future delivery, not disagreement with the official requirement. Group implementation choices are in [decisions.md](decisions.md).

## Administration and submission (PDF pp. 1, 3)

- [x] The user confirmed on 2026-09-30 that the Canvas group was formed and currently has 4 members.
- [ ] Verify the registration completion time against the 2026-09-28 09:00 deadline if claiming timely registration. Any late group change follows the written-consent rule by 2026-10-12 09:00.
- [ ] Submit all deliverables in one ZIP by 2026-11-20 20:00.
- [ ] Use DOC, DOCX, or PDF for documents unless the PDF specifies a different format.
- [ ] Place the completed Honour Declaration in the ZIP root, acknowledge real GenAI-assisted content, and state member-agreed actual contribution percentages. Obtain the real form, identity data, and signatures from humans.

## Product stories (PDF p. 4)

- [ ] **US1** — Create different types of PIR in one PIM.
- [ ] **US2** — Create a plain-text note.
- [ ] **US3** — Create a task with description and deadline.
- [ ] **US4** — Create an event with description, starting time, and alarm.
- [ ] **US5** — Create a contact with name, address, and mobile number.
- [ ] **US6** — Modify an existing PIR.
- [ ] **US7** — Search by type; text containment in note text, description, name, address, or mobile number; time `<`, `>`, `=` on deadline, starting time, or alarm; combinations with `&&`, `||`, `!`.
- [ ] **US8** — Print detailed data for one PIR or all PIRs.
- [ ] **US9** — Delete a specified PIR.
- [ ] **US10** — Store PIRs in a `.pim` file.
- [ ] **US11** — Load PIRs from a `.pim` file.

## Product and document constraints (PDF pp. 1–2)

- [ ] Run the PIM via a command-line interface. The group chose Python; Java or Python is officially allowed.
- [ ] Put all model code in a separate package named `model`; use only the selected language's standard libraries in the implementation. Other main components must be identifiable.
- [ ] SRS (6 points): cover all stories and important functional/non-functional requirements with valid, consistent, complete, realistic, verifiable statements. Follow the Lecture 04 structure, omitting only the four chapters the PDF excludes.
- [ ] Design document (5 points): include architecture, main-component structure/relationship, and search-then-update process diagrams, each with explanatory text; explain architecture choice and component instantiation. Document classes/fields/public or protected methods (or procedural types/functions), with return type, name, argument names/types, and possible exceptions.
- [ ] Implementation (6 points): complete source, developer manual, user manual, system demo, and a requirements coverage table of implemented/not-implemented Appendix B stories **and** SRS requirements in the source-code root.
- [ ] Developer manual: state actual Python version, IDE, build/launch commands and parameters and/or debugging launch, for at least one platform.
- [ ] User manual: document all commands, formats, invalid-command behavior, and output interpretation.
- [ ] Automatically execute all model unit tests (4 points) and pass; each test identifies exercised functionality and expected results. Put model line coverage in a separate report in the source-code root. No minimum percentage is specified.

## Video and presentation (PDF pp. 2–3)

- [ ] System demo: MP4, no more than 4 minutes, showing important features.
- [ ] Presentation (4 points): PDF slides and MP4 recording, no more than 5 minutes; cover creation, defining a search criterion, and searching for PIRs, overall architecture/component design, and one lesson from requirements engineering, API design, or unit testing.
- [ ] Every actual member presents for at least 1 minute. Each presenter shows their student ID card and face at the beginning of their presentation; the current speaker's face stays visible. Human review verifies these facts against the real recording.

## Official grading dimensions (PDF p. 4)

- [ ] Review SRS completeness, document quality, and requirements quality.
- [ ] Review design completeness, document/design quality, and diagram quality.
- [ ] Review implementation completeness, document/code quality, and requirements coverage.
- [ ] Review model-test completeness, test quality, and test coverage.
- [ ] Review presentation completeness, required content, delivery, and timing.
