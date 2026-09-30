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
| Runtime | Target Python 3.11 or newer. Record the actual development version in the developer manual. This fixes a testable baseline without claiming a course minimum. |
| Record identity | Each PIR receives a positive integer ID starting at 1. IDs increase monotonically, are unique, and are not reused after deletion or reload. A failed creation does not consume an ID. IDs and record types cannot be changed by `update`. Duplicate field values are permitted. |
| Record schema | `note`: `text`; `task`: `description`, `deadline`; `event`: `description`, `start_time`, `alarm_time`; `contact`: `name`, `address`, `mobile_number`. All fields are required, single-line, and nonempty after trimming leading/trailing whitespace; store the trimmed value. Mobile numbers remain strings, preserving `+` and leading zeros; no region-specific validation. |
| Date and time | Use `YYYY-MM-DD HH:mm`, 24-hour local time without a timezone, at minute precision. Reject impossible calendar dates. Compare values chronologically. Past dates are allowed; no alarm/start ordering constraint is added. |
| CLI commands | `help`, `add TYPE "FIELD"...`, `list [TYPE]`, `show ID`, `show all`, `update ID FIELD "VALUE"`, `delete ID`, `search EXPR`, `save "PATH.pim"`, `load "PATH.pim"`, `exit`. `add` requires the fields in the schema order above. `update` changes exactly one field. `search` takes the remaining command line as its expression. `list` and `search` show ID, type, and the complete first text field (`text`, `description`, or `name`); `show` gives all fields. Results and `show all` are ordered by ascending ID. EOF exits normally. |
| CLI tokens | Command names, type names, and field names are case-insensitive. String/path arguments with spaces use double quotes; within them `\"` and `\\` escape a quote and backslash. A one-token value may also be unquoted except that search literals must be quoted. Wrong argument counts or malformed quoting are errors. Relative paths are resolved from the process working directory. |
| Search grammar | Atom forms are `type = "TYPE"`, `TEXT_FIELD contains "STRING"`, and a time field followed by one of `<`, `>`, `=` and a quoted `YYYY-MM-DD HH:mm` value. Text fields are `text`, `description`, `name`, `address`, `mobile_number`; time fields are `deadline`, `start_time`, `alarm_time`. A nonempty string is required for `contains`. Type names and text containment are case-insensitive. Parentheses bind first, then `!`, then `&&`, then logical OR (&#124;&#124;); operators of equal precedence group left to right. Spaces may appear between tokens. |
| Search evaluation | An atom using a valid field absent from a particular record is false; its negation is true. An unknown field, invalid operator or literal, malformed expression, or unmatched parenthesis is an error for the whole search. Search errors do not change stored data. Type matching uses the four canonical type names. |
| Save format | `.pim` files contain UTF-8 JSON with exactly four top-level keys: `format` set to `COMP3211-PIM`, `version` set to integer `1`, `next_id`, and `records`. `records` is an ID-ascending array of objects with `id`, `type`, and exactly the data fields for that type. The file extension is exactly `.pim`. Saving may replace an existing file; write to a temporary sibling and replace it only after successful serialization. |
| Load behavior | Parse and validate the entire file, including format/version, exact record schemas, field values, unique positive IDs, and a next ID greater than all existing IDs. On success replace the in-memory collection and next ID; do not merge. On any failure, preserve the current in-memory state. |
| Invalid input | Unknown commands, missing/invalid IDs, wrong fields/types, invalid dates/search expressions, invalid paths/files, and I/O failures produce a useful message and return to the prompt. A failed operation does not partially change in-memory data. |
| Scope | Build one local CLI PIM. No GUI, network, accounts, database, recurring tasks, tags, or notifications; the PDF says extra features earn no extra credit (p. 1). |

## Change control

WP01 must turn these choices into verifiable requirements and examples. WP02 may choose internal class and function names but must not silently change the public CLI, fields, search semantics, or save/load behavior. Record any group-approved change here with its date, reason, and affected requirements before changing downstream artifacts.
