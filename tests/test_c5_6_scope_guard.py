from __future__ import annotations

import inspect

from compiler.models import hast as H
from compiler.models import ir as I
from compiler.models import values as V
from compiler.parse.c5_5_registry import C5_5_REGISTRY
from compiler.parse.c5_6_registry import C5_6_REGISTRY
from compiler.version import LANGUAGE_EDITION


EXPECTED_NEW_IDS = {
    "C56.INDEX.GENERAL.ZERO",
    "C56.INDEX.GENERAL.BEFORE.ONE",
    "C56.INDEX.GENERAL.AFTER.ONE",
    "C56.INDEX.GENERAL.BEFORE.TWO",
    "C56.INDEX.GENERAL.AFTER.TWO",
    "C56.INDEX.GENERAL.BEFORE.MANY",
    "C56.INDEX.GENERAL.AFTER.MANY",
    "C56.INPUT.DECLARE.INDEX",
    "C56.INPUT.READ.INDEX",
    "C56.INDEX.GENERAL.CURRENT.PLACE",
    "C56.PLACE.REPLACE.INDEX",
    "C56.ROLE.DECLARE.INDEX",
    "C56.INDEX.GENERAL.CURRENT.ROLE",
    "C56.INDEX.GENERAL.IMMEDIATE",
    "C56.INDEX.GENERAL.SUCC",
    "C56.INDEX.GENERAL.PRED",
    "C56.PROP.INDEX.LT",
}


def _new_productions():
    old = {p.production_id for p in C5_5_REGISTRY.productions}
    return [p for p in C5_6_REGISTRY.productions if p.production_id not in old]


def test_c56_adds_exactly_the_b16_approved_surface():
    new = _new_productions()
    assert {p.production_id for p in new} == EXPECTED_NEW_IDS
    assert len(new) == 17
    assert {p.lhs for p in new} <= {
        "IndexValue", "PreparatoryUnit", "AtomicAction", "Proposition",
    }
    assert not any(p.lhs in {"CollectionValue", "NumberValue", "SymbolValue"} for p in new)


def test_c56_has_only_one_new_semantic_operation_family():
    new = _new_productions()
    proposition_ids = {p.production_id for p in new if p.lhs == "Proposition"}
    assert proposition_ids == {"C56.PROP.INDEX.LT"}

    # Generic literals and carrier heads must reuse existing Value/carrier nodes.
    assert hasattr(H, "HastIndexLTProposition")
    assert hasattr(I, "IRIndexLTProposition")
    assert issubclass(H.HastIndexLTProposition, H.HastProposition)
    assert not issubclass(H.HastIndexLTProposition, H.HastValue)
    assert issubclass(I.IRIndexLTProposition, I.IRProposition)
    assert not issubclass(I.IRIndexLTProposition, I.IRValue)
    assert callable(V.index_lt)

    forbidden_class_fragments = (
        "GeneralIndex",
        "YearIndex",
        "GenericIndex",
        "DayIndex",
        "SignedNatural",
        "IntegerValue",
        "IndexDistance",
        "IndexEqual",
    )
    names = set(dir(H)) | set(dir(I)) | set(dir(V))
    assert not any(
        fragment in name
        for name in names
        for fragment in forbidden_class_fragments
    )


def test_c56_adds_no_generic_index_collection_kind_or_distance_equality_surface():
    new = _new_productions()
    words = {
        getattr(symbol, "text", None)
        for p in new
        for symbol in p.rhs
        if getattr(symbol, "text", None) is not None
    }
    assert "מרחק" not in words

    ids = " ".join(sorted(p.production_id for p in new)).upper()
    for forbidden in (
        "DISTANCE", "EQUALITY", "EQUAL", "CONVERT",
        "INTEGER", "DAY", "DATE", "TIME", "TIMESTAMP",
        "COLLECTION.GENERAL", "GENERIC.INDEX.COLLECTION",
    ):
        assert forbidden not in ids

    assert not any(p.lhs == "CollectionValue" for p in new)


def test_c56_language_edition_is_frozen_and_registry_only_advances():
    assert LANGUAGE_EDITION == "core-0.1-integration-candidate-a13-b12"
    assert C5_6_REGISTRY.language_edition == C5_5_REGISTRY.language_edition
    assert C5_6_REGISTRY.registry_version == "c5.6-a17-b16.1"


def test_no_profile_field_or_profile_runtime_tag_is_introduced():
    index_value_fields = {f.name for f in inspect.signature(V.BidirectionalIndexValue).parameters.values()}
    assert index_value_fields == {"side", "magnitude"}

    hast_fields = {f.name for f in __import__("dataclasses").fields(H.HastIndexValue)}
    ir_fields = {f.name for f in __import__("dataclasses").fields(I.IRIndexValue)}
    assert hast_fields == {"source_span", "side", "magnitude"}
    assert ir_fields == {"source_span", "side", "magnitude"}

    for forbidden in ("profile", "unit", "year_profile", "general_profile"):
        assert forbidden not in index_value_fields
        assert forbidden not in hast_fields
        assert forbidden not in ir_fields
