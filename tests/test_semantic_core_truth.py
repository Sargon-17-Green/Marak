import inspect
import unittest

import compiler.semantic_core.truth as truth
from compiler.semantic_core.state import NUMBER_ASPECT, SemanticSnapshot, StateReferentId
from compiler.semantic_core.truth import (
    AddNumber, ConsequenceSelection, CurrentNumber, EqualNumberProposition,
    IntegerNumber, NumberIssue, Satisfaction, SubtractNumber, ZeroProposition,
    denote_number, judge_proposition, select_consequence,
)


class TruthSemanticCoreTests(unittest.TestCase):
    def test_exact_arithmetic_denotation(self):
        term = SubtractNumber(AddNumber(IntegerNumber(10**100), IntegerNumber(7)), IntegerNumber(3))
        self.assertEqual(denote_number(term, SemanticSnapshot()).value, 10**100 + 4)

    def test_zero_integer_is_not_itself_a_proposition(self):
        with self.assertRaises(TypeError):
            judge_proposition(IntegerNumber(0), SemanticSnapshot())  # type: ignore[arg-type]

    def test_nonzero_integer_is_not_truthy(self):
        with self.assertRaises(TypeError):
            select_consequence(IntegerNumber(8), SemanticSnapshot())  # type: ignore[arg-type]

    def test_numeric_equality_returns_meta_semantic_judgment(self):
        result = judge_proposition(EqualNumberProposition(IntegerNumber(4), IntegerNumber(4)), SemanticSnapshot())
        self.assertEqual(result.outcome, Satisfaction.HOLDS)
        self.assertNotIsInstance(result.outcome, bool)

    def test_zero_proposition_and_selection(self):
        p = ZeroProposition(SubtractNumber(IntegerNumber(1), IntegerNumber(1)))
        self.assertEqual(select_consequence(p, SemanticSnapshot()), ConsequenceSelection.HOLDS_CONSEQUENCE)
        p2 = ZeroProposition(IntegerNumber(1))
        self.assertEqual(select_consequence(p2, SemanticSnapshot()), ConsequenceSelection.DOES_NOT_HOLD_CONSEQUENCE)

    def test_missing_current_fact_is_proposition_error_not_false(self):
        p = ZeroProposition(CurrentNumber(StateReferentId("missing")))
        result = select_consequence(p, SemanticSnapshot())
        self.assertIsInstance(result, NumberIssue)
        self.assertEqual(result.code, "NO_CURRENT_NUMBER")

    def test_state_query_is_pure(self):
        r = StateReferentId("r")
        s = SemanticSnapshot().establish(r, NUMBER_ASPECT, 0)
        before = s.observable_facts()
        self.assertEqual(select_consequence(ZeroProposition(CurrentNumber(r)), s), ConsequenceSelection.HOLDS_CONSEQUENCE)
        self.assertEqual(s.observable_facts(), before)

    def test_no_boolean_value_class_is_exported(self):
        names = {name for name, value in inspect.getmembers(truth, inspect.isclass)}
        self.assertNotIn("Boolean", names)
        self.assertNotIn("BooleanValue", names)


if __name__ == "__main__":
    unittest.main()
