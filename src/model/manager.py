"""In-memory PIM collection and ID allocation."""

from collections.abc import Mapping, Sequence
from dataclasses import replace

from model.errors import RecordNotFoundError, ValidationError
from model.records import Contact, Event, Note, Record, Task
from model.search import Criterion
from model.validation import parse_local_time, validate_id

_FIELDS = {
    "note": ("text",),
    "task": ("description", "deadline"),
    "event": ("description", "start_time", "alarm_time"),
    "contact": ("name", "address", "mobile_number"),
}
_TIME_FIELDS = frozenset(("deadline", "start_time", "alarm_time"))


def _type_name(value: object) -> str:
    if not isinstance(value, str) or value.casefold() not in _FIELDS:
        raise ValidationError(f"unknown record type: {value!r}")
    return value.casefold()


class PIMManager:
    def __init__(self) -> None:
        self._records: dict[int, Record] = {}
        self._next_id = 1

    @property
    def next_id(self) -> int:
        return self._next_id

    def _create(self, record_type: str, *values: object) -> Record:
        classes = {"note": Note, "task": Task, "event": Event, "contact": Contact}
        fields = _FIELDS[record_type]
        kwargs = {name: parse_local_time(value) if name in _TIME_FIELDS else value for name, value in zip(fields, values)}
        record = classes[record_type](self._next_id, **kwargs)
        self._records[record.id] = record
        self._next_id += 1
        return record

    def create_note(self, text: str) -> Note:
        return self._create("note", text)

    def create_task(self, description: str, deadline: str) -> Task:
        return self._create("task", description, deadline)

    def create_event(self, description: str, start_time: str, alarm_time: str) -> Event:
        return self._create("event", description, start_time, alarm_time)

    def create_contact(self, name: str, address: str, mobile_number: str) -> Contact:
        return self._create("contact", name, address, mobile_number)

    def get(self, record_id: int) -> Record:
        validate_id(record_id)
        try:
            return self._records[record_id]
        except KeyError as error:
            raise RecordNotFoundError(f"record ID {record_id} was not found") from error

    def list_all(self, record_type: str | None = None) -> tuple[Record, ...]:
        canonical = _type_name(record_type) if record_type is not None else None
        return tuple(record for _, record in sorted(self._records.items()) if canonical is None or record.type == canonical)

    def update(self, record_id: int, field_name: str, value: str) -> Record:
        record = self.get(record_id)
        if not isinstance(field_name, str):
            raise ValidationError(f"invalid field: {field_name!r}")
        field = field_name.casefold()
        if field not in _FIELDS[record.type]:
            raise ValidationError(f"field {field_name!r} cannot be updated for {record.type}")
        replacement = replace(record, **{field: parse_local_time(value) if field in _TIME_FIELDS else value})
        self._records[record_id] = replacement
        return replacement

    def delete(self, record_id: int) -> None:
        self.get(record_id)
        del self._records[record_id]

    def search(self, criterion: Criterion) -> tuple[Record, ...]:
        if not isinstance(criterion, Criterion):
            raise ValidationError("search requires a Criterion")
        return tuple(record for record in self.list_all() if criterion.matches(record))

    @classmethod
    def from_rows(cls, rows: Sequence[Mapping[str, object]], file_next_id: int, previous_next_id: int) -> "PIMManager":
        for label, value in (("file_next_id", file_next_id), ("previous_next_id", previous_next_id)):
            try:
                validate_id(value)
            except ValidationError as error:
                raise ValidationError(f"invalid {label}: {value!r}") from error
        if isinstance(rows, (str, bytes)) or not isinstance(rows, Sequence):
            raise ValidationError("records must be an array")
        result = cls()
        last_id = 0
        classes = {"note": Note, "task": Task, "event": Event, "contact": Contact}
        for row in rows:
            if not isinstance(row, Mapping):
                raise ValidationError("record must be an object")
            record_type = _type_name(row.get("type"))
            expected = {"id", "type", *_FIELDS[record_type]}
            if set(row) != expected or row["type"] != record_type:
                raise ValidationError(f"invalid {record_type} record keys or type")
            record_id = validate_id(row["id"])
            if record_id <= last_id:
                raise ValidationError("record IDs must be unique and ascending")
            values = {name: parse_local_time(row[name]) if name in _TIME_FIELDS else row[name] for name in _FIELDS[record_type]}
            record = classes[record_type](record_id, **values)
            result._records[record_id] = record
            last_id = record_id
        if file_next_id <= last_id:
            raise ValidationError("file next_id must exceed the maximum record ID")
        result._next_id = max(file_next_id, previous_next_id)
        return result
