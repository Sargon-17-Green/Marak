from __future__ import annotations
import unittest
from compiler.api import check, run_reference, run_source
from compiler.models.hast import HastEqualProposition, HastNumber
from compiler.runtime.observables import backend_observable, reference_observable
from tests.m4_support import a13_json, ZERO

class M4ResolutionTests(unittest.TestCase):
    def test_same_spelling_across_place_and_act_has_distinct_typed_ids(self):
        src=("יהי מקום ושמו ראובן ובמקום אשר שמו ראובן יהי המספר אשר הוא אחד לבדו "
             "יהי מעשה ושמו ראובן זה דבר המעשה אשר שמו ראובן "
             "שים במקום אשר שמו ראובן את המספר אשר הוא שנים תחת המספר אשר במקום אשר שמו ראובן "
             "עד הנה דבר המעשה אשר שמו ראובן ועתה עשה את המעשה אשר שמו ראובן")
        r=check(src); self.assertTrue(r.valid,[d.code for d in r.diagnostics])
        self.assertEqual(r.hast.places[0].spelling,"ראובן")
        self.assertEqual(r.hast.acts[0].spelling,"ראובן")
        self.assertNotEqual(r.hast.places[0].serial,r.hast.acts[0].serial)

    def test_a13_negative_resolution_cases_have_no_hoisting(self):
        data={x["id"]:x for x in a13_json("a13_program_conformance.json")["negative"]}
        for key in ("N-REF-BEFORE-INTRO-001","N-FWD-ACT-001"):
            r=check(data[key]["source"])
            self.assertFalse(r.valid)
            self.assertIn("REF0101",[d.code for d in r.diagnostics])

    def test_mutual_recursion_only_after_prior_introductions(self):
        data={x["id"]:x for x in a13_json("a13_program_conformance.json")["positive"]}
        self.assertTrue(check(data["P-MUTUAL-001"]["source"]).valid)

    def test_duplicate_same_kind_rejected(self):
        data={x["id"]:x for x in a13_json("a13_program_conformance.json")["negative"]}
        self.assertIn("REF0102",[d.code for d in check(data["N-DUP-PLACE-001"]["source"]).diagnostics])
        self.assertIn("REF0104",[d.code for d in check(data["N-DUP-ROLE-001"]["source"]).diagnostics])

class M4NaturalRuntimeTests(unittest.TestCase):
    STATIC_UNDERFLOW=("יהי מקום ושמו גד ובמקום אשר שמו גד יהי המספר אשר הוא שלשה לבדו "
      "ועתה שים במקום אשר שמו גד את המספר הנחשב בגרע את המספר אשר הוא שלשה מן המספר אשר הוא שנים תחת המספר אשר במקום אשר שמו גד")
    DYNAMIC_UNDERFLOW=("יהי מקום ושמו גד ובמקום אשר שמו גד יהי המספר אשר הוא שנים לבדו "
      "יהי מקום ושמו עזר ובמקום אשר שמו עזר יהי המספר אשר הוא שלשה לבדו "
      "ועתה שים במקום אשר שמו גד את המספר הנחשב בגרע את המספר אשר במקום אשר שמו עזר מן המספר אשר במקום אשר שמו גד תחת המספר אשר במקום אשר שמו גד")

    def test_static_underflow_is_semantic_domain_diagnostic(self):
        r=check(self.STATIC_UNDERFLOW); self.assertFalse(r.valid)
        d=next(d for d in r.diagnostics if d.code=="SEM0201")
        self.assertEqual(d.metadata["semantic_code"],"ARITHMETIC_DOMAIN_ERROR")

    def test_dynamic_underflow_is_defined_runtime_error_and_destination_unchanged(self):
        c=check(self.DYNAMIC_UNDERFLOW); self.assertTrue(c.valid)
        _,ref=run_reference(self.DYNAMIC_UNDERFLOW); vm=run_source(self.DYNAMIC_UNDERFLOW).outcome
        self.assertEqual(reference_observable(ref),backend_observable(vm))
        obs=reference_observable(ref)
        self.assertEqual(obs["outcome"],"Error")
        self.assertEqual(obs["error"]["code"],"ARITHMETIC_DOMAIN_ERROR")
        self.assertEqual(obs["facts"],[["גד",2],["עזר",3]])

    def test_prior_effect_preserved_failed_replacement_uncommitted_later_suppressed(self):
        src=("יהי מקום ושמו גד ובמקום אשר שמו גד יהי המספר אשר הוא חמשה לבדו "
             "יהי מקום ושמו עזר ובמקום אשר שמו עזר יהי המספר אשר הוא שנים לבדו "
             "יהי מקום ושמו לוי ובמקום אשר שמו לוי יהי המספר אשר הוא שלשה לבדו "
             "ועתה שים במקום אשר שמו גד את המספר אשר הוא ארבעה תחת המספר אשר במקום אשר שמו גד "
             "ואחרי כן שים במקום אשר שמו עזר את המספר הנחשב בגרע את המספר אשר במקום אשר שמו לוי מן המספר אשר במקום אשר שמו עזר תחת המספר אשר במקום אשר שמו עזר "
             "ואחרי כן שים במקום אשר שמו גד את המספר אשר הוא אחד תחת המספר אשר במקום אשר שמו גד")
        _,ref=run_reference(src); obs=reference_observable(ref)
        self.assertEqual(obs["outcome"],"Error")
        self.assertEqual(obs["facts"],[["גד",4],["עזר",2],["לוי",3]])
        self.assertEqual(obs,backend_observable(run_source(src).outcome))

    def test_preparation_failure_prevents_principal_without_rollback_of_earlier_fact(self):
        src=("יהי מקום ושמו גד ובמקום אשר שמו גד יהי המספר אשר הוא שנים לבדו "
             "יהי מקום ושמו עזר ובמקום אשר שמו עזר יהי המספר הנחשב בגרע את המספר אשר הוא שלשה מן המספר אשר במקום אשר שמו גד לבדו "
             "ועתה שים במקום אשר שמו גד את המספר אשר הוא תשעה תחת המספר אשר במקום אשר שמו גד")
        self.assertTrue(check(src).valid)
        _,ref=run_reference(src); obs=reference_observable(ref)
        self.assertEqual(obs["outcome"],"Error"); self.assertEqual(obs["error"]["phase"],"PREPARATION")
        self.assertEqual(obs["facts"],[["גד",2]])
        self.assertEqual(obs,backend_observable(run_source(src).outcome))

    def test_conditional_does_not_execute_unselected_dynamic_failure(self):
        src=("יהי מקום ושמו גד ובמקום אשר שמו גד יהי המספר אשר הוא שנים לבדו "
             "יהי מקום ושמו עזר ובמקום אשר שמו עזר יהי המספר אשר הוא שלשה לבדו "
             "ועתה אם המספר אשר הוא אחד הוא המספר אשר הוא אחד "
             "שים במקום אשר שמו גד את המספר אשר הוא ארבעה תחת המספר אשר במקום אשר שמו גד "
             "ואם לא שים במקום אשר שמו גד את המספר הנחשב בגרע את המספר אשר במקום אשר שמו עזר מן המספר אשר במקום אשר שמו גד תחת המספר אשר במקום אשר שמו גד")
        r=check(src); self.assertTrue(r.valid,[d.code for d in r.diagnostics])
        obs=reference_observable(run_reference(src)[1])
        self.assertEqual(obs["outcome"],"Normal"); self.assertEqual(obs["facts"],[["גד",4],["עזר",3]])
        self.assertEqual(obs,backend_observable(run_source(src).outcome))

    def test_proposition_is_not_number_value(self):
        src=("יהי מקום ושמו גד ובמקום אשר שמו גד יהי המספר אשר הוא אחד לבדו "
             "ועתה אם המספר אשר הוא אחד הוא המספר אשר הוא אחד "
             "שים במקום אשר שמו גד את המספר אשר הוא שנים תחת המספר אשר במקום אשר שמו גד "
             "ואם לא שים במקום אשר שמו גד את המספר אשר הוא שלשה תחת המספר אשר במקום אשר שמו גד")
        r=check(src); self.assertTrue(r.valid)
        prop=r.hast.principal.proposition
        self.assertIsInstance(prop,HastEqualProposition)
        self.assertNotIsInstance(prop,HastNumber)

    def test_post_action_recurrence_executes_first_action_then_checks(self):
        dec=("שים במקום אשר שמו גד את המספר הנחשב בגרע את המספר אשר הוא אחד מן המספר אשר במקום אשר שמו גד תחת המספר אשר במקום אשר שמו גד")
        src=("יהי מקום ושמו גד ובמקום אשר שמו גד יהי המספר אשר הוא שלשה לבדו ועתה "+dec+" וכן תעשה עד אשר המספר אשר במקום אשר שמו גד הוא "+ZERO)
        r=check(src); self.assertTrue(r.valid,[d.code for d in r.diagnostics])
        obs=reference_observable(run_reference(src)[1]); self.assertEqual(obs["facts"],[["גד",0]])
        self.assertEqual(obs,backend_observable(run_source(src).outcome))

if __name__ == '__main__': unittest.main()
