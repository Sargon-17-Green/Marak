#!/usr/bin/env python3
from b12_reference_core import *

def tiny_countdown(start):
    spec=ProgramSpec(
      (
        PlaceIntro("R",ULit(start)),PlaceIntro("sink",ULit(0)),
        ActIntro("L"),ActIntro("H"),ActIntro("D"),
        BodyDef("L",UConditional(UEqual(UCurrent("R"),ULit(0)),UPerform("H"),UPerform("D"))),
        BodyDef("H",UReplace("sink",UCurrent("sink"))),
        BodyDef("D",USequence((UReplace("R",USubtractFrom(ULit(1),UCurrent("R"))),UPerform("L")))),
      ),
      UPerform("L")
    )
    rp=resolve_program(spec)
    ev=Evaluator(rp,fuel=10000)
    out=ev.run()
    R=next(p for p in rp.places if p.spelling=="R")
    sink=next(p for p in rp.places if p.spelling=="sink")
    return out,out.state.get(R),out.state.get(sink),rp

def test_halt_normal_completion_and_projection():
    for n in range(0,128):
        out,r,sink,rp=tiny_countdown(n)
        assert isinstance(out,NormalOutcome)
        assert r==0
        assert sink==0 # state-preserving proof sink
    print("RM COUNTDOWN CASES: 128")

def test_decjz_underflow_guard():
    # Start at zero: helper D is never performed; no subtraction underflow.
    out,r,sink,_=tiny_countdown(0)
    assert isinstance(out,NormalOutcome) and r==0
    # Positive starts can only invoke D while R>0.
    for n in range(1,65):
        out,r,sink,_=tiny_countdown(n)
        assert isinstance(out,NormalOutcome) and r==0
    print("RM UNDERFLOW-GUARD CASES: 65")

if __name__=="__main__":
    test_halt_normal_completion_and_projection()
    print("PASS test_halt_normal_completion_and_projection")
    test_decjz_underflow_guard()
    print("PASS test_decjz_underflow_guard")
    print("B12 RM WITNESS: PASS")
