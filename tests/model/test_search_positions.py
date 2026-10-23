"""Location assertions use independent offsets in the original expression."""

import unittest
from model.errors import SearchSyntaxError
from model.search import parse_criterion


class SearchPositionTests(unittest.TestCase):
    def check_position(self, expression, position):
        with self.assertRaises(SearchSyntaxError) as raised:
            parse_criterion(expression)
        self.assertEqual(getattr(raised.exception, "position", None), position)
        self.assertIn(f"character {position}", str(raised.exception))

    def test_unknown_field_and_unexpected_token_point_to_the_token(self):
        self.check_position('  unknown = "x"', 3)
        expression = 'type = "note" stray'
        self.check_position(expression, expression.index('stray') + 1)

    def test_bad_operator_and_missing_operator_point_to_the_offending_token(self):
        self.check_position('deadline ! "2026-01-01 00:00"', 10)
        self.check_position('type "note"', 6)

    def test_invalid_type_text_and_time_literals_point_to_opening_quote(self):
        for expression in ('type = "unknown"', 'text contains ""', 'deadline < "bad time"'):
            with self.subTest(expression=expression):
                self.check_position(expression, expression.index('"') + 1)

    def test_invalid_escape_points_to_backslash_and_unclosed_quote_to_start(self):
        self.check_position(r'text contains "bad\q"', 19)
        self.check_position('text contains "unclosed', 15)

    def test_unmatched_parentheses_point_to_the_unmatched_parenthesis(self):
        self.check_position(' (type = "note"', 2)
        expression = 'type = "note")'
        self.check_position(expression, len(expression))

    def test_incomplete_expression_points_one_character_past_end(self):
        for expression in ('', '   ', 'type =', 'type = "note" && '):
            with self.subTest(expression=expression):
                self.check_position(expression, len(expression) + 1)

    def test_unicode_and_escaped_literals_keep_original_source_offsets(self):
        expression = r'text contains "中文\"x" && @'
        self.check_position(expression, expression.index('@') + 1)
