from __future__ import annotations

import unittest

from compiler.api import check, run_reference, run_source
from compiler.ir_lower import lower_validated_hast
from compiler.runtime.ir_reference import execute_reference_ir
from compiler.runtime.observables import backend_observable, ir_reference_observable, reference_observable
from tests.m4_support import a13_json, role_sum_program, tiny_source


class M4IRReferenceTests(unittest.TestCase):
    def _triple(self, source: str, *, fuel: int | None = None):
        checked = check(source)
        self.assertTrue(checked.valid, [d.code for d in checked.diagnostics])
        ir = lower_validated_hast(checked.hast)
        hast_out = run_reference(source, fuel=fuel)[1]
        ir_out = execute_reference_ir(ir, fuel=fuel)
        backend_out = run_source(source, fuel=fuel).outcome
        return reference_observable(hast_out), ir_reference_observable(ir_out), backend_observable(backend_out)

    def test_tiny_rm_three_way_equivalence(self):
        hast, ir, backend = self._triple(tiny_source())
        self.assertEqual(hast, ir)
        self.assertEqual(ir, backend)
        self.assertEqual(ir["outcome"], "Normal")

    def test_role_correspondence_three_way_equivalence(self):
        a = self._triple(role_sum_program())
        b = self._triple(role_sum_program(reverse=True))
        self.assertEqual(a[0], a[1]); self.assertEqual(a[1], a[2])
        self.assertEqual(b[0], b[1]); self.assertEqual(b[1], b[2])
        self.assertEqual(a[0], b[0])

    def test_all_a13_positive_programs_three_way_equivalent_with_harness_fuel(self):
        for fixture in a13_json("a13_program_conformance.json")["positive"]:
            with self.subTest(fixture=fixture["id"]):
                h, i, b = self._triple(fixture["source"], fuel=200)
                self.assertEqual(h, i)
                self.assertEqual(i, b)

    def test_fuel_exhaustion_is_three_way_divergence_not_language_error(self):
        # Tiny RM needs more than one execution step.  Fuel is a harness control only.
        h, i, b = self._triple(tiny_source(), fuel=1)
        self.assertEqual(h["outcome"], "Divergence")
        self.assertEqual(h, i)
        self.assertEqual(i, b)
        self.assertNotIn("error", i)


if __name__ == "__main__":
    unittest.main()
