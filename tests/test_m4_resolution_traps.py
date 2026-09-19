from __future__ import annotations
import unittest
from compiler.api import check, run_reference, run_source
from compiler.runtime.observables import reference_observable, backend_observable
from tests.m4_support import a13_json

class M4NameVisibilityTrapTests(unittest.TestCase):
    def test_self_initializer_rejected(self):
        src=("יהי מקום ושמו גד ובמקום אשר שמו גד יהי המספר אשר במקום אשר שמו גד לבדו "
             "ועתה שים במקום אשר שמו גד את המספר אשר הוא אחד תחת המספר אשר במקום אשר שמו גד")
        r=check(src); self.assertFalse(r.valid); self.assertIn("REF0106",[d.code for d in r.diagnostics])

    def test_earlier_place_initializer_reference_allowed(self):
        src=("יהי מקום ושמו גד ובמקום אשר שמו גד יהי המספר אשר הוא שנים לבדו "
             "יהי מקום ושמו עזר ובמקום אשר שמו עזר יהי המספר אשר במקום אשר שמו גד לבדו "
             "ועתה שים במקום אשר שמו עזר את המספר אשר במקום אשר שמו עזר תחת המספר אשר במקום אשר שמו עזר")
        r=check(src); self.assertTrue(r.valid,[d.code for d in r.diagnostics])
        obs=reference_observable(run_reference(src)[1]); self.assertEqual(obs["facts"],[["גד",2],["עזר",2]])
        self.assertEqual(obs,backend_observable(run_source(src).outcome))

    def test_duplicate_act_rejected(self):
        src=("יהי מעשה ושמו ראובן יהי מעשה ושמו ראובן "
             "זה דבר המעשה אשר שמו ראובן עשה את המעשה אשר שמו ראובן עד הנה דבר המעשה אשר שמו ראובן "
             "ועתה עשה את המעשה אשר שמו ראובן")
        r=check(src); self.assertFalse(r.valid); self.assertIn("REF0103",[d.code for d in r.diagnostics])

    def test_duplicate_body_rejected(self):
        body="זה דבר המעשה אשר שמו ראובן עשה את המעשה אשר שמו ראובן עד הנה דבר המעשה אשר שמו ראובן"
        src="יהי מעשה ושמו ראובן "+body+" "+body+" ועתה עשה את המעשה אשר שמו ראובן"
        r=check(src); self.assertFalse(r.valid); self.assertIn("REF0105",[d.code for d in r.diagnostics])

    def test_no_hoisting_even_if_compiler_can_prescan(self):
        x=next(x for x in a13_json("a13_program_conformance.json")["negative"] if x["id"]=="N-FWD-ACT-001")
        r=check(x["source"]); self.assertFalse(r.valid); self.assertIn("REF0101",[d.code for d in r.diagnostics])

    def test_no_halt_surface_construction(self):
        x=next(x for x in a13_json("a13_program_conformance.json")["negative"] if x["id"]=="N-HALT-001")
        r=check(x["source"]); self.assertFalse(r.valid); self.assertIn("PARSE0002",[d.code for d in r.diagnostics])

    def test_main_trap_act_name_has_no_entry_magic(self):
        src=("יהי מקום ושמו גד ובמקום אשר שמו גד יהי המספר אשר הוא אחד לבדו "
             "יהי מעשה ושמו ראשי יהי מעשה ושמו שמעון "
             "זה דבר המעשה אשר שמו ראשי שים במקום אשר שמו גד את המספר אשר הוא שנים תחת המספר אשר במקום אשר שמו גד עד הנה דבר המעשה אשר שמו ראשי "
             "זה דבר המעשה אשר שמו שמעון שים במקום אשר שמו גד את המספר אשר במקום אשר שמו גד תחת המספר אשר במקום אשר שמו גד עד הנה דבר המעשה אשר שמו שמעון "
             "ועתה עשה את המעשה אשר שמו שמעון")
        r=check(src); self.assertTrue(r.valid,[d.code for d in r.diagnostics])
        obs=reference_observable(run_reference(src)[1]); self.assertEqual(obs["facts"],[["גד",1]])

    def test_preparation_after_entry_has_specific_program_diagnostic(self):
        x=next(x for x in a13_json("a13_program_conformance.json")["negative"] if x["id"]=="N-DEFINITION-AFTER-ENTRY-001")
        r=check(x["source"]); self.assertIn("PROG0003",[d.code for d in r.diagnostics])

if __name__=='__main__': unittest.main()
