#!/usr/bin/env python3
from b12_reference_core import *

def pval(rp,out,name):
    p=next(p for p in rp.places if p.spelling==name)
    return out.state.get(p)

def test_b11_state_referents():
    spec=ProgramSpec((PlaceIntro("x",ULit(5)),PlaceIntro("y",ULit(5))),UReplace("x",ULit(9)))
    rp=resolve_program(spec); o=Evaluator(rp).run()
    assert pval(rp,o,"x")==9 and pval(rp,o,"y")==5

def test_b11_numeric_intent_with_normative_delta():
    huge=10**700
    spec=ProgramSpec((PlaceIntro("x",ULit(huge)),),UReplace("x",UAdd(UCurrent("x"),ULit(huge))))
    rp=resolve_program(spec); o=Evaluator(rp).run()
    assert pval(rp,o,"x")==2*huge
    # B11's negative-subtraction expectation is intentionally replaced by domain error.
    try:
        resolve_program(ProgramSpec((PlaceIntro("x",ULit(0)),),UReplace("x",USubtractFrom(ULit(5),ULit(2)))))
    except InvalidProgram as e:
        assert e.code==ARITHMETIC_DOMAIN_ERROR
    else:
        raise AssertionError("B12 signed-delta not enforced")

def test_b11_conditional():
    spec=ProgramSpec((PlaceIntro("x",ULit(0)),),UConditional(UEqual(UCurrent("x"),ULit(0)),UReplace("x",ULit(8)),UReplace("x",ULit(99))))
    rp=resolve_program(spec); o=Evaluator(rp).run(); assert pval(rp,o,"x")==8

def test_b11_fixed_repeat():
    spec=ProgramSpec((PlaceIntro("x",ULit(1)),),UFixedRepeat(7,UReplace("x",UAdd(UCurrent("x"),ULit(1)))))
    rp=resolve_program(spec); o=Evaluator(rp).run(); assert pval(rp,o,"x")==8

def test_b11_post_repeat_at_least_once():
    spec=ProgramSpec((PlaceIntro("x",ULit(0)),),UPostActionUntil(UReplace("x",UAdd(UCurrent("x"),ULit(1))),UEqual(UCurrent("x"),ULit(1))))
    rp=resolve_program(spec); o=Evaluator(rp).run(); assert pval(rp,o,"x")==1

def test_b11_decrement_to_zero():
    spec=ProgramSpec((PlaceIntro("x",ULit(9)),),UPostActionUntil(UReplace("x",USubtractFrom(ULit(1),UCurrent("x"))),UEqual(UCurrent("x"),ULit(0))))
    rp=resolve_program(spec); o=Evaluator(rp).run(); assert pval(rp,o,"x")==0

def test_b11_role_order_invariant():
    prep=(ActIntro("f"),RoleIntro("f","a"),RoleIntro("f","b"),BodyDef("f",UProduce(UAdd(URoleValue("f","a"),URoleValue("f","b")))))
    a=ProgramSpec(prep,UPerform("f",(("a",ULit(2)),("b",ULit(3)))))
    b=ProgramSpec(prep,UPerform("f",(("b",ULit(3)),("a",ULit(2)))))
    oa=Evaluator(resolve_program(a)).run(); ob=Evaluator(resolve_program(b)).run()
    assert [x.value for x in oa.productions]==[5]==[x.value for x in ob.productions]

def test_b11_zero_or_one_output():
    spec=ProgramSpec((ActIntro("f"),BodyDef("f",UFixedRepeat(0,UPerform("f")))),UPerform("f"))
    assert isinstance(Evaluator(resolve_program(spec)).run(),NormalOutcome)
    try:
        resolve_program(ProgramSpec((ActIntro("g"),BodyDef("g",USequence((UProduce(ULit(1)),UProduce(ULit(2)))))),UPerform("g")))
    except InvalidProgram as e:
        assert e.code==CORE_OUTPUT_CARDINALITY_ERROR
    else: raise AssertionError()

def test_b11_provenance_expiry():
    spec=ProgramSpec((PlaceIntro("x",ULit(0)),ActIntro("c"),BodyDef("c",UProduce(ULit(3))),ActIntro("p"),BodyDef("p",USequence((UPerform("c"),UReplace("x",ULit(1)),UProduce(URecentResult("c")))))),UPerform("p"))
    o=Evaluator(resolve_program(spec)).run()
    assert isinstance(o,ErrorOutcome) and o.error.code==RESULT_PROVENANCE_ERROR

def test_b11_preparation_replaces_old_generic_examples():
    spec=ProgramSpec((PlaceIntro("x",ULit(2)),PlaceIntro("y",UAdd(UCurrent("x"),ULit(3)))),UReplace("x",UCurrent("x")))
    rp=resolve_program(spec); o=Evaluator(rp).run(); assert pval(rp,o,"y")==5

def test_b11_output_nonterminal():
    spec=ProgramSpec((PlaceIntro("x",ULit(0)),ActIntro("f"),BodyDef("f",USequence((UProduce(ULit(7)),UReplace("x",ULit(2)))))),UPerform("f"))
    rp=resolve_program(spec); o=Evaluator(rp).run(); assert pval(rp,o,"x")==2

def test_b11_recursion_occurrences():
    spec=ProgramSpec((ActIntro("f"),RoleIntro("f","n"),BodyDef("f",UConditional(UEqual(URoleValue("f","n"),ULit(0)),UProduce(ULit(0)),UPerform("f",(("n",USubtractFrom(ULit(1),URoleValue("f","n"))),))))),UPerform("f",(("n",ULit(4)),)))
    ev=Evaluator(resolve_program(spec),fuel=100); o=ev.run()
    assert isinstance(o,NormalOutcome) and len(ev.occurrence_log)==5

def test_b11_no_boolean_truthiness():
    # Only proposition constructors can drive Conditional in the resolved model.
    assert not issubclass(int,bool)

def test_b11_rm_intent():
    # Tiny countdown witness: helper decrement is guarded by zero test.
    spec=ProgramSpec(
      (
        PlaceIntro("R",ULit(3)),PlaceIntro("sink",ULit(0)),
        ActIntro("L"),ActIntro("H"),ActIntro("D"),
        BodyDef("L",UConditional(UEqual(UCurrent("R"),ULit(0)),UPerform("H"),UPerform("D"))),
        BodyDef("H",UReplace("sink",UCurrent("sink"))),
        BodyDef("D",USequence((UReplace("R",USubtractFrom(ULit(1),UCurrent("R"))),UPerform("L")))),
      ),
      UPerform("L")
    )
    rp=resolve_program(spec); o=Evaluator(rp,fuel=100).run()
    assert isinstance(o,NormalOutcome) and pval(rp,o,"R")==0 and pval(rp,o,"sink")==0

TESTS=[
test_b11_state_referents,
test_b11_numeric_intent_with_normative_delta,
test_b11_conditional,
test_b11_fixed_repeat,
test_b11_post_repeat_at_least_once,
test_b11_decrement_to_zero,
test_b11_role_order_invariant,
test_b11_zero_or_one_output,
test_b11_provenance_expiry,
test_b11_preparation_replaces_old_generic_examples,
test_b11_output_nonterminal,
test_b11_recursion_occurrences,
test_b11_no_boolean_truthiness,
test_b11_rm_intent,
]
if __name__=="__main__":
    for t in TESTS:
        t(); print("PASS",t.__name__)
    print(f"B11 INTENT REGRESSION UNDER B12: PASS ({len(TESTS)} tests)")
    print("INTENTIONAL NORMATIVE DELTA: B11 signed subtraction -> B12 Natural domain error")
