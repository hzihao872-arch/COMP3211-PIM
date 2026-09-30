# WP02 Technical Contract — COMP3211 PIM

**Status:** WP02 design baseline, 2026-09-30. This document specifies proposed code interfaces for WP03; the functions and classes do not yet exist. [SRS.md](../srs/SRS.md) and [decisions.md](../../decisions.md) govern observable behavior. The class and module names below are WP02 design choices, not course requirements.

## 1. Module boundaries and dependencies

| Proposed file | Responsibility | May import |
|---|---|---|
| `src/model/records.py` | Four immutable PIR types and `Record` union | `model.errors`, `model.validation`, standard library |
| `src/model/validation.py` | Text and local-minute validation/conversion | `model.errors`, standard library |
| `src/model/search.py` | Criterion nodes, tokenizer, recursive-descent parser, evaluation | `model.records`, `model.validation`, `model.errors`, standard library |
| `src/model/manager.py` | In-memory collection, IDs, CRUD, search, restoration | Other `model` modules, standard library |
| `src/model/errors.py` | Model exception types | Standard library |
| `src/storage/pim_file.py` | UTF-8 JSON file boundary and atomic replacement | `model`, standard library |
| `src/controller/cli.py` | Command parsing, prompt, display, error translation, active-manager swap | `model`, `storage`, standard library |
| `src/main.py` | Construct initial manager and controller, then start CLI | `controller`, `model`, standard library |

`model` must never import `controller` or `storage` and must perform no terminal, path, or file I/O. `storage` never prints or reads terminal input. No module invokes third-party libraries or Python `eval`/`exec` for search. The existing files under `src/` are scaffolding, not an implemented API.

## 2. Types, records, and validation

```python
RecordType = Literal["note", "task", "event", "contact"]
TextField = Literal["text", "description", "name", "address", "mobile_number"]
TimeField = Literal["deadline", "start_time", "alarm_time"]
Record = Note | Task | Event | Contact
```

Each record is a frozen dataclass. Its `id` and `type` cannot be modified; `type: RecordType` is a read-only literal property. Each generated constructor validates through `__post_init__`: it rejects invalid ID/value types, blank or multiline text, and aware or non-minute datetimes; it trims accepted text with `object.__setattr__`. Invalid direct construction raises `ValidationError`. The manager also validates all command inputs before constructing a record so a failed creation cannot consume an ID. `PIMManager.update` replaces one immutable record with a validated new record, committing only after all checks succeed. Field names and constructor order are fixed:

| Class | Public fields and Python types | `type` |
|---|---|---|
| `Note` | `id: int`, `text: str` | `"note"` |
| `Task` | `id: int`, `description: str`, `deadline: datetime` | `"task"` |
| `Event` | `id: int`, `description: str`, `start_time: datetime`, `alarm_time: datetime` | `"event"` |
| `Contact` | `id: int`, `name: str`, `address: str`, `mobile_number: str` | `"contact"` |

The four dataclass constructors are public Python constructors but are not command entry points. Their signatures and possible `ValidationError` are listed in the Design Document. The only accepted external time representation is the exact local `YYYY-MM-DD HH:mm` string. No timezone information or seconds are retained. Past times and either ordering of an event's start and alarm are valid. The model stores naive `datetime` values at minute precision. Mobile numbers remain strings; duplicate data values are allowed.

| Public function | Return | Exception | Rule |
|---|---|---|---|
| `parse_local_time(value: str) -> datetime` | Naive minute-precision `datetime` | `ValidationError` | Require a string; parse and round-trip format to enforce exact zero-padded syntax and reject impossible dates/offsets. |
| `format_local_time(value: datetime) -> str` | Exact `YYYY-MM-DD HH:mm` | `ValidationError` | Reject timezone-aware values and nonzero seconds or microseconds. |

Private text validation requires a `str`, rejects `\r` and `\n`, trims leading/trailing whitespace, and rejects the empty result. Search `contains` literals are different: they must be quoted and nonempty, but are **not** trimmed. Type, command, and field names are canonicalized with `casefold()`. Accepted record field values are validated in the model even when supplied by storage rather than the CLI.

## 3. Model errors and manager API

`PIMError(Exception)` is the model base class. `ValidationError(PIMError)` identifies an invalid field, type, ID, or value. `RecordNotFoundError(PIMError)` identifies a valid positive ID absent from the collection. `SearchSyntaxError(ValidationError)` identifies an invalid search expression. The exception message names the rejected field/token or failure category; it does not contain a traceback for the user.

```python
class PIMManager:
    @property
    def next_id(self) -> int: ...

    def create_note(self, text: str) -> Note: ...
    def create_task(self, description: str, deadline: str) -> Task: ...
    def create_event(self, description: str, start_time: str,
                     alarm_time: str) -> Event: ...
    def create_contact(self, name: str, address: str,
                       mobile_number: str) -> Contact: ...

    def get(self, record_id: int) -> Record: ...
    def list_all(self, record_type: str | None = None) -> tuple[Record, ...]: ...
    def update(self, record_id: int, field_name: str, value: str) -> Record: ...
    def delete(self, record_id: int) -> None: ...
    def search(self, criterion: Criterion) -> tuple[Record, ...]: ...

    @classmethod
    def from_rows(cls, rows: Sequence[Mapping[str, object]],
                  file_next_id: int, previous_next_id: int) -> PIMManager: ...
```

| API | Success and failure contract |
|---|---|
| `PIMManager()` | Starts empty with `next_id == 1`; construction itself has no external I/O. |
| `create_*` | Normalize all fields, parse times, then assign the current ID and advance `next_id` exactly once. Invalid input raises `ValidationError` without consuming an ID or changing records. |
| `get` | Return the immutable PIR; invalid ID type/value raises `ValidationError`, absent positive ID raises `RecordNotFoundError`. A Boolean is not an integer ID. |
| `list_all` | Return an ID-ascending tuple; optional type name is case-insensitive; invalid type raises `ValidationError`. The tuple may be empty. |
| `update` | Accept exactly one data field of the selected type, case-insensitively. Validate before replacing the record; ID/type are never updateable. Return the replacement. Invalid field/value raises `ValidationError`; absent ID raises `RecordNotFoundError`. No partial mutation. |
| `delete` | Remove exactly one existing PIR. Invalid ID raises `ValidationError`; absent ID raises `RecordNotFoundError`. Never reduce `next_id`. |
| `search` | Require an instance of the `Criterion` abstract base class, or raise `ValidationError`; evaluate a valid criterion against every record and return an ID-ascending tuple. No mutation. |
| `next_id` | Read-only; used by storage for snapshots and by load to preserve the higher counter. |
| `from_rows` | Validate every row's exact keys, type, required fields and values, unique positive integer IDs, ascending row order, and `file_next_id > max(id, default=0)`; reject Boolean IDs/counters. Build a new manager with `next_id = max(previous_next_id, file_next_id)`. Raise `ValidationError` on any fault; never mutate an existing manager. |

All IDs created in a running session remain below the manager's counter. Loading an older snapshot may restore older records, but a later creation uses the higher of the current and file counters. A new process can know only the counter preserved in its loaded file; no external history database is implied.

## 4. Criterion syntax and evaluation

The public parser API is `parse_criterion(expression: str) -> Criterion`; it raises `SearchSyntaxError` before any record is evaluated. `Criterion` is an `abc.ABC` abstract base class defining `matches(record: Record) -> bool`, so `PIMManager.search` can reject non-criterion arguments with `isinstance`. All criterion nodes are immutable:

| Class | Fields | Public method |
|---|---|---|
| `TypeCriterion` | `value: RecordType` | `matches(record: Record) -> bool` |
| `TextCriterion` | `field: TextField`, `needle: str` | `matches(record: Record) -> bool` |
| `TimeCriterion` | `field: TimeField`, `operator: Literal["<", ">", "="]`, `value: datetime` | `matches(record: Record) -> bool` |
| `AndCriterion` | `left: Criterion`, `right: Criterion` | `matches(record: Record) -> bool` |
| `OrCriterion` | `left: Criterion`, `right: Criterion` | `matches(record: Record) -> bool` |
| `NotCriterion` | `operand: Criterion` | `matches(record: Record) -> bool` |

`matches` returns a Boolean and raises no exception for a parser-produced criterion and a valid record. A valid field absent from a given PIR evaluates false; negation then evaluates true. Type and text comparisons use `casefold()`. Times compare chronologically as naive local `datetime` values.

Direct construction of a concrete node is supported. Each frozen node validates in `__post_init__` and raises `ValidationError` on invalid arguments: type values must be one of the four canonical names (case-folded on input); text/time field names must be in their respective vocabularies (case-folded on input); a text needle must be a nonempty string and is preserved without trimming; a time operator must be `<`, `>`, or `=` and its `datetime` must be naive at minute precision; Boolean child operands must be `Criterion` instances. The parser catches such validation failures and exposes them as `SearchSyntaxError` for an invalid expression. Quoting is checked only by the parser because direct constructors receive decoded values.

The tokenizer recognizes identifiers, quoted literals with only `\"` and `\\` escapes, `(`, `)`, `!`, `&&`, `||`, `<`, `>`, and `=`. It accepts adjacent symbolic tokens (`!name`, `(type`, `)`) and optional whitespace where token boundaries remain clear. It rejects unknown escapes and unterminated quotes. The recursive-descent parser uses this grammar; binary chains are constructed left to right:

```text
expression := or_expr
or_expr    := and_expr ("||" and_expr)*
and_expr   := not_expr ("&&" not_expr)*
not_expr   := "!" not_expr | "(" expression ")" | atom
atom       := "type" "=" QUOTED_TYPE
            | TEXT_FIELD "contains" QUOTED_NONEMPTY_TEXT
            | TIME_FIELD ("<" | ">" | "=") QUOTED_LOCAL_TIME
```

`type` and field names are case-insensitive. `contains` is the fixed operator spelling. All three atom categories require quoted literals, including one-token values. Unknown fields, wrong operators for a field, unknown type literals, invalid time strings, empty containment strings, trailing tokens, and unmatched parentheses raise `SearchSyntaxError` for the whole expression. Tokenization and parsing finish before `PIMManager.search` is called; no partial results are printed.

## 5. `.pim` storage boundary

```python
def save_pim(manager: PIMManager, path: Path) -> None: ...
def load_pim(path: Path, current_next_id: int) -> PIMManager: ...
```

Both functions raise `PersistenceError(Exception)` for invalid `.pim` path/extension, malformed or unsupported file, model validation failure in loaded data, or file-system I/O failure. `PersistenceError` carries a user-safe failure category and detail. `save_pim` does not mutate its manager; `load_pim` never mutates the caller's manager. The controller replaces its active manager reference only after `load_pim` returns successfully.

The JSON root has **exactly** `format`, `version`, `next_id`, and `records`: `format` is `"COMP3211-PIM"`, `version` is the integer `1`, `next_id` is a positive integer, and `records` is an ascending-ID array. Every record object has `id`, `type`, and exactly its type's data fields; time fields use the exact external string format. No extra or missing keys are accepted. `load_pim` rejects duplicate JSON object keys, nonstandard JSON constants, incorrect primitive types, duplicate/nonpositive IDs, unsupported version, invalid fields, and a file counter no greater than its maximum ID. UTF-8 decoding and JSON parsing must finish before a new manager is returned.

For save, resolve the path already supplied by the controller, require the exact lowercase `.pim` suffix, serialize the complete state, write it to a temporary file in the destination directory, and call `os.replace` only after successful serialization and write. Clean up a leftover temporary file on failure. A failed save leaves an existing destination's bytes unchanged; this is not a promise against sudden power loss. For load, validate the entire file and call `PIMManager.from_rows(rows, file_next_id, current_next_id)`; a failure preserves the active manager and its counter. Relative paths are resolved by the controller against the process working directory captured for the session.

## 6. CLI boundary and output contract

`CommandController.__init__(self, manager: PIMManager, working_directory: Path) -> None` holds `_manager` and `_working_directory`; it raises `ValidationError` for an argument of the wrong type. Its public `run(input_stream: TextIO, output_stream: TextIO) -> None` writes `pim> `, reads one line at a time, dispatches the command, and prints results or `Error: CATEGORY: DETAIL`; EOF and `exit` terminate normally. It catches `PIMError`, `PersistenceError`, and its own `CommandSyntaxError`, then continues. It does not catch unrelated programming defects as user errors. `main() -> None` in `src/main.py` creates the manager and controller and calls `run` with standard streams and `Path.cwd()`.

The error categories are fixed: `COMMAND` for command syntax, `VALIDATION` for model field/type/ID validation, `NOT_FOUND` for an absent valid ID, and `SEARCH` for a malformed criterion. `PersistenceError` carries one of `PATH`, `FORMAT`, or `IO`; the controller prints that category. Catch `SearchSyntaxError` before its `ValidationError` base class. `DETAIL` identifies the rejected token, field, path, or failure category without a traceback. This mapping gives CLI tests stable categories while leaving platform-specific I/O wording flexible.

| Command | Parsing and output |
|---|---|
| `help` | No arguments; print all command forms, field order, quoting/escaping, time format, and search grammar. |
| `add TYPE "FIELD"...` | Exactly the number of fields in §2 order. Print `Created TYPE ID`. |
| `list [TYPE]` | Optional type filter. Print one `ID | TYPE | FIRST_TEXT_VALUE` line per PIR in ID order, or `No PIRs.` if empty. The complete first text field is shown. |
| `show ID` / `show all` | Print `id:`, `type:`, and every data field label/value; separate multiple records by a blank line. `show all` is ID ordered; an empty collection prints `No PIRs.`. |
| `update ID FIELD "VALUE"` | Exactly one field/value pair; print `Updated ID`. |
| `delete ID` | Print `Deleted ID`. |
| `search EXPR` | Pass the untouched expression remainder to `parse_criterion`, then to `manager.search`; print the same summaries as `list` or `No matching PIRs.`. A criterion is defined and applied in this one command. |
| `save "PATH.pim"` | Resolve path against `_working_directory`, call `save_pim`, then print `Saved N PIR(s) to PATH`. |
| `load "PATH.pim"` | Resolve path, call `load_pim(path, manager.next_id)`, swap `_manager` only on success, then print `Loaded N PIR(s) from PATH`. |
| `exit` | No arguments; end without saving implicitly. |

Commands, type names, and field names are case-insensitive. Command tokens require separating whitespace. Non-search values and paths with spaces need double quotes; one-token values may be unquoted. Inside quotes only `\"` and `\\` are escapes. Wrong counts, malformed quoting, unknown commands, invalid decimal-positive ID tokens, and unknown types/fields raise `CommandSyntaxError` or model validation errors before a mutation. ID tokens contain decimal digits and must represent a value greater than zero. Search parsing is separate from command-argument parsing so symbolic operators may adjoin atoms. A useful error identifies the rejected input or failure category; the next prompt appears after every handled error.

## 7. FR/NFR allocation and WP03 test seams

| Requirement IDs | Owning component/API and planned verification seam |
|---|---|
| FR-01–FR-11 | Record types, validation, `PIMManager.create_*`, `next_id`; model tests cover all four schemas, dates, trimming, ID monotonicity, duplicates. |
| FR-12–FR-15 | `CommandController.run` and command tokenizer; injected text streams allow command, case, count, and quoting checks. |
| FR-16–FR-17 | `PIMManager.update`; model tests check one-field replacement, invalid field/ID, and no mutation. |
| FR-18–FR-25 | `PIMManager.list_all/get/delete` plus controller formatting, help, exit/EOF; model and CLI tests cover ordering and full details. |
| FR-26–FR-40 | `parse_criterion`, criterion nodes, `PIMManager.search`, controller summaries; model tests cover every text field, all nine time field/comparator pairs, Boolean operators, precedence, absent-field semantics, and errors. |
| FR-41–FR-48 | `save_pim`, `load_pim`, `PIMManager.from_rows`, controller reference swap; round-trip, malformed-file, atomic-failure, and higher-counter tests. |
| FR-49–FR-50 | Controller error translation plus validation-before-commit in model and storage; failure-state and next-command checks. |
| NFR-01–NFR-05 | Local CLI, declared Python versions, import audit, separate `model` package and identifiable `controller`/`storage` packages. |

WP03 will create model tests before each implementation step and later add CLI/storage acceptance tests. This table is a design-to-requirement allocation, not a claim that tests or behavior already exist.
