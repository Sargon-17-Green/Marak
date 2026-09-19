import json
from pathlib import Path
import unittest

from compiler.api import check, parse
from compiler.parse.a8_registry import A8_REGISTRY
from compiler.parse.grammar import NameTerminal

ROOT = Path(__file__).resolve().parents[1]


class A8RegistryTests(unittest.TestCase):
    def test_snapshot_matches_code(self):
        disk = json.loads((ROOT / "spec" / "A8_CONSTRUCTION_REGISTRY.json").read_text(encoding="utf-8"))
        self.assertEqual(disk, A8_REGISTRY.to_dict())

    def test_explicit_name_slot_accepts_grammar_word_as_name(self):
        source = "עשה את המצוה אשר שמה עשה"
        result = parse(source, registry=A8_REGISTRY)
        self.assertEqual(len(result.forest.alternatives), 1)
        self.assertEqual(result.forest.alternatives[0].root.construction_id, "A8.REUSABLE_ACTION_PERFORMANCE")

    def test_bare_word_is_not_a_name_reference(self):
        result = parse("ראובן", registry=A8_REGISTRY)
        self.assertEqual(result.forest.alternatives, ())

    def test_two_calls_do_not_sequence_from_source_order_alone(self):
        result = parse(
            "עשה את המצוה אשר שמה ראובן עשה את המצוה אשר שמה שמעון",
            registry=A8_REGISTRY,
        )
        self.assertEqual(result.forest.alternatives, ())

    def test_overt_sequence_marker_parses_surface(self):
        result = parse(
            "עשה את המצוה אשר שמה ראובן ואחרי כן עשה את המצוה אשר שמה שמעון",
            registry=A8_REGISTRY,
        )
        self.assertEqual(len(result.forest.alternatives), 1)
        self.assertEqual(result.forest.alternatives[0].root.construction_id, "A2.EXPLICIT_SEQUENCE")

    def test_counted_repeat_parses_surface(self):
        result = parse("שלש פעמים עשה את המצוה אשר שמה ראובן", registry=A8_REGISTRY)
        self.assertEqual(len(result.forest.alternatives), 1)
        self.assertEqual(result.forest.alternatives[0].root.construction_id, "A3.COUNTED_ATOMIC_REPEAT")

    def test_normative_surface_parse_is_semantically_blocked_by_b6(self):
        result = check("עשה את המצוה אשר שמה ראובן", registry=A8_REGISTRY)
        self.assertFalse(result.valid)
        self.assertEqual([d.code for d in result.diagnostics], ["SEM0001"])
        meta = result.diagnostics[0].metadata
        self.assertTrue(meta["surface_parse_preserved"])
        self.assertTrue(meta["reference_model_not_normative"])
        self.assertEqual(meta["blocked_constructions"][0]["construction_id"], "A8.REUSABLE_ACTION_PERFORMANCE")

    def test_name_terminal_is_open_class_slot_not_identifier_lexer(self):
        prods = [p for p in A8_REGISTRY.productions if p.construction_id == "A8.REUSABLE_ACTION_PERFORMANCE"]
        self.assertTrue(any(any(isinstance(s, NameTerminal) for s in p.rhs) for p in prods))


if __name__ == "__main__":
    unittest.main()
