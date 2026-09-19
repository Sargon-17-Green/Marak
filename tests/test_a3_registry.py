import unittest

from compiler.api import check, normalize
from compiler.lex.words import lex_words
from compiler.parse.a3_registry import A3_REGISTRY
from compiler.parse.grammar import ConstructionKind, SpecStatus
from compiler.parse.parser import Parser


class A3RegistryTests(unittest.TestCase):
    def test_sequence_and_counted_repeat_are_normative_shells(self):
        ids = {d.construction_id: d for d in A3_REGISTRY.declarations}
        self.assertIs(ids["A2.EXPLICIT_SEQUENCE"].status, SpecStatus.NORMATIVE)
        self.assertIs(ids["A3.COUNTED_ATOMIC_REPEAT"].status, SpecStatus.NORMATIVE)
        self.assertIs(ids["A3.NO_GENERIC_END"].kind, ConstructionKind.NEGATIVE)
        self.assertTrue(A3_REGISTRY.admitted_root_productions)

    def test_repeat_counts_are_exactly_three_through_nine(self):
        words = set()
        for p in A3_REGISTRY.productions_for("RepeatCount"):
            words.add(tuple(getattr(x, "text", None) for x in p.rhs))
        self.assertEqual(words, {
            ("שלש", "פעמים"), ("ארבע", "פעמים"), ("חמש", "פעמים"),
            ("שש", "פעמים"), ("שבע", "פעמים"), ("שמנה", "פעמים"),
            ("תשע", "פעמים"),
        })

    def test_atomic_action_is_not_invented(self):
        result = check("שלש פעמים עשה דבר", registry=A3_REGISTRY)
        self.assertFalse(result.valid)
        self.assertEqual(result.diagnostics[0].code, "PARSE0002")
        self.assertEqual(result.parse_result.failure.furthest_token, 2)
        self.assertIn("nonterminal:AtomicAction", result.parse_result.failure.expected)

    def test_sequence_marker_does_not_make_arbitrary_words_actions(self):
        result = check("אב ואחרי כן גד", registry=A3_REGISTRY)
        self.assertFalse(result.valid)
        self.assertEqual(result.diagnostics[0].code, "PARSE0002")
        self.assertIn("nonterminal:AtomicAction", result.parse_result.failure.expected)


if __name__ == "__main__":
    unittest.main()
