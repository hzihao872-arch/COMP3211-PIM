"""Command-line parsing, presentation, and application coordination."""

from dataclasses import fields
from datetime import datetime
from pathlib import Path
import re
from typing import TextIO

from controller.output import TerminalOutput
from controller.help import COMMAND_HELP, HELP_OVERVIEW, command_help
from model.errors import PIMError, ValidationError
from model.diagnostics import MAX_ERROR_DETAIL, bounded_detail, preview
from model.schema import FIELDS as _FIELDS, MAX_RECORD_ID
from model.manager import PIMManager
from model.search import parse_criterion
from model.validation import format_local_time
from storage.pim_file import load_pim, save_pim


class InputReadError(PIMError):
    """An unusable command-input stream; this must terminate the session."""

    category = "IO"


class CommandSyntaxError(PIMError):
    """An invalid command form or argument token."""

    category = "COMMAND"

    def __init__(self, detail: str, position: int | None = None) -> None:
        self.position = position
        suffix = f" at character {position}" if position is not None else ""
        super().__init__(bounded_detail(detail, MAX_ERROR_DETAIL - len(suffix)) + suffix)


def _arguments(line: str) -> list[str]:
    result = []
    index = 0
    while index < len(line):
        while index < len(line) and line[index].isspace():
            index += 1
        if index >= len(line):
            break
        if line[index] == '"':
            quote_start = index
            index += 1
            value = []
            while index < len(line) and line[index] != '"':
                char = line[index]
                if char == "\\":
                    escape_start = index
                    index += 1
                    if index >= len(line) or line[index] not in ('"', "\\"):
                        raise CommandSyntaxError("invalid quoted escape", escape_start + 1)
                    char = line[index]
                value.append(char)
                index += 1
            if index >= len(line):
                raise CommandSyntaxError("unterminated quoted argument", quote_start + 1)
            index += 1
            if index < len(line) and not line[index].isspace():
                raise CommandSyntaxError("quoted arguments must be separated by spaces", index + 1)
            result.append("".join(value))
        else:
            start = index
            while index < len(line) and not line[index].isspace():
                if line[index] == '"':
                    raise CommandSyntaxError("quote must begin an argument", index + 1)
                index += 1
            result.append(line[start:index])
    return result


def _id(token: str) -> int:
    if not re.fullmatch(r"[0-9]+", token):
        raise CommandSyntaxError(f"invalid positive decimal ID: {preview(token)}")
    significant = token.lstrip("0") or "0"
    if len(significant) > len(str(MAX_RECORD_ID)):
        raise CommandSyntaxError(f"decimal ID exceeds {MAX_RECORD_ID}")
    value = int(significant)
    if value == 0:
        raise CommandSyntaxError(f"invalid positive decimal ID: {preview(token)}")
    return value


def _count(args: list[str], minimum: int, maximum: int, command: str) -> None:
    if not minimum <= len(args) <= maximum:
        raise CommandSyntaxError(f"wrong argument count for {command}; usage: {COMMAND_HELP[command][0]}")


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
        self._dirty = bool(manager.list_all())

    def _warn_unsaved(self, output_stream: TextIO) -> None:
        if self._dirty:
            output_stream.write('Warning: unsaved changes will be lost; use save "PATH.pim" before exiting.\n')

    def _try_warn_unsaved(self, output_stream: TextIO) -> None:
        try:
            self._warn_unsaved(output_stream)
            output_stream.flush()
        except (OSError, UnicodeError, KeyboardInterrupt):
            pass  # A termination warning must not mask the original failure.

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
        match = re.match(r"(\S+)(?:\s+(.*))?", line.lstrip().rstrip("\r\n"))
        command = match.group(1).casefold()
        remainder = match.group(2) or ""
        if command == "search":
            criterion = parse_criterion(remainder)
            self._print_records(self._manager.search(criterion), output_stream, "No matching PIRs.")
            return False
        args = _arguments(line.rstrip("\r\n"))
        command = args.pop(0).casefold()
        if command == "help":
            _count(args, 0, 1, command)
            topic = args[0].casefold() if args else None
            if topic is not None and topic not in COMMAND_HELP:
                raise CommandSyntaxError(f"unknown help topic: {preview(topic)}; type help for command names")
            output_stream.write(command_help(topic) if topic is not None else HELP_OVERVIEW)
        elif command == "add":
            if not args:
                raise CommandSyntaxError("add requires a type")
            record_type = args.pop(0).casefold()
            if record_type not in _FIELDS:
                raise ValidationError(f"unknown record type: {preview(record_type)}")
            _count(args, len(_FIELDS[record_type]), len(_FIELDS[record_type]), command)
            record = getattr(self._manager, f"create_{record_type}")(*args)
            self._dirty = True
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
            self._dirty = True
            output_stream.write(f"Updated {record.id}\n")
        elif command == "delete":
            _count(args, 1, 1, command)
            record_id = _id(args[0])
            self._manager.delete(record_id)
            self._dirty = True
            output_stream.write(f"Deleted {record_id}\n")
        elif command == "save":
            _count(args, 1, 1, command)
            path = self._path(args[0])
            save_pim(self._manager, path)
            self._dirty = False
            output_stream.write(f"Saved {len(self._manager.list_all())} PIR(s) to {path}\n")
        elif command == "load":
            _count(args, 1, 2, command)
            if len(args) == 2 and args[1].casefold() not in ("force=true", "force=false"):
                raise CommandSyntaxError("load accepts only force=true or force=false; type help load")
            force = len(args) == 2 and args[1].casefold() == "force=true"
            if self._dirty and not force:
                raise CommandSyntaxError('unsaved changes; save first or use load "PATH.pim" force=true to discard them')
            path = self._path(args[0])
            replacement = load_pim(path, self._manager.next_id)
            self._manager = replacement
            self._dirty = False
            output_stream.write(f"Loaded {len(replacement.list_all())} PIR(s) from {path}\n")
        elif command == "exit":
            _count(args, 0, 0, command)
            self._warn_unsaved(output_stream)
            return True
        else:
            raise CommandSyntaxError(f"unknown command: {preview(command)}; type help for command names")
        return False

    def run(self, input_stream: TextIO, output_stream: TextIO) -> None:
        output_stream = TerminalOutput(output_stream)
        try:
            self._run(input_stream, output_stream)
        except KeyboardInterrupt:
            self._try_warn_unsaved(output_stream)
            raise

    def _run(self, input_stream: TextIO, output_stream: TerminalOutput) -> None:
        while True:
            output_stream.write("pim> ")
            output_stream.flush()
            try:
                line = input_stream.readline()
            except (OSError, UnicodeError) as error:
                self._try_warn_unsaved(output_stream)
                raise InputReadError(f"cannot read input: {bounded_detail(str(error))}") from error
            if line == "":
                self._warn_unsaved(output_stream)
                return
            try:
                if self._dispatch(line, output_stream):
                    return
            except PIMError as error:
                output_stream.write(f"Error: {error.category}: {error}\n")
