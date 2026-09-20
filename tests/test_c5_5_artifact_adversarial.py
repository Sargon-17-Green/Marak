from __future__ import annotations

import dataclasses
import hashlib
import json

import pytest

from compiler.api import compile_source
from compiler.artifact.format import ArtifactVerificationError, artifact_dict, verify_artifact
from compiler.models import ir as I
from compiler.models.domains import (
    BIDIRECTIONAL_INDEX, NATURAL, CollectionDomain, ProgramInputId,
    SymbolDomain, SymbolDomainId,
)
from compiler.models.program_contract import ir_program_contract_id, reowner_program_inputs
from tests.test_c5_2_surface_pipeline import member, num, place_typed, replace_nat, symbol_domain
from tests.test_c5_3_collections import place_book, replace_book
from tests.test_c5_5_program_inputs import input_nat, input_nat_ref
from tests.test_c5_5_typed_inputs import (
    input_collection, input_collection_ref, input_symbol, input_symbol_ref,
)


EDITION="core-0.1-integration-candidate-a13-b12"


def nat_program():
    src=" ".join([
        input_nat("קלט"),
        f"יהי מקום ושמו יעד ובמקום אשר שמו יעד יהי {input_nat_ref('קלט')} לבדו",
        "ועתה "+replace_nat("יעד",num(1)),
    ])
    c=compile_source(src); assert c.valid,[d.to_dict() for d in c.diagnostics]
    return c.ir


def malicious_bytes(program):
    obj=artifact_dict(program,language_edition=EDITION)
    return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False).encode("utf-8")+b"\n"


def expect_ir_reject(program,needle):
    with pytest.raises(ArtifactVerificationError,match=needle):
        verify_artifact(malicious_bytes(program))


def with_recomputed_owner(program):
    return reowner_program_inputs(program,ir_program_contract_id(program))


def resign(obj):
    payload=json.dumps(obj["program"],ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False).encode("utf-8")
    obj["payload_sha256"]=hashlib.sha256(payload).hexdigest()
    return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False).encode("utf-8")+b"\n"


def test_undeclared_and_forged_program_input_ids_are_rejected():
    p=nat_program(); init=p.initial_facts[0]
    assert isinstance(init.value,I.IRReadProgramInputNumber)
    pid=init.value.input_id
    forged=ProgramInputId(999_001,"זר",pid.program_contract)
    bad=dataclasses.replace(p,initial_facts=(dataclasses.replace(init,value=dataclasses.replace(init.value,input_id=forged)),))
    expect_ir_reject(with_recomputed_owner(bad),"IR_PROGRAM_INPUT_READ")


def test_consistent_program_input_owner_forgery_is_rejected_against_recomputed_program_contract():
    p=nat_program()
    contract=p.program_input_domains[0]
    init=p.initial_facts[0]
    assert isinstance(init.value,I.IRReadProgramInputNumber)
    forged=ProgramInputId(contract.input_id.serial,contract.input_id.spelling,"marak-ir-contract-sha256:"+"0"*64)
    bad=dataclasses.replace(
        p,
        program_input_domains=(dataclasses.replace(contract,input_id=forged),),
        initial_facts=(dataclasses.replace(init,value=dataclasses.replace(init.value,input_id=forged)),),
    )
    expect_ir_reject(bad,"IR_PROGRAM_INPUT_OWNERSHIP")


def test_duplicate_conflicting_and_cross_owner_input_contracts_are_rejected():
    p=nat_program(); contract=p.program_input_domains[0]
    expect_ir_reject(dataclasses.replace(p,program_input_domains=(contract,contract)),"IR_PROGRAM_INPUT_DOMAIN_CONTRACT")

    foreign=ProgramInputId(999_002,"אחר","marak-program-sha256:foreign")
    extra=I.IRProgramInputDomain(p.source_span,foreign,NATURAL)
    expect_ir_reject(dataclasses.replace(p,program_input_domains=(contract,extra)),"IR_PROGRAM_INPUT_DOMAIN_CONTRACT")

    conflicting=dataclasses.replace(contract,domain=BIDIRECTIONAL_INDEX)
    expect_ir_reject(dataclasses.replace(p,program_input_domains=(contract,conflicting)),"IR_PROGRAM_INPUT_DOMAIN_CONTRACT")


def test_natural_and_index_input_read_domain_forgery_is_rejected():
    p=nat_program(); init=p.initial_facts[0]; pid=p.program_input_domains[0].input_id
    sid=SymbolDomainId(999_010,"מזויף")
    symbol_contract=dataclasses.replace(p.program_input_domains[0],domain=SymbolDomain(sid))
    bad=dataclasses.replace(
        p,
        program_input_domains=(symbol_contract,),
        symbol_domains=p.symbol_domains+(I.IRSymbolDomainDeclaration(p.source_span,sid),),
    )
    expect_ir_reject(with_recomputed_owner(bad),"IR_PROGRAM_INPUT_READ")

    forged_read=I.IRReadProgramInputValue(init.value.source_span,pid,BIDIRECTIONAL_INDEX)
    bad=dataclasses.replace(p,initial_facts=(dataclasses.replace(init,value=forged_read),))
    expect_ir_reject(with_recomputed_owner(bad),"IR_PROGRAM_INPUT_READ")


def test_symbol_input_wrong_declared_symbol_domain_is_rejected():
    d1,d2="צבעים","חיות"
    src=" ".join([
        symbol_domain(d1),member(d1,"אדום",1,"אדום"),
        symbol_domain(d2),member(d2,"חתול",1,"חתול"),
        input_symbol("קלט",d1),place_typed("יעד",input_symbol_ref("קלט",d1)),
        "ועתה "+replace_nat("דגל",num(1)),
    ])
    src=f"יהי מקום ושמו דגל ובמקום אשר שמו דגל יהי {num(1)} לבדו "+src
    c=compile_source(src); assert c.valid,[d.to_dict() for d in c.diagnostics]
    p=c.ir
    init=next(x for x in p.initial_facts if isinstance(x.value,I.IRReadProgramInputValue))
    d2id=next(x.domain_id for x in p.symbol_domains if x.domain_id.spelling==d2)
    forged=dataclasses.replace(init.value,domain=SymbolDomain(d2id))
    initials=tuple(dataclasses.replace(x,value=forged) if x is init else x for x in p.initial_facts)
    expect_ir_reject(with_recomputed_owner(dataclasses.replace(p,initial_facts=initials)),"IR_PROGRAM_INPUT_READ")


def test_collection_and_nested_collection_element_domain_forgery_is_rejected():
    for kind,forged_domain in [
        ("ספר מספרים",CollectionDomain(BIDIRECTIONAL_INDEX)),
        ("ספר ספרי מספרים",CollectionDomain(CollectionDomain(BIDIRECTIONAL_INDEX))),
    ]:
        src=" ".join([
            input_collection("קלט",kind),
            place_book("יעד",input_collection_ref("קלט")),
            "ועתה "+replace_book("יעד",input_collection_ref("קלט")),
        ])
        c=compile_source(src); assert c.valid,[d.to_dict() for d in c.diagnostics]
        p=c.ir; init=p.initial_facts[0]
        assert isinstance(init.value,I.IRReadProgramInputValue)
        forged=dataclasses.replace(init.value,domain=forged_domain)
        expect_ir_reject(with_recomputed_owner(dataclasses.replace(p,initial_facts=(dataclasses.replace(init,value=forged),))),"IR_PROGRAM_INPUT_READ")


@pytest.mark.parametrize("mutation,needle",[
    ("unknown_tag","unknown artifact tag"),
    ("missing_field","wrong fields"),
    ("optional_default","wrong fields"),
    ("bound_value","wrong fields"),
])
def test_valid_digest_serialized_input_forgery_is_rejected(mutation,needle):
    p=nat_program(); obj=artifact_dict(p,language_edition=EDITION)
    read=obj["program"]["initial_facts"][0]["value"]
    contract=obj["program"]["program_input_domains"][0]
    if mutation=="unknown_tag":
        read["tag"]="IRReadProgramInputMystery"
    elif mutation=="missing_field":
        del read["input_id"]
    elif mutation=="optional_default":
        contract["optional"]=True
        contract["default"]={"tag":"NaturalValue","value":1}
    else:
        contract["bound_value"]={"host_value":17}
    with pytest.raises(ArtifactVerificationError,match=needle):
        verify_artifact(resign(obj))


def test_previous_0_5_artifact_is_rejected_not_reinterpreted():
    p=nat_program(); obj=artifact_dict(p,language_edition=EDITION)
    obj["artifact_version"]="core-artifact-0.5-candidate-1"
    data=json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")+b"\n"
    with pytest.raises(ArtifactVerificationError,match="unknown artifact version"):
        verify_artifact(data)
