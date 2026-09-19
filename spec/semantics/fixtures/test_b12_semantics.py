#!/usr/bin/env python3
from b12_reference_core import *

def assert_invalid(code, thunk):
    try:
        thunk()
    except InvalidProgram as e:
        assert e.code==code, (e.code,code)
        return
    raise AssertionError(f"expected InvalidProgram({code})")

def build(spec, **evkw):
    return Evaluator(resolve_program(spec), **evkw)

def place_value(resolved, outcome, spelling):
    pid=next(p for p in resolved.places if p.spelling==spelling)
    return outcome.state.get(pid)

# ---- Numeric ----
def test_numeric_3_minus_2():
    spec=ProgramSpec((PlaceIntro("x",ULit(0)),),UReplace("x",USubtractFrom(ULit(2),ULit(3))))
    rp=resolve_program(spec); out=Evaluator(rp).run()
    assert isinstance(out,NormalOutcome) and place_value(rp,out,"x")==1

def test_numeric_3_minus_3():
    spec=ProgramSpec((PlaceIntro("x",ULit(9)),),UReplace("x",USubtractFrom(ULit(3),ULit(3))))
    rp=resolve_program(spec); out=Evaluator(rp).run()
    assert isinstance(out,NormalOutcome) and place_value(rp,out,"x")==0

def test_static_underflow_rejected():
    assert_invalid(ARITHMETIC_DOMAIN_ERROR, lambda: resolve_program(
        ProgramSpec((PlaceIntro("x",ULit(0)),),UReplace("x",USubtractFrom(ULit(3),ULit(2))))
    ))

def test_dynamic_underflow_runtime_error_and_target_unchanged():
    spec=ProgramSpec(
        (PlaceIntro("a",ULit(3)),PlaceIntro("b",ULit(2)),PlaceIntro("target",ULit(8))),
        UReplace("target",USubtractFrom(UCurrent("a"),UCurrent("b")))
    )
    rp=resolve_program(spec); out=Evaluator(rp).run()
    assert isinstance(out,ErrorOutcome)
    assert out.error.code==ARITHMETIC_DOMAIN_ERROR
    assert place_value(rp,out,"target")==8

def test_no_negative_literal():
    assert_invalid(ARITHMETIC_DOMAIN_ERROR, lambda: resolve_program(
        ProgramSpec((PlaceIntro("x",ULit(-1)),),UReplace("x",ULit(0)))
    ))

def test_huge_natural_exactness():
    huge=10**1200
    spec=ProgramSpec((PlaceIntro("x",ULit(huge)),),UReplace("x",UAdd(UCurrent("x"),ULit(huge))))
    rp=resolve_program(spec); out=Evaluator(rp).run()
    assert place_value(rp,out,"x")==2*huge

# ---- Effect boundary / error propagation ----
def test_prior_completed_action_preserved_failed_action_uncommitted_later_suppressed():
    spec=ProgramSpec(
        (PlaceIntro("x",ULit(0)),PlaceIntro("a",ULit(5)),PlaceIntro("b",ULit(2)),PlaceIntro("z",ULit(0))),
        USequence((
            UReplace("x",ULit(7)),
            UReplace("z",USubtractFrom(UCurrent("a"),UCurrent("b"))),
            UReplace("x",ULit(99)),
        ))
    )
    rp=resolve_program(spec); out=Evaluator(rp).run()
    assert isinstance(out,ErrorOutcome) and out.error.code==ARITHMETIC_DOMAIN_ERROR
    assert place_value(rp,out,"x")==7
    assert place_value(rp,out,"z")==0

def test_preparation_underflow_prevents_principal():
    spec=ProgramSpec(
        (
            PlaceIntro("a",ULit(3)),
            PlaceIntro("b",ULit(2)),
            PlaceIntro("bad",USubtractFrom(UCurrent("a"),UCurrent("b"))),
            PlaceIntro("ran",ULit(0)),
        ),
        UReplace("ran",ULit(1))
    )
    rp=resolve_program(spec); out=Evaluator(rp).run()
    assert isinstance(out,ErrorOutcome)
    assert out.error.phase=="PREPARATION"
    ran=next(p for p in rp.places if p.spelling=="ran")
    assert ran not in out.state.as_dict()

# ---- Program preparation/principal ----
def test_preparation_establishes_initial_state():
    spec=ProgramSpec(
        (PlaceIntro("a",ULit(4)),PlaceIntro("b",UAdd(UCurrent("a"),ULit(3)))),
        UReplace("a",UCurrent("a"))
    )
    rp=resolve_program(spec); out=Evaluator(rp).run()
    assert isinstance(out,NormalOutcome)
    assert place_value(rp,out,"a")==4 and place_value(rp,out,"b")==7

def test_preparation_act_definition_does_not_perform():
    spec=ProgramSpec(
        (PlaceIntro("x",ULit(0)),ActIntro("f"),BodyDef("f",UReplace("x",ULit(9)))),
        UReplace("x",ULit(1))
    )
    rp=resolve_program(spec); out=Evaluator(rp).run()
    assert place_value(rp,out,"x")==1

def test_principal_explicit_sequence_normal_completion():
    spec=ProgramSpec(
        (PlaceIntro("x",ULit(0)),),
        USequence((UReplace("x",ULit(1)),UReplace("x",UAdd(UCurrent("x"),ULit(1)))))
    )
    rp=resolve_program(spec); out=Evaluator(rp).run()
    assert isinstance(out,NormalOutcome) and place_value(rp,out,"x")==2

def test_single_principal_run_not_implicit_top_level_execution():
    spec=ProgramSpec(
        (PlaceIntro("x",ULit(0)),ActIntro("f"),BodyDef("f",UReplace("x",UAdd(UCurrent("x"),ULit(1))))),
        UPerform("f")
    )
    rp=resolve_program(spec); out=Evaluator(rp).run()
    assert place_value(rp,out,"x")==1

# ---- Visibility/static identity ----
def test_prior_place_reference_valid():
    resolve_program(ProgramSpec(
        (PlaceIntro("a",ULit(4)),PlaceIntro("b",UCurrent("a"))),
        UReplace("a",ULit(4))
    ))

def test_future_place_reference_invalid():
    assert_invalid(REFERENCE_BEFORE_INTRODUCTION, lambda: resolve_program(ProgramSpec(
        (PlaceIntro("a",UCurrent("b")),PlaceIntro("b",ULit(1))),
        UReplace("b",ULit(1))
    )))

def test_place_self_initializer_invalid():
    assert_invalid(REFERENCE_BEFORE_INTRODUCTION, lambda: resolve_program(ProgramSpec(
        (PlaceIntro("x",UCurrent("x")),),
        UReplace("x",ULit(1))
    )))

def test_same_spelling_different_kinds_distinct():
    spec=ProgramSpec(
        (PlaceIntro("same",ULit(0)),ActIntro("same"),BodyDef("same",UReplace("same",ULit(2)))),
        UPerform("same")
    )
    rp=resolve_program(spec)
    p=next(x for x in rp.places if x.spelling=="same")
    a=next(x.act for x in rp.acts if x.act.spelling=="same")
    assert p.kind=="place" and a.kind=="act" and p!=a
    out=Evaluator(rp).run()
    assert place_value(rp,out,"same")==2

def test_duplicate_place_rejected():
    assert_invalid(DUPLICATE_PLACE, lambda: resolve_program(ProgramSpec(
        (PlaceIntro("x",ULit(0)),PlaceIntro("x",ULit(1))),
        UReplace("x",ULit(2))
    )))

def test_duplicate_act_rejected():
    assert_invalid(DUPLICATE_ACT, lambda: resolve_program(ProgramSpec(
        (ActIntro("f"),ActIntro("f")),
        UPerform("f")
    )))

def test_duplicate_role_rejected():
    assert_invalid(DUPLICATE_ROLE, lambda: resolve_program(ProgramSpec(
        (ActIntro("f"),RoleIntro("f","n"),RoleIntro("f","n"),BodyDef("f",UProduce(ULit(1)))),
        UPerform("f",(("n",ULit(0)),))
    )))

def test_duplicate_body_rejected():
    assert_invalid(DUPLICATE_BODY, lambda: resolve_program(ProgramSpec(
        (ActIntro("f"),BodyDef("f",UProduce(ULit(1))),BodyDef("f",UProduce(ULit(1)))),
        UPerform("f")
    )))

# ---- recursion and roles ----
def test_self_recursion_valid_and_diverges_under_harness():
    spec=ProgramSpec(
        (ActIntro("f"),BodyDef("f",UPerform("f"))),
        UPerform("f")
    )
    out=build(spec,fuel=30).run()
    assert isinstance(out,DivergenceOutcome)

def test_mutual_recursion_with_prior_introductions_valid():
    spec=ProgramSpec(
        (ActIntro("a"),ActIntro("b"),BodyDef("a",UPerform("b")),BodyDef("b",UPerform("a"))),
        UPerform("a")
    )
    out=build(spec,fuel=30).run()
    assert isinstance(out,DivergenceOutcome)

def test_mutual_recursion_future_identity_invalid():
    assert_invalid(REFERENCE_BEFORE_INTRODUCTION, lambda: resolve_program(ProgramSpec(
        (ActIntro("a"),BodyDef("a",UPerform("b")),ActIntro("b"),BodyDef("b",UPerform("a"))),
        UPerform("a")
    )))

def test_role_association_is_occurrence_specific():
    # rec(n): if n=0 produce 0, else perform rec(n-1).
    spec=ProgramSpec(
        (
            ActIntro("rec"),
            RoleIntro("rec","n"),
            BodyDef("rec",
                UConditional(
                    UEqual(URoleValue("rec","n"),ULit(0)),
                    UProduce(ULit(0)),
                    UPerform("rec",(("n",USubtractFrom(ULit(1),URoleValue("rec","n"))),))
                )
            ),
        ),
        UPerform("rec",(("n",ULit(5)),))
    )
    ev=build(spec,fuel=100)
    out=ev.run()
    assert isinstance(out,NormalOutcome)
    # same RoleId serial, values are occurrence-specific 5..0
    vals=[pairs[0][1] for _,_,pairs in ev.occurrence_log]
    role_ids=[pairs[0][0] for _,_,pairs in ev.occurrence_log]
    assert vals==[5,4,3,2,1,0]
    assert len(set(role_ids))==1

def test_role_value_outside_occurrence_invalid():
    assert_invalid(ROLE_VALUE_OUTSIDE_PERFORMANCE, lambda: resolve_program(ProgramSpec(
        (ActIntro("f"),RoleIntro("f","n"),BodyDef("f",UProduce(URoleValue("f","n")))),
        UReplace("dummy",URoleValue("f","n"))
    )))

# ---- output/provenance/completion ----
def test_role_value_outside_occurrence_invalid():
    assert_invalid(ROLE_VALUE_OUTSIDE_PERFORMANCE, lambda: resolve_program(ProgramSpec(
        (
            PlaceIntro("dummy",ULit(0)),
            ActIntro("f"),RoleIntro("f","n"),BodyDef("f",UProduce(URoleValue("f","n")))
        ),
        UReplace("dummy",URoleValue("f","n"))
    )))

def test_output_nonterminal_then_state_action():
    spec=ProgramSpec(
        (
            PlaceIntro("x",ULit(0)),
            ActIntro("f"),
            BodyDef("f",USequence((UProduce(ULit(7)),UReplace("x",ULit(1)))))
        ),
        UPerform("f")
    )
    rp=resolve_program(spec); out=Evaluator(rp).run()
    assert isinstance(out,NormalOutcome)
    assert place_value(rp,out,"x")==1
    assert [p.value for p in out.productions]==[7]

def test_immediate_result_provenance():
    spec=ProgramSpec(
        (
            PlaceIntro("x",ULit(0)),
            ActIntro("child"), BodyDef("child",UProduce(ULit(12))),
            ActIntro("parent"), BodyDef("parent",
                USequence((UPerform("child"),UProduce(URecentResult("child"))))
            )
        ),
        UPerform("parent")
    )
    out=build(spec).run()
    assert isinstance(out,NormalOutcome)
    assert [(p.act.spelling,p.value) for p in out.productions]==[("child",12),("parent",12)]

def test_stale_provenance_runtime_fallback_error():
    spec=ProgramSpec(
        (
            PlaceIntro("x",ULit(0)),
            ActIntro("child"), BodyDef("child",UProduce(ULit(12))),
            ActIntro("parent"), BodyDef("parent",
                USequence((UPerform("child"),UReplace("x",ULit(1)),UProduce(URecentResult("child"))))
            )
        ),
        UPerform("parent")
    )
    out=build(spec).run()
    assert isinstance(out,ErrorOutcome) and out.error.code==RESULT_PROVENANCE_ERROR
    assert place_value(resolve_program(spec),out,"x")==1

def test_no_output_result_reference_runtime_fallback_error():
    spec=ProgramSpec(
        (
            ActIntro("child"), BodyDef("child",UFixedRepeat(0,UPerform("child"))),
            ActIntro("parent"), BodyDef("parent",USequence((UPerform("child"),UProduce(URecentResult("child")))))
        ),
        UPerform("parent")
    )
    out=build(spec,fuel=100).run()
    assert isinstance(out,ErrorOutcome) and out.error.code==RESULT_PROVENANCE_ERROR

def test_finite_act_and_whole_program_normal_completion():
    spec=ProgramSpec(
        (PlaceIntro("x",ULit(0)),ActIntro("f"),BodyDef("f",UReplace("x",ULit(4)))),
        UPerform("f")
    )
    out=build(spec).run()
    assert isinstance(out,NormalOutcome)

# ---- trace ----
def test_trace_nonobservable():
    spec=ProgramSpec(
        (PlaceIntro("x",ULit(0)),),
        USequence((UReplace("x",ULit(1)),UReplace("x",ULit(2))))
    )
    rp=resolve_program(spec)
    a=Evaluator(rp,debug_trace=False); oa=a.run()
    b=Evaluator(rp,debug_trace=True); ob=b.run()
    assert observable(oa)==observable(ob)
    assert a.trace==[] and len(b.trace)>0

# ---- recurrence ----
def test_post_action_checkpoint_first_action_always_occurs():
    spec=ProgramSpec(
        (PlaceIntro("x",ULit(0)),),
        UPostActionUntil(UReplace("x",UAdd(UCurrent("x"),ULit(1))),UEqual(ULit(0),ULit(0)))
    )
    rp=resolve_program(spec); out=Evaluator(rp).run()
    assert place_value(rp,out,"x")==1

def test_decrement_recurrence_stays_in_naturals():
    spec=ProgramSpec(
        (PlaceIntro("x",ULit(5)),),
        UPostActionUntil(UReplace("x",USubtractFrom(ULit(1),UCurrent("x"))),UEqual(UCurrent("x"),ULit(0)))
    )
    rp=resolve_program(spec); out=Evaluator(rp).run()
    assert isinstance(out,NormalOutcome) and place_value(rp,out,"x")==0

TESTS=[
 test_numeric_3_minus_2,
 test_numeric_3_minus_3,
 test_static_underflow_rejected,
 test_dynamic_underflow_runtime_error_and_target_unchanged,
 test_no_negative_literal,
 test_huge_natural_exactness,
 test_prior_completed_action_preserved_failed_action_uncommitted_later_suppressed,
 test_preparation_underflow_prevents_principal,
 test_preparation_establishes_initial_state,
 test_preparation_act_definition_does_not_perform,
 test_principal_explicit_sequence_normal_completion,
 test_single_principal_run_not_implicit_top_level_execution,
 test_prior_place_reference_valid,
 test_future_place_reference_invalid,
 test_place_self_initializer_invalid,
 test_same_spelling_different_kinds_distinct,
 test_duplicate_place_rejected,
 test_duplicate_act_rejected,
 test_duplicate_role_rejected,
 test_duplicate_body_rejected,
 test_self_recursion_valid_and_diverges_under_harness,
 test_mutual_recursion_with_prior_introductions_valid,
 test_mutual_recursion_future_identity_invalid,
 test_role_association_is_occurrence_specific,
 test_role_value_outside_occurrence_invalid,
 test_output_nonterminal_then_state_action,
 test_immediate_result_provenance,
 test_stale_provenance_runtime_fallback_error,
 test_no_output_result_reference_runtime_fallback_error,
 test_finite_act_and_whole_program_normal_completion,
 test_trace_nonobservable,
 test_post_action_checkpoint_first_action_always_occurs,
 test_decrement_recurrence_stays_in_naturals,
]

if __name__=="__main__":
    for t in TESTS:
        t()
        print("PASS",t.__name__)
    print(f"B12 SEMANTIC TESTS: PASS ({len(TESTS)} tests)")
