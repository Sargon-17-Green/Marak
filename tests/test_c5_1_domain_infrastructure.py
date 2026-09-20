from __future__ import annotations

import dataclasses
import hashlib
import json
from dataclasses import dataclass

import pytest

from compiler.artifact.format import ArtifactVerificationError, artifact_dict, serialize_artifact, verify_artifact, verify_ir
from compiler.backend.portable import execute_ir
from compiler.ir_lower import lower_validated_hast
from compiler.models import hast as H
from compiler.models import ir as I
from compiler.models.domains import (
    BIDIRECTIONAL_INDEX, NATURAL, CollectionDomain, ProgramInputId,
    SymbolDomain, SymbolDomainId, SymbolMemberId,
)
from compiler.models.symbols import ActId, PlaceId, RoleId
from compiler.models.values import (
    BidirectionalIndexValue, CollectionValue, NaturalValue, SymbolValue,
)
from compiler.runtime.invocation import (
    DUPLICATE_INPUT_BINDING, EXTRA_INPUT_BINDING, INPUT_DOMAIN_MISMATCH,
    MISSING_INPUT_BINDING, InputBinding, ValidatedInvocation, validate_invocation,
)
from compiler.runtime.ir_reference import execute_reference_ir
from compiler.runtime.observables import backend_observable, ir_reference_observable, reference_observable
from compiler.runtime.reference import execute_reference
from compiler.source.source_map import OriginalPoint, OriginalSpan
from compiler.validate.domains import DomainValidationError, validate_hast_domains


def sp() -> OriginalSpan:
    p = OriginalPoint("<c5.1-fixture>", 0, 0, 1, 1)
    return OriginalSpan(p, p)


def _program(domain, literal: H.HastValue) -> H.HastCoreProgram:
    s=sp(); place=PlaceId(1,"?????????"); act=ActId(2,"?????????"); role=RoleId(3,act,"??????????")
    prep=(
        H.HastPlaceIntroduction(s,place,literal),
        H.HastActIntroduction(s,act),
        H.HastRoleDeclaration(s,role),
        H.HastActBody(s,act,H.HastProduceResult(s,H.HastCurrentRoleValue(s,role,domain))),
    )
    principal=H.HastThen(s,(
        H.HastPerformAct(s,act,(H.HastRoleAssociation(s,role,H.HastCurrentValue(s,place,domain)),)),
        H.HastReplaceCurrentFact(s,place,H.HastRecentTypedResult(s,act,domain)),
    ))
    return H.HastCoreProgram(
        s,prep,principal,(place,),(act,),(role,),
        (H.HastPlaceDomain(place,domain),),
        (H.HastRoleDomain(role,domain),),
        (H.HastActOutputDomain(act,domain),),
        (),
    )


def _roundtrip(program: H.HastCoreProgram):
    validate_hast_domains(program)
    ir=lower_validated_hast(program)
    data=serialize_artifact(ir,language_edition="core-0.1-integration-candidate-a13-b12")
    decoded=verify_artifact(data)
    ref=execute_reference(program)
    irr=execute_reference_ir(decoded)
    vm=execute_ir(decoded)
    ro,io,bo=reference_observable(ref),ir_reference_observable(irr),backend_observable(vm)
    assert ro==io==bo
    return ir,data,bo


def _artifact_bytes(program: I.IRProgram) -> bytes:
    obj=artifact_dict(program,language_edition="core-0.1-integration-candidate-a13-b12")
    return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False).encode("utf-8")+b"\n"


def test_symbol_flows_place_role_output_recent_result_and_artifact():
    d_id=SymbolDomainId(101,"???"); member=SymbolMemberId(1,"????"); d=SymbolDomain(d_id)
    program=_program(d,H.HastSymbolValue(sp(),d_id,member,"????"))
    _,data,obs=_roundtrip(program)
    assert verify_artifact(data)
    assert obs["facts"]==[["?????????","????"]]
    assert obs["products"]==[["?????????","????"]]


def test_bidirectional_index_flows_same_carrier_chain():
    program=_program(BIDIRECTIONAL_INDEX,H.HastIndexValue(sp(),"before",7))
    _,_,obs=_roundtrip(program)
    assert obs["facts"]==[["?????????",{"index":"BeforeZero","magnitude":7}]]


def test_collection_flows_same_carrier_chain():
    d_id=SymbolDomainId(201,"???"); member=SymbolMemberId(1,"???"); elem=SymbolDomain(d_id); d=CollectionDomain(elem)
    literal=H.HastCollectionValue(sp(),elem,(H.HastSymbolValue(sp(),d_id,member,"???"),))
    _,_,obs=_roundtrip(_program(d,literal))
    assert obs["facts"]==[["?????????",["???"]]]


def test_a13_core_contracts_are_explicitly_natural():
    from compiler.api import check
    from tests.m4_support import tiny_source
    c=check(tiny_source()); assert c.valid and c.hast
    assert all(x.domain==NATURAL for x in c.hast.place_domains)
    assert all(x.domain==NATURAL for x in c.hast.role_domains)


def test_expected_type_does_not_rescue_unresolved_expression():
    @dataclass(frozen=True,slots=True)
    class Unresolved(H.HastValue):
        pass
    d=SymbolDomain(SymbolDomainId(301,"???")); place=PlaceId(1,"?")
    p=H.HastCoreProgram(sp(),(H.HastPlaceIntroduction(sp(),place,Unresolved(sp())),),H.HastThen(sp(),(H.HastReplaceCurrentFact(sp(),place,Unresolved(sp())),)),(place,),(),(),(H.HastPlaceDomain(place,d),),(),(),())
    with pytest.raises(DomainValidationError,match="DOMAIN_UNRESOLVED_EXPRESSION") as exc:
        validate_hast_domains(p)
    assert exc.value.issue.diagnostic_code == "DOM0001"


def test_program_input_contract_validation_is_preparation_independent():
    base=_program(BIDIRECTIONAL_INDEX,H.HastIndexValue(sp(),"zero",0))
    inp=ProgramInputId(1,"???"); d=SymbolDomain(SymbolDomainId(401,"???"))
    with_input=dataclasses.replace(base,program_input_domains=(H.HastProgramInputDomain(inp,d),))
    ir=lower_validated_hast(with_input)
    good=validate_invocation(ir,(InputBinding(inp,SymbolValue(d.identity,SymbolMemberId(1,"?"),"?")),))
    assert isinstance(good,ValidatedInvocation)
    assert [x.code for x in validate_invocation(ir,())]==[MISSING_INPUT_BINDING]
    extra=ProgramInputId(2,"???")
    assert [x.code for x in validate_invocation(ir,(InputBinding(extra,NaturalValue(1)),))]==[EXTRA_INPUT_BINDING,MISSING_INPUT_BINDING]
    assert [x.code for x in validate_invocation(ir,(InputBinding(inp,NaturalValue(1)),))]==[INPUT_DOMAIN_MISMATCH]
    duplicate=(InputBinding(inp,SymbolValue(d.identity,SymbolMemberId(1,"?"),"?")),)*2
    assert [x.code for x in validate_invocation(ir,duplicate)]==[DUPLICATE_INPUT_BINDING]


def _symbol_ir():
    did=SymbolDomainId(501,"???"); mid=SymbolMemberId(1,"????"); d=SymbolDomain(did)
    ir,_,_=_roundtrip(_program(d,H.HastSymbolValue(sp(),did,mid,"????")))
    return ir,d,did,mid


def test_artifact_rejects_symbol_place_initialized_by_natural():
    ir,_,_,_= _symbol_ir()
    bad=dataclasses.replace(ir,initial_facts=(dataclasses.replace(ir.initial_facts[0],value=I.IRNatural(sp(),1)),))
    with pytest.raises(ArtifactVerificationError,match="PLACE_INITIALIZER"):
        verify_artifact(_artifact_bytes(bad))


def test_artifact_rejects_collection_role_associated_with_symbol():
    did=SymbolDomainId(601,"???"); mid=SymbolMemberId(1,"?"); elem=SymbolDomain(did); coll=CollectionDomain(elem)
    ir,_,_=_roundtrip(_program(coll,H.HastCollectionValue(sp(),elem,(H.HastSymbolValue(sp(),did,mid,"?"),))))
    assoc=ir.principal.actions[0].associations[0]
    bad_assoc=dataclasses.replace(assoc,value=I.IRSymbolValue(sp(),did,mid,"?"))
    perform=dataclasses.replace(ir.principal.actions[0],associations=(bad_assoc,))
    bad=dataclasses.replace(ir,principal=dataclasses.replace(ir.principal,actions=(perform,ir.principal.actions[1])))
    with pytest.raises(ArtifactVerificationError,match="ROLE_ASSOCIATION"):
        verify_artifact(_artifact_bytes(bad))


def test_artifact_rejects_mixed_output_domains_across_branches():
    ir,d,did,mid=_symbol_ir(); definition=ir.acts[0]
    cond=I.IRConditional(sp(),I.IREqualProposition(sp(),I.IRNatural(sp(),0),I.IRNatural(sp(),0)),I.IRProduceResult(sp(),I.IRSymbolValue(sp(),did,mid,"????")),I.IRProduceResult(sp(),I.IRNatural(sp(),1)))
    bad=dataclasses.replace(ir,acts=(dataclasses.replace(definition,body=cond),))
    with pytest.raises(ArtifactVerificationError,match="DOMAIN_OUTPUT"):
        verify_artifact(_artifact_bytes(bad))


def test_artifact_rejects_wrong_typed_immediate_result_head():
    ir,d,_,_=_symbol_ir(); replacement=ir.principal.actions[1]
    bad_read=I.IRRecentTypedResult(sp(),ir.acts[0].act,BIDIRECTIONAL_INDEX)
    bad=dataclasses.replace(ir,principal=dataclasses.replace(ir.principal,actions=(ir.principal.actions[0],dataclasses.replace(replacement,value=bad_read))))
    with pytest.raises(ArtifactVerificationError,match="RESULT_HEAD"):
        verify_artifact(_artifact_bytes(bad))


def test_artifact_rejects_unknown_domain_tag():
    ir,_,_,_=_symbol_ir(); data=serialize_artifact(ir,language_edition="core-0.1-integration-candidate-a13-b12")
    obj=json.loads(data); domain=next(x for x in _walk(obj["program"]) if x.get("tag")=="SymbolDomain"); domain["tag"]="UnknownDomain"
    obj["payload_sha256"]=hashlib.sha256(json.dumps(obj["program"],ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False).encode()).hexdigest()
    bad=json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False).encode()+b"\n"
    with pytest.raises(ArtifactVerificationError,match="unknown artifact tag"):
        verify_artifact(bad)


def _walk(obj):
    if isinstance(obj,dict):
        yield obj
        for v in obj.values(): yield from _walk(v)
    elif isinstance(obj,list):
        for v in obj: yield from _walk(v)


def test_artifact_rejects_collection_element_domain_metadata_mismatch():
    ir,d,did,mid=_symbol_ir(); other=SymbolDomainId(777,"???")
    invalid=I.IRCollectionValue(sp(),SymbolDomain(other),(I.IRSymbolValue(sp(),did,mid,"????"),))
    # Give the place a Collection<other> contract so only element-domain inconsistency is under test.
    place=ir.place_domains[0].place
    coll=CollectionDomain(SymbolDomain(other))
    bad=dataclasses.replace(ir,initial_facts=(I.IRInitialFact(sp(),place,invalid),),place_domains=(I.IRPlaceDomain(sp(),place,coll),),principal=I.IRReplaceCurrentFact(sp(),place,invalid),acts=(),act_output_domains=(),symbols=tuple(x for x in ir.symbols if x.kind=="place"),role_domains=())
    with pytest.raises(ArtifactVerificationError,match="COLLECTION_ELEMENT"):
        verify_artifact(_artifact_bytes(bad))


def test_artifact_rejects_conflicting_program_input_domain_declarations():
    ir,d,_,_=_symbol_ir(); inp=ProgramInputId(1,"???")
    bad=dataclasses.replace(ir,program_input_domains=(I.IRProgramInputDomain(sp(),inp,d),I.IRProgramInputDomain(sp(),inp,NATURAL)))
    with pytest.raises(ArtifactVerificationError,match="PROGRAM_INPUT_DOMAIN_CONTRACT"):
        verify_artifact(_artifact_bytes(bad))


def test_artifact_v01_schema_is_rejected_not_reinterpreted():
    ir,_,_,_=_symbol_ir()
    obj=artifact_dict(ir,language_edition="core-0.1-integration-candidate-a13-b12")
    obj["artifact_version"]="core-artifact-0.1-candidate-1"
    bad=json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False).encode("utf-8")+b"\n"
    with pytest.raises(ArtifactVerificationError,match="unknown artifact version"):
        verify_artifact(bad)


def test_symbol_observation_is_invariant_under_internal_identity_renumbering():
    d1=SymbolDomainId(9101,"colors"); m1=SymbolMemberId(1,"red_source")
    d2=SymbolDomainId(77,"colors"); m2=SymbolMemberId(900,"red_source")
    _,_,obs1=_roundtrip(_program(SymbolDomain(d1),H.HastSymbolValue(sp(),d1,m1,"RED")))
    _,_,obs2=_roundtrip(_program(SymbolDomain(d2),H.HastSymbolValue(sp(),d2,m2,"RED")))
    assert obs1==obs2


def _symbol_observation(*, domain_serial: int, domain_spelling: str, member_serial: int, member_spelling: str, label: str, nested: bool = False):
    did=SymbolDomainId(domain_serial,domain_spelling)
    mid=SymbolMemberId(member_serial,member_spelling)
    elem=SymbolDomain(did)
    symbol=H.HastSymbolValue(sp(),did,mid,label)
    if nested:
        domain=CollectionDomain(elem)
        literal=H.HastCollectionValue(sp(),elem,(symbol,))
    else:
        domain=elem
        literal=symbol
    _,_,obs=_roundtrip(_program(domain,literal))
    return obs


def test_symbol_observation_domain_source_rename_invariant():
    a=_symbol_observation(domain_serial=1,domain_spelling="color",member_serial=1,member_spelling="red_source",label="RED")
    b=_symbol_observation(domain_serial=1,domain_spelling="hue",member_serial=1,member_spelling="red_source",label="RED")
    assert a==b


def test_symbol_observation_member_source_rename_invariant():
    a=_symbol_observation(domain_serial=1,domain_spelling="color",member_serial=1,member_spelling="red_source",label="RED")
    b=_symbol_observation(domain_serial=1,domain_spelling="color",member_serial=1,member_spelling="scarlet_source",label="RED")
    assert a==b


def test_symbol_observation_identity_and_source_rename_invariant():
    a=_symbol_observation(domain_serial=10,domain_spelling="color",member_serial=20,member_spelling="red_source",label="RED")
    b=_symbol_observation(domain_serial=900,domain_spelling="hue",member_serial=700,member_spelling="scarlet_source",label="RED")
    assert a==b


def test_symbol_observation_changes_with_external_label():
    a=_symbol_observation(domain_serial=1,domain_spelling="color",member_serial=1,member_spelling="red_source",label="RED")
    b=_symbol_observation(domain_serial=1,domain_spelling="color",member_serial=1,member_spelling="red_source",label="CRIMSON")
    assert a!=b
    assert a["facts"][0][1]=="RED"
    assert b["facts"][0][1]=="CRIMSON"


def test_nested_collection_symbol_observation_erases_source_identity_recursively():
    a=_symbol_observation(domain_serial=10,domain_spelling="color",member_serial=20,member_spelling="red_source",label="RED",nested=True)
    b=_symbol_observation(domain_serial=900,domain_spelling="hue",member_serial=700,member_spelling="scarlet_source",label="RED",nested=True)
    assert a==b
    assert a["facts"][0][1]==["RED"]


@pytest.mark.parametrize(
    ("field","semantic_code"),
    [
        ("place_domains","DOMAIN_PLACE_CONTRACT"),
        ("role_domains","DOMAIN_ROLE_CONTRACT"),
        ("act_output_domains","DOMAIN_OUTPUT_CONTRACT"),
    ],
)
def test_hast_duplicate_static_domain_contracts_rejected_before_ir(field,semantic_code):
    p=_program(BIDIRECTIONAL_INDEX,H.HastIndexValue(sp(),"zero",0))
    records=getattr(p,field)
    bad=dataclasses.replace(p,**{field:records+(records[0],)})
    with pytest.raises(DomainValidationError,match=semantic_code):
        validate_hast_domains(bad)


def test_hast_duplicate_program_input_domain_contract_rejected_before_ir():
    p=_program(BIDIRECTIONAL_INDEX,H.HastIndexValue(sp(),"zero",0))
    inp=ProgramInputId(41,"calculation_day")
    record=H.HastProgramInputDomain(inp,NATURAL)
    bad=dataclasses.replace(p,program_input_domains=(record,record))
    with pytest.raises(DomainValidationError,match="DOMAIN_PROGRAM_INPUT_DUPLICATE"):
        validate_hast_domains(bad)


def test_natural_program_input_invocation_contract():
    p=_program(BIDIRECTIONAL_INDEX,H.HastIndexValue(sp(),"zero",0))
    inp=ProgramInputId(51,"calculation_day")
    declared=dataclasses.replace(p,program_input_domains=(H.HastProgramInputDomain(inp,NATURAL),))
    ir=lower_validated_hast(declared)

    valid=validate_invocation(ir,(InputBinding(inp,NaturalValue(123)),))
    assert isinstance(valid,ValidatedInvocation)

    symbol_domain=SymbolDomainId(52,"symbol_domain")
    wrong=validate_invocation(ir,(InputBinding(inp,SymbolValue(symbol_domain,SymbolMemberId(1,"member"),"VISIBLE")),))
    assert [x.code for x in wrong]==[INPUT_DOMAIN_MISMATCH]

    missing=validate_invocation(ir,())
    assert [x.code for x in missing]==[MISSING_INPUT_BINDING]

    duplicate=validate_invocation(ir,(InputBinding(inp,NaturalValue(1)),InputBinding(inp,NaturalValue(2))))
    assert [x.code for x in duplicate]==[DUPLICATE_INPUT_BINDING]

    extra_id=ProgramInputId(53,"target_day")
    extra=validate_invocation(ir,(InputBinding(inp,NaturalValue(123)),InputBinding(extra_id,NaturalValue(456))))
    assert [x.code for x in extra]==[EXTRA_INPUT_BINDING]



def test_duplicate_visible_symbol_labels_do_not_define_symbol_equality():
    from compiler.models.values import observable_value
    did=SymbolDomainId(61,"colors")
    a=SymbolValue(did,SymbolMemberId(1,"member_a"),"VISIBLE")
    b=SymbolValue(did,SymbolMemberId(2,"member_b"),"VISIBLE")
    assert a != b
    assert observable_value(a) == observable_value(b) == "VISIBLE"
