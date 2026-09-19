import unittest

from compiler.api import check, normalize
from compiler.parse.a0_registry import A0_REGISTRY
from compiler.lex.words import lex_words
from compiler.morphology.api import MorphAnalysis
from compiler.parse.forest import AmbiguityStatus, ParseAlternative, ParseForest, ParseNode
from compiler.parse.grammar import (
    ConstructionDeclaration,
    ConstructionKind,
    MorphTerminal,
    Nonterminal,
    Production,
    SpecStatus,
    WordTerminal,
    registry_from_parts,
)
from compiler.parse.parser import Parser


def tokens(text: str):
    return lex_words(normalize(text))


def registry(*, declarations, productions):
    return registry_from_parts(
        language_edition="test",
        registry_version="test.1",
        declarations=declarations,
        productions=productions,
        source_snapshot="synthetic-test-only",
    )


def normative_decl(cid="C"):
    return ConstructionDeclaration(cid, ConstructionKind.POSITIVE, SpecStatus.NORMATIVE, ("TEST",), "synthetic")


class ProductionRegistryTests(unittest.TestCase):
    def test_a0_positive_grammar_is_blocked_not_guessed(self):
        r = check("עשה דבר", registry=A0_REGISTRY)
        self.assertFalse(r.valid)
        self.assertEqual(r.diagnostics[0].code, "PARSE0001")
        self.assertIn("A0.ATOMIC_IMPERATIVE_CANDIDATE", r.diagnostics[0].metadata["proposed_positive"])

    def test_proposed_production_is_not_admitted(self):
        d = ConstructionDeclaration("C", ConstructionKind.POSITIVE, SpecStatus.PROPOSED, ("TEST",), "synthetic")
        p = Production("P", "C", "Program", (WordTerminal("אב"),), "S", root=True)
        reg = registry(declarations=(d,), productions=(p,))
        self.assertEqual(reg.admitted_productions, ())
        result = Parser(reg).parse(tokens("אב"), {})
        self.assertFalse(result.grammar_available)
        self.assertEqual(result.forest.alternatives, ())

    def test_word_terminal_cannot_smuggle_transparent_characters_into_grammar(self):
        with self.assertRaises(ValueError):
            WordTerminal("אב1")
        with self.assertRaises(ValueError):
            WordTerminal("אב-")

    def test_morph_terminal_rejects_duplicate_feature_keys(self):
        with self.assertRaises(ValueError):
            MorphTerminal(lemma="עשה", features=(("mood", "imperative"), ("mood", "perfect")))

    def test_nonpositive_construction_cannot_own_production(self):
        d = ConstructionDeclaration("C", ConstructionKind.NEGATIVE, SpecStatus.NORMATIVE, ("TEST",), "synthetic")
        p = Production("P", "C", "Program", (WordTerminal("אב"),), "S", root=True)
        with self.assertRaises(ValueError):
            registry(declarations=(d,), productions=(p,))


class ChartParserTests(unittest.TestCase):
    def test_exact_literal_program(self):
        d = normative_decl()
        p = Production("P", "C", "Program", (WordTerminal("אב"), WordTerminal("גד")), "S", root=True)
        result = Parser(registry(declarations=(d,), productions=(p,))).parse(tokens("אב גד"), {})
        self.assertEqual(len(result.forest.alternatives), 1)
        root = result.forest.alternatives[0].root
        self.assertEqual((root.token_start, root.token_end), (0, 2))
        self.assertEqual([c.text for c in root.children], ["אב", "גד"])
        self.assertEqual(result.forest.ambiguity_status, AmbiguityStatus.UNIQUE)

    def test_nonterminal_composition(self):
        d = normative_decl()
        ps = (
            Production("P0", "C", "Program", (Nonterminal("A"), Nonterminal("B")), "S0", root=True),
            Production("P1", "C", "A", (WordTerminal("אב"),), "S1"),
            Production("P2", "C", "B", (WordTerminal("גד"),), "S2"),
        )
        result = Parser(registry(declarations=(d,), productions=ps)).parse(tokens("אב גד"), {})
        self.assertEqual(len(result.forest.alternatives), 1)
        self.assertEqual([x.symbol for x in result.forest.alternatives[0].root.children], ["A", "B"])

    def test_two_parses_are_preserved_without_ranking(self):
        d1, d2 = normative_decl("C1"), normative_decl("C2")
        ps = (
            Production("P1", "C1", "Program", (WordTerminal("אב"),), "SAME", root=True),
            Production("P2", "C2", "Program", (WordTerminal("אב"),), "SAME", root=True),
        )
        result = Parser(registry(declarations=(d2, d1), productions=ps[::-1])).parse(tokens("אב"), {})
        self.assertEqual(len(result.forest.alternatives), 2)
        self.assertEqual(result.forest.ambiguity_status, AmbiguityStatus.UNRESOLVED_MULTIPLE)
        self.assertTrue(result.forest.requires_disambiguation)
        self.assertEqual([a.root.production_id for a in result.forest.alternatives], ["P1", "P2"])

    def test_same_semantic_id_does_not_fake_equivalence(self):
        root1 = ParseNode("P1", "C", "Program", 0, 1, 0, 2, None)
        root2 = ParseNode("P2", "C", "Program", 0, 1, 0, 2, None)
        forest = ParseForest((ParseAlternative(root1, "S"), ParseAlternative(root2, "S")))
        self.assertEqual(forest.ambiguity_status, AmbiguityStatus.UNRESOLVED_MULTIPLE)

    def test_semantic_equivalence_requires_explicit_fingerprint(self):
        root1 = ParseNode("P1", "C", "Program", 0, 1, 0, 2, None)
        root2 = ParseNode("P2", "C", "Program", 0, 1, 0, 2, None)
        eq = ParseForest((ParseAlternative(root1, "S", "K"), ParseAlternative(root2, "S", "K")))
        neq = ParseForest((ParseAlternative(root1, "S", "K1"), ParseAlternative(root2, "S", "K2")))
        self.assertEqual(eq.ambiguity_status, AmbiguityStatus.PROVEN_EQUIVALENT)
        self.assertEqual(neq.ambiguity_status, AmbiguityStatus.PROVEN_DISTINCT)

    def test_left_recursive_ambiguous_grammar_preserves_both_trees(self):
        d = normative_decl()
        ps = (
            Production("P0", "C", "Program", (Nonterminal("X"),), "SP", root=True),
            Production("P1", "C", "X", (Nonterminal("X"), Nonterminal("X")), "SX"),
            Production("P2", "C", "X", (WordTerminal("אב"),), "SA"),
        )
        result = Parser(registry(declarations=(d,), productions=ps)).parse(tokens("אב אב אב"), {})
        self.assertEqual(len(result.forest.alternatives), 2)
        self.assertEqual(result.forest.ambiguity_status, AmbiguityStatus.UNRESOLVED_MULTIPLE)
        self.assertGreater(result.metrics.derivations, result.metrics.state_keys)

    def test_no_match_reports_furthest_and_expected(self):
        d = normative_decl()
        p = Production("P", "C", "Program", (WordTerminal("אב"), WordTerminal("גד")), "S", root=True)
        result = Parser(registry(declarations=(d,), productions=(p,))).parse(tokens("אב דה"), {})
        self.assertEqual(result.forest.alternatives, ())
        self.assertEqual(result.failure.furthest_token, 1)
        self.assertEqual(result.failure.expected, ("word:גד",))

    def test_registration_order_does_not_change_forest_order(self):
        d1, d2 = normative_decl("C1"), normative_decl("C2")
        p1 = Production("P1", "C1", "Program", (WordTerminal("אב"),), "S1", root=True)
        p2 = Production("P2", "C2", "Program", (WordTerminal("אב"),), "S2", root=True)
        r1 = Parser(registry(declarations=(d1, d2), productions=(p1, p2))).parse(tokens("אב"), {})
        r2 = Parser(registry(declarations=(d2, d1), productions=(p2, p1))).parse(tokens("אב"), {})
        self.assertEqual(r1.forest, r2.forest)
        self.assertEqual(r1.metrics, r2.metrics)


class MorphologyTerminalTests(unittest.TestCase):
    def test_all_licensed_morphology_candidates_are_preserved(self):
        d = normative_decl()
        p = Production("P", "C", "Program", (MorphTerminal(lemma="עשה"),), "S", root=True)
        ts = tokens("עשה")
        morph = {
            0: (
                MorphAnalysis("R2", "עשה", (("mood", "imperative"),)),
                MorphAnalysis("R1", "עשה", (("mood", "perfect"),)),
                MorphAnalysis("R3", "אחר", ()),
            )
        }
        result = Parser(registry(declarations=(d,), productions=(p,))).parse(ts, morph)
        self.assertEqual(len(result.forest.alternatives), 2)
        rules = [a.root.children[0].morphology_rule_id for a in result.forest.alternatives]
        self.assertEqual(rules, ["R1", "R2"])

    def test_feature_constraints_are_exact_subset_matches(self):
        d = normative_decl()
        p = Production(
            "P", "C", "Program",
            (MorphTerminal(lemma="עשה", features=(("mood", "imperative"),)),),
            "S", root=True,
        )
        ts = tokens("עשה")
        morph = {0: (
            MorphAnalysis("R1", "עשה", (("mood", "perfect"),)),
            MorphAnalysis("R2", "עשה", (("mood", "imperative"), ("person", "2ms"))),
        )}
        result = Parser(registry(declarations=(d,), productions=(p,))).parse(ts, morph)
        self.assertEqual(len(result.forest.alternatives), 1)
        self.assertEqual(result.forest.alternatives[0].root.children[0].morphology_rule_id, "R2")


if __name__ == "__main__":
    unittest.main()
