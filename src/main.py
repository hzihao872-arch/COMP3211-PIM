"""Composition root for the command-line PIM."""

from pathlib import Path
import sys

from controller.cli import CommandController
from model.manager import PIMManager


def main() -> None:
    CommandController(PIMManager(), Path.cwd()).run(sys.stdin, sys.stdout)


if __name__ == "__main__":
    main()
