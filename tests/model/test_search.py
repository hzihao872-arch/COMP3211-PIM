"""Search grammar, semantics, and invalid expressions (US7)."""

import unittest
from datetime import datetime

from model.errors import SearchSyntaxError, ValidationError
from model.records import Contact, Event, Note, Task
from model.search import (
    AndCriterion, NotCriterion, OrCriterion, TextCriterion, TimeCriterion,
    TypeCriterion, parse_criterion,
)


class SearchTests(unittest.TestCase):
    def setUp(self):
        self.note = Note(1, "Alpha Memo")
        self.task = Task(2, "Alpha Task", datetime(2026, 10, 1, 9))
        self.event = Event(3, "Alpha Event", datetime(2026, 10, 2, 10), datetime(2026, 10, 1, 8))
        self.contact = Contact(4, "Alice", "Alpha Road", "+00123")
        self.records = (self.note, self.task, self.event, self.contact)

    def matches(self, expression):
        criterion = parse_criterion(expression)
        return tuple(record.id for record in self.records if criterion.matches(record))

    def test_type_and_all_text_fields_are_case_insensitive(self):
        self.assertEqual(self.matches('TyPe = "TaSk"'), (2,))
        cases = {
            "text": (1,), "description": (2, 3), "name": (4,),
            "address": (4,), "mobile_number": (4,),
        }
        for field, ids in cases.items():
            needle = "001" if field == "mobile_number" else ("ALICE" if field == "name" else "ALPHA")
            with self.subTest(field=field):
                self.assertEqual(self.matches(f'{field} CONTAINS "{needle}"'), ids)

    def test_each_time_field_and_comparison_operator(self):
        values = {"deadline": (2, "2026-10-01 09:00"), "start_time": (3, "2026-10-02 10:00"), "alarm_time": (3, "2026-10-01 08:00")}
        for field, (record_id, moment) in values.items():
            for operator, query in (("<", "2026-12-01 00:00"), (">", "2026-01-01 00:00"), ("=", moment)):
                with self.subTest(field=field, operator=operator):
                    self.assertEqual(self.matches(f'{field} {operator} "{query}"'), (record_id,))

    def test_boolean_precedence_parentheses_negation_and_absent_field(self):
        self.assertEqual(self.matches('type = "note" || type = "task" && description contains "task"'), (1, 2))
        self.assertEqual(self.matches('(type = "note" || type = "task") && description contains "task"'), (2,))
        self.assertEqual(self.matches('!description contains "alpha"'), (1, 4))
        self.assertEqual(self.matches('!!(type = "event")'), (3,))
        self.assertEqual(self.matches('type = "note" && type = "task" || type = "contact"'), (4,))

    def test_quoted_escapes_and_adjacent_symbols(self):
        note = Note(5, 'A "quoted" \\ memo')
        criterion = parse_criterion('!(type="task")&&text contains "\\"quoted\\" \\\\"')
        self.assertTrue(criterion.matches(note))
        self.assertFalse(criterion.matches(self.task))

    def test_invalid_expression_is_rejected_whole(self):
        invalid = (
            "", "   ", 'type = task', 'type = "other"', 'unknown = "x"',
            'text = "x"', 'deadline contains "x"', 'text contains ""',
            'deadline < "bad"', 'type = "note" &&', '&& type = "note"',
            'type = "note" || || type = "task"', '(type = "note"',
            'type = "note")', 'type = "note" type = "task"',
            'text contains "bad\\n"', 'text contains "unterminated',
        )
        for expression in invalid:
            with self.subTest(expression=expression), self.assertRaises(SearchSyntaxError):
                parse_criterion(expression)
        with self.assertRaises(SearchSyntaxError):
            parse_criterion(42)

    def test_direct_nodes_validate_and_remain_immutable(self):
        self.assertTrue(TypeCriterion("NOTE").matches(self.note))
        self.assertTrue(TextCriterion("TEXT", "Memo").matches(self.note))
        self.assertTrue(TimeCriterion("DEADLINE", "=", datetime(2026, 10, 1, 9)).matches(self.task))
        self.assertTrue(AndCriterion(TypeCriterion("note"), NotCriterion(TypeCriterion("task"))).matches(self.note))
        self.assertTrue(OrCriterion(TypeCriterion("task"), TypeCriterion("note")).matches(self.note))
        for factory in (
            lambda: TypeCriterion("other"), lambda: TextCriterion("bad", "x"),
            lambda: TextCriterion("text", ""), lambda: TimeCriterion("bad", "=", datetime.now()),
            lambda: TimeCriterion("deadline", "!=", datetime(2026, 1, 1)),
            lambda: NotCriterion("bad"), lambda: AndCriterion(TypeCriterion("note"), "bad"),
        ):
            with self.assertRaises(ValidationError):
                factory()

    def test_deep_valid_expressions_evaluate_without_recursion(self):
        expressions = (
            '!' * 1200 + 'type = "note"',
            '(' * 1200 + 'type = "note"' + ')' * 1200,
            ' && '.join(['type = "note"'] * 1200),
            ' || '.join(['type = "note"'] * 1200),
        )
        for expression in expressions:
            with self.subTest(length=len(expression)):
                self.assertEqual(self.matches(expression), (1,))


if __name__ == "__main__":
    unittest.main()
