"""Command-line parsing, presentation, and application coordination."""

from dataclasses import fields
from datetime import datetime
from pathlib import Path
import re
from typing import TextIO

from model.errors import RecordNotFoundError, SearchSyntaxError, ValidationError
from model.manager import PIMManager
from model.search import parse_criterion
from model.validation import format_local_time
from storage.pim_file import PersistenceError, load_pim, save_pim

_FIELDS = {
    "note": ("text",),
    "task": ("description", "deadline"),
    "event": ("description", "start_time", "alarm_time"),
    "contact": ("name", "address", "mobile_number"),
}
_HELP = '''Commands:
  help
  add TYPE "FIELD"...  (note: text; task: description deadline; event: description start_time alarm_time; contact: name address mobile_number)
  list [TYPE]
  show ID | show all
  update ID FIELD "VALUE"
  delete ID
  search EXPR
  save "PATH.pim" | load "PATH.pim"
  exit
Types/fields/commands ignore case. Values with spaces need double quotes; inside quotes use \\" and \\\\.
Time: YYYY-MM-DD HH:mm (local, 24-hour).
Search atoms: type = "TYPE"; FIELD contains "TEXT"; deadline/start_time/alarm_time <, >, or = "TIME".
Combine with !, &&, ||, and parentheses; precedence: parentheses, !, &&, ||.
'''


class CommandSyntaxError(Exception):
    """An invalid command form or argument token."""


def _arguments(line: str) -> list[str]:
    result = []
    index = 0
    while index < len(line):
        while index < len(line) and line[index].isspace():
            index += 1
        if index >= len(line):
            break
        if line[index] == '"':
            index += 1
            value = []
            while index < len(line) and line[index] != '"':
                char = line[index]
                if char == "\\":
                    index += 1
                    if index >= len(line) or line[index] not in ('"', "\\"):
                        raise CommandSyntaxError("invalid quoted escape")
                    char = line[index]
                value.append(char)
                index += 1
            if index >= len(line):
                raise CommandSyntaxError("unterminated quoted argument")
            index += 1
            if index < len(line) and not line[index].isspace():
                raise CommandSyntaxError("quoted arguments must be separated by spaces")
            result.append("".join(value))
        else:
            start = index
            while index < len(line) and not line[index].isspace():
                if line[index] == '"':
                    raise CommandSyntaxError("quote must begin an argument")
                index += 1
            result.append(line[start:index])
    return result


def _id(token: str) -> int:
    if not re.fullmatch(r"[0-9]+", token) or int(token) == 0:
        raise CommandSyntaxError(f"invalid positive decimal ID: {token!r}")
    return int(token)


def _count(args: list[str], minimum: int, maximum: int, command: str) -> None:
    if not minimum <= len(args) <= maximum:
        raise CommandSyntaxError(f"wrong argument count for {command}")


def _summary(record) -> str:
    first = _FIELDS[record.type][0]
    return f"{record.id} | {record.type} | {getattr(record, first)}"


def _details(record) -> str:
    lines = [f"id: {record.id}", f"type: {record.type}"]
    for field in fields(record):
        if field.name != "id":
            value = getattr(record, field.name)
            lines.append(f"{field.name}: {format_local_time(value) if isinstance(value, datetime) else value}")
    return "\n".join(lines)


class CommandController:
    def __init__(self, manager: PIMManager, working_directory: Path) -> None:
        if not isinstance(manager, PIMManager) or not isinstance(working_directory, Path):
            raise ValidationError("controller requires PIMManager and Path working_directory")
        self._manager = manager
        self._working_directory = working_directory

    def _path(self, value: str) -> Path:
        path = Path(value)
        return path if path.is_absolute() else self._working_directory / path

    def _print_records(self, records, output_stream: TextIO, empty: str, detailed: bool = False) -> None:
        if not records:
            output_stream.write(empty + "\n")
        elif detailed:
            output_stream.write("\n\n".join(_details(record) for record in records) + "\n")
        else:
            output_stream.write("\n".join(_summary(record) for record in records) + "\n")

    def _dispatch(self, line: str, output_stream: TextIO) -> bool:
        stripped = line.strip()
        if not stripped:
            return False
        match = re.match(r"(\S+)(?:\s+(.*))?", stripped)
        command = match.group(1).casefold()
        remainder = match.group(2) or ""
        if command == "search":
            criterion = parse_criterion(remainder)
            self._print_records(self._manager.search(criterion), output_stream, "No matching PIRs.")
            return False
        args = _arguments(stripped)
        command = args.pop(0).casefold()
        if command == "help":
            _count(args, 0, 0, command)
            output_stream.write(_HELP)
        elif command == "add":
            if not args:
                raise CommandSyntaxError("add requires a type")
            record_type = args.pop(0).casefold()
            if record_type not in _FIELDS:
                raise ValidationError(f"unknown record type: {record_type!r}")
            _count(args, len(_FIELDS[record_type]), len(_FIELDS[record_type]), command)
            record = getattr(self._manager, f"create_{record_type}")(*args)
            output_stream.write(f"Created {record.type} {record.id}\n")
        elif command == "list":
            _count(args, 0, 1, command)
            self._print_records(self._manager.list_all(args[0] if args else None), output_stream, "No PIRs.")
        elif command == "show":
            _count(args, 1, 1, command)
            if args[0].casefold() == "all":
                self._print_records(self._manager.list_all(), output_stream, "No PIRs.", detailed=True)
            else:
                output_stream.write(_details(self._manager.get(_id(args[0]))) + "\n")
        elif command == "update":
            _count(args, 3, 3, command)
            record = self._manager.update(_id(args[0]), args[1], args[2])
            output_stream.write(f"Updated {record.id}\n")
        elif command == "delete":
            _count(args, 1, 1, command)
            record_id = _id(args[0])
            self._manager.delete(record_id)
            output_stream.write(f"Deleted {record_id}\n")
        elif command == "save":
            _count(args, 1, 1, command)
            path = self._path(args[0])
            save_pim(self._manager, path)
            output_stream.write(f"Saved {len(self._manager.list_all())} PIR(s) to {path}\n")
        elif command == "load":
            _count(args, 1, 1, command)
            path = self._path(args[0])
            replacement = load_pim(path, self._manager.next_id)
            self._manager = replacement
            output_stream.write(f"Loaded {len(replacement.list_all())} PIR(s) from {path}\n")
        elif command == "exit":
            _count(args, 0, 0, command)
            return True
        else:
            raise CommandSyntaxError(f"unknown command: {command!r}")
        return False

    def run(self, input_stream: TextIO, output_stream: TextIO) -> None:
        while True:
            output_stream.write("pim> ")
            line = input_stream.readline()
            if line == "":
                return
            try:
                if self._dispatch(line, output_stream):
                    return
            except SearchSyntaxError as error:
                output_stream.write(f"Error: SEARCH: {error}\n")
            except RecordNotFoundError as error:
                output_stream.write(f"Error: NOT_FOUND: {error}\n")
            except ValidationError as error:
                output_stream.write(f"Error: VALIDATION: {error}\n")
            except PersistenceError as error:
                output_stream.write(f"Error: {error.category}: {error}\n")
            except CommandSyntaxError as error:
                output_stream.write(f"Error: COMMAND: {error}\n")
