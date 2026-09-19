import json
from pathlib import Path
import unittest

from compiler.api import check, parse
from compiler.parse.a10_registry import A10_REGISTRY

ROOT = Path(__file__).resolve().parents[1]
THREE = "המספר אשר הוא שלשה"
FOUR = "המספר אשר הוא ארבעה"


class A10RegistryTests(unittest.TestCase):
    def test_snapshot_matches_code(self):
        disk = json.loads((ROOT / "spec" / "A10_CONSTRUCTION_REGISTRY.json").read_text(encoding="utf-8"))
        self.assertEqual(disk, A10_REGISTRY.to_dict())

    def test_a8_mitzvah_performance_is_superseded(self):
        self.assertEqual(parse("עשה את המצוה אשר שמה ראובן", registry=A10_REGISTRY).forest.alternatives, ())

    def test_named_act_identity_fragment(self):
        r = parse("יהי מעשה ושמו ראובן", registry=A10_REGISTRY, start_lhs="NamedActIdentity")
        self.assertEqual(len(r.forest.alternatives), 1)

    def test_named_act_performance_parses_but_semantics_remains_gated(self):
        source = "עשה את המעשה אשר שמו ראובן"
        r = parse(source, registry=A10_REGISTRY)
        self.assertEqual(len(r.forest.alternatives), 1)
        c = check(source, registry=A10_REGISTRY)
        self.assertIn("SEM0001", [d.code for d in c.diagnostics])

    def test_current_place_number_is_explicit_value_fragment(self):
        r = parse("המספר אשר במקום אשר שמו ראובן", registry=A10_REGISTRY, start_lhs="NumberValue")
        self.assertEqual(len(r.forest.alternatives), 1)
        self.assertEqual(r.forest.alternatives[0].root.construction_id, "A10.NAMED_PLACE_STATE")

    def test_normative_state_introduction_fixture_parses(self):
        source = "יהי מקום ושמו ראובן ובמקום אשר שמו ראובן יהי המספר אשר הוא שלשה לבדו"
        r = parse(source, registry=A10_REGISTRY)
        self.assertEqual(len(r.forest.alternatives), 1)
        self.assertEqual(r.forest.alternatives[0].root.construction_id, "A10.PLACE_INTRODUCTION")

    def test_state_introduction_requires_explicit_same_place_name(self):
        source = "יהי מקום ושמו ראובן ובמקום אשר שמו שמעון יהי המספר אשר הוא שלשה לבדו"
        c = check(source, registry=A10_REGISTRY)
        self.assertIn("REF0001", [d.code for d in c.diagnostics])

    def test_normative_replacement_fixture_parses(self):
        source = "שים במקום אשר שמו ראובן את המספר אשר הוא ארבעה תחת המספר אשר במקום אשר שמו ראובן"
        r = parse(source, registry=A10_REGISTRY)
        self.assertEqual(len(r.forest.alternatives), 1)
        self.assertEqual(r.forest.alternatives[0].root.construction_id, "A10.PLACE_REPLACEMENT")

    def test_replacement_different_named_places_is_rejected_by_resolution_constraint(self):
        source = "שים במקום אשר שמו ראובן את המספר אשר הוא ארבעה תחת המספר אשר במקום אשר שמו שמעון"
        c = check(source, registry=A10_REGISTRY)
        self.assertIn("REF0001", [d.code for d in c.diagnostics])

    def test_after_gated_recurrence_parses_with_one_atomic_action(self):
        zero = "המספר הנחשב בגרע את המספר אשר הוא אחד מן המספר אשר הוא אחד"
        source = f"עשה את המעשה אשר שמו ראובן וכן תעשה עד אשר {zero} הוא {zero}"
        r = parse(source, registry=A10_REGISTRY)
        self.assertEqual(len(r.forest.alternatives), 1)
        self.assertEqual(r.forest.alternatives[0].root.construction_id, "A10.AFTER_GATED_RECURRENCE")
        # recurrence semantics itself is ready; the nested act model is what gates check.
        c = check(source, registry=A10_REGISTRY)
        blocked = [d for d in c.diagnostics if d.code == "SEM0001"]
        self.assertEqual(len(blocked), 1)
        ids = {x["construction_id"] for x in blocked[0].metadata["blocked_constructions"]}
        self.assertIn("A10.NAMED_ACT_PERFORMANCE", ids)
        self.assertNotIn("A10.AFTER_GATED_RECURRENCE", ids)

    def test_bare_until_and_unpointed_עשה_variant_do_not_parse(self):
        zero = "המספר הנחשב בגרע את המספר אשר הוא אחד מן המספר אשר הוא אחד"
        self.assertEqual(parse(f"עשה את המעשה אשר שמו ראובן עד אשר {zero} הוא {zero}", registry=A10_REGISTRY).forest.alternatives, ())
        self.assertEqual(parse(f"עשה את המעשה אשר שמו ראובן וכן עשה עד אשר {zero} הוא {zero}", registry=A10_REGISTRY).forest.alternatives, ())


if __name__ == "__main__":
    unittest.main()
