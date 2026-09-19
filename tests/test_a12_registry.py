import json
from pathlib import Path
import unittest

from compiler.api import check, parse
from compiler.hast.lower_a9 import lower_numeric_truth_fragment
from compiler.models.hast import HastExactInteger
from compiler.parse.a12_registry import A12_REGISTRY
from compiler.parse.grammar import (
    ConstructionDeclaration, ConstructionKind, ConstructionRegistry,
    NumeralTerminal, Production, SemanticReadiness, SpecStatus, WordTerminal,
)
from compiler.parse.numeral_lexicons import (
    A12_DIRECT_NUMERAL_LEXICON_ID, A12_DIRECT_NUMERALS, A12_VALUE_BY_TEXT,
    match_numeral_lexicon,
)

ROOT = Path(__file__).resolve().parents[1]
ONE = "המספר אשר הוא אחד"
TWO = "המספר אשר הוא שנים"
THREE = "המספר אשר הוא שלשה"


class A12RegistryTests(unittest.TestCase):
    def test_snapshot_matches_code(self):
        disk = json.loads((ROOT / "spec" / "A12_CONSTRUCTION_REGISTRY.json").read_text(encoding="utf-8"))
        self.assertEqual(disk, A12_REGISTRY.to_dict())

    def test_frozen_direct_numeral_frontier_parses_representatives(self):
        samples = {
            1: "אחד",
            11: "אחד עשר",
            101: "מאה ואחד",
            9999: "תשעת אלפים ותשע מאות ותשעים ותשעה",
        }
        for value, words in samples.items():
            with self.subTest(value=value):
                r = parse(f"המספר אשר הוא {words}", registry=A12_REGISTRY, start_lhs="NumberValue")
                self.assertEqual(len(r.forest.alternatives), 1)
                hast = lower_numeric_truth_fragment(r.forest.alternatives[0])
                self.assertIsInstance(hast, HastExactInteger)
                self.assertEqual(hast.value, value)

    def test_all_9999_frozen_lexicon_entries_are_unique_and_exactly_recoverable(self):
        self.assertEqual(len(A12_DIRECT_NUMERALS), 10000)
        self.assertEqual(len(A12_VALUE_BY_TEXT), 9999)
        for value in range(1, 10000):
            text = A12_DIRECT_NUMERALS[value]
            words = tuple(text.split())
            matches = match_numeral_lexicon(A12_DIRECT_NUMERAL_LEXICON_ID, words, 0)
            self.assertIn((len(words), value, text), matches)

    def test_numeral_terminal_does_not_greedily_take_longest_boundary(self):
        registry = ConstructionRegistry(
            language_edition="test-only",
            registry_version="test-only-numeral-boundary",
            declarations=(ConstructionDeclaration(
                "TEST.NUMERAL.BOUNDARY", ConstructionKind.POSITIVE, SpecStatus.NORMATIVE,
                ("TEST-ONLY",), "Synthetic parser test; not language grammar.",
            ),),
            productions=(Production(
                "TEST.NUMERAL.BOUNDARY", "TEST.NUMERAL.BOUNDARY", "Start",
                (NumeralTerminal(A12_DIRECT_NUMERAL_LEXICON_ID), WordTerminal("ואחד"), WordTerminal("עשר")),
                "TEST.NUMERAL.BOUNDARY", root=True,
            ),),
        )
        r = parse("מאה ואחד עשר", registry=registry)
        self.assertEqual(len(r.forest.alternatives), 1)
        leaf_values = []
        def walk(e):
            if hasattr(e, "numeric_value") and e.numeric_value is not None:
                leaf_values.append(e.numeric_value)
            if hasattr(e, "children"):
                for c in e.children:
                    walk(c)
        walk(r.forest.alternatives[0].root)
        self.assertEqual(leaf_values, [100])

    def test_singular_body_is_current_and_a11_plural_alias_is_rejected(self):
        current = "זה דבר המעשה אשר שמו ראובן עשה את המעשה אשר שמו שמעון עד הנה דבר המעשה אשר שמו ראובן"
        old = "אלה דברי המעשה אשר שמו ראובן עשה את המעשה אשר שמו שמעון עד הנה דברי המעשה אשר שמו ראובן"
        self.assertEqual(len(parse(current, registry=A12_REGISTRY).forest.alternatives), 1)
        self.assertEqual(parse(old, registry=A12_REGISTRY).forest.alternatives, ())

    def test_body_name_mismatch_is_not_repaired_by_nearest_body(self):
        source = "זה דבר המעשה אשר שמו ראובן עשה את המעשה אשר שמו שמעון עד הנה דבר המעשה אשר שמו יהודה"
        self.assertIn("REF0021", [d.code for d in check(source, registry=A12_REGISTRY).diagnostics])

    def test_single_immediate_result_only(self):
        single = "המספר אשר יצא עתה מן המעשה אשר שמו ראובן"
        ordinal = "המספר הראשון אשר יצא עתה מן המעשה אשר שמו ראובן"
        old = "המספר אשר יצא מן המעשה אשר שמו ראובן"
        self.assertEqual(len(parse(single, registry=A12_REGISTRY, start_lhs="NumberValue").forest.alternatives), 1)
        self.assertEqual(parse(ordinal, registry=A12_REGISTRY, start_lhs="NumberValue").forest.alternatives, ())
        self.assertEqual(parse(old, registry=A12_REGISTRY, start_lhs="NumberValue").forest.alternatives, ())

    def test_multiple_result_productions_parse_but_fail_a12_semantic_validation(self):
        source = (
            f"זה דבר המעשה אשר שמו ראובן הוצא מן המעשה הזה את {ONE} ואחרי כן "
            f"הוצא מן המעשה הזה את {TWO} עד הנה דבר המעשה אשר שמו ראובן"
        )
        c = check(source, registry=A12_REGISTRY)
        self.assertNotIn("PARSE0002", [d.code for d in c.diagnostics])
        self.assertIn("SEM0012", [d.code for d in c.diagnostics])

    def test_a11_performance_local_state_is_not_in_frozen_core(self):
        local = f"יהי במעשה הזה מקום ושמו לוי ובמקום אשר במעשה הזה שמו לוי יהי {THREE} לבדו"
        self.assertEqual(parse(local, registry=A12_REGISTRY, start_lhs="BodyAtomicAction").forest.alternatives, ())

    def test_named_role_surface_remains_non_positional(self):
        source = (
            f"עשה את המעשה אשר שמו ראובן בהיות {THREE} תחת הדבר אשר במעשה אשר שמו ראובן שמו שמעון"
        )
        c = check(source, registry=A12_REGISTRY)
        codes = [d.code for d in c.diagnostics]
        self.assertNotIn("PARSE0002", codes)
        self.assertNotIn("REF0014", codes)
        self.assertNotIn("SEM0001", codes)

    def test_b11_closes_all_a12_reusable_act_semantic_gates(self):
        expected = {
            "A10.NAMED_ACT_PERFORMANCE",
            "A11.INPUT_ROLE",
            "A11.ROLE_ASSOCIATION",
            "A11.CURRENT_PERFORMANCE",
            "A12.BODY_SCOPE",
            "A12.RESULT_PRODUCTION",
            "A12.IMMEDIATE_RESULT_REFERENCE",
        }
        gates = {g.construction_id: g for g in A12_REGISTRY.semantic_gates if g.construction_id in expected}
        self.assertEqual(set(gates), expected)
        self.assertTrue(all(g.status is SemanticReadiness.READY for g in gates.values()))

    def test_b11_mapped_body_no_longer_receives_sem0001(self):
        source = "זה דבר המעשה אשר שמו ראובן הוצא מן המעשה הזה את המספר אשר הוא אחד עד הנה דבר המעשה אשר שמו ראובן"
        c = check(source, registry=A12_REGISTRY)
        codes = [d.code for d in c.diagnostics]
        self.assertNotIn("PARSE0002", codes)
        self.assertNotIn("SEM0001", codes)
        self.assertNotIn("SEM0012", codes)

    def test_upstream_a12_adversarial_fixture_matrix(self):
        fixture_path = ROOT / "tests" / "fixtures" / "a12" / "A12_ADVERSARIAL_FIXTURES.json"
        data = json.loads(fixture_path.read_text(encoding="utf-8"))
        lhs_by_positive = {3: "NumberValue", 4: "NumberValue", 5: "Proposition", 8: "BodyAtomicAction"}
        for index, source in enumerate(data["positive"], 1):
            with self.subTest(kind="positive", index=index):
                parsed = parse(source, registry=A12_REGISTRY, start_lhs=lhs_by_positive.get(index))
                self.assertTrue(parsed.forest.alternatives)
        for case in data["negative"]:
            with self.subTest(kind="negative", case=case["id"]):
                parsed = parse(case["source"], registry=A12_REGISTRY)
                checked = check(case["source"], registry=A12_REGISTRY)
                rejected = (not parsed.forest.alternatives) or any(
                    d.code in {"REF0021", "SEM0012", "REF0014", "REF0016"}
                    for d in checked.diagnostics
                )
                self.assertTrue(rejected, (case["id"], checked.diagnostics))


if __name__ == "__main__":
    unittest.main()
