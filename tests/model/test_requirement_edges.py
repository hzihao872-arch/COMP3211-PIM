"""Direct acceptance evidence for SRS boundaries omitted from the first suite."""

import unittest
from dataclasses import asdict
from datetime import datetime

from model.errors import SearchSyntaxError, ValidationError
from model.manager import PIMManager
from model.records import Event, Note, Task
from model.search import AndCriterion, OrCriterion, TypeCriterion, parse_criterion


class ModelRequirementTests(unittest.TestCase):
    def test_past_times_and_alarm_after_start_are_accepted(self):
        """FR-04/07: historical times and either alarm ordering are valid data."""
        manager = PIMManager()
        task = manager.create_task("archive", "2000-01-01 00:00")
        event = manager.create_event("archive", "2000-01-01 00:00", "2000-01-02 00:00")
        self.assertEqual(task.deadline, datetime(2000, 1, 1))
        self.assertEqual(event.start_time, datetime(2000, 1, 1))
        self.assertEqual(event.alarm_time, datetime(2000, 1, 2))
        self.assertEqual(manager.list_all(), (task, event))

    def test_every_mutable_field_changes_only_that_field(self):
        """FR-16: all nine fields are editable, retaining ID/type/other fields."""
        manager = PIMManager()
        records = (
            (manager.create_note("old"), {"text": "New Note"}),
            (manager.create_task("old", "2026-01-01 09:00"),
             {"description": "New Task", "deadline": "2027-02-02 10:00"}),
            (manager.create_event("old", "2026-01-01 09:00", "2026-01-01 08:00"),
             {"description": "New Event", "start_time": "2027-02-02 10:00",
              "alarm_time": "2027-02-03 11:00"}),
            (manager.create_contact("old", "old road", "001"),
             {"name": "New Name", "address": "New Road", "mobile_number": "+0099"}),
        )
        for record, changes in records:
            for field, value in changes.items():
                with self.subTest(record_type=record.type, field=field):
                    before = asdict(manager.get(record.id))
                    old_collection = manager.list_all()
                    old_next = manager.next_id
                    changed = manager.update(record.id, field.upper(), value)
                    expected = dict(before)
                    expected[field] = (datetime.strptime(value, "%Y-%m-%d %H:%M")
                                       if field in {"deadline", "start_time", "alarm_time"}
                                       else value)
                    self.assertEqual(asdict(changed), expected)
                    self.assertEqual(changed.type, record.type)
                    self.assertEqual(manager.next_id, old_next)
                    self.assertEqual(tuple(r for r in manager.list_all() if r.id != record.id),
                                     tuple(r for r in old_collection if r.id != record.id))

    def test_time_comparisons_cross_calendar_boundaries(self):
        """FR-32: <, >, = compare full dates, including leap days and years."""
        boundaries = (
            ("2026-01-01 23:59", "2026-01-02 00:00"),
            ("2026-01-31 23:59", "2026-02-01 00:00"),
            ("2024-02-28 23:59", "2024-02-29 00:00"),
            ("2024-02-29 23:59", "2024-03-01 00:00"),
            ("2026-12-31 23:59", "2027-01-01 00:00"),
        )
        for earlier, later in boundaries:
            moment = datetime.strptime(earlier, "%Y-%m-%d %H:%M")
            for field in ("deadline", "start_time", "alarm_time"):
                record = Task(1, "test", moment) if field == "deadline" else Event(1, "test", moment, moment)
                for operator, query, expected in (
                    ("<", later, True), (">", later, False), ("=", later, False),
                    ("<", earlier, False), (">", earlier, False), ("=", earlier, True),
                ):
                    with self.subTest(field=field, boundary=later, op=operator, query=query):
                        self.assertEqual(parse_criterion(f'{field} {operator} "{query}"').matches(record), expected)
                later_moment = datetime.strptime(later, "%Y-%m-%d %H:%M")
                later_record = Task(1, "test", later_moment) if field == "deadline" else Event(1, "test", later_moment, later_moment)
                self.assertTrue(parse_criterion(f'{field} > "{earlier}"').matches(later_record))

    def test_and_or_full_truth_tables(self):
        """FR-33/34: both direct nodes and parsed expressions obey all four rows."""
        record = Note(1, "memo")
        for left, right, and_expected, or_expected in (
            (False, False, False, False), (False, True, False, True),
            (True, False, False, True), (True, True, True, True),
        ):
            left_type, right_type = ("note" if left else "task"), ("note" if right else "task")
            with self.subTest(left=left, right=right):
                self.assertEqual(AndCriterion(TypeCriterion(left_type), TypeCriterion(right_type)).matches(record), and_expected)
                self.assertEqual(OrCriterion(TypeCriterion(left_type), TypeCriterion(right_type)).matches(record), or_expected)
                self.assertEqual(parse_criterion(f'type = "{left_type}" && type = "{right_type}"').matches(record), and_expected)
                self.assertEqual(parse_criterion(f'type = "{left_type}" || type = "{right_type}"').matches(record), or_expected)

    def test_invalid_model_api_inputs_preserve_collection(self):
        """Malformed direct API inputs must fail without changing existing data."""
        manager = PIMManager()
        manager.create_note("keep")
        before = manager.list_all(), manager.next_id
        operations = (
            lambda: manager.update(1, None, "value"),
            lambda: PIMManager.from_rows(None, 2, 2),
            lambda: PIMManager.from_rows([None], 2, 2),
            lambda: OrCriterion(TypeCriterion("note"), "invalid"),
        )
        for operation in operations:
            with self.assertRaises(ValidationError):
                operation()
            self.assertEqual((manager.list_all(), manager.next_id), before)

    def test_unrecognized_search_character_is_rejected(self):
        """A trailing invalid symbol cannot silently alter a valid search."""
        with self.assertRaises(SearchSyntaxError):
            parse_criterion('type = "note" @')
