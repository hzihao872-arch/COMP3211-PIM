"""Pure search criteria, tokenizer, parser, and evaluation."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from model.errors import SearchSyntaxError, ValidationError
from model.records import Record, RecordType, TextField, TimeField
from model.validation import parse_local_time, validate_datetime

_TYPES = frozenset(("note", "task", "event", "contact"))
_TEXT = frozenset(("text", "description", "name", "address", "mobile_number"))
_TIME = frozenset(("deadline", "start_time", "alarm_time"))


def _canonical(value: object, choices: frozenset[str], label: str) -> str:
    if not isinstance(value, str) or value.casefold() not in choices:
        raise ValidationError(f"invalid {label}: {value!r}")
    return value.casefold()


class Criterion(ABC):
    @abstractmethod
    def matches(self, record: Record) -> bool:
        """Evaluate a valid record without side effects."""


@dataclass(frozen=True)
class TypeCriterion(Criterion):
    value: RecordType

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", _canonical(self.value, _TYPES, "type"))

    def matches(self, record: Record) -> bool:
        return record.type == self.value


@dataclass(frozen=True)
class TextCriterion(Criterion):
    field: TextField
    needle: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "field", _canonical(self.field, _TEXT, "text field"))
        if not isinstance(self.needle, str) or not self.needle:
            raise ValidationError("contains text must be nonempty")

    def matches(self, record: Record) -> bool:
        value = getattr(record, self.field, None)
        return isinstance(value, str) and self.needle.casefold() in value.casefold()


@dataclass(frozen=True)
class TimeCriterion(Criterion):
    field: TimeField
    operator: Literal["<", ">", "="]
    value: datetime

    def __post_init__(self) -> None:
        object.__setattr__(self, "field", _canonical(self.field, _TIME, "time field"))
        if self.operator not in ("<", ">", "="):
            raise ValidationError(f"invalid time operator: {self.operator!r}")
        validate_datetime(self.field, self.value)

    def matches(self, record: Record) -> bool:
        current = getattr(record, self.field, None)
        if current is None:
            return False
        if self.operator == "<":
            return current < self.value
        if self.operator == ">":
            return current > self.value
        return current == self.value


@dataclass(frozen=True)
class AndCriterion(Criterion):
    left: Criterion
    right: Criterion

    def __post_init__(self) -> None:
        if not isinstance(self.left, Criterion) or not isinstance(self.right, Criterion):
            raise ValidationError("&& requires two criteria")

    def matches(self, record: Record) -> bool:
        return self.left.matches(record) and self.right.matches(record)


@dataclass(frozen=True)
class OrCriterion(Criterion):
    left: Criterion
    right: Criterion

    def __post_init__(self) -> None:
        if not isinstance(self.left, Criterion) or not isinstance(self.right, Criterion):
            raise ValidationError("|| requires two criteria")

    def matches(self, record: Record) -> bool:
        return self.left.matches(record) or self.right.matches(record)


@dataclass(frozen=True)
class NotCriterion(Criterion):
    operand: Criterion

    def __post_init__(self) -> None:
        if not isinstance(self.operand, Criterion):
            raise ValidationError("! requires a criterion")

    def matches(self, record: Record) -> bool:
        return not self.operand.matches(record)


def _tokenize(expression: str) -> list[tuple[str, str]]:
    tokens: list[tuple[str, str]] = []
    index = 0
    while index < len(expression):
        char = expression[index]
        if char.isspace():
            index += 1
        elif char == '"':
            index += 1
            value = []
            while index < len(expression) and expression[index] != '"':
                char = expression[index]
                if char == "\\":
                    index += 1
                    if index >= len(expression) or expression[index] not in ('"', "\\"):
                        raise SearchSyntaxError("invalid quoted escape")
                    char = expression[index]
                value.append(char)
                index += 1
            if index >= len(expression):
                raise SearchSyntaxError("unterminated quoted literal")
            tokens.append(("quoted", "".join(value)))
            index += 1
        elif char.isascii() and (char.isalpha() or char == "_"):
            start = index
            index += 1
            while index < len(expression) and expression[index].isascii() and (expression[index].isalnum() or expression[index] == "_"):
                index += 1
            tokens.append(("word", expression[start:index]))
        elif expression.startswith("&&", index) or expression.startswith("||", index):
            tokens.append(("symbol", expression[index:index + 2]))
            index += 2
        elif char in "()!<>=":
            tokens.append(("symbol", char))
            index += 1
        else:
            raise SearchSyntaxError(f"invalid search token: {char!r}")
    return tokens


class _Parser:
    def __init__(self, tokens: list[tuple[str, str]]) -> None:
        self.tokens = tokens
        self.position = 0

    def _peek(self) -> tuple[str, str] | None:
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def _take(self, kind: str | None = None, value: str | None = None) -> str:
        token = self._peek()
        if token is None or (kind is not None and token[0] != kind) or (value is not None and token[1].casefold() != value):
            raise SearchSyntaxError(f"expected {value or kind or 'search token'}; found {token!r}")
        self.position += 1
        return token[1]

    def _accept(self, value: str) -> bool:
        token = self._peek()
        if token is not None and token[1] == value:
            self.position += 1
            return True
        return False

    def parse(self) -> Criterion:
        result = self._or()
        if self._peek() is not None:
            raise SearchSyntaxError(f"unexpected search token: {self._peek()!r}")
        return result

    def _or(self) -> Criterion:
        result = self._and()
        while self._accept("||"):
            result = OrCriterion(result, self._and())
        return result

    def _and(self) -> Criterion:
        result = self._not()
        while self._accept("&&"):
            result = AndCriterion(result, self._not())
        return result

    def _not(self) -> Criterion:
        if self._accept("!"):
            return NotCriterion(self._not())
        if self._accept("("):
            result = self._or()
            self._take("symbol", ")")
            return result
        return self._atom()

    def _atom(self) -> Criterion:
        field = self._take("word").casefold()
        if field == "type":
            self._take("symbol", "=")
            return TypeCriterion(self._take("quoted"))
        if field in _TEXT:
            self._take("word", "contains")
            return TextCriterion(field, self._take("quoted"))
        if field in _TIME:
            operator = self._take("symbol")
            value = parse_local_time(self._take("quoted"))
            return TimeCriterion(field, operator, value)
        raise SearchSyntaxError(f"unknown search field: {field!r}")


def parse_criterion(expression: str) -> Criterion:
    if not isinstance(expression, str):
        raise SearchSyntaxError("search expression must be text")
    try:
        return _Parser(_tokenize(expression)).parse()
    except ValidationError as error:
        if isinstance(error, SearchSyntaxError):
            raise
        raise SearchSyntaxError(str(error)) from error
