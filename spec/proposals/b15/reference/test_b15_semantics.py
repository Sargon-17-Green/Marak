#!/usr/bin/env python3
from __future__ import annotations
import sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT))
from spec.proposals.b13.reference.b13_reference_model import (
    Natural, SymbolDomain, SymbolMember, from_math_index,
    FiniteOrderedCollection, NAT_DOMAIN
)
from spec.proposals.b15.reference.b15_reference_model import *

def okexpr(domain,value): return Expr(domain,lambda:value)
def badexpr(domain,code="E"):
    def f(): raise RuntimeFault(code)
    return Expr(domain,f)
def divexpr(domain):
    def f(): raise Diverged()
    return Expr(domain,f)
def ikey(i): return i.math()
def sid(s): return (s.domain.serial,s.serial)

class B15IndependentTests(unittest.TestCase):
    def setUp(self):
        self.colors=SymbolDomain(1,"colors")
        self.months=SymbolDomain(2,"months")
        self.red=SymbolMember(self.colors,1,"same")
        self.red2=SymbolMember(self.colors,2,"same")
        self.blue=SymbolMember(self.colors,3,"blue")
        self.tin=SymbolMember(self.months,1,"same")

    def test_place_domain_static_before_initializer_evaluation(self):
        e=badexpr("Symbol:1","INIT_FAIL")
        p=declare_place("p",e)
        self.assertEqual(p.domain,"Symbol:1")
        s=State()
        with self.assertRaises(RuntimeFault) as cm: establish_place(s,p,e)
        self.assertEqual(cm.exception.code,"INIT_FAIL")
        self.assertFalse(s.has(p))

    def test_place_divergent_initializer_has_no_partial_place(self):
        e=divexpr("BidirectionalIndex"); p=declare_place("y",e); s=State()
        with self.assertRaises(Diverged): establish_place(s,p,e)
        self.assertFalse(s.has(p))

    def test_place_unresolved_domain_not_rescued_by_context(self):
        with self.assertRaises(InvalidProgram) as cm:
            declare_place("p",Expr(None,lambda:self.red))
        self.assertEqual(cm.exception.code,UNRESOLVED_VALUE_DOMAIN)

    def test_place_identity_not_value_and_typed_current(self):
        p=declare_place("p",okexpr("Symbol:1",self.red))
        s=establish_place(State(),p,okexpr("Symbol:1",self.red))
        self.assertEqual(current_place(s,p,"Symbol:1"),self.red)
        self.assertNotEqual(p,self.red)
        with self.assertRaises(InvalidProgram): current_place(s,p,"Symbol:2")

    def test_wrong_domain_replacement_rejected_before_rhs_eval(self):
        p=declare_place("p",okexpr("Symbol:1",self.red))
        s=establish_place(State(),p,okexpr("Symbol:1",self.red))
        touched={"x":False}
        def thunk(): touched["x"]=True; return from_math_index(1)
        rhs=Expr("BidirectionalIndex",thunk)
        with self.assertRaises(InvalidProgram) as cm: replace_place(s,p,rhs,"Symbol:1")
        self.assertEqual(cm.exception.code,PLACE_DOMAIN_MISMATCH)
        self.assertFalse(touched["x"]); self.assertEqual(s.get(p),self.red)

    def test_failed_rhs_no_commit_prior_state_preserved(self):
        p=declare_place("p",okexpr("Symbol:1",self.red))
        s=establish_place(State(),p,okexpr("Symbol:1",self.red))
        with self.assertRaises(RuntimeFault): replace_place(s,p,badexpr("Symbol:1"),"Symbol:1")
        self.assertEqual(s.get(p),self.red)

    def test_collection_append_is_pure_state_changes_only_on_replace(self):
        c0=FiniteOrderedCollection(NAT_DOMAIN,())
        p=declare_place("book",okexpr("Collection<Natural>",c0))
        s=establish_place(State(),p,okexpr("Collection<Natural>",c0))
        c1=c0.append(Natural(1))
        self.assertEqual(c0.items,()); self.assertEqual(s.get(p).items,())
        s2=replace_place(s,p,okexpr("Collection<Natural>",c1),"Collection<Natural>")
        self.assertEqual(s.get(p).items,()); self.assertEqual(tuple(x.n for x in s2.get(p).items),(1,))

    def test_role_domain_static_and_wrong_domain_before_occurrence(self):
        r=RoleContract("echo","x","Symbol:1"); touched={"x":False}
        def thunk(): touched["x"]=True; return self.tin
        with self.assertRaises(InvalidProgram) as cm:
            start_occurrence(1,"echo",(r,),((r,Expr("Symbol:2",thunk)),))
        self.assertEqual(cm.exception.code,ROLE_DOMAIN_MISMATCH); self.assertFalse(touched["x"])

    def test_same_role_spelling_different_act_not_interchangeable(self):
        r1=RoleContract("a","x","Symbol:1"); r2=RoleContract("b","x","Symbol:1")
        with self.assertRaises(InvalidProgram):
            start_occurrence(1,"a",(r1,),((r2,okexpr("Symbol:1",self.red)),))

    def test_recursive_non_natural_role_occurrences_are_distinct(self):
        role=RoleContract("rec","x","Symbol:1")
        outer=start_occurrence(1,"rec",(role,),((role,okexpr("Symbol:1",self.red)),))
        inner=start_occurrence(2,"rec",(role,),((role,okexpr("Symbol:1",self.blue)),))
        self.assertEqual(inner.role_value(role,"Symbol:1"),self.blue)
        self.assertEqual(outer.role_value(role,"Symbol:1"),self.red)
        self.assertNotEqual(inner.token,outer.token)

    def test_output_contract_zero_same_and_mixed_sites(self):
        self.assertIsNone(resolve_output_contract(()))
        self.assertEqual(resolve_output_contract(("Symbol:1","Symbol:1")),"Symbol:1")
        with self.assertRaises(InvalidProgram) as cm:
            resolve_output_contract(("Symbol:1","BidirectionalIndex"))
        self.assertEqual(cm.exception.code,MIXED_OUTPUT_DOMAINS)

    def test_output_is_nonterminal_and_provenance_survives_later_callee_body_action(self):
        out=resolve_output_contract(("Symbol:1",))
        occ=start_occurrence(1,"emit",(),(),out)
        occ=emit(occ,okexpr("Symbol:1",self.red)); occ=later_action(occ)
        self.assertEqual(occ.completed_actions,1)
        prov=complete_occurrence(occ)
        validate_immediate_reference(out,"Symbol:1",True)
        self.assertEqual(read_immediate(prov,"emit","Symbol:1"),self.red)

    def test_zero_output_runtime_path_uses_b12_result_provenance_error(self):
        out=resolve_output_contract(("Symbol:1","Symbol:1"))
        prov=complete_occurrence(start_occurrence(1,"maybe",(),(),out))
        validate_immediate_reference(out,"Symbol:1",True)
        with self.assertRaises(RuntimeFault) as cm: read_immediate(prov,"maybe","Symbol:1")
        self.assertEqual(cm.exception.code,RESULT_PROVENANCE_ERROR)

    def test_wrong_immediate_head_is_static_invalid(self):
        out=resolve_output_contract(("Collection<Natural>",))
        with self.assertRaises(InvalidProgram) as cm:
            validate_immediate_reference(out,"Collection<Symbol:1>",True)
        self.assertEqual(cm.exception.code,IMMEDIATE_RESULT_HEAD_MISMATCH)

    def test_structurally_stale_immediate_is_static_invalid_and_runtime_fallback_stays_b12(self):
        out=resolve_output_contract(("Symbol:1",))
        with self.assertRaises(InvalidProgram) as cm:
            validate_immediate_reference(out,"Symbol:1",False)
        self.assertEqual(cm.exception.code,STALE_RESULT_REFERENCE)
        occ=emit(start_occurrence(1,"emit",(),(),out),okexpr("Symbol:1",self.red))
        prov=invalidate(complete_occurrence(occ))
        with self.assertRaises(RuntimeFault) as cm: read_immediate(prov,"emit","Symbol:1")
        self.assertEqual(cm.exception.code,RESULT_PROVENANCE_ERROR)

    def test_second_output_same_occurrence_rejected(self):
        out=resolve_output_contract(("Symbol:1","Symbol:1"))
        occ=emit(start_occurrence(1,"emit",(),(),out),okexpr("Symbol:1",self.red))
        with self.assertRaises(RuntimeFault) as cm: emit(occ,okexpr("Symbol:1",self.blue))
        self.assertEqual(cm.exception.code,CORE_OUTPUT_CARDINALITY_ERROR)

    def test_repeated_performances_each_have_independent_output_no_collection(self):
        vals=[]
        for token,v in enumerate((self.red,self.blue),1):
            out=resolve_output_contract(("Symbol:1",))
            occ=emit(start_occurrence(token,"emit",(),(),out),okexpr("Symbol:1",v))
            vals.append(complete_occurrence(occ).output)
        self.assertEqual(vals,[self.red,self.blue])
        self.assertFalse(isinstance(vals[0],FiniteOrderedCollection))

    def test_index_crossing_laws_and_farther_magnitudes(self):
        z=from_math_index(0); a1=from_math_index(1); b1=from_math_index(-1)
        self.assertEqual(index_pred(a1,"BidirectionalIndex",from_math_index,ikey),z)
        self.assertEqual(index_pred(z,"BidirectionalIndex",from_math_index,ikey),b1)
        self.assertEqual(index_succ(b1,"BidirectionalIndex",from_math_index,ikey),z)
        self.assertEqual(index_succ(z,"BidirectionalIndex",from_math_index,ikey),a1)
        for n in range(-50,51):
            i=from_math_index(n)
            self.assertEqual(ikey(index_succ(i,"BidirectionalIndex",from_math_index,ikey)),n+1)
            self.assertEqual(ikey(index_pred(i,"BidirectionalIndex",from_math_index,ikey)),n-1)

    def test_index_step_rejects_natural_no_promotion(self):
        with self.assertRaises(InvalidProgram) as cm:
            index_pred(Natural(0),"Natural",from_math_index,ikey)
        self.assertEqual(cm.exception.code,INDEX_OPERAND_DOMAIN_MISMATCH)

    def test_megillah_year_progression_needs_no_natural_to_index(self):
        i=from_math_index(5000)
        for _ in range(5000): i=index_pred(i,"BidirectionalIndex",from_math_index,ikey)
        self.assertEqual(i,from_math_index(0))
        i=index_pred(i,"BidirectionalIndex",from_math_index,ikey)
        self.assertEqual(i,from_math_index(-1))
        i=index_succ(i,"BidirectionalIndex",from_math_index,ikey)
        self.assertEqual(i,from_math_index(0))

    def test_symbol_equality_member_identity_not_label(self):
        self.assertTrue(symbol_equal(self.red,self.red,"Symbol:1","Symbol:1",sid))
        self.assertFalse(symbol_equal(self.red,self.red2,"Symbol:1","Symbol:1",sid))
        self.assertEqual(self.red.label,self.red2.label)

    def test_cross_domain_symbol_equality_static_invalid_not_false(self):
        with self.assertRaises(InvalidProgram) as cm:
            symbol_equal(self.red,self.tin,"Symbol:1","Symbol:2",sid)
        self.assertEqual(cm.exception.code,SYMBOL_EQUALITY_DOMAIN_MISMATCH)

    def test_symbol_equality_is_proposition_consumed_by_control(self):
        holds=symbol_equal(self.red,self.red,"Symbol:1","Symbol:1",sid)
        chosen=self.red if holds else self.blue
        self.assertEqual(chosen,self.red)

    def test_consumer_cannot_rescue_untyped_book(self):
        ambiguous=Expr(None,lambda:FiniteOrderedCollection(NAT_DOMAIN,()))
        p=PlaceContract("book","Collection<Natural>")
        s=State((("book",FiniteOrderedCollection(NAT_DOMAIN,())),))
        with self.assertRaises(InvalidProgram) as cm:
            replace_place(s,p,ambiguous,"Collection<Natural>")
        self.assertEqual(cm.exception.code,UNRESOLVED_VALUE_DOMAIN)

    def test_consumer_cannot_rescue_bare_symbol_identifier(self):
        role=RoleContract("a","r","Symbol:1")
        with self.assertRaises(InvalidProgram) as cm:
            start_occurrence(1,"a",(role,),((role,Expr(None,lambda:"red")),))
        self.assertEqual(cm.exception.code,UNRESOLVED_VALUE_DOMAIN)

    def test_program_A_symbol_flow(self):
        p=declare_place("saved",okexpr("Symbol:1",self.red))
        state=establish_place(State(),p,okexpr("Symbol:1",self.red))
        role=RoleContract("echo","arg","Symbol:1")
        out=resolve_output_contract(("Symbol:1","Symbol:1"))
        occ=start_occurrence(1,"echo",(role,),((role,okexpr("Symbol:1",current_place(state,p,"Symbol:1"))),),out)
        arg=occ.role_value(role,"Symbol:1")
        self.assertTrue(symbol_equal(arg,self.red,"Symbol:1","Symbol:1",sid))
        occ=emit(occ,okexpr("Symbol:1",arg)); occ=later_action(occ)
        prov=complete_occurrence(occ)
        state=replace_place(state,p,okexpr("Symbol:1",read_immediate(prov,"echo","Symbol:1")),"Symbol:1")
        self.assertEqual(state.get(p),self.red)

    def test_program_B_index_flow(self):
        p=declare_place("year",okexpr("BidirectionalIndex",from_math_index(1)))
        state=establish_place(State(),p,okexpr("BidirectionalIndex",from_math_index(1)))
        seq=[("pred",0),("pred",-1),("succ",0),("succ",1)]
        for op,expected in seq:
            fn=index_pred if op=="pred" else index_succ
            v=fn(state.get(p),"BidirectionalIndex",from_math_index,ikey)
            state=replace_place(state,p,okexpr("BidirectionalIndex",v),"BidirectionalIndex")
            self.assertEqual(ikey(state.get(p)),expected)
        role=RoleContract("echoYear","arg","BidirectionalIndex")
        out=resolve_output_contract(("BidirectionalIndex",))
        occ=start_occurrence(1,"echoYear",(role,),((role,okexpr("BidirectionalIndex",state.get(p))),),out)
        occ=emit(occ,okexpr("BidirectionalIndex",occ.role_value(role,"BidirectionalIndex")))
        prov=complete_occurrence(occ)
        state=replace_place(state,p,okexpr("BidirectionalIndex",read_immediate(prov,"echoYear","BidirectionalIndex")),"BidirectionalIndex")
        self.assertEqual(ikey(state.get(p)),1)

    def test_program_C_collection_flow(self):
        empty=FiniteOrderedCollection(NAT_DOMAIN,())
        p=declare_place("book",okexpr("Collection<Natural>",empty))
        state=establish_place(State(),p,okexpr("Collection<Natural>",empty))
        old=state.get(p); c1=old.append(Natural(1))
        self.assertEqual(old.items,())
        state=replace_place(state,p,okexpr("Collection<Natural>",c1),"Collection<Natural>")
        prior=state.get(p); c2=prior.append(Natural(2))
        self.assertEqual(tuple(x.n for x in prior.items),(1,))
        state=replace_place(state,p,okexpr("Collection<Natural>",c2),"Collection<Natural>")
        role=RoleContract("echoBook","arg","Collection<Natural>")
        out=resolve_output_contract(("Collection<Natural>",))
        occ=start_occurrence(1,"echoBook",(role,),((role,okexpr("Collection<Natural>",state.get(p))),),out)
        book=occ.role_value(role,"Collection<Natural>")
        self.assertEqual(book.count(),Natural(2)); self.assertEqual(book.select(Natural(2)),Natural(2))
        occ=emit(occ,okexpr("Collection<Natural>",book)); prov=complete_occurrence(occ)
        state=replace_place(state,p,okexpr("Collection<Natural>",read_immediate(prov,"echoBook","Collection<Natural>")),"Collection<Natural>")
        self.assertEqual(tuple(x.n for x in state.get(p).items),(1,2))

    def test_D_adequacy_all_seven(self):
        self.assertEqual(set(D_ADEQUACY),{f"{i:03d}" for i in range(1,8)})
        self.assertTrue(all(v=="EXECUTABLE_AFTER_INTEGRATION" for v in D_ADEQUACY.values()))

if __name__=="__main__":
    unittest.main(verbosity=2)
