"""Composition root for the command-line PIM."""

from pathlib import Path
import os
import sys

from controller.cli import CommandController
from controller.output import ClosedOutputPipe, TerminalOutput
from model.manager import PIMManager


def main() -> None:
    CommandController(PIMManager(), Path.cwd()).run(sys.stdin, sys.stdout)


def cli() -> int:
    """Handle user interruption and a downstream consumer closing stdout."""
    try:
        main()
        TerminalOutput(sys.stdout).flush()
        return 0
    except KeyboardInterrupt:
        return 130
    except ClosedOutputPipe:
        # Avoid another error when Python flushes buffered stdout at shutdown.
        descriptor = os.open(os.devnull, os.O_WRONLY)
        try:
            os.dup2(descriptor, sys.stdout.fileno())
        finally:
            os.close(descriptor)
        return 0


if __name__ == "__main__":
    raise SystemExit(cli())
