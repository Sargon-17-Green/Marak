from __future__ import annotations

from compiler.api import compile_source
from compiler.backend.portable import execute_ir
from compiler.models.domains import ProgramInputId, SymbolDomainId, SymbolMemberId
from compiler.models.values import NaturalValue, SymbolValue
from compiler.runtime.invocation import (
    DUPLICATE_INPUT_BINDING, EXTRA_INPUT_BINDING, INPUT_DOMAIN_MISMATCH,
    MISSING_INPUT_BINDING, InputBinding, InvalidInvocation, ValidatedInvocation,
    validate_invocation,
)
from compiler.runtime.ir_reference import execute_reference_ir
from compiler.runtime.observables import backend_observable, ir_reference_observable, reference_observable
from compiler.runtime.reference import execute_reference
from tests.test_c5_2_surface_pipeline import act, body, current, num, output, perform, replace_nat


def input_nat(role: str) -> str:
    return (
        f"יהי למלאכה הזאת דבר ושמו {role} "
        f"ובטרם תחל המלאכה הזאת יעמד מספר "
        f"תחת הדבר אשר למלאכה הזאת שמו {role}"
    )


def input_nat_ref(role: str) -> str:
    return f"המספר אשר עומד תחת הדבר אשר למלאכה הזאת שמו {role}"


def place_nat_value(place: str, value: str) -> str:
    return f"יהי מקום ושמו {place} ובמקום אשר שמו {place} יהי {value} לבדו"


def add(left: str, right: str) -> str:
    return f"המספר הנחשב בהוסיף את {left} על {right}"


def subtract(amount: str, source: str) -> str:
    return f"המספר הנחשב בגרע את {amount} מן {source}"


def input_id(compiled, spelling: str):
    return next(x.input_id for x in compiled.ir.program_input_domains if x.input_id.spelling == spelling)


def three(compiled, bindings):
    h = reference_observable(execute_reference(compiled.hast, bindings=bindings))
    i = ir_reference_observable(execute_reference_ir(compiled.ir, bindings=bindings))
    b = backend_observable(execute_ir(compiled.ir, bindings=bindings))
    assert h == i == b
    return b


def test_natural_input_is_available_to_preparation_initializer_before_principal():
    role="קלט"; target="יעד"
    src=" ".join([
        input_nat(role),
        place_nat_value(target,input_nat_ref(role)),
        "ועתה "+replace_nat(target,add(current(target),num(1))),
    ])
    c=compile_source(src)
    assert c.valid,[d.to_dict() for d in c.diagnostics]
    pid=input_id(c,role)
    obs=three(c,(InputBinding(pid,NaturalValue(41)),))
    assert dict(obs["facts"])[target]==42


def test_two_same_domain_inputs_bind_by_identity_not_order():
    left,right,target="ראשון","שני","יעד"
    src=" ".join([
        input_nat(left),input_nat(right),place_nat_value(target,num(1)),
        "ועתה "+replace_nat(target,add(input_nat_ref(left),input_nat_ref(right))),
    ])
    c=compile_source(src)
    assert c.valid,[d.to_dict() for d in c.diagnostics]
    a,b=input_id(c,left),input_id(c,right)
    forward=three(c,(InputBinding(a,NaturalValue(7)),InputBinding(b,NaturalValue(13))))
    reverse=three(c,(InputBinding(b,NaturalValue(13)),InputBinding(a,NaturalValue(7))))
    assert forward==reverse
    assert dict(forward["facts"])[target]==20


def test_natural_input_is_usable_in_principal_and_named_act_body():
    role="קלט"; target="יעד"; worker="פולט"
    src=" ".join([
        input_nat(role),place_nat_value(target,num(1)),
        act(worker),body(worker,output(input_nat_ref(role))),
        "ועתה "+replace_nat(target,input_nat_ref(role))+" ואחרי כן "+perform(worker),
    ])
    c=compile_source(src)
    assert c.valid,[d.to_dict() for d in c.diagnostics]
    pid=input_id(c,role)
    obs=three(c,(InputBinding(pid,NaturalValue(23)),))
    assert dict(obs["facts"])[target]==23
    assert obs["products"]==[[worker,23]]


def test_program_input_reads_remain_immutable_after_place_mutation():
    role="קלט"; target="יעד"
    src=" ".join([
        input_nat(role),place_nat_value(target,input_nat_ref(role)),
        "ועתה "+replace_nat(target,num(999))+" ואחרי כן "+replace_nat(target,input_nat_ref(role)),
    ])
    c=compile_source(src)
    assert c.valid,[d.to_dict() for d in c.diagnostics]
    pid=input_id(c,role)
    obs=three(c,(InputBinding(pid,NaturalValue(17)),))
    assert dict(obs["facts"])[target]==17


def test_invalid_invocation_precedes_preparation_and_has_exact_categories():
    role="קלט"; target="יעד"
    # With a valid binding of 2, Preparation evaluates 1-2 and raises the
    # existing ARITHMETIC_DOMAIN_ERROR. Invalid invocations must stop earlier.
    src=" ".join([
        input_nat(role),
        place_nat_value(target,subtract(input_nat_ref(role),num(1))),
        "ועתה "+replace_nat(target,num(1)),
    ])
    c=compile_source(src)
    assert c.valid,[d.to_dict() for d in c.diagnostics]
    pid=input_id(c,role)

    valid_error=backend_observable(execute_ir(c.ir,bindings=(InputBinding(pid,NaturalValue(2)),)))
    assert valid_error["outcome"]=="Error"
    assert valid_error["error"]["phase"]=="PREPARATION"

    foreign=ProgramInputId(999,"זר","foreign-program")
    symbol=SymbolValue(SymbolDomainId(800,"צבעים"),SymbolMemberId(1,"אדום"),"אדום")
    cases=[
        ((),[MISSING_INPUT_BINDING]),
        ((InputBinding(pid,NaturalValue(1)),InputBinding(foreign,NaturalValue(3))),[EXTRA_INPUT_BINDING]),
        ((InputBinding(pid,NaturalValue(1)),InputBinding(pid,NaturalValue(2))),[DUPLICATE_INPUT_BINDING]),
        ((InputBinding(pid,symbol),),[INPUT_DOMAIN_MISMATCH]),
    ]
    for bindings,codes in cases:
        observed=three(c,bindings)
        assert observed["outcome"]=="InvalidInvocation"
        assert [x["code"] for x in observed["issues"]]==codes


def test_cross_program_binding_and_validated_invocation_cannot_cross_owner_contract():
    role="קלט"; target="יעד"
    src_a=" ".join([input_nat(role),place_nat_value(target,num(1)),"ועתה "+replace_nat(target,input_nat_ref(role))])
    src_b=" ".join([input_nat(role),place_nat_value(target,num(2)),"ועתה "+replace_nat(target,add(input_nat_ref(role),num(1)))])
    a=compile_source(src_a); b=compile_source(src_b)
    assert a.valid and b.valid
    aid,bid=input_id(a,role),input_id(b,role)
    assert aid.serial==bid.serial and aid.spelling==bid.spelling
    assert aid.program_contract!=bid.program_contract

    binding=InputBinding(aid,NaturalValue(5))
    issues=validate_invocation(b.ir,(binding,))
    assert [x.code for x in issues]==[EXTRA_INPUT_BINDING,MISSING_INPUT_BINDING]

    validated=validate_invocation(a.ir,(binding,))
    assert isinstance(validated,ValidatedInvocation)
    for outcome,project in [
        (execute_reference(b.hast,bindings=validated),reference_observable),
        (execute_reference_ir(b.ir,bindings=validated),ir_reference_observable),
        (execute_ir(b.ir,bindings=validated),backend_observable),
    ]:
        obs=project(outcome)
        assert obs["outcome"]=="InvalidInvocation"
        assert [x["code"] for x in obs["issues"]]==[EXTRA_INPUT_BINDING,MISSING_INPUT_BINDING]


def test_no_input_program_keeps_zero_binding_execution_compatibility():
    target="יעד"
    src=" ".join([place_nat_value(target,num(1)),"ועתה "+replace_nat(target,num(2))])
    c=compile_source(src)
    assert c.valid,[d.to_dict() for d in c.diagnostics]
    assert not c.ir.program_input_domains
    obs=three(c,())
    assert dict(obs["facts"])[target]==2
