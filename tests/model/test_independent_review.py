"""Independent truth-table oracle for Boolean precedence and grouped negation."""

import itertools
import unittest

from model.records import Note
from model.search import parse_criterion


class BooleanCompositionTests(unittest.TestCase):
    def test_three_atom_compositions_against_independent_truth_tables(self):
        """US7/FR-33–36: all eight assignments distinguish grouping and precedence."""
        a, b, c = (f'text contains "{letter}"' for letter in "abc")
        expressions = (
            (f"{a} || {b} && {c}", lambda x, y, z: x or (y and z)),
            (f"({a} || {b}) && {c}", lambda x, y, z: (x or y) and z),
            (f"!{a} && {b} || {c}", lambda x, y, z: ((not x) and y) or z),
            (f"!({a} && ({b} || !{c}))", lambda x, y, z: not (x and (y or not z))),
            (f"!({a} || {b}) && !!{c}", lambda x, y, z: not (x or y) and z),
            (f"{a} && !({b} && {c})", lambda x, y, z: x and not (y and z)),
        )
        for values in itertools.product((False, True), repeat=3):
            text = " ".join(letter for letter, present in zip("abc", values) if present) or "empty"
            record = Note(1, text)
            for expression, expected in expressions:
                with self.subTest(values=values, expression=expression):
                    self.assertEqual(parse_criterion(expression).matches(record), expected(*values))
