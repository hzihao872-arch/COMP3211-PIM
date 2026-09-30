"""Validated version-one .pim JSON snapshots with atomic replacement."""

import json
import os
import tempfile
from pathlib import Path

from model.errors import ValidationError
from model.manager import PIMManager
from model.validation import format_local_time, validate_id

_FORMAT = "COMP3211-PIM"
_FIELDS = {
    "note": ("text",),
    "task": ("description", "deadline"),
    "event": ("description", "start_time", "alarm_time"),
    "contact": ("name", "address", "mobile_number"),
}
_TIME_FIELDS = frozenset(("deadline", "start_time", "alarm_time"))


class PersistenceError(Exception):
    def __init__(self, category: str, detail: str) -> None:
        self.category = category
        super().__init__(detail)


def _path(path: Path) -> Path:
    if not isinstance(path, Path) or path.suffix != ".pim" or "\x00" in str(path):
        raise PersistenceError("PATH", f"path must have lowercase .pim suffix: {path!r}")
    return path


def _row(record) -> dict[str, object]:
    row: dict[str, object] = {"id": record.id, "type": record.type}
    for field in _FIELDS[record.type]:
        value = getattr(record, field)
        row[field] = format_local_time(value) if field in _TIME_FIELDS else value
    return row


def save_pim(manager: PIMManager, path: Path) -> None:
    destination = _path(path)
    if not isinstance(manager, PIMManager):
        raise PersistenceError("FORMAT", "save requires a PIMManager")
    temporary: Path | None = None
    try:
        snapshot = {
            "format": _FORMAT, "version": 1, "next_id": manager.next_id,
            "records": [_row(record) for record in manager.list_all()],
        }
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".tmp", prefix=".pim-", dir=destination.parent, delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(snapshot, stream, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
            stream.write("\n")
        os.replace(temporary, destination)
    except (OSError, UnicodeError) as error:
        raise PersistenceError("IO", f"cannot save {destination}: {error}") from error
    except (TypeError, ValueError, ValidationError) as error:
        raise PersistenceError("FORMAT", f"invalid snapshot: {error}") from error
    finally:
        if temporary is not None:
            try:
                temporary.unlink(missing_ok=True)
            except OSError:
                pass


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_constant(value: str) -> object:
    raise ValueError(f"nonstandard JSON constant: {value}")


def load_pim(path: Path, current_next_id: int) -> PIMManager:
    source = _path(path)
    try:
        validate_id(current_next_id)
    except ValidationError as error:
        raise PersistenceError("FORMAT", f"invalid current next ID: {error}") from error
    try:
        content = source.read_text(encoding="utf-8")
    except OSError as error:
        raise PersistenceError("IO", f"cannot load {source}: {error}") from error
    except UnicodeError as error:
        raise PersistenceError("FORMAT", f"invalid UTF-8 in {source}: {error}") from error
    try:
        root = json.loads(content, object_pairs_hook=_unique_object, parse_constant=_reject_constant)
        if not isinstance(root, dict) or set(root) != {"format", "version", "next_id", "records"}:
            raise ValueError("snapshot root keys must be format, version, next_id, records")
        if root["format"] != _FORMAT or type(root["version"]) is not int or root["version"] != 1:
            raise ValueError("unsupported format or version")
        if not isinstance(root["records"], list):
            raise ValueError("records must be an array")
        return PIMManager.from_rows(root["records"], root["next_id"], current_next_id)
    except (ValueError, TypeError, ValidationError) as error:
        raise PersistenceError("FORMAT", f"invalid .pim file: {error}") from error
