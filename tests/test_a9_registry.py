import json
from pathlib import Path
import unittest

from compiler.api import check, parse
from compiler.parse.a9_registry import A9_REGISTRY

ROOT = Path(__file__).resolve().parents[1]
ONE = "המספר אשר הוא אחד"
ZERO = "המספר הנחשב בגרע את המספר אשר הוא אחד מן המספר אשר הוא אחד"


class A9RegistryTests(unittest.TestCase):
    def test_snapshot_matches_code(self):
        disk = json.loads((ROOT / "spec" / "A9_CONSTRUCTION_REGISTRY.json").read_text(encoding="utf-8"))
        self.assertEqual(disk, A9_REGISTRY.to_dict())

    def test_a8_reusable_action_is_not_currently_admitted(self):
        result = parse("עשה את המצוה אשר שמה ראובן", registry=A9_REGISTRY)
        self.assertEqual(result.forest.alternatives, ())
        self.assertNotIn(
            "A8.REUSABLE_ACTION_PERFORMANCE",
            {d.construction_id for d in A9_REGISTRY.declarations},
        )

    def test_literal_one_can_be_parsed_as_number_fragment_without_becoming_program_root(self):
        fragment = parse(ONE, registry=A9_REGISTRY, start_lhs="NumberValue")
        self.assertEqual(len(fragment.forest.alternatives), 1)
        self.assertEqual(fragment.forest.alternatives[0].root.symbol, "NumberValue")
        whole = check(ONE, registry=A9_REGISTRY)
        self.assertFalse(whole.valid)
        self.assertEqual([d.code for d in whole.diagnostics], ["PARSE0002"])

    def test_derived_zero_uses_stable_subtraction_frame(self):
        fragment = parse(ZERO, registry=A9_REGISTRY, start_lhs="NumberValue")
        self.assertEqual(len(fragment.forest.alternatives), 1)
        self.assertEqual(fragment.forest.alternatives[0].root.construction_id, "A9.PURE_SUBTRACTION_FRAME")

    def test_recursive_pure_addition_frame(self):
        source = f"המספר הנחשב בהוסיף את {ZERO} על {ONE}"
        fragment = parse(source, registry=A9_REGISTRY, start_lhs="NumberValue")
        self.assertEqual(len(fragment.forest.alternatives), 1)
        self.assertEqual(fragment.forest.alternatives[0].root.construction_id, "A9.PURE_ADDITION_FRAME")

    def test_numeric_identity_is_proposition_not_boolean_value(self):
        source = f"{ZERO} הוא {ZERO}"
        fragment = parse(source, registry=A9_REGISTRY, start_lhs="Proposition")
        self.assertEqual(len(fragment.forest.alternatives), 1)
        self.assertEqual(fragment.forest.alternatives[0].root.symbol, "Proposition")

    def test_paired_conditional_shell_is_present_but_cannot_invent_consequence_leaf(self):
        roots = {p.production_id for p in A9_REGISTRY.admitted_root_productions}
        self.assertIn("A9.CONDITIONAL.PAIRED", roots)
        source = f"אם {ZERO} הוא {ZERO} עשה דבר ואם לא עשה דבר"
        result = parse(source, registry=A9_REGISTRY)
        self.assertEqual(result.forest.alternatives, ())
        self.assertIsNotNone(result.parse_result.failure)

    def test_arbitrary_9999_ceiling_is_not_encoded(self):
        number_productions = [p for p in A9_REGISTRY.productions if p.lhs == "NumberValue"]
        self.assertFalse(any(getattr(sym, "text", None) == "תשעתאלפים" for p in number_productions for sym in p.rhs))
        self.assertEqual({p.production_id for p in number_productions}, {
            "A9.NUMBER.LITERAL.ONE", "A9.NUMBER.ADD", "A9.NUMBER.SUBTRACT"
        })


if __name__ == "__main__":
    unittest.main()
