"""Validated version-one .pim JSON snapshots with atomic replacement."""

import json
import os
import tempfile
from pathlib import Path

from model.errors import PIMError, ValidationError
from model.diagnostics import bounded_detail, preview
from model.manager import PIMManager
from model.schema import FIELDS as _FIELDS, TIME_FIELDS as _TIME_FIELDS
from model.validation import format_local_time, validate_next_id

_FORMAT = "COMP3211-PIM"


class PersistenceError(PIMError):
    def __init__(self, category: str, detail: str) -> None:
        self.category = category
        super().__init__(detail)


def _label(path: Path) -> str:
    # Keep the filename useful when a long directory prefix must be abbreviated.
    text = str(path)
    return preview(text) if len(text) <= 60 else f"{preview(path.name)} in {preview(str(path.parent))}"


def _path(path: Path) -> Path:
    if not isinstance(path, Path) or path.suffix != ".pim" or "\x00" in str(path):
        value = str(path) if isinstance(path, Path) else path
        raise PersistenceError("PATH", f"path must have lowercase .pim suffix: {preview(value)}")
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
        validate_next_id(manager.next_id)
        snapshot = {
            "format": _FORMAT, "version": 1, "next_id": manager.next_id,
            "records": [_row(record) for record in manager.list_all()],
        }
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".tmp", prefix=".pim-", dir=destination.parent, delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(snapshot, stream, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, destination)
    except (OSError, UnicodeError) as error:
        raise PersistenceError("IO", f"cannot save {_label(destination)}: {bounded_detail(str(error))}") from error
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
            raise ValueError(f"duplicate JSON key: {preview(key)}")
        result[key] = value
    return result


def _reject_constant(value: str) -> object:
    raise ValueError(f"nonstandard JSON constant: {value}")


def load_pim(path: Path, current_next_id: int) -> PIMManager:
    source = _path(path)
    try:
        validate_next_id(current_next_id)
    except ValidationError as error:
        raise PersistenceError("FORMAT", f"invalid current next ID: {error}") from error
    try:
        content = source.read_text(encoding="utf-8-sig")
    except OSError as error:
        raise PersistenceError("IO", f"cannot load {_label(source)}: {bounded_detail(str(error))}") from error
    except UnicodeError as error:
        raise PersistenceError("FORMAT", f"invalid UTF-8 in {_label(source)}: {error}") from error
    try:
        root = json.loads(content, object_pairs_hook=_unique_object, parse_constant=_reject_constant)
        if not isinstance(root, dict) or set(root) != {"format", "version", "next_id", "records"}:
            raise ValueError("snapshot root keys must be format, version, next_id, records")
        if root["format"] != _FORMAT or type(root["version"]) is not int or root["version"] != 1:
            raise ValueError("unsupported format or version")
        if not isinstance(root["records"], list):
            raise ValueError("records must be an array")
        return PIMManager.from_rows(root["records"], root["next_id"], current_next_id)
    except (ValueError, TypeError, ValidationError, RecursionError) as error:
        raise PersistenceError("FORMAT", f"invalid .pim file {_label(source)}: {error}") from error
