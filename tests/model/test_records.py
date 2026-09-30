"""Record construction and field validation (FR-02–FR-08)."""

import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

from model.errors import ValidationError
from model.records import Contact, Event, Note, Task
from model.validation import format_local_time, parse_local_time


class RecordTests(unittest.TestCase):
    def test_four_types_trim_values_and_keep_mobile_text(self):
        note = Note(1, "  memo  ")
        task = Task(2, "  work  ", datetime(2026, 10, 1, 9))
        event = Event(3, "  meet  ", datetime(2026, 10, 2), datetime(2026, 10, 1))
        contact = Contact(4, "  Li  ", "  Room 1  ", "  +00123  ")
        self.assertEqual((note.type, note.text), ("note", "memo"))
        self.assertEqual((task.type, task.description), ("task", "work"))
        self.assertEqual((event.type, event.description), ("event", "meet"))
        self.assertEqual((contact.type, contact.mobile_number), ("contact", "+00123"))
        with self.assertRaises(FrozenInstanceError):
            note.text = "changed"

    def test_invalid_direct_construction(self):
        for bad_id in (0, -1, True, "1"):
            with self.subTest(id=bad_id), self.assertRaises(ValidationError):
                Note(bad_id, "x")
        for bad in ("", "  ", "two\nlines", 2):
            with self.subTest(value=bad), self.assertRaises(ValidationError):
                Note(1, bad)
        for bad_date in ("2026-10-01 09:00", datetime(2026, 1, 1, tzinfo=timezone.utc), datetime(2026, 1, 1, 0, 0, 1)):
            with self.subTest(date=bad_date), self.assertRaises(ValidationError):
                Task(1, "x", bad_date)

    def test_external_time_has_exact_minute_format(self):
        value = parse_local_time("2026-02-28 09:05")
        self.assertEqual(format_local_time(value), "2026-02-28 09:05")
        for bad in ("2026-2-28 09:05", "2026-02-30 09:05", "2026-02-28T09:05", "2026-02-28 09:05Z", 123):
            with self.subTest(value=bad), self.assertRaises(ValidationError):
                parse_local_time(bad)

    def test_unicode_line_separators_are_not_single_line_text(self):
        for separator in ("\u0085", "\u2028", "\u2029", "\v", "\f"):
            with self.subTest(separator=repr(separator)), self.assertRaises(ValidationError):
                Note(1, "before" + separator + "after")

    def test_lone_surrogate_is_not_valid_text(self):
        with self.assertRaises(ValidationError):
            Note(1, "before\ud800after")


if __name__ == "__main__":
    unittest.main()
