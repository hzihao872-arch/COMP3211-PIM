# PIM Product Decisions

The official rules are recorded separately in [the official requirements matrix](docs/plans/official-requirements-matrix.md). The rules below are **WP00 group design choices**, not claims made by the course PDF. They form the working baseline requested for this package; the AI-assisted workshop is not a meeting or vote of human members. A human group review can record amendments here before WP01 is approved.

## Existing project choices

| Topic | Choice | Recorded | Basis |
|---|---|---|---|
| Implementation language | Python | 2026-09-21 | Existing repository decision; PDF permits Java or Python (p. 1). |
| Repository and branch | Private GitHub repository; `main` is the default branch | 2026-09-21 | Existing collaboration decision. |
| Test framework | Standard-library `unittest` | 2026-09-21 | Existing choice; the PDF recommends a framework but does not mandate one (p. 2). |
| Package structure | Separate `model`, `controller`, and `storage` packages | 2026-09-21 | `model` is official; the other names are a group architecture choice. |

## WP00 product baseline (2026-09-30)

| Topic | Decision and reason |
|---|---|
| Runtime | Support Python 3.11; support any newer version only when it is explicitly listed and verified in the developer manual. Record the actual development version there. This fixes a testable baseline without claiming a course minimum. |
| Record identity | Each PIR receives an integer ID in 1..9999999999999999999 starting at 1. The next-ID counter may additionally be 10000000000000000000, a persisted exhaustion marker. Exhausted creation fails before mutation. Within one process session, newly assigned IDs increase monotonically and are not reused after deletion or reload. Loading also respects the file counter. A fresh process without a loaded snapshot has no external ID history and starts at 1. A failed creation does not consume an ID. IDs and record types cannot be changed by `update`. Duplicate field values are permitted. |
| Record schema | `note`: `text`; `task`: `description`, `deadline`; `event`: `description`, `start_time`, `alarm_time`; `contact`: `name`, `address`, `mobile_number`. All fields are required. Text fields are single-line and nonempty after trimming leading/trailing whitespace; store the trimmed text. Time fields follow the exact date/time format below and do not accept surrounding whitespace. Mobile numbers remain strings, preserving `+` and leading zeros; no region-specific validation. |
| Date and time | Use `YYYY-MM-DD HH:mm`, 24-hour local time without a timezone, at minute precision. Reject impossible calendar dates. Compare values chronologically. Past dates are allowed; no alarm/start ordering constraint is added. |
| CLI commands | `help [COMMAND]`, `add TYPE "FIELD"...`, `list [TYPE]`, `show ID`, `show all`, `update ID FIELD "VALUE"`, `delete ID`, `search EXPR`, `save "PATH.pim"`, `load "PATH.pim" [force=true&#124;force=false]`, `exit`. `add` requires the fields in the schema order above. `update` changes exactly one field. `search` takes the remaining command line as its expression. `list` and `search` show ID, type, and the complete first text field (`text`, `description`, or `name`); `show` gives all fields. Results and `show all` are ordered by ascending ID. EOF exits normally. |
| CLI tokens | Command names, type names, and field names are case-insensitive. String/path arguments with spaces use double quotes; within them `\"` and `\\` escape a quote and backslash. A one-token value may also be unquoted except that search literals must be quoted. Wrong argument counts or malformed quoting are errors. Relative paths are resolved from the process working directory. |
| Search grammar | Atom forms are `type = "TYPE"`, `TEXT_FIELD contains "STRING"`, and a time field followed by one of `<`, `>`, `=` and a quoted `YYYY-MM-DD HH:mm` value. Text fields are `text`, `description`, `name`, `address`, `mobile_number`; time fields are `deadline`, `start_time`, `alarm_time`. A nonempty string is required for `contains`. Type names and text containment are case-insensitive. Parentheses bind first, then `!`, then `&&`, then logical OR (&#124;&#124;); operators of equal precedence group left to right. Spaces may appear between tokens. |
| Search evaluation | An atom using a valid field absent from a particular record is false; its negation is true. An unknown field, invalid operator or literal, malformed expression, or unmatched parenthesis is an error for the whole search. Search errors do not change stored data. Type matching uses the four canonical type names. |
| Save format | `.pim` files contain UTF-8 JSON with exactly four top-level keys: `format` set to `COMP3211-PIM`, `version` set to integer `1`, `next_id`, and `records`. `records` is an ID-ascending array of objects with `id`, `type`, and exactly the data fields for that type. The file extension is exactly `.pim`. Saving may replace an existing file; write to a temporary sibling and replace it only after successful serialization. |
| Load behavior | Reject a load with unsaved changes unless its final option is `force=true` (case-insensitive); omitted force or `force=false` keeps protection. Reject other options. Parse and validate the entire file, including format/version, exact record schemas, field values, unique positive IDs, and a file `next_id` greater than all IDs in that file. On success replace the in-memory collection; set the next ID to the greater of its pre-load value and the file's `next_id` so loading an older snapshot never reassigns an ID already issued in this session. Do not merge records. On any failure, preserve the current in-memory collection and next ID. |
| Invalid input | Unknown commands, missing/invalid IDs, wrong fields/types, invalid dates/search expressions, invalid paths/files, and file I/O failures produce a useful message and return to the prompt. A failed operation does not partially change in-memory data. |
| Scope | Build one local CLI PIM. No GUI, network, accounts, database, recurring tasks, tags, or notifications; the PDF says extra features earn no extra credit (p. 1). |

## Change control

WP01 must turn these choices into verifiable requirements and examples. WP02 may choose internal class and function names but must not silently change the public CLI, fields, search semantics, or save/load behavior. Record any group-approved change here with its date, reason, and affected requirements before changing downstream artifacts.

| Date | WP01 clarification | Reason | Affected SRS requirements | Human status |
|---|---|---|---|---|
| 2026-09-30 | On successful load, use the greater of the pre-load and file `next_id` values. | The earlier wording simultaneously prohibited ID reuse after reload and restored an older file counter; this rule resolves that conflict. | FR-09, FR-46, FR-47 | AI-assisted working-baseline clarification; group review remains pending. |
| 2026-09-30 | Name Python 3.11 as the verified target; list later versions only after verification. | An unbounded “or newer” claim cannot be objectively tested. | NFR-02 | AI-assisted working-baseline clarification; group review remains pending. |

| 2026-10-23 | Clarified text-only trimming, exact time format, session-scoped ID history, and file-I/O recovery. | Independent review found wording broader than the implemented and intended contract; no new feature or relaxation of field validation. | FR-06, FR-07, FR-09, FR-49 | AI-assisted clarification; group review pending. |

## Authorized usability refinement (2026-10-23)

The user explicitly requested keeping this PIM mainline and adding the peer's unsaved-data protection, focused help and positioned errors. This refines the earlier CLI baseline. Successful add/update/delete sets a conservative controller dirty flag, even if an update repeats the same value. Successful save/load clears it; failures and read-only commands preserve it. Injected existing records start dirty. Exit and EOF warn once and terminate; there is no implicit save or confirmation loop. `help COMMAND` adds usage/details/examples. Search errors count one-based Unicode characters within EXPR; missing input points to length plus one. Quoted command errors count characters in the original command line. FR-24/25/44/46/49 and FR-51–FR-54 record the behavior. Record schemas, ID allocation and version 1 snapshots remain compatible. Human membership/contribution declarations remain pending.

## 2026-10-23 - Source hardening decisions

The user authorized implementation of `suggestion_v2.md`. Adopt bounded ID/counter ranges (FR-09), bounded ASCII diagnostics and record/file context (FR-49), flush/fsync before snapshot replacement (FR-43), UTF-8 BOM input compatibility, and best-effort dirty Ctrl+C warnings. Shared record metadata lives in `model/schema.py`; all expected failures derive from `PIMError`. Existing quoting and complete list/search fields remain unchanged. Final PDFs and candidate ZIPs remain historical until a separately prepared release.

## 2026-10-23 - Fatal command-input errors

Following the review of `suggestion_v3.md`, the user authorized a focused read-boundary fix: OSError/UnicodeError from command input terminates with status 1, bounded stderr and one best-effort dirty warning. Do not return success, retry a broken input, catch unrelated programming errors or save implicitly. Normal command recovery, EOF, Ctrl+C and output-pipe closure keep their existing contracts. FR-49 and its catalogue entry are synchronized.
