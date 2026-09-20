from __future__ import annotations

import dataclasses
import json

import pytest

from compiler.api import compile_source
from compiler.artifact.format import (
    ARTIFACT_FORMAT_VERSION,
    ArtifactVerificationError,
    artifact_dict,
    verify_artifact,
)
from compiler.models import ir as I
from compiler.models.domains import SymbolDomain, SymbolDomainId, SymbolMemberId
from tests.test_c5_2_surface_pipeline import (
    gt_source,
    index_flow_source,
    symbol_flow_source,
)


def compiled(source: str) -> I.IRProgram:
    result=compile_source(source)
    assert result.valid, [d.to_dict() for d in result.diagnostics]
    assert result.ir is not None
    return result.ir


def malicious_bytes(program: I.IRProgram) -> bytes:
    obj=artifact_dict(program,language_edition="core-0.1-integration-candidate-a13-b12")
    return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False).encode("utf-8")+b"\n"


def expect_reject(program: I.IRProgram, needle: str):
    with pytest.raises(ArtifactVerificationError) as exc:
        verify_artifact(malicious_bytes(program))
    assert needle in str(exc.value)


def test_forged_symbol_label_is_rejected_after_valid_digest():
    p=compiled(symbol_flow_source())
    init=p.initial_facts[0]
    assert isinstance(init.value,I.IRSymbolValue)
    forged=dataclasses.replace(init.value,external_label="תווית מזויפת")
    bad=dataclasses.replace(p,initial_facts=(dataclasses.replace(init,value=forged),)+p.initial_facts[1:])
    expect_reject(bad,"IR_SYMBOL_LABEL_FORGERY")


def test_unknown_symbol_member_identity_is_rejected():
    p=compiled(symbol_flow_source())
    init=p.initial_facts[0]
    assert isinstance(init.value,I.IRSymbolValue)
    unknown=dataclasses.replace(init.value,member_id=SymbolMemberId(999_001,"זר"))
    bad=dataclasses.replace(p,initial_facts=(dataclasses.replace(init,value=unknown),)+p.initial_facts[1:])
    expect_reject(bad,"IR_SYMBOL_VALUE_IDENTITY")


def test_cross_domain_symbol_equality_is_rejected_at_artifact_boundary():
    p=compiled(symbol_flow_source())
    d2=SymbolDomainId(900_001,"אחרת")
    m2=SymbolMemberId(900_002,"זר")
    span=p.source_span
    domains=p.symbol_domains+(I.IRSymbolDomainDeclaration(span,d2),)
    members=p.symbol_members+(I.IRSymbolMemberDeclaration(span,d2,m2,"זר"),)
    act=p.acts[0]
    assert isinstance(act.body,I.IRThen)
    cond=act.body.actions[0]
    assert isinstance(cond,I.IRConditional)
    prop=cond.proposition
    assert isinstance(prop,I.IRSymbolEqualProposition)
    foreign=I.IRSymbolValue(prop.right.source_span,d2,m2,"זר")
    bad_prop=dataclasses.replace(prop,right=foreign)
    bad_cond=dataclasses.replace(cond,proposition=bad_prop)
    bad_body=dataclasses.replace(act.body,actions=(bad_cond,)+act.body.actions[1:])
    bad_act=dataclasses.replace(act,body=bad_body)
    bad=dataclasses.replace(p,acts=(bad_act,),symbol_domains=domains,symbol_members=members)
    expect_reject(bad,"IR_SYMBOL_EQUALITY_DOMAIN")


def test_malformed_index_internal_state_is_rejected():
    p=compiled(index_flow_source())
    init=p.initial_facts[0]
    assert isinstance(init.value,I.IRIndexValue)
    bad_value=dataclasses.replace(init.value,side="zero",magnitude=1)
    bad=dataclasses.replace(p,initial_facts=(dataclasses.replace(init,value=bad_value),)+p.initial_facts[1:])
    with pytest.raises(ArtifactVerificationError,match="BidirectionalIndex zero"):
        verify_artifact(malicious_bytes(bad))


def test_index_successor_with_natural_operand_is_rejected():
    p=compiled(index_flow_source())
    assert isinstance(p.principal,I.IRThen)
    last=p.principal.actions[-1]
    assert isinstance(last,I.IRReplaceCurrentFact)
    assert isinstance(last.value,I.IRIndexSuccessor)
    bad_succ=dataclasses.replace(last.value,operand=I.IRNatural(last.value.source_span,7))
    bad_last=dataclasses.replace(last,value=bad_succ)
    bad=dataclasses.replace(p,principal=dataclasses.replace(p.principal,actions=p.principal.actions[:-1]+(bad_last,)))
    expect_reject(bad,"IR_DOMAIN_INDEX_OPERAND")


def test_natural_gt_with_index_operand_is_rejected():
    p=compiled(gt_source())
    assert isinstance(p.principal,I.IRConditional)
    prop=p.principal.proposition
    assert isinstance(prop,I.IRNaturalGTProposition)
    bad_prop=dataclasses.replace(prop,left=I.IRIndexValue(prop.left.source_span,"zero",0))
    bad=dataclasses.replace(p,principal=dataclasses.replace(p.principal,proposition=bad_prop))
    expect_reject(bad,"IR_NATURAL_GT_DOMAIN")


def test_symbol_order_unknown_member_and_self_edge_are_rejected():
    p=compiled(symbol_flow_source())
    edge=p.symbol_order_edges[0]
    unknown=dataclasses.replace(edge,after_member_id=SymbolMemberId(999_003,"זר"))
    expect_reject(dataclasses.replace(p,symbol_order_edges=(unknown,)),"IR_SYMBOL_ORDER_MEMBER")
    self_edge=dataclasses.replace(edge,after_member_id=edge.before_member_id)
    expect_reject(dataclasses.replace(p,symbol_order_edges=(self_edge,)),"IR_SYMBOL_ORDER_SELF")


def test_duplicate_symbol_member_identity_is_rejected():
    p=compiled(symbol_flow_source())
    duplicate=p.symbol_members[0]
    expect_reject(dataclasses.replace(p,symbol_members=p.symbol_members+(duplicate,)),"IR_SYMBOL_MEMBER_DUPLICATE")


def test_previous_artifact_schema_is_cleanly_rejected():
    p=compiled(gt_source())
    obj=artifact_dict(p,language_edition="core-0.1-integration-candidate-a13-b12")
    obj["artifact_version"]="core-artifact-0.3-candidate-1"
    data=json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")+b"\n"
    with pytest.raises(ArtifactVerificationError,match="unknown artifact version"):
        verify_artifact(data)


def test_artifact_version_is_explicitly_current_candidate():
    assert ARTIFACT_FORMAT_VERSION=="core-artifact-0.6-candidate-1"
