"""Pure validation shared by record construction and search."""

from datetime import datetime

from model.errors import ValidationError
from model.diagnostics import preview
from model.schema import MAX_NEXT_ID, MAX_RECORD_ID


_LINE_BREAKS = frozenset("\r\n\v\f\x1c\x1d\x1e\x85\u2028\u2029")


def validate_id(value: object) -> int:
    if type(value) is not int or not 1 <= value <= MAX_RECORD_ID:
        raise ValidationError(f"id must be an integer in 1..{MAX_RECORD_ID}: {preview(value)}")
    return value


def validate_next_id(value: object) -> int:
    if type(value) is not int or not 1 <= value <= MAX_NEXT_ID:
        raise ValidationError(f"next_id must be an integer in 1..{MAX_NEXT_ID}: {preview(value)}")
    return value


def validate_text(field: str, value: object) -> str:
    if not isinstance(value, str) or any(char in _LINE_BREAKS for char in value):
        raise ValidationError(f"{field} must be single-line text")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as error:
        raise ValidationError(f"{field} must be valid UTF-8 text") from error
    result = value.strip()
    if not result:
        raise ValidationError(f"{field} must not be empty")
    return result


def validate_datetime(field: str, value: object) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is not None or value.second or value.microsecond:
        raise ValidationError(f"{field} must be a local minute-precision datetime")
    return value


def parse_local_time(value: str) -> datetime:
    if not isinstance(value, str):
        raise ValidationError("time must use YYYY-MM-DD HH:mm")
    try:
        result = datetime.strptime(value, "%Y-%m-%d %H:%M")
    except ValueError as error:
        raise ValidationError(f"invalid time: {preview(value)}") from error
    if result.strftime("%Y-%m-%d %H:%M") != value:
        raise ValidationError(f"invalid time: {preview(value)}")
    return result


def format_local_time(value: datetime) -> str:
    return validate_datetime("time", value).strftime("%Y-%m-%d %H:%M")
