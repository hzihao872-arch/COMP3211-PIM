"""Composition root for the command-line PIM."""

from pathlib import Path
import os
import sys
from typing import TextIO

from controller.cli import CommandController, InputReadError
from controller.output import ClosedOutputPipe, TerminalOutput
from model.manager import PIMManager


def main() -> None:
    CommandController(PIMManager(), Path.cwd()).run(sys.stdin, sys.stdout)


def _silence_closed_stream(stream: TextIO) -> None:
    # Avoid another error when Python flushes a failed stream at shutdown.
    descriptor = os.open(os.devnull, os.O_WRONLY)
    try:
        os.dup2(descriptor, stream.fileno())
    finally:
        os.close(descriptor)


def _report_input_failure(error: InputReadError) -> None:
    for stream, message in ((sys.stderr, f"Error: IO: {error}\n"), (sys.stdout, "")):
        try:
            output = TerminalOutput(stream)
            if message:
                output.write(message)
            output.flush()
        except (OSError, UnicodeError, KeyboardInterrupt):
            try:
                _silence_closed_stream(stream)
            except (AttributeError, OSError, ValueError):
                pass  # A supplied stream may not expose a usable descriptor.


def cli() -> int:
    """Keep input failure, user interruption and output-pipe closure distinct."""
    try:
        main()
        TerminalOutput(sys.stdout).flush()
        return 0
    except InputReadError as error:
        _report_input_failure(error)
        return 1
    except KeyboardInterrupt:
        try:
            TerminalOutput(sys.stdout).flush()
        except ClosedOutputPipe:
            _silence_closed_stream(sys.stdout)
        except OSError:
            pass  # Interruption does not depend on an available output device.
        return 130
    except ClosedOutputPipe:
        _silence_closed_stream(sys.stdout)
        return 0


if __name__ == "__main__":
    raise SystemExit(cli())
