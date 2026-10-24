"""Shared, read-only record metadata and identifier limits."""

from types import MappingProxyType


FIELDS = MappingProxyType({
    "note": ("text",),
    "task": ("description", "deadline"),
    "event": ("description", "start_time", "alarm_time"),
    "contact": ("name", "address", "mobile_number"),
})
TYPES = frozenset(FIELDS)
TIME_FIELDS = frozenset(("deadline", "start_time", "alarm_time"))
TEXT_FIELDS = frozenset(field for fields in FIELDS.values() for field in fields) - TIME_FIELDS

MAX_RECORD_ID = 10**19 - 1
# A serializable exhaustion marker, not an assignable record ID.
MAX_NEXT_ID = MAX_RECORD_ID + 1
