"""Collection creation, CRUD, ordering, and snapshot restoration."""

import unittest

from model.errors import RecordNotFoundError, ValidationError
from model.manager import PIMManager


class ManagerTests(unittest.TestCase):
    def test_create_all_types_and_monotonic_ids(self):
        manager = PIMManager()
        self.assertEqual(manager.next_id, 1)
        records = (
            manager.create_note(" x "),
            manager.create_task("x", "2026-10-01 09:00"),
            manager.create_event("x", "2026-10-02 10:00", "2026-10-01 10:00"),
            manager.create_contact("x", "a", "+001"),
        )
        self.assertEqual([item.id for item in records], [1, 2, 3, 4])
        self.assertEqual(manager.next_id, 5)
        self.assertEqual(tuple(records), manager.list_all())
        manager.delete(2)
        self.assertEqual(manager.create_note("x").id, 5)

    def test_invalid_creation_does_not_consume_id(self):
        manager = PIMManager()
        for create in (
            lambda: manager.create_note(" "),
            lambda: manager.create_task("x", "2026-02-30 09:00"),
            lambda: manager.create_event("x", "bad", "2026-01-01 09:00"),
            lambda: manager.create_contact("x", "a", "\n"),
        ):
            with self.assertRaises(ValidationError):
                create()
        self.assertEqual((manager.next_id, manager.list_all()), (1, ()))

    def test_get_list_update_delete_and_invalid_ids(self):
        manager = PIMManager()
        note = manager.create_note("hello")
        task = manager.create_task("work", "2026-10-01 09:00")
        self.assertEqual(manager.get(note.id), note)
        self.assertEqual(manager.list_all("TASK"), (task,))
        changed = manager.update(task.id, "DEADLINE", "2026-10-02 09:00")
        self.assertEqual(changed.deadline.day, 2)
        self.assertEqual(manager.update(note.id, "TEXT", " world ").text, "world")
        for bad in (0, True, "1"):
            with self.subTest(id=bad), self.assertRaises(ValidationError):
                manager.get(bad)
        with self.assertRaises(RecordNotFoundError):
            manager.get(999)
        manager.delete(note.id)
        with self.assertRaises(RecordNotFoundError):
            manager.delete(note.id)

    def test_failed_update_is_atomic_and_forbidden_fields(self):
        manager = PIMManager()
        event = manager.create_event("meeting", "2026-10-01 10:00", "2026-10-01 09:00")
        for field, value in (("id", "5"), ("type", "note"), ("name", "x"), ("start_time", "bad")):
            with self.subTest(field=field), self.assertRaises(ValidationError):
                manager.update(event.id, field, value)
            self.assertIs(manager.get(event.id), event)
        self.assertEqual(manager.next_id, 2)

    def test_from_rows_checks_schema_order_and_counters(self):
        rows = [
            {"id": 2, "type": "note", "text": "memo"},
            {"id": 5, "type": "task", "description": "work", "deadline": "2026-10-01 09:00"},
        ]
        manager = PIMManager.from_rows(rows, file_next_id=6, previous_next_id=10)
        self.assertEqual((manager.next_id, [r.id for r in manager.list_all()]), (10, [2, 5]))
        bad_rows = (
            list(reversed(rows)), [rows[0], rows[0]], [{**rows[0], "extra": "bad"}],
            [{**rows[0], "id": True}], [{**rows[1], "deadline": "bad"}],
        )
        for bad in bad_rows:
            with self.subTest(rows=bad), self.assertRaises(ValidationError):
                PIMManager.from_rows(bad, 6, 1)
        for counter in (True, 0, 5):
            with self.subTest(counter=counter), self.assertRaises(ValidationError):
                PIMManager.from_rows(rows, counter, 1)


if __name__ == "__main__":
    unittest.main()
