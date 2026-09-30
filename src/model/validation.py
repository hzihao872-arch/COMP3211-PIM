"""Pure validation shared by record construction and search."""

from datetime import datetime

from model.errors import ValidationError


def validate_id(value: object) -> int:
    if type(value) is not int or value <= 0:
        raise ValidationError(f"id must be a positive integer: {value!r}")
    return value


def validate_text(field: str, value: object) -> str:
    if not isinstance(value, str) or "\r" in value or "\n" in value:
        raise ValidationError(f"{field} must be single-line text")
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
        raise ValidationError(f"invalid time: {value!r}") from error
    if result.strftime("%Y-%m-%d %H:%M") != value:
        raise ValidationError(f"invalid time: {value!r}")
    return result


def format_local_time(value: datetime) -> str:
    return validate_datetime("time", value).strftime("%Y-%m-%d %H:%M")
