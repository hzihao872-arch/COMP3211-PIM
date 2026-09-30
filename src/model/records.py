"""Immutable personal information records."""

from dataclasses import dataclass
from datetime import datetime
from typing import Literal, TypeAlias

from model.validation import validate_datetime, validate_id, validate_text

RecordType: TypeAlias = Literal["note", "task", "event", "contact"]
TextField: TypeAlias = Literal["text", "description", "name", "address", "mobile_number"]
TimeField: TypeAlias = Literal["deadline", "start_time", "alarm_time"]


@dataclass(frozen=True)
class Note:
    id: int
    text: str

    def __post_init__(self) -> None:
        validate_id(self.id)
        object.__setattr__(self, "text", validate_text("text", self.text))

    @property
    def type(self) -> Literal["note"]:
        return "note"


@dataclass(frozen=True)
class Task:
    id: int
    description: str
    deadline: datetime

    def __post_init__(self) -> None:
        validate_id(self.id)
        object.__setattr__(self, "description", validate_text("description", self.description))
        validate_datetime("deadline", self.deadline)

    @property
    def type(self) -> Literal["task"]:
        return "task"


@dataclass(frozen=True)
class Event:
    id: int
    description: str
    start_time: datetime
    alarm_time: datetime

    def __post_init__(self) -> None:
        validate_id(self.id)
        object.__setattr__(self, "description", validate_text("description", self.description))
        validate_datetime("start_time", self.start_time)
        validate_datetime("alarm_time", self.alarm_time)

    @property
    def type(self) -> Literal["event"]:
        return "event"


@dataclass(frozen=True)
class Contact:
    id: int
    name: str
    address: str
    mobile_number: str

    def __post_init__(self) -> None:
        validate_id(self.id)
        for field in ("name", "address", "mobile_number"):
            object.__setattr__(self, field, validate_text(field, getattr(self, field)))

    @property
    def type(self) -> Literal["contact"]:
        return "contact"


Record: TypeAlias = Note | Task | Event | Contact
