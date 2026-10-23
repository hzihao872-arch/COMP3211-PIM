# Group presentation speaking script

**Group:** 89. Replace `MEMBER_A` through `MEMBER_D` only with the four real members and their verified student IDs. Do not infer contribution percentages.<br>
**Implementation:** Current usability release candidate; use its accompanying manifest and test report.<br>
**Recording:** `Presentation_Recording.mp4`, maximum **5:00**. The planned windows total about **4:48** and reserve short handovers. They are estimates, not measured rehearsal or video durations. Each real member must speak for at least **1:00**, confirmed by timing the recording.

At the beginning of **each member's** first speaking turn, show that member's real student ID card and face. Keep the current speaker's face visible throughout their speech. Check the final recording for both rules.

The script was revised on 2026-10-23 and must be timed in a real rehearsal. Aim initially for about 65-70 seconds of speech per member, then adjust wording to the actual delivery. The final member's architecture-and-testing section may need shortening. Reserve time for identity display and handovers, and verify both each person's minimum of 60 seconds and the complete recording's maximum of 300 seconds on the exported MP4. Planned windows are not measured evidence.

## MEMBER_A — planned 0:00–1:10 — slides 1–2

“We built a command-line personal information manager for notes, tasks, events, and contacts. The program stores them together and gives each new record an increasing ID. The first requirement I want to show is creation. FR-03 says a task must have a description and a deadline. In the current program, `add task "draft" "2026-10-01 09:00"` creates task 2 after a note has been added. `show 2` prints both fields, and the deadline follows the local year-month-day, hour-minute format. Notes, events, and contacts have their own required fields. We keep the data model separate from the command parser so a rejected field does not consume an ID. The model checks accepted values, including empty text and impossible dates. A failed creation leaves the collection and next ID unchanged.”

## MEMBER_B — planned 1:12–2:22 — slide 3

“The next requirement is how a user defines a search criterion. FR-26 makes the expression after `search` the criterion for that command. It is parsed and run immediately, with no stored query to manage later. Here the left side asks for a task before a deadline, and the right side looks for text containing `memo`. Parentheses group the type and time conditions. `&&` means both conditions must hold, while `||` allows either branch. Search values must be in quotes, even the single word `task`. The parser creates criterion objects and rejects malformed input before the manager searches; it never evaluates the user's expression as Python code. The grammar also supports NOT. An unknown field or unmatched parenthesis produces a search error with its character position. `help search` explains the grammar and examples.”

## MEMBER_C — planned 2:24–3:34 — slide 4

“FR-27 requires the valid criterion to be evaluated against every current record, and FR-39 requires matching summaries in increasing ID order. With our four sample records, the compound expression returns note 1 because its text contains `memo`, and task 2 because it is a task with an earlier deadline. The event and contact do not match. The summaries show each ID, type, and first text field. We then update task 2's description to `revised`, inspect it, and delete note 1. Saving and loading in a second process restores the remaining three records. A later note receives ID 5. The system preserves the counter, so deleting a record does not recycle its ID. Loading validates the whole snapshot before replacing the active collection. Unsaved edits block loading unless the user explicitly adds `force=true`.”

## MEMBER_D — planned 3:36–4:48 — slides 5–6

“The architecture uses layered, MVC-style separation. `CommandController` handles terminal commands and output. `PIMManager` owns records and IDs; criteria and validators sit in the `model` package. The storage adapter validates a complete replacement before loading changes the active manager. This separation lets model tests run without terminal or file input. The AI-assisted development record shows a testing lesson: deep expressions initially exceeded Python's recursion limit. A failing regression guided iterative parsing and evaluation. It also checks the next command, proving the session continues. The usability release suite passes 86 tests on Python 3.11.9, 3.12.3 and 3.13.5. On Python 3.13.5, source-line tracing covers 431 of 436 model lines, or 98.85 percent. Non-source bookkeeping entries are excluded; this is not branch coverage. The tests assert specific outcomes, including every editable field and Boolean truth tables.”

**Evidence cross-check:** Before recording, confirm the test count and model coverage against the candidate's `Test_Coverage.pdf` and slide 6. This script describes a planned delivery, not a completed human rehearsal.

**Group review:** Understand and verify the AI-assisted example before presenting it. Describe your own actual learning and contributions accurately; the script is a draft for adaptation, not evidence that every member personally implemented the recorded fix.

## Rehearsal record for the group

Fill this only from actual timed rehearsal or the final MP4. If any person speaks for less than 1:00, revise their wording or handovers and record again.

| Speaker | Real name and student ID | Measured speaking start/end | Measured speaking duration | ID card and face checked | Face visible throughout |
|---|---|---|---|---|---|
| MEMBER_A | Human input pending | Not yet rehearsed | Not yet measured | Pending | Pending |
| MEMBER_B | Human input pending | Not yet rehearsed | Not yet measured | Pending | Pending |
| MEMBER_C | Human input pending | Not yet rehearsed | Not yet measured | Pending | Pending |
| MEMBER_D | Human input pending | Not yet rehearsed | Not yet measured | Pending | Pending |

**Whole recording duration:** Not yet measured. **Human review of facts, delivery, and pronunciation:** Pending.
