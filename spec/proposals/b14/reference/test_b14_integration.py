from __future__ import annotations
import importlib.util
import sys
import unittest
from pathlib import Path

HERE=Path(__file__).resolve().parent
B14=HERE.parent
ROOT=HERE.parents[3]

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    sys.modules[name]=mod
    spec.loader.exec_module(mod)
    return mod

b13=load("b13_model",ROOT/"spec/proposals/b13/reference/b13_reference_model.py")
a15=load("a15_ref",ROOT/"spec/proposals/a15/tools/a15_reference.py")
num=load("a15_num",ROOT/"spec/proposals/a15/tools/a15_numeral_reference.py")
cap=load("b14_cap",HERE/"b14_integration_model.py")

class B14IntegrationTests(unittest.TestCase):
    def test_symbol_same_label_cross_domain_distinct(self):
        d1=b13.SymbolDomain(1,"months"); d2=b13.SymbolDomain(2,"cutlets")
        a=b13.SymbolMember(d1,1,"door"); b=b13.SymbolMember(d2,1,"door")
        self.assertFalse(b13.symbol_equal(a,b)); self.assertEqual(a.label,b.label)

    def test_symbol_identity_not_label(self):
        d=b13.SymbolDomain(1,"months")
        a=b13.SymbolMember(d,1,"same"); b=b13.SymbolMember(d,2,"same")
        self.assertFalse(b13.symbol_equal(a,b))

    def test_symbol_order_complete_and_incomplete(self):
        d=a15.SymbolDomain("months")
        d.declare("a",["א"]); d.declare("b",["ב"]); d.declare("c",["ג"])
        d.establish_adjacent_order(["a","b","c"])
        self.assertLess(d.order_key(d.value("a")),d.order_key(d.value("c")))
        e=a15.SymbolDomain("x"); e.declare("a",["א"]); e.declare("b",["ב"])
        with self.assertRaises(a15.SurfaceError): e.establish_adjacent_order(["a"])

    def test_index_before_zero_after_and_progression(self):
        z=b13.from_math_index(0)
        self.assertEqual(z.pred().math(),-1)
        self.assertEqual(z.succ().math(),1)
        self.assertEqual(b13.from_math_index(-1).succ().math(),0)
        self.assertEqual(b13.from_math_index(1).pred().math(),0)

    def test_dynamic_index_surface_absent_in_a15(self):
        p=(ROOT/"spec/proposals/a15/A15_BIDIRECTIONAL_INDEX_SURFACE.md").read_text(encoding="utf-8")
        self.assertIn("does not add new source spellings for those operations",p)

    def test_collection_immutable_accumulation(self):
        c0=b13.FiniteOrderedCollection(b13.NAT_DOMAIN,())
        c1=c0.append(b13.Natural(3)); c2=c1.append(b13.Natural(1))
        self.assertEqual(c0.items,()); self.assertEqual(tuple(x.n for x in c2.items),(3,1))

    def test_collection_duplicates_and_ordinal(self):
        c=b13.FiniteOrderedCollection(b13.NAT_DOMAIN,(b13.Natural(4),b13.Natural(4),b13.Natural(9)))
        self.assertEqual(c.select(b13.Natural(1)).n,4)
        self.assertEqual(c.select(b13.Natural(2)).n,4)
        with self.assertRaises(b13.SemanticFailure) as cm: c.select(b13.Natural(0))
        self.assertEqual(cm.exception.code,b13.COLLECTION_POSITION_ERROR)

    def test_nested_lex_order(self):
        inner=b13.collection_domain(b13.NAT_DOMAIN)
        a=b13.FiniteOrderedCollection(b13.NAT_DOMAIN,(b13.Natural(2),))
        b=b13.FiniteOrderedCollection(b13.NAT_DOMAIN,(b13.Natural(1),b13.Natural(9)))
        outer=b13.FiniteOrderedCollection(inner,(a,b))
        ordered=b13.order_collection(outer,lambda x,y:b13.lex_lt(b13.NAT_DOMAIN,b13.nat_lt,x,y))
        self.assertEqual(tuple(tuple(v.n for v in c.items) for c in ordered.items),((1,9),(2,)))

    def test_wrong_domain_membership_is_not_admitted_surface(self):
        c=b13.FiniteOrderedCollection(b13.NAT_DOMAIN,(b13.Natural(1),))
        d=b13.SymbolDomain(1,"d"); s=b13.SymbolMember(d,1,"x")
        with self.assertRaises(cap.SurfaceDomainError) as cm:
            cap.typed_membership(c,s)
        self.assertEqual(str(cm.exception),"VALUE_DOMAIN_MISMATCH")

    def test_natural_gt(self):
        self.assertTrue(b13.nat_gt(b13.Natural(10**200),b13.Natural(9)))

    def test_huge_direct_numeral_exact(self):
        self.assertEqual(num.format_natural(14_777_149),
            "ארבעה עשר אלף אלפים ושבע מאות אלף ושבעים אלף ושבעת אלפים ומאה וארבעים ותשעה")
        self.assertTrue(len(num.format_natural(99_999_999))>0)

    def test_repeat_zero_one_large(self):
        for n in (0,1,10000):
            calls=[]
            r=b13.repeat_exactly(lambda n=n:b13.Natural(n),
                lambda state,i:(calls.append(i) or b13.StepNormal(state+1,())),0)
            self.assertIsInstance(r,b13.StepNormal)
            self.assertEqual(r.state,n); self.assertEqual(len(calls),n)

    def test_repeat_dynamic_count_once(self):
        q={"count":3,"observed":0}
        def count():
            q["observed"]+=1
            return b13.Natural(q["count"])
        def action(state,i):
            q["count"]=99
            return b13.StepNormal(state+1,())
        r=b13.repeat_exactly(count,action,0)
        self.assertEqual((r.state,q["observed"]),(3,1))

    def test_repeat_error_boundary(self):
        def action(state,i):
            if i==3:return b13.StepError(state,"X",())
            return b13.StepNormal(state+1,(i,))
        r=b13.repeat_exactly(lambda:b13.Natural(5),action,0)
        self.assertIsInstance(r,b13.StepError)
        self.assertEqual((r.state,r.outputs),(2,(1,2)))

    def test_repeat_divergence(self):
        def action(state,i):
            if i==2:return b13.StepDivergence(("before-diverge",))
            return b13.StepNormal(state+1,(i,))
        r=b13.repeat_exactly(lambda:b13.Natural(4),action,0)
        self.assertIsInstance(r,b13.StepDivergence)
        self.assertEqual(r.outputs,(1,"before-diverge"))

    def test_repeated_output_rule_same_occurrence(self):
        occ=cap.Occurrence(); occ.produce(1)
        with self.assertRaises(cap.OutputCardinalityError): occ.produce(2)

    def test_repeated_named_performances_each_output_once(self):
        outputs=[]
        for i in range(3):
            occ=cap.Occurrence(); occ.produce(i); outputs.append(occ.produced)
        self.assertEqual(outputs,[0,1,2])

    def _contract(self):
        a=b13.ProgramInputId(1,"calc",b13.NAT_DOMAIN)
        b=b13.ProgramInputId(2,"target",b13.NAT_DOMAIN)
        return b13.ProgramContract((a,b)),a,b

    def test_inputs_identity_order_independent(self):
        c,a,b=self._contract()
        x=b13.bind_invocation(c,((b,b13.Natural(22)),(a,b13.Natural(11))))
        self.assertEqual((x.get(a).n,x.get(b).n),(11,22))

    def test_inputs_missing_extra_duplicate_wrong_domain(self):
        c,a,b=self._contract()
        with self.assertRaises(b13.InvalidInvocation) as cm:
            b13.bind_invocation(c,((a,b13.Natural(1)),))
        self.assertEqual(cm.exception.code,b13.MISSING_INPUT_BINDING)
        extra=b13.ProgramInputId(3,"x",b13.NAT_DOMAIN)
        with self.assertRaises(b13.InvalidInvocation) as cm:
            b13.bind_invocation(c,((a,b13.Natural(1)),(b,b13.Natural(2)),(extra,b13.Natural(3))))
        self.assertEqual(cm.exception.code,b13.EXTRA_INPUT_BINDING)
        with self.assertRaises(b13.InvalidInvocation) as cm:
            b13.bind_invocation(c,((a,b13.Natural(1)),(a,b13.Natural(2)),(b,b13.Natural(3))))
        self.assertEqual(cm.exception.code,b13.DUPLICATE_INPUT_BINDING)
        idx=b13.from_math_index(1)
        with self.assertRaises(b13.InvalidInvocation) as cm:
            b13.bind_invocation(c,((a,idx),(b,b13.Natural(3))))
        self.assertEqual(cm.exception.code,b13.INPUT_DOMAIN_MISMATCH)

    def test_natural_input_to_working_state_is_composable(self):
        c,a,b=self._contract()
        x=b13.bind_invocation(c,((a,b13.Natural(7)),(b,b13.Natural(9))))
        working=x.get(a)  # abstract value passed to A13 numeric place initializer
        self.assertEqual(working,b13.Natural(7))

    def test_domain_composition_gap_registry(self):
        for d in ("Symbol","BidirectionalIndex","Collection"):
            self.assertEqual(cap.SURFACE[d]["value"],cap.SUPPORTED_WITH_EXACT_SURFACE)
            self.assertEqual(cap.SURFACE[d]["program_input"],cap.SUPPORTED_WITH_EXACT_SURFACE)
            for k in ("state","replacement","act_role","act_output","immediate_result","observation"):
                self.assertEqual(cap.SURFACE[d][k],cap.SEMANTICALLY_SUPPORTED_BUT_NO_SURFACE)

    def test_all_five_gap_ids_recorded(self):
        self.assertEqual(len(cap.GAPS),5)
        self.assertEqual(cap.GAPS[0],"B14-A-SURFACE-GAP-001")
        self.assertEqual(cap.GAPS[-1],"B14-A-SURFACE-GAP-005")

if __name__=="__main__":
    unittest.main(verbosity=2)
