"""ID exhaustion, atomic failure and bounded invalid-data diagnostics."""

import unittest

from model.diagnostics import MAX_ERROR_DETAIL, MAX_PREVIEW, preview
from model.errors import SearchSyntaxError, ValidationError
from model.manager import PIMManager
from model.records import Note
from model.schema import MAX_NEXT_ID, MAX_RECORD_ID
from model.validation import validate_id, validate_next_id


class ModelHardeningTests(unittest.TestCase):
    def test_last_id_and_exhaustion_preserve_state_for_every_record_type(self):
        """FR-09/10/50: the last ID is usable; later creates cannot mutate state."""
        manager = PIMManager.from_rows([], MAX_RECORD_ID, 1)
        self.assertEqual(manager.create_note("last").id, MAX_RECORD_ID)
        self.assertEqual(manager.next_id, MAX_NEXT_ID)
        before = manager.list_all(), manager.next_id
        for create in (
            lambda: manager.create_note("no"),
            lambda: manager.create_task("no", "2026-01-01 09:00"),
            lambda: manager.create_event("no", "2026-01-01 09:00", "2026-01-01 08:00"),
            lambda: manager.create_contact("no", "road", "001"),
        ):
            with self.assertRaisesRegex(ValidationError, "exhausted"):
                create()
            self.assertEqual((manager.list_all(), manager.next_id), before)

    def test_record_and_counter_ranges_are_distinct_and_reject_huge_integers(self):
        """A valid exhaustion marker is a counter, never a record ID."""
        self.assertEqual(validate_id(MAX_RECORD_ID), MAX_RECORD_ID)
        self.assertEqual(validate_next_id(MAX_NEXT_ID), MAX_NEXT_ID)
        for value in (False, True, 0, -1, "1", MAX_NEXT_ID, 10**5000):
            with self.subTest(value_type=type(value).__name__):
                with self.assertRaises(ValidationError) as error:
                    Note(value, "invalid")
                self.assertLessEqual(len(str(error.exception)), MAX_ERROR_DETAIL)
        for value in (False, 0, MAX_NEXT_ID + 1, 10**5000):
            with self.assertRaises(ValidationError):
                validate_next_id(value)

    def test_restore_reports_record_index_and_preserves_higher_counter(self):
        """FR-45/46: row failures are located, and an exhausted session stays exhausted."""
        good = {"id": 1, "type": "note", "text": "good"}
        for bad in (None, {"id": 2, "type": "note", "text": ""},
                    {"id": 1, "type": "note", "text": "duplicate"}):
            with self.assertRaisesRegex(ValidationError, "record #2"):
                PIMManager.from_rows([good, bad], 3, 1)
        self.assertEqual(PIMManager.from_rows([good], 2, MAX_NEXT_ID).next_id, MAX_NEXT_ID)

    def test_invalid_counter_and_root_errors_are_not_labelled_as_records(self):
        for rows, file_next, previous in (([], MAX_NEXT_ID + 1, 1), ([], 1, False), (None, 1, 1)):
            with self.assertRaises(ValidationError) as error:
                PIMManager.from_rows(rows, file_next, previous)
            self.assertNotIn("record #", str(error.exception))

    def test_diagnostics_bound_unicode_and_keep_search_position(self):
        """Malformed values cannot overflow output or hide the positioned suffix."""
        for value in ("x" * 10**6, "\U0001f600" * 10**6, "'\\\x1b" * 1000, 10**5000, [], None, True, 1.5):
            self.assertLessEqual(len(preview(value)), MAX_PREVIEW)
        self.assertEqual(preview("short"), "'short'")
        error = SearchSyntaxError("\x1b\r\U0001f600" * 10000, 999)
        message = str(error)
        self.assertLessEqual(len(message), MAX_ERROR_DETAIL)
        self.assertTrue(message.endswith("at character 999"))
        self.assertNotIn("\x1b", message)
