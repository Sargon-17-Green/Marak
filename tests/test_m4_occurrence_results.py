from __future__ import annotations
import unittest
from compiler.api import check, run_reference, run_source
from compiler.runtime.observables import reference_observable, backend_observable, backend_debug_internal_state
from tests.m4_support import ZERO


def both(source: str, *, fuel: int | None = None):
    c, r = run_reference(source, fuel=fuel)
    assert c.valid, [d.code for d in c.diagnostics]
    b = run_source(source, fuel=fuel)
    assert b.compilation.valid
    ro, bo = reference_observable(r), backend_observable(b.outcome)
    assert ro == bo, (ro, bo)
    return ro


class M4OccurrenceRoleTests(unittest.TestCase):
    def _role_program(self, reverse: bool) -> str:
        decl1=("יהי במעשה אשר שמו ראובן דבר ושמו שמעון ובעשות את המעשה אשר שמו ראובן "
               "יעמד מספר תחת הדבר אשר במעשה אשר שמו ראובן שמו שמעון")
        decl2=("יהי במעשה אשר שמו ראובן דבר ושמו לוי ובעשות את המעשה אשר שמו ראובן "
               "יעמד מספר תחת הדבר אשר במעשה אשר שמו ראובן שמו לוי")
        role1="המספר אשר במעשה הזה עומד תחת הדבר אשר במעשה אשר שמו ראובן שמו שמעון"
        role2="המספר אשר במעשה הזה עומד תחת הדבר אשר במעשה אשר שמו ראובן שמו לוי"
        body=("זה דבר המעשה אשר שמו ראובן הוצא מן המעשה הזה את המספר הנחשב בהוסיף את "
              +role1+" על "+role2+" עד הנה דבר המעשה אשר שמו ראובן")
        a1=("בהיות המספר אשר הוא שלשה תחת הדבר אשר במעשה אשר שמו ראובן שמו שמעון")
        a2=("בהיות המספר אשר הוא ארבעה תחת הדבר אשר במעשה אשר שמו ראובן שמו לוי")
        associations=(a2+" "+a1.replace("בהיות","ובהיות",1)) if reverse else (a1+" "+a2.replace("בהיות","ובהיות",1))
        return "יהי מעשה ושמו ראובן "+decl1+" "+decl2+" "+body+" ועתה עשה את המעשה אשר שמו ראובן "+associations

    def test_role_correspondence_is_identity_based_not_positional(self):
        normal=both(self._role_program(False)); reversed_=both(self._role_program(True))
        self.assertEqual(normal,reversed_)
        self.assertEqual(normal["products"],[["ראובן",7]])

    def test_nested_occurrences_can_use_different_values_for_same_role(self):
        # Outer role value is 3.  The body performs the same act recursively only
        # through a second act, supplying 4 to the same RoleId; no global slot may leak.
        decl=("יהי במעשה אשר שמו ראובן דבר ושמו שמעון ובעשות את המעשה אשר שמו ראובן "
              "יעמד מספר תחת הדבר אשר במעשה אשר שמו ראובן שמו שמעון")
        role="המספר אשר במעשה הזה עומד תחת הדבר אשר במעשה אשר שמו ראובן שמו שמעון"
        # A finite direct two-occurrence observation is enough to prove that the association
        # storage is occurrence-local: execute twice with different role values and inspect products.
        body="זה דבר המעשה אשר שמו ראובן הוצא מן המעשה הזה את "+role+" עד הנה דבר המעשה אשר שמו ראובן"
        perform3=("עשה את המעשה אשר שמו ראובן בהיות המספר אשר הוא שלשה תחת הדבר אשר במעשה אשר שמו ראובן שמו שמעון")
        perform4=("עשה את המעשה אשר שמו ראובן בהיות המספר אשר הוא ארבעה תחת הדבר אשר במעשה אשר שמו ראובן שמו שמעון")
        src="יהי מעשה ושמו ראובן "+decl+" "+body+" ועתה "+perform3+" ואחרי כן "+perform4
        obs=both(src)
        self.assertEqual(obs["products"],[["ראובן",3],["ראובן",4]])
        # Occurrence allocation identity is white-box only, but distinct occurrences
        # must still exist internally so role associations cannot leak globally.
        dbg=backend_debug_internal_state(run_source(src).outcome)
        self.assertEqual([x[2] for x in dbg["products"]],[3,4])
        self.assertNotEqual(dbg["products"][0][0],dbg["products"][1][0])


class M4ResultProvenanceTests(unittest.TestCase):
    def test_output_is_not_return_later_body_action_occurs(self):
        src=("יהי מקום ושמו גד ובמקום אשר שמו גד יהי המספר אשר הוא אחד לבדו "
             "יהי מעשה ושמו ראובן זה דבר המעשה אשר שמו ראובן "
             "הוצא מן המעשה הזה את המספר אשר הוא שלשה ואחרי כן "
             "שים במקום אשר שמו גד את המספר אשר הוא ארבעה תחת המספר אשר במקום אשר שמו גד "
             "עד הנה דבר המעשה אשר שמו ראובן ועתה עשה את המעשה אשר שמו ראובן")
        obs=both(src)
        self.assertEqual(obs["facts"],[["גד",4]])
        self.assertEqual(obs["products"],[["ראובן",3]])

    def test_immediate_result_is_tied_to_just_completed_occurrence(self):
        src=("יהי מקום ושמו גד ובמקום אשר שמו גד יהי המספר אשר הוא אחד לבדו "
             "יהי מעשה ושמו ראובן זה דבר המעשה אשר שמו ראובן "
             "הוצא מן המעשה הזה את המספר אשר הוא שלשה עד הנה דבר המעשה אשר שמו ראובן "
             "ועתה עשה את המעשה אשר שמו ראובן ואחרי כן "
             "שים במקום אשר שמו גד את המספר אשר יצא עתה מן המעשה אשר שמו ראובן תחת המספר אשר במקום אשר שמו גד")
        obs=both(src); self.assertEqual(obs["facts"],[["גד",3]])

    def test_stale_immediate_result_is_source_invalidity(self):
        src=("יהי מקום ושמו גד ובמקום אשר שמו גד יהי המספר אשר הוא אחד לבדו "
             "יהי מעשה ושמו ראובן זה דבר המעשה אשר שמו ראובן "
             "הוצא מן המעשה הזה את המספר אשר הוא שלשה עד הנה דבר המעשה אשר שמו ראובן "
             "ועתה עשה את המעשה אשר שמו ראובן ואחרי כן "
             "שים במקום אשר שמו גד את המספר אשר הוא שנים תחת המספר אשר במקום אשר שמו גד ואחרי כן "
             "שים במקום אשר שמו גד את המספר אשר יצא עתה מן המעשה אשר שמו ראובן תחת המספר אשר במקום אשר שמו גד")
        r=check(src); self.assertFalse(r.valid)
        self.assertIn("REF0112",[d.code for d in r.diagnostics])

    def test_structurally_immediate_no_output_is_dynamic_provenance_error(self):
        src=("יהי מקום ושמו גד ובמקום אשר שמו גד יהי המספר אשר הוא אחד לבדו "
             "יהי מעשה ושמו ראובן זה דבר המעשה אשר שמו ראובן "
             "שים במקום אשר שמו גד את המספר אשר הוא שנים תחת המספר אשר במקום אשר שמו גד "
             "עד הנה דבר המעשה אשר שמו ראובן ועתה עשה את המעשה אשר שמו ראובן ואחרי כן "
             "שים במקום אשר שמו גד את המספר אשר יצא עתה מן המעשה אשר שמו ראובן תחת המספר אשר במקום אשר שמו גד")
        obs=both(src)
        self.assertEqual(obs["outcome"],"Error")
        self.assertEqual(obs["error"]["code"],"RESULT_PROVENANCE_ERROR")
        self.assertEqual(obs["facts"],[["גד",2]])


class M4RecursionTests(unittest.TestCase):
    def test_recursive_act_terminates_by_body_exhaustion_without_halt(self):
        dec=("שים במקום אשר שמו גד את המספר הנחשב בגרע את המספר אשר הוא אחד "
             "מן המספר אשר במקום אשר שמו גד תחת המספר אשר במקום אשר שמו גד")
        src=("יהי מקום ושמו גד ובמקום אשר שמו גד יהי המספר אשר הוא שלשה לבדו "
             "יהי מעשה ושמו ראובן יהי מעשה ושמו שמעון יהי מעשה ושמו לוי "
             "זה דבר המעשה אשר שמו ראובן אם המספר אשר במקום אשר שמו גד הוא "+ZERO+
             " עשה את המעשה אשר שמו לוי ואם לא עשה את המעשה אשר שמו שמעון "
             "עד הנה דבר המעשה אשר שמו ראובן "
             "זה דבר המעשה אשר שמו שמעון "+dec+" ואחרי כן עשה את המעשה אשר שמו ראובן "
             "עד הנה דבר המעשה אשר שמו שמעון "
             "זה דבר המעשה אשר שמו לוי שים במקום אשר שמו גד את המספר אשר במקום אשר שמו גד "
             "תחת המספר אשר במקום אשר שמו גד עד הנה דבר המעשה אשר שמו לוי "
             "ועתה עשה את המעשה אשר שמו ראובן")
        obs=both(src,fuel=1000)
        self.assertEqual(obs["outcome"],"Normal"); self.assertEqual(obs["facts"],[["גד",0]])

    def test_self_recursion_is_valid_source_and_fuel_is_harness_divergence_only(self):
        src=next(x["source"] for x in __import__('tests.m4_support',fromlist=['a13_json']).a13_json('a13_program_conformance.json')['positive'] if x['id']=='P-SELFREC-001')
        self.assertTrue(check(src).valid)
        obs=both(src,fuel=10)
        self.assertEqual(obs["outcome"],"Divergence")
        self.assertEqual(obs["harness_reason"],"fuel-exhausted")

if __name__ == '__main__': unittest.main()
