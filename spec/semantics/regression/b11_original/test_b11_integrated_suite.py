#!/usr/bin/env python3
from b11_reference_core import *

def state(**pairs):
    s=Snapshot.empty()
    refs={}
    for k,v in pairs.items():
        r=Referent(k); refs[k]=r; s=s.establish(r,Integer(v))
    return s,refs

def test_state_without_cells():
    s,r=state(x=5,y=5)
    s2=s.replace(r["x"],Integer(9))
    assert s.query(r["x"])==Integer(5)
    assert s2.query(r["x"])==Integer(9)
    assert s2.query(r["y"])==Integer(5)

def test_exact_huge_arithmetic_and_negative_subtraction():
    rt=Runtime()
    s=Snapshot.empty()
    a=10**700
    assert rt.denote(Add(Lit(a),Lit(a)),s)==Integer(2*a)
    assert rt.denote(Sub(Lit(9),Lit(4)),s)==Integer(5)  # 4-9? Wait semantics is a-b in evaluator
    assert rt.denote(Sub(Lit(4),Lit(9)),s)==Integer(-5)

def test_conditional_no_boolean_value():
    s,r=state(x=0)
    rt=Runtime()
    u=Conditional(Zero(Current(r["x"])),Replace(r["x"],Lit(8)),Replace(r["x"],Lit(99)))
    s2,_=rt.exec_unit(u,s)
    assert s2.query(r["x"])==Integer(8)

def test_fixed_repeat():
    s,r=state(x=1)
    rt=Runtime()
    u=FixedRepeat(7,Replace(r["x"],Add(Current(r["x"]),Lit(1))))
    s2,_=rt.exec_unit(u,s)
    assert s2.query(r["x"])==Integer(8)

def test_post_action_recurrence_is_at_least_once():
    s,r=state(x=0)
    rt=Runtime()
    u=PostRepeatUntil(Replace(r["x"],Add(Current(r["x"]),Lit(1))),Equal(Current(r["x"]),Lit(1)))
    s2,_=rt.exec_unit(u,s)
    assert s2.query(r["x"])==Integer(1)

def test_post_action_recurrence_decrement():
    s,r=state(x=9)
    rt=Runtime()
    u=PostRepeatUntil(Replace(r["x"],Sub(Current(r["x"]),Lit(1))),Zero(Current(r["x"])))
    s2,_=rt.exec_unit(u,s)
    assert s2.query(r["x"])==Integer(0)

def test_named_roles_order_invariant_and_output_nonterminal():
    s,r=state(g=0)
    acts={
      "f":ActDef(frozenset({"a","b"}),(
          Produce(Add(RoleNum("a"),RoleNum("b"))),
          Replace(r["g"],Lit(7)),
      ))
    }
    rt=Runtime(acts)
    o1=rt.perform("f",(("a",Lit(2)),("b",Lit(3))),s)
    o2=rt.perform("f",(("b",Lit(3)),("a",Lit(2))),s)
    assert o1.result==o2.result==Integer(5)
    assert o1.state.query(r["g"])==Integer(7)

def test_zero_or_one_output_profile():
    acts={
      "none":ActDef(frozenset(),(NoOp(),)),
      "two":ActDef(frozenset(),(Produce(Lit(1)),Produce(Lit(2)))),
    }
    rt=Runtime(acts)
    assert rt.perform("none",tuple(),Snapshot.empty()).result is None
    try:
        rt.perform("two",tuple(),Snapshot.empty())
    except SourceInvalid as e:
        assert "second output" in str(e)
    else:
        raise AssertionError("A12 second output accepted")

def test_immediate_result_context_expires():
    s,r=state(x=0)
    acts={
      "child":ActDef(frozenset(),(Produce(Lit(12)),)),
      "good":ActDef(frozenset(),(Perform("child"),Produce(RecentResult("child")))),
      "bad":ActDef(frozenset(),(
          Perform("child"),
          Replace(r["x"],Lit(1)),
          Produce(RecentResult("child")),
      ))
    }
    rt=Runtime(acts)
    assert rt.perform("good",tuple(),s).result==Integer(12)
    try:
        rt.perform("bad",tuple(),s)
    except ProductReferenceError:
        pass
    else:
        raise AssertionError("stale result accepted")

def test_multiplication_semantic_example():
    # General semantic example, using exact B numeric operation.
    rt=Runtime()
    assert rt.denote(Mul(Lit(123456789),Lit(987654321)),Snapshot.empty()) == Integer(123456789*987654321)

def test_factorial_semantic_example():
    # Use explicit state + post-action recurrence; multiplication is B numeric foundation.
    s,r=state(n=10,acc=1)
    rt=Runtime()
    step=Perform("factstep")
    rt.acts["factstep"]=ActDef(frozenset(),(
        Replace(r["acc"],Mul(Current(r["acc"]),Current(r["n"]))),
        Replace(r["n"],Sub(Current(r["n"]),Lit(1))),
    ))
    u=PostRepeatUntil(step,Zero(Current(r["n"])))
    s2,_=rt.exec_unit(u,s)
    assert s2.query(r["acc"])==Integer(3628800)

def test_gcd_semantic_example():
    # B numeric foundation Rem; not an A12 surface primitive.
    s,r=state(a=1071,b=462)
    rt=Runtime()
    while s.query(r["b"]).value != 0:
        rem=rt.denote(Rem(Current(r["a"]),Current(r["b"])),s)
        s=s.replace(r["a"],s.query(r["b"]))
        s=s.replace(r["b"],rem)
    assert s.query(r["a"])==Integer(21)

def test_fibonacci_semantic_example():
    s,r=state(a=0,b=1,i=0,n=30,tmp=0)
    acts={}
    rt=Runtime(acts)
    rt.acts["fibstep"]=ActDef(frozenset(),(
        Replace(r["tmp"],Add(Current(r["a"]),Current(r["b"]))),
        Replace(r["a"],Current(r["b"])),
        Replace(r["b"],Current(r["tmp"])),
        Replace(r["i"],Add(Current(r["i"]),Lit(1))),
    ))
    # Post-action recurrence is fine because n=30>0.
    u=PostRepeatUntil(Perform("fibstep"),Equal(Current(r["i"]),Current(r["n"])))
    s2,_=rt.exec_unit(u,s)
    assert s2.query(r["a"])==Integer(832040)

def rm_transfer(start_r,start_s):
    s,ref=state(R=start_r,S=start_s)
    rt=Runtime()
    rt.acts.update({
      "L0":ActDef(frozenset(),(
        Conditional(
          Zero(Current(ref["R"])),
          Perform("HALT"),
          Perform("DEC")
        ),
      )),
      "DEC":ActDef(frozenset(),(
        Replace(ref["R"],Sub(Current(ref["R"]),Lit(1))),
        Perform("INC"),
      )),
      "INC":ActDef(frozenset(),(
        Replace(ref["S"],Add(Current(ref["S"]),Lit(1))),
        Perform("L0"),
      )),
      "HALT":ActDef(frozenset(),(
        Produce(Current(ref["S"])),
      )),
    })
    # Child HALT output is intentionally not auto-forwarded.
    # The witness observes final machine state after recursive performance unwinds.
    out=rt.perform("L0",tuple(),s)
    return out.state.query(ref["R"]).value,out.state.query(ref["S"]).value

def test_register_machine_mapping_grid():
    for r0 in range(0,18):
        for s0 in range(0,18):
            r,s=rm_transfer(r0,s0)
            assert (r,s)==(0,r0+s0)

TESTS=[
 test_state_without_cells,
 test_exact_huge_arithmetic_and_negative_subtraction,
 test_conditional_no_boolean_value,
 test_fixed_repeat,
 test_post_action_recurrence_is_at_least_once,
 test_post_action_recurrence_decrement,
 test_named_roles_order_invariant_and_output_nonterminal,
 test_zero_or_one_output_profile,
 test_immediate_result_context_expires,
 test_multiplication_semantic_example,
 test_factorial_semantic_example,
 test_gcd_semantic_example,
 test_fibonacci_semantic_example,
 test_register_machine_mapping_grid,
]

if __name__=="__main__":
    for t in TESTS:
        t()
        print("PASS",t.__name__)
    print(f"B11 INTEGRATED SUITE: PASS ({len(TESTS)} tests)")
    print("RM GRID CASES: 324")
