"""Manager search integration and search-then-update (US6/US7)."""

import unittest

from model.errors import ValidationError
from model.manager import PIMManager
from model.search import parse_criterion


class SearchIntegrationTests(unittest.TestCase):
    def test_search_orders_records_and_does_not_mutate(self):
        manager = PIMManager()
        manager.create_note("memo")
        task = manager.create_task("meeting", "2026-10-01 09:00")
        manager.create_event("meeting", "2026-10-02 09:00", "2026-10-01 08:00")
        before = manager.list_all()
        criterion = parse_criterion('(type = "task" || type = "event") && description contains "MEET"')
        self.assertEqual([item.id for item in manager.search(criterion)], [2, 3])
        self.assertEqual(manager.search(parse_criterion('type = "contact"')), ())
        self.assertEqual(manager.list_all(), before)
        with self.assertRaises(ValidationError):
            manager.search("type = note")
        self.assertEqual(manager.list_all(), before)
        selected = manager.search(parse_criterion('type = "task"'))[0]
        manager.update(selected.id, "description", "revised")
        self.assertEqual(manager.get(task.id).description, "revised")


if __name__ == "__main__":
    unittest.main()
