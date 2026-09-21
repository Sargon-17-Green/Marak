#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path
import unittest

from spec.proposals.b13.reference.b13_reference_model import (
    BidirectionalIndex, INDEX_DOMAIN, Natural, ProgramContract, ProgramInputId,
    bind_invocation, from_math_index, index_lt,
)
from spec.proposals.b15.reference.b15_reference_model import (
    Expr, State, PlaceContract, RoleContract, establish_place, replace_place, current_place,
    start_occurrence, resolve_output_contract, emit, complete_occurrence, read_immediate,
    InvalidProgram, UNRESOLVED_VALUE_DOMAIN,
)
from spec.proposals.b16.reference.b16_reference_model import *

ROOT=Path(__file__).resolve().parents[4]

def git_blob_sha(path:Path)->str:
    raw=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

class B16SemanticTests(unittest.TestCase):
    def test_01_registry_identity(self):
        data=json.loads((ROOT/"spec/CURRENT_CONSTRUCTION_REGISTRY.json").read_text(encoding="utf-8"))
        self.assertEqual(data["registry_version"],"c5.5-a15-b13.1")
        self.assertEqual(git_blob_sha(ROOT/"spec/CURRENT_CONSTRUCTION_REGISTRY.json"),
                         "c4a174b1cb3bc265773f3d0bdc1a99037749d5d8")

    def test_02_compiler_identity(self):
        py=(ROOT/"pyproject.toml").read_text(encoding="utf-8")
        self.assertIn('version = "0.5.5a1"',py)
        self.assertEqual(git_blob_sha(ROOT/"pyproject.toml"),
                         "c16ccd59c924ec90d74b3b79a55cd122f9c84ed0")

    def test_03_zero_profile_identity(self):
        y=resolve_index(SourceProfile.YEAR,0)
        g=resolve_index(SourceProfile.GENERAL,0)
        self.assertEqual(lower_index(y),lower_index(g))

    def test_04_profile_identity_wide_grid(self):
        for z in range(-250,251):
            self.assertEqual(lower_index(resolve_index(SourceProfile.YEAR,z)),
                             lower_index(resolve_index(SourceProfile.GENERAL,z)))

    def test_05_profile_erased_from_semantic_fingerprint(self):
        for z in (-10,-1,0,1,10):
            y=resolve_index(SourceProfile.YEAR,z)
            g=resolve_index(SourceProfile.GENERAL,z)
            self.assertEqual(semantic_fingerprint(lower_index(y)),
                             semantic_fingerprint(lower_index(g)))
            self.assertNotIn("year",repr(semantic_fingerprint(lower_index(y))).lower())
            self.assertNotIn("general",repr(semantic_fingerprint(lower_index(y))).lower())

    def test_06_value_only_synthesis_requires_explicit_profile(self):
        with self.assertRaisesRegex(ValueError,"TARGET_PROFILE_REQUIRED"):
            synthesize_source(from_math_index(0),None)

    def test_07_source_preserving_profile_can_be_retained_outside_value(self):
        src=resolve_index(SourceProfile.GENERAL,-7)
        rebuilt=synthesize_source(lower_index(src),src.profile)
        self.assertEqual(rebuilt,src)
        self.assertEqual(lower_index(rebuilt),from_math_index(-7))

    def test_08_cross_profile_program_input(self):
        inp=ProgramInputId(1,"coordinate",INDEX_DOMAIN)
        contract=ProgramContract((inp,))
        y=lower_index(resolve_index(SourceProfile.YEAR,4))
        g=lower_index(resolve_index(SourceProfile.GENERAL,-4))
        self.assertEqual(bind_invocation(contract,((inp,y),)).get(inp),y)
        self.assertEqual(bind_invocation(contract,((inp,g),)).get(inp),g)

    def test_09_cross_profile_year_value_to_generic_place(self):
        p=PlaceContract("p",INDEX_DOMAIN_KEY)
        y=lower_index(resolve_index(SourceProfile.YEAR,5))
        s=establish_place(State(),p,Expr(INDEX_DOMAIN_KEY,lambda:y))
        self.assertEqual(current_place(s,p,INDEX_DOMAIN_KEY),from_math_index(5))

    def test_10_cross_profile_general_value_to_year_place(self):
        p=PlaceContract("p",INDEX_DOMAIN_KEY)
        g=lower_index(resolve_index(SourceProfile.GENERAL,-5))
        s=establish_place(State(),p,Expr(INDEX_DOMAIN_KEY,lambda:g))
        s=replace_place(s,p,Expr(INDEX_DOMAIN_KEY,lambda:from_math_index(2)),INDEX_DOMAIN_KEY)
        self.assertEqual(current_place(s,p,INDEX_DOMAIN_KEY),from_math_index(2))

    def test_11_cross_profile_role_association(self):
        role=RoleContract("act","r",INDEX_DOMAIN_KEY)
        y=lower_index(resolve_index(SourceProfile.YEAR,-3))
        occ=start_occurrence(1,"act",(role,),((role,Expr(INDEX_DOMAIN_KEY,lambda:y)),))
        self.assertEqual(occ.role_value(role,INDEX_DOMAIN_KEY),y)

    def test_12_cross_profile_output_and_immediate_result(self):
        role=RoleContract("act","r",INDEX_DOMAIN_KEY)
        g=lower_index(resolve_index(SourceProfile.GENERAL,8))
        out=resolve_output_contract((INDEX_DOMAIN_KEY,))
        occ=start_occurrence(1,"act",(role,),((role,Expr(INDEX_DOMAIN_KEY,lambda:g)),),out)
        occ=emit(occ,Expr(INDEX_DOMAIN_KEY,lambda:occ.role_value(role,INDEX_DOMAIN_KEY)))
        prov=complete_occurrence(occ)
        self.assertEqual(read_immediate(prov,"act",INDEX_DOMAIN_KEY),g)

    def test_13_expected_type_does_not_rescue_unresolved_source(self):
        p=PlaceContract("p",INDEX_DOMAIN_KEY)
        with self.assertRaises(InvalidProgram) as cm:
            establish_place(State(),p,Expr(None,lambda:from_math_index(1)))
        self.assertEqual(cm.exception.code,UNRESOLVED_VALUE_DOMAIN)

    def test_14_strict_order_wide_grid(self):
        vals=[from_math_index(z) for z in range(-75,76)]
        for a in vals:
            for b in vals:
                self.assertEqual(index_lt(a,b),a.math()<b.math())

    def test_15_strict_order_trichotomy(self):
        for a in range(-30,31):
            for b in range(-30,31):
                ia,ib=from_math_index(a),from_math_index(b)
                cases=(index_lt(ia,ib),index_lt(ib,ia),ia==ib)
                self.assertEqual(sum(bool(x) for x in cases),1)

    def test_16_same_day_branching_without_equality_surface(self):
        self.assertEqual(classify_by_order(from_math_index(-2),from_math_index(5)),"before")
        self.assertEqual(classify_by_order(from_math_index(5),from_math_index(-2)),"after")
        self.assertEqual(classify_by_order(from_math_index(5),from_math_index(5)),"same")

    def test_17_same_day_branching_wide_grid(self):
        for a in range(-40,41):
            for b in range(-40,41):
                got=classify_by_order(from_math_index(a),from_math_index(b))
                exp="before" if a<b else ("after" if a>b else "same")
                self.assertEqual(got,exp)

    def test_18_succ_pred_origin_crossings(self):
        z=from_math_index(0)
        self.assertEqual(from_math_index(1).pred(),z)
        self.assertEqual(z.pred(),from_math_index(-1))
        self.assertEqual(from_math_index(-1).succ(),z)
        self.assertEqual(z.succ(),from_math_index(1))

    def test_19_succ_pred_inverse_far_grid(self):
        for z in range(-1000,1001):
            i=from_math_index(z)
            self.assertEqual(i.succ().pred(),i)
            self.assertEqual(i.pred().succ(),i)

    def test_20_steps_are_profile_neutral(self):
        for z in range(-50,51):
            y=lower_index(resolve_index(SourceProfile.YEAR,z))
            g=lower_index(resolve_index(SourceProfile.GENERAL,z))
            self.assertEqual(y.succ(),g.succ())
            self.assertEqual(y.pred(),g.pred())

    def test_21_distance_algorithm_same(self):
        a=from_math_index(17)
        self.assertEqual(distance_by_language_primitives(a,a),Natural(0))

    def test_22_distance_algorithm_forward(self):
        self.assertEqual(distance_by_language_primitives(from_math_index(-5),from_math_index(9)),Natural(14))

    def test_23_distance_algorithm_backward(self):
        self.assertEqual(distance_by_language_primitives(from_math_index(9),from_math_index(-5)),Natural(14))

    def test_24_distance_algorithm_differential_grid(self):
        vals=[from_math_index(z) for z in range(-35,36)]
        for a in vals:
            for b in vals:
                self.assertEqual(distance_by_language_primitives(a,b),a.distance(b))

    def test_25_direct_distance_surface_absent(self):
        self.assertIn("distance",DELIBERATELY_ABSENT_INDEX_SURFACE)
        self.assertNotIn("distance",LANGUAGE_LEVEL_INDEX_SURFACE)

    def test_26_index_equality_surface_not_required(self):
        self.assertIn("equality",DELIBERATELY_ABSENT_INDEX_SURFACE)
        for z in (-9,0,11):
            self.assertEqual(classify_by_order(from_math_index(z),from_math_index(z)),"same")

    def test_27_no_natural_index_surface_conversion(self):
        self.assertIn("natural_to_index",DELIBERATELY_ABSENT_INDEX_SURFACE)
        self.assertIn("index_to_natural",DELIBERATELY_ABSENT_INDEX_SURFACE)

    def test_28_no_signed_arithmetic_widening(self):
        for op in ("signed_add","signed_subtract","unary_minus"):
            self.assertIn(op,DELIBERATELY_ABSENT_INDEX_SURFACE)
            self.assertNotIn(op,LANGUAGE_LEVEL_INDEX_SURFACE)

    def test_29_no_arbitrary_profile_noun(self):
        self.assertIn("arbitrary_profile_noun",DELIBERATELY_ABSENT_INDEX_SURFACE)
        self.assertEqual(set(SourceProfile),{SourceProfile.YEAR,SourceProfile.GENERAL})

    def test_30_semantic_domain_remains_single(self):
        vals=[lower_index(resolve_index(p,z)) for p in SourceProfile for z in (-3,0,4)]
        self.assertTrue(all(isinstance(v,BidirectionalIndex) for v in vals))
        self.assertEqual({semantic_fingerprint(v)[0] for v in vals},{INDEX_DOMAIN_KEY})

if __name__=="__main__":
    unittest.main(verbosity=2)
