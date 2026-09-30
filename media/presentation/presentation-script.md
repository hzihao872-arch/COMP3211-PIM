# Group presentation speaking script

**Group:** 89. Replace `MEMBER_A` through `MEMBER_D` only with the four real members and their verified student IDs. Do not infer contribution percentages.<br>
**Frozen implementation:** `4d3508db0447a3ac6346a2a2789da89208f88fd5`.<br>
**Recording:** `Presentation_Recording.mp4`, maximum **5:00**. The planned windows total about **4:48** and reserve short handovers. They are estimates, not measured rehearsal or video durations. Each real member must speak for at least **1:00**, confirmed by timing the recording.

At the beginning of **each member's** first speaking turn, show that member's real student ID card and face. Keep the current speaker's face visible throughout their speech. Check the final recording for both rules.

Text-length estimate for rehearsal planning: A 128 words, B 127, C 123, D 134. At an assumed 120 spoken words per minute, the text alone would take about 64, 64, 62, and 67 seconds respectively, before pauses, ID display, or handovers. This is **not** a timed human read-through. The group must measure each actual speaking interval and shorten or expand the script to meet both timing limits.

## MEMBER_A — planned 0:00–1:10 — slides 1–2

“We built a command-line personal information manager for notes, tasks, events, and contacts. The program stores them together and gives each new record an increasing ID. The first requirement I want to show is creation. FR-03 says a task must have a description and a deadline. In the frozen program, `add task "draft" "2026-10-01 09:00"` creates task 2 after a note has been added. `show 2` prints both fields, and the deadline follows the local year-month-day, hour-minute format. Notes, events, and contacts have their own required fields. We keep the data model separate from the command parser so a rejected field does not consume an ID. The model checks accepted values, including empty text and impossible dates. A failed creation leaves the collection and next ID unchanged.”

## MEMBER_B — planned 1:12–2:22 — slide 3

“The next requirement is how a user defines a search criterion. FR-26 makes the expression after `search` the criterion for that command. It is parsed and run immediately, with no stored query to manage later. Here the left side asks for a task before a deadline, and the right side looks for text containing `memo`. Parentheses group the type and time conditions. `&&` means both conditions must hold, while `||` allows either branch. Search values must be in quotes, even the single word `task`. The parser creates criterion objects and rejects malformed input before the manager searches; it never evaluates the user's expression as Python code. The grammar also supports NOT. An unknown field or unmatched parenthesis produces a search error without partial results or any data change.”

## MEMBER_C — planned 2:24–3:34 — slide 4

“FR-27 requires the valid criterion to be evaluated against every current record, and FR-39 requires matching summaries in increasing ID order. With our four sample records, the compound expression returns note 1 because its text contains `memo`, and task 2 because it is a task with an earlier deadline. The event and contact do not match. The summaries show each ID, type, and first text field. We then update task 2's description to `revised`, inspect it, and delete note 1. Saving and loading in a second process restores the remaining three records. A later note receives ID 5. The system preserves the counter, so deleting a record does not recycle its ID. Loading validates the whole snapshot before replacing the active collection.”

## MEMBER_D — planned 3:36–4:48 — slides 5–6

“The architecture separates the command controller, model, and file storage. `CommandController` reads the terminal command and shows results. `PIMManager` owns records and IDs; search criteria and validators sit in the `model` package. The storage adapter writes a versioned `.pim` snapshot and validates a complete replacement manager before a load changes the live one. This separation lets model tests run without terminal or file input. Our lesson came from unit testing: deep expressions first exceeded Python's recursion limit. We added a failing regression test, replaced recursive parsing and evaluation with iterative stacks, and reran the full suite. The regression checks a following command too, so we know the session continues. The WP04 evidence records 33 passing tests and 411 of 430 model lines covered on Python 3.13.5. Python 3.11 remains unverified.”

## Rehearsal record for the group

Fill this only from actual timed rehearsal or the final MP4. If any person speaks for less than 1:00, revise their wording or handovers and record again.

| Speaker | Real name and student ID | Measured speaking start/end | Measured speaking duration | ID card and face checked | Face visible throughout |
|---|---|---|---|---|---|
| MEMBER_A | Human input pending | Not yet rehearsed | Not yet measured | Pending | Pending |
| MEMBER_B | Human input pending | Not yet rehearsed | Not yet measured | Pending | Pending |
| MEMBER_C | Human input pending | Not yet rehearsed | Not yet measured | Pending | Pending |
| MEMBER_D | Human input pending | Not yet rehearsed | Not yet measured | Pending | Pending |

**Whole recording duration:** Not yet measured. **Human review of facts, delivery, and pronunciation:** Pending.
