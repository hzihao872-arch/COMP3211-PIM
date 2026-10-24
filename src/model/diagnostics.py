"""Bounded, printable diagnostics without presentation or I/O dependencies."""


MAX_PREVIEW = 80
MAX_ERROR_DETAIL = 1024


def preview(value: object) -> str:
    """Describe invalid data without formatting unbounded strings or integers."""
    if isinstance(value, str):
        parts = []
        used = 2  # Opening and closing quotes.
        for char in value:
            piece = "\\'" if char == "'" else ascii(char)[1:-1]
            if used + len(piece) > MAX_PREVIEW - 3:
                return "'" + "".join(parts) + "...'"
            parts.append(piece)
            used += len(piece)
        return "'" + "".join(parts) + "'"
    if type(value) is int:
        if value.bit_length() > 250:
            return "<integer outside supported range>"
        return repr(value)
    if value is None or isinstance(value, (bool, float)):
        return repr(value)
    return f"<{type(value).__name__}>"


def bounded_detail(text: str, limit: int = MAX_ERROR_DETAIL) -> str:
    """Escape non-ASCII/control characters and truncate only between escapes."""
    parts = []
    used = 0
    for char in text:
        if ord(char) < 32 or 127 <= ord(char) <= 159:
            piece = f"\\x{ord(char):02x}"
        else:
            piece = char if " " <= char <= "~" else ascii(char)[1:-1]
        if used + len(piece) > limit - 3:
            return "".join(parts) + "..."
        parts.append(piece)
        used += len(piece)
    return "".join(parts)
