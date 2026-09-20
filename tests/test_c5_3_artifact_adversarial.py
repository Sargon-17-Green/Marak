from __future__ import annotations

import dataclasses
import json

import pytest

from compiler.api import compile_source
from compiler.artifact.format import ArtifactVerificationError, artifact_dict, verify_artifact
from compiler.models import ir as I
from compiler.models.domains import BIDIRECTIONAL_INDEX, NATURAL, CollectionDomain, SymbolDomainId
from tests.test_c5_2_surface_pipeline import member, order, symbol_domain
from tests.test_c5_3_collections import (
    book_place, empty_nat, nat_book, place_book, replace_book,
    sort_nat, sort_sym, symbol_book,
)


def compiled(source: str) -> I.IRProgram:
    result=compile_source(source)
    assert result.valid,[d.to_dict() for d in result.diagnostics]
    assert result.ir is not None
    return result.ir


def malicious_bytes(program: I.IRProgram) -> bytes:
    obj=artifact_dict(program,language_edition="core-0.1-integration-candidate-a13-b12")
    return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False).encode("utf-8")+b"\n"


def expect_reject(program: I.IRProgram, needle: str):
    with pytest.raises(ArtifactVerificationError) as exc:
        verify_artifact(malicious_bytes(program))
    assert needle in str(exc.value)


def natural_sort_program():
    return compiled(" ".join([
        place_book("ספר",nat_book(3,1)),
        "ועתה "+replace_book("ספר",sort_nat(book_place("ספר"))),
    ]))


def symbol_sort_program():
    d="צבעים"
    return compiled(" ".join([
        symbol_domain(d),member(d,"א",1,"א"),member(d,"ב",1,"ב"),order(d,"ב","א"),
        place_book("ספר",symbol_book(d,"א","ב")),
        "ועתה "+replace_book("ספר",sort_sym(d,book_place("ספר"))),
    ]))


def test_forged_collection_literal_element_domain_rejected_after_valid_digest():
    p=compiled(" ".join([place_book("ספר",nat_book(3)),"ועתה "+replace_book("ספר",book_place("ספר"))]))
    init=p.initial_facts[0]
    assert isinstance(init.value,I.IRCollectionAppend)
    leaf=init.value.item
    assert isinstance(leaf,I.IRNatural)
    forged=I.IRCollectionValue(init.value.source_span,BIDIRECTIONAL_INDEX,(leaf,))
    bad=dataclasses.replace(p,initial_facts=(dataclasses.replace(init,value=forged),))
    expect_reject(bad,"IR_DOMAIN_COLLECTION_ELEMENT")


def test_forged_append_element_metadata_rejected():
    p=compiled(" ".join([place_book("ספר",nat_book(3)),"ועתה "+replace_book("ספר",book_place("ספר"))]))
    init=p.initial_facts[0]
    assert isinstance(init.value,I.IRCollectionAppend)
    forged=dataclasses.replace(init.value,element_domain=BIDIRECTIONAL_INDEX)
    bad=dataclasses.replace(p,initial_facts=(dataclasses.replace(init,value=forged),))
    expect_reject(bad,"IR_DOMAIN_COLLECTION")


def test_non_natural_position_operand_rejected():
    p=compiled(" ".join([
        place_book("ספר",nat_book(3)),
        "ועתה "+replace_book("ספר",book_place("ספר")),
    ]))
    span=p.source_span
    invalid=I.IRCollectionSelectValue(span,I.IRCollectionValue(span,NATURAL,()),NATURAL,I.IRIndexValue(span,"zero",0),"ordinal")
    init=p.initial_facts[0]
    bad=dataclasses.replace(p,initial_facts=(dataclasses.replace(init,value=invalid),))
    with pytest.raises(ArtifactVerificationError,match="Collection position operand"):
        verify_artifact(malicious_bytes(bad))


def test_unknown_collection_order_tag_rejected():
    p=natural_sort_program()
    assert isinstance(p.principal,I.IRReplaceCurrentFact)
    order_node=p.principal.value
    assert isinstance(order_node,I.IRCollectionOrder)
    bad_order=dataclasses.replace(order_node,order_kind="host-default")
    bad=dataclasses.replace(p,principal=dataclasses.replace(p.principal,value=bad_order))
    with pytest.raises(ArtifactVerificationError,match="unknown Collection order tag"):
        verify_artifact(malicious_bytes(bad))


def test_symbol_sort_without_explicit_complete_profile_rejected():
    p=symbol_sort_program()
    assert p.symbol_order_edges
    bad=dataclasses.replace(p,symbol_order_edges=())
    expect_reject(bad,"IR_COLLECTION_ORDER_INCOMPLETE")


def test_symbol_order_profile_domain_forgery_rejected():
    p=symbol_sort_program()
    assert isinstance(p.principal,I.IRReplaceCurrentFact)
    order_node=p.principal.value
    assert isinstance(order_node,I.IRCollectionOrder)
    forged_domain=SymbolDomainId(999001,"זר")
    bad_order=dataclasses.replace(order_node,symbol_domain_id=forged_domain)
    bad=dataclasses.replace(p,principal=dataclasses.replace(p.principal,value=bad_order))
    expect_reject(bad,"IR_COLLECTION_ORDER_PROFILE")


def test_recursive_nested_element_domain_forgery_rejected():
    span=natural_sort_program().source_span
    inner=I.IRCollectionValue(span,NATURAL,(I.IRNatural(span,1),))
    forged_outer=I.IRCollectionValue(span,CollectionDomain(BIDIRECTIONAL_INDEX),(inner,))
    p=natural_sort_program()
    init=p.initial_facts[0]
    bad=dataclasses.replace(p,initial_facts=(dataclasses.replace(init,value=forged_outer),))
    expect_reject(bad,"IR_DOMAIN_COLLECTION_ELEMENT")
