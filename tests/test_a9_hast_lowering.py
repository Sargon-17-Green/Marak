import unittest

from compiler.api import parse
from compiler.hast.lower_a9 import A9LoweringError, lower_a9_fragment
from compiler.models.hast import HastAddNumber, HastEqualNumberProposition, HastExactInteger, HastSubtractNumber
from compiler.parse.a9_registry import A9_REGISTRY
from compiler.semantic_core.from_hast import number_term_from_hast, proposition_from_hast
from compiler.semantic_core.state import SemanticSnapshot
from compiler.semantic_core.truth import Satisfaction, denote_number, judge_proposition

ONE = "המספר אשר הוא אחד"
ZERO = "המספר הנחשב בגרע את המספר אשר הוא אחד מן המספר אשר הוא אחד"


def one_parse(source: str, lhs: str):
    result = parse(source, file="sample.md", registry=A9_REGISTRY, start_lhs=lhs)
    if len(result.forest.alternatives) != 1:
        raise AssertionError(result.forest.alternatives)
    return result.forest.alternatives[0]


class A9HastLoweringTests(unittest.TestCase):
    def test_literal_one_lowers_with_source_provenance(self):
        hast = lower_a9_fragment(one_parse(ONE, "NumberValue"))
        self.assertIsInstance(hast, HastExactInteger)
        self.assertEqual(hast.value, 1)
        self.assertEqual(hast.source_span.start.file, "sample.md")
        self.assertEqual(hast.source_span.start.char_offset, 0)
        self.assertEqual(hast.source_span.end.char_offset, len(ONE))

    def test_derived_zero_lowers_and_denotes_zero(self):
        hast = lower_a9_fragment(one_parse(ZERO, "NumberValue"))
        self.assertIsInstance(hast, HastSubtractNumber)
        result = denote_number(number_term_from_hast(hast), SemanticSnapshot())
        self.assertEqual(result.value, 0)

    def test_nested_addition_lowers_structurally_without_precedence_guess(self):
        source = f"המספר הנחשב בהוסיף את {ZERO} על {ONE}"
        hast = lower_a9_fragment(one_parse(source, "NumberValue"))
        self.assertIsInstance(hast, HastAddNumber)
        self.assertIsInstance(hast.left, HastSubtractNumber)
        self.assertIsInstance(hast.right, HastExactInteger)
        self.assertEqual(denote_number(number_term_from_hast(hast), SemanticSnapshot()).value, 1)

    def test_numeric_identity_lowers_to_proposition_not_boolean_value(self):
        source = f"{ZERO} הוא {ZERO}"
        hast = lower_a9_fragment(one_parse(source, "Proposition"))
        self.assertIsInstance(hast, HastEqualNumberProposition)
        judgment = judge_proposition(proposition_from_hast(hast), SemanticSnapshot())
        self.assertEqual(judgment.outcome, Satisfaction.HOLDS)

    def test_root_control_shell_is_deliberately_not_lowered(self):
        # No complete control parse exists because A9 has no admitted consequence leaf.
        source = f"אם {ZERO} הוא {ZERO} עשה דבר ואם לא עשה דבר"
        result = parse(source, registry=A9_REGISTRY)
        self.assertEqual(result.forest.alternatives, ())


if __name__ == "__main__":
    unittest.main()
