import json
from pathlib import Path
import unittest

from compiler.api import check, parse
from compiler.parse.a11_registry import A11_REGISTRY

ROOT = Path(__file__).resolve().parents[1]
THREE = "המספר אשר הוא שלשה"
FOUR = "המספר אשר הוא ארבעה"


class A11RegistryTests(unittest.TestCase):
    def test_snapshot_matches_code(self):
        disk = json.loads((ROOT / "spec" / "A11_CONSTRUCTION_REGISTRY.json").read_text(encoding="utf-8"))
        self.assertEqual(disk, A11_REGISTRY.to_dict())

    def test_named_act_identity_is_complete_top_level_unit(self):
        c = check("יהי מעשה ושמו ראובן", registry=A11_REGISTRY)
        self.assertTrue(c.valid)
        self.assertEqual(len(c.forest.alternatives), 1)

    def test_body_scope_parses_and_is_semantically_gated(self):
        source = "אלה דברי המעשה אשר שמו ראובן עשה את המעשה אשר שמו שמעון עד הנה דברי המעשה אשר שמו ראובן"
        c = check(source, registry=A11_REGISTRY)
        self.assertIn("SEM0001", [d.code for d in c.diagnostics])
        self.assertNotIn("PARSE0002", [d.code for d in c.diagnostics])

    def test_mismatched_body_closer_is_not_nearest_body_repaired(self):
        source = "אלה דברי המעשה אשר שמו ראובן עשה את המעשה אשר שמו שמעון עד הנה דברי המעשה אשר שמו יהודה"
        c = check(source, registry=A11_REGISTRY)
        self.assertIn("REF0011", [d.code for d in c.diagnostics])

    def test_named_role_declaration_parses_without_positional_model(self):
        source = (
            "יהי במעשה אשר שמו ראובן דבר ושמו שמעון ובעשות את המעשה אשר שמו ראובן "
            "יעמד מספר תחת הדבר אשר במעשה אשר שמו ראובן שמו שמעון"
        )
        c = check(source, registry=A11_REGISTRY)
        self.assertIn("SEM0001", [d.code for d in c.diagnostics])
        self.assertNotIn("PARSE0002", [d.code for d in c.diagnostics])

    def test_role_declaration_requires_explicit_owner_and_role_coreference(self):
        owner_bad = (
            "יהי במעשה אשר שמו ראובן דבר ושמו שמעון ובעשות את המעשה אשר שמו יהודה "
            "יעמד מספר תחת הדבר אשר במעשה אשר שמו ראובן שמו שמעון"
        )
        role_bad = (
            "יהי במעשה אשר שמו ראובן דבר ושמו שמעון ובעשות את המעשה אשר שמו ראובן "
            "יעמד מספר תחת הדבר אשר במעשה אשר שמו ראובן שמו יהודה"
        )
        self.assertIn("REF0012", [d.code for d in check(owner_bad, registry=A11_REGISTRY).diagnostics])
        self.assertIn("REF0013", [d.code for d in check(role_bad, registry=A11_REGISTRY).diagnostics])

    def test_role_association_is_by_explicit_name_not_position(self):
        source = (
            f"עשה את המעשה אשר שמו ראובן בהיות {THREE} תחת הדבר אשר במעשה אשר שמו ראובן שמו שמעון"
        )
        c = check(source, registry=A11_REGISTRY)
        self.assertIn("SEM0001", [d.code for d in c.diagnostics])
        self.assertNotIn("REF0014", [d.code for d in c.diagnostics])

    def test_role_association_owner_mismatch_and_duplicate_role_are_rejected(self):
        owner_bad = (
            f"עשה את המעשה אשר שמו ראובן בהיות {THREE} תחת הדבר אשר במעשה אשר שמו יהודה שמו שמעון"
        )
        duplicate = (
            f"עשה את המעשה אשר שמו ראובן בהיות {THREE} תחת הדבר אשר במעשה אשר שמו ראובן שמו שמעון "
            f"ובהיות {FOUR} תחת הדבר אשר במעשה אשר שמו ראובן שמו שמעון"
        )
        self.assertIn("REF0014", [d.code for d in check(owner_bad, registry=A11_REGISTRY).diagnostics])
        self.assertIn("REF0016", [d.code for d in check(duplicate, registry=A11_REGISTRY).diagnostics])

    def test_result_production_is_body_only_and_not_top_level_root(self):
        source = f"הוצא מן המעשה הזה את {THREE}"
        self.assertEqual(parse(source, registry=A11_REGISTRY).forest.alternatives, ())
        r = parse(source, registry=A11_REGISTRY, start_lhs="BodyAtomicAction")
        self.assertEqual(len(r.forest.alternatives), 1)

    def test_result_production_does_not_end_body(self):
        source = (
            f"אלה דברי המעשה אשר שמו ראובן הוצא מן המעשה הזה את {THREE} ואחרי כן "
            "עשה את המעשה אשר שמו שמעון עד הנה דברי המעשה אשר שמו ראובן"
        )
        r = parse(source, registry=A11_REGISTRY)
        self.assertEqual(len(r.forest.alternatives), 1)

    def test_immediate_result_reference_requires_atah(self):
        good = "המספר אשר יצא עתה מן המעשה אשר שמו ראובן"
        old_a10 = "המספר אשר יצא מן המעשה אשר שמו ראובן"
        self.assertEqual(len(parse(good, registry=A11_REGISTRY, start_lhs="NumberValue").forest.alternatives), 1)
        self.assertEqual(parse(old_a10, registry=A11_REGISTRY, start_lhs="NumberValue").forest.alternatives, ())

    def test_multiple_result_ordinal_forms_are_explicit(self):
        first = "המספר הראשון אשר יצא עתה מן המעשה אשר שמו ראובן"
        second = "המספר השני אשר יצא עתה מן המעשה אשר שמו ראובן"
        self.assertEqual(len(parse(first, registry=A11_REGISTRY, start_lhs="NumberValue").forest.alternatives), 1)
        self.assertEqual(len(parse(second, registry=A11_REGISTRY, start_lhs="NumberValue").forest.alternatives), 1)

    def test_performance_owned_local_state_is_body_only(self):
        local = f"יהי במעשה הזה מקום ושמו לוי ובמקום אשר במעשה הזה שמו לוי יהי {THREE} לבדו"
        self.assertEqual(parse(local, registry=A11_REGISTRY).forest.alternatives, ())
        self.assertEqual(len(parse(local, registry=A11_REGISTRY, start_lhs="BodyAtomicAction").forest.alternatives), 1)

    def test_local_place_mismatch_is_rejected(self):
        source = (
            f"אלה דברי המעשה אשר שמו ראובן יהי במעשה הזה מקום ושמו לוי "
            f"ובמקום אשר במעשה הזה שמו יהודה יהי {THREE} לבדו עד הנה דברי המעשה אשר שמו ראובן"
        )
        self.assertIn("REF0017", [d.code for d in check(source, registry=A11_REGISTRY).diagnostics])

    def test_current_role_value_is_not_bare_role_dereference(self):
        source = "המספר אשר במעשה הזה עומד תחת הדבר אשר במעשה אשר שמו ראובן שמו שמעון"
        self.assertEqual(len(parse(source, registry=A11_REGISTRY, start_lhs="NumberValue").forest.alternatives), 1)
        self.assertEqual(parse("שמעון", registry=A11_REGISTRY, start_lhs="NumberValue").forest.alternatives, ())


if __name__ == "__main__":
    unittest.main()
