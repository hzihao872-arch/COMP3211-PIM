"""Render terminal-safe text while leaving model and snapshot values intact."""

from contextlib import contextmanager
import errno
import os
import stat
from typing import Iterator, TextIO


class ClosedOutputPipe(BrokenPipeError):
    """The output consumer closed its pipe during write or flush."""


@contextmanager
def _output_boundary(stream: TextIO) -> Iterator[None]:
    try:
        yield
    except OSError as error:
        closed_pipe = isinstance(error, BrokenPipeError)
        if not closed_pipe and os.name == "nt" and error.errno == errno.EINVAL:
            try:
                closed_pipe = stat.S_ISFIFO(os.fstat(stream.fileno()).st_mode)
            except (AttributeError, OSError, ValueError):
                closed_pipe = False
        if closed_pipe:
            raise ClosedOutputPipe(str(error)) from error
        raise


class TerminalOutput:
    """Small write/flush adapter; genuine stream failures still propagate."""

    def __init__(self, stream: TextIO) -> None:
        self._stream = stream

    def write(self, text: str) -> int:
        # Keep our line layout, but display C0/C1 terminal commands as text.
        rendered = "".join(
            f"\\x{ord(char):02x}"
            if (ord(char) < 32 and char not in "\n\t") or 127 <= ord(char) <= 159
            else char
            for char in text
        )
        encoding = getattr(self._stream, "encoding", None) or "utf-8"
        rendered = rendered.encode(encoding, errors="backslashreplace").decode(encoding)
        with _output_boundary(self._stream):
            self._stream.write(rendered)
        return len(text)

    def flush(self) -> None:
        with _output_boundary(self._stream):
            self._stream.flush()
