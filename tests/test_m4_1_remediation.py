from __future__ import annotations

import dataclasses
import io
import json
import subprocess
import sys
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

import pytest

from compiler.api import check, compile_source, run_reference, run_source
from compiler.artifact.format import ArtifactVerificationError, serialize_artifact, verify_artifact
from compiler.backend.portable import PortableVM, VMNormal, VMResourceExhaustion, execute_ir
from compiler.cli.main import main as cli_main
from compiler.models import ir as I
from compiler.runtime.ir_reference import IRReferenceEvaluator, IRReferenceNormal, IRReferenceResourceExhaustion, execute_reference_ir
from compiler.runtime.observables import (
    backend_debug_internal_state,
    backend_observable,
    ir_reference_observable,
    reference_observable,
)
from compiler.runtime.reference import ReferenceEvaluator, NormalOutcome, ResourceExhaustionOutcome, execute_reference
from compiler.version import LANGUAGE_EDITION

ROOT = Path(__file__).resolve().parents[1]
ZERO = "המספר הנחשב בגרע את המספר אשר הוא אחד מן המספר אשר הוא אחד"

def num(n:int)->str:
    if n == 0: return ZERO
    from compiler.parse.numeral_lexicons import A12_DIRECT_NUMERALS
    if n <= 9999:
        return f"המספר אשר הוא {A12_DIRECT_NUMERALS[n]}"
    # A13 productive magnitude is expressed by recursively composing the already
    # normative pure addition form; this is test-source construction, not a new literal.
    q, r = divmod(n, 9999)
    parts = [f"המספר אשר הוא {A12_DIRECT_NUMERALS[9999]}"] * q
    if r:
        parts.append(f"המספר אשר הוא {A12_DIRECT_NUMERALS[r]}")
    expr = parts[0]
    for part in parts[1:]:
        expr = add(part, expr)
    return expr
def place_intro(name,n): return f"יהי מקום ושמו {name} ובמקום אשר שמו {name} יהי {num(n)} לבדו"
def current(name): return f"המספר אשר במקום אשר שמו {name}"
def replace(name,v): return f"שים במקום אשר שמו {name} את {v} תחת המספר אשר במקום אשר שמו {name}"
def add(a,b): return f"המספר הנחשב בהוסיף את {a} על {b}"
def sub(a,b): return f"המספר הנחשב בגרע את {a} מן {b}"
def eq(a,b): return f"{a} הוא {b}"
def act(a): return f"יהי מעשה ושמו {a}"
def perform(a): return f"עשה את המעשה אשר שמו {a}"
def body(a,x): return f"זה דבר המעשה אשר שמו {a} {x} עד הנה דבר המעשה אשר שמו {a}"
def output(v): return f"הוצא מן המעשה הזה את {v}"
def role_decl(a,r): return f"יהי במעשה אשר שמו {a} דבר ושמו {r} ובעשות את המעשה אשר שמו {a} יעמד מספר תחת הדבר אשר במעשה אשר שמו {a} שמו {r}"
def role_val(a,r): return f"המספר אשר במעשה הזה עומד תחת הדבר אשר במעשה אשר שמו {a} שמו {r}"
def assoc(a,r,v,first=True): return f"{'בהיות' if first else 'ובהיות'} {v} תחת הדבר אשר במעשה אשר שמו {a} שמו {r}"
def perform_roles(a, pairs): return " ".join([perform(a)] + [assoc(a,r,v,i==0) for i,(r,v) in enumerate(pairs)])
def deep_countdown(n:int)->str:
    return " ".join([
        place_intro("גד",n),act("ראובן"),act("שמעון"),act("יהודה"),
        body("ראובן",f"אם {eq(current('גד'),ZERO)} {perform('יהודה')} ואם לא {perform('שמעון')}"),
        body("שמעון",replace("גד",sub(num(1),current("גד")))+" ואחרי כן "+perform("ראובן")),
        body("יהודה",replace("גד",current("גד"))),
        "ועתה "+perform("ראובן")])
def role_caller_source()->str:
    A,B,ra,rb="ראובן","שמעון","לוי","עזר"
    return " ".join([act(A),act(B),role_decl(A,ra),role_decl(B,rb),
        body(A,perform_roles(B,[(rb,role_val(A,ra))])),
        body(B,output(role_val(B,rb))),
        "ועתה "+perform_roles(A,[(ra,num(5))])])
def recursive_role_source()->str:
    A,B,C,rn,rm="ראובן","שמעון","יהודה","לוי","עזר"
    return " ".join([place_intro("גד",0),act(A),act(B),act(C),role_decl(A,rn),role_decl(B,rm),
        body(A,f"אם {eq(role_val(A,rn),ZERO)} {perform(C)} ואם לא {perform_roles(B,[(rm,role_val(A,rn))])}"),
        body(B,perform_roles(A,[(rn,sub(num(1),role_val(B,rm)))])+" ואחרי כן "+replace("גד",role_val(B,rm))),
        body(C,replace("גד",current("גד"))),
        "ועתה "+perform_roles(A,[(rn,num(5))])])


def three(source, fuel=None):
    c=compile_source(source); assert c.valid, [d.to_dict() for d in c.diagnostics]
    h=execute_reference(c.hast,fuel=fuel); i=execute_reference_ir(c.ir,fuel=fuel); b=execute_ir(c.ir,fuel=fuel)
    return c,reference_observable(h),ir_reference_observable(i),backend_observable(b)


def test_e_find_023_iterative_recursion_depths_and_cleanup():
    for depth in (300,1000):
        c=compile_source(deep_countdown(depth)); assert c.valid
        rh=ReferenceEvaluator(c.hast); h=rh.run()
        ri=IRReferenceEvaluator(c.ir); i=ri.run()
        vm=PortableVM(c.ir); b=vm.run()
        assert isinstance(h,NormalOutcome); assert isinstance(i,IRReferenceNormal); assert isinstance(b,VMNormal)
        assert rh.active_performances == ri.active_performances == vm.active_performances == 0
        assert reference_observable(h)==ir_reference_observable(i)==backend_observable(b)

def test_e_find_023_execution_survives_low_host_recursion_limit():
    code = r'''import sys
from compiler.api import compile_source
from compiler.runtime.reference import execute_reference
from compiler.runtime.ir_reference import execute_reference_ir
from compiler.backend.portable import execute_ir
from tests.test_m4_1_remediation import deep_countdown
c=compile_source(deep_countdown(300)); assert c.valid
sys.setrecursionlimit(80)
assert type(execute_reference(c.hast)).__name__ == "NormalOutcome"
assert type(execute_reference_ir(c.ir)).__name__ == "IRReferenceNormal"
assert type(execute_ir(c.ir)).__name__ == "VMNormal"
print("PASS")'''
    p=subprocess.run([sys.executable,"-c",code],cwd=ROOT,text=True,capture_output=True,env={**__import__('os').environ,"PYTHONPATH":str(ROOT)})
    assert p.returncode==0,(p.stdout,p.stderr); assert p.stdout.strip()=="PASS"; assert "RecursionError" not in p.stderr

def test_e_find_023_no_fuel_has_no_artificial_quota_and_cli_firewall():
    data=json.loads((ROOT/'tests/fixtures/a13/a13_program_conformance.json').read_text(encoding='utf-8'))
    source=next(x['source'] for x in data['positive'] if x['id']=='P-SELFREC-001')
    sf=ROOT/'tests/fixtures/m4_2_selfrec_tmp.txt'; sf.write_text(source,encoding='utf-8')
    code = f"from pathlib import Path;from compiler.api import compile_source;from compiler.backend.portable import execute_ir;s=Path({str(sf)!r}).read_text(encoding='utf-8');c=compile_source(s);execute_ir(c.ir);print('TERMINATED')"
    try:
        with pytest.raises(subprocess.TimeoutExpired):
            subprocess.run([sys.executable,'-c',code],cwd=ROOT,env={**__import__('os').environ,'PYTHONPATH':str(ROOT)},text=True,capture_output=True,timeout=0.75)
    finally:
        sf.unlink(missing_ok=True)
    # Public CLI has a stable exception firewall: no traceback on an injected host failure.
    err=io.StringIO()
    with mock.patch('compiler.cli.main.api.check',side_effect=RecursionError('injected')), redirect_stderr(err):
        rc=cli_main(['check','-'])
    assert rc==70; text=err.getvalue(); assert 'TOOL_INTERNAL_FAILURE' in text; assert 'Traceback' not in text

def _artifact_bad_cases():
    base=compile_source(" ".join([place_intro('גד',1),act('ראובן'),body('ראובן',output(num(1))),'ועתה '+perform('ראובן')]))
    assert base.valid; ir=base.ir; sp=ir.source_span
    place=next(s.serial for s in ir.symbols if s.kind=='place'); actid=next(s.serial for s in ir.symbols if s.kind=='act')
    yield 'output-outside-performance',dataclasses.replace(ir,principal=I.IRProduceResult(sp,I.IRNatural(sp,1)))
    yield 'self-initializer',dataclasses.replace(ir,initial_facts=(I.IRInitialFact(sp,place,I.IRReadCurrentFact(sp,place)),))
    ad=ir.acts[0]; yield 'two-outputs-same-path',dataclasses.replace(ir,acts=(dataclasses.replace(ad,body=I.IRThen(sp,(I.IRProduceResult(sp,I.IRNatural(sp,1)),I.IRProduceResult(sp,I.IRNatural(sp,2))))),))
    yield 'recent-result-in-initializer',dataclasses.replace(ir,initial_facts=(I.IRInitialFact(sp,place,I.IRRecentResult(sp,actid)),))
    yield 'static-constant-underflow',dataclasses.replace(ir,principal=I.IRReplaceCurrentFact(sp,place,I.IRCheckedSubtractNatural(sp,I.IRNatural(sp,3),I.IRNatural(sp,2))))
    yield 'output-in-fixed-recurrence',dataclasses.replace(ir,acts=(dataclasses.replace(ad,body=I.IRFixedRecurrence(sp,3,I.IRProduceResult(sp,I.IRNatural(sp,1)))),))
    c2=compile_source(" ".join([place_intro('גד',1),place_intro('עזר',2),'ועתה '+replace('גד',num(1))])); p1,p2=[s.serial for s in c2.ir.symbols if s.kind=='place']
    yield 'forward-initializer-read',dataclasses.replace(c2.ir,initial_facts=(I.IRInitialFact(c2.ir.source_span,p1,I.IRReadCurrentFact(c2.ir.source_span,p2)),c2.ir.initial_facts[1]))
    A,B,r1,r2='ראובן','שמעון','לוי','יהודה'
    s=" ".join([act(A),role_decl(A,r1),body(A,output(role_val(A,r1))),act(B),role_decl(B,r2),body(B,output(role_val(B,r2))),'ועתה '+perform_roles(A,[(r1,num(1))])])
    c3=compile_source(s); sy={x.spelling:x.serial for x in c3.ir.symbols if x.kind=='role'}
    actA=next(x for x in c3.ir.acts if next(z for z in c3.ir.symbols if z.serial==x.act).spelling==A)
    badbody=I.IRProduceResult(c3.ir.source_span,I.IRReadRoleNumber(c3.ir.source_span,sy[r2]))
    yield 'wrong-owner-role-read',dataclasses.replace(c3.ir,acts=tuple(dataclasses.replace(x,body=badbody) if x.act==actA.act else x for x in c3.ir.acts))

def test_e_find_024_all_eight_semantic_artifact_cases_rejected():
    for name,bad in _artifact_bad_cases():
        with pytest.raises(ArtifactVerificationError), pytest.raises(Exception) if False else _nullcontext():
            verify_artifact(serialize_artifact(bad,language_edition=LANGUAGE_EDITION))

class _nullcontext:
    def __enter__(self): return self
    def __exit__(self,*a): return False

def test_e_find_025_caller_role_value_and_recursive_isolation():
    _,h,i,b=three(role_caller_source()); assert h==i==b; assert h['products']==[['שמעון',5]]
    _,h,i,b=three(recursive_role_source(),fuel=500); assert h==i==b; assert dict(h['facts'])['גד']==5

def test_e_find_021_public_quotient_erases_serials_but_debug_retains_them():
    p1=" ".join([place_intro('גד',1),'ועתה '+replace('גד',num(2))])
    unused=" ".join([act('ראובן'),body('ראובן',output(num(7)))])
    p2=" ".join([unused,place_intro('גד',1),'ועתה '+replace('גד',num(2))])
    c1=compile_source(p1); c2=compile_source(p2); b1=execute_ir(c1.ir); b2=execute_ir(c2.ir)
    assert backend_observable(b1)==backend_observable(b2)=={'outcome':'Normal','facts':[['גד',2]],'products':[]}
    # Occurrence numbering can differ internally without changing language observation.
    pre=act('שמעון')+' '+body('שמעון',replace('גד',current('גד'))); A=act('ראובן')+' '+body('ראובן',output(num(5)))
    x1=compile_source(' '.join([place_intro('גד',1),pre,A,'ועתה '+perform('ראובן')]))
    x2=compile_source(' '.join([place_intro('גד',1),pre,A,'ועתה '+perform('שמעון')+' ואחרי כן '+perform('ראובן')]))
    o1,o2=execute_ir(x1.ir),execute_ir(x2.ir)
    assert backend_observable(o1)==backend_observable(o2)
    assert backend_debug_internal_state(o1)!=backend_debug_internal_state(o2)

def test_e_find_022_name_slot_is_not_principal_marker():
    source=' '.join([act('ועתה'),body('ועתה',output(num(1)))])
    c=check(source); assert not c.valid
    codes=[d.code for d in c.diagnostics]; assert 'PROG0001' in codes; assert 'PROG0002' not in codes

def test_public_run_source_maps_unexpected_backend_exception_to_tooling_failure():
    source=place_intro('גד',1)+' ועתה '+replace('גד',num(2))
    with mock.patch('compiler.api.execute_ir',side_effect=ValueError('host detail must not escape')):
        r=run_source(source)
    assert r.compilation.valid
    o=backend_observable(r.outcome)
    assert o=={'tooling_status':'InternalFailure','category':'IMPLEMENTATION_INTERNAL_FAILURE','host_exception_type':'ValueError'}
