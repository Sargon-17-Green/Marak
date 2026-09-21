from __future__ import annotations

import dataclasses
import hashlib
import json

import pytest

from compiler.api import compile_source
from compiler.artifact.format import (
    ARTIFACT_FORMAT_VERSION,
    ArtifactVerificationError,
    artifact_dict,
    verify_artifact,
    verify_ir,
)
from compiler.models import ir as I
from compiler.version import LANGUAGE_EDITION
from tests.test_c5_2_surface_pipeline import num, place_nat, replace_nat
from tests.test_c5_6_general_index_surface import general_index, index_lt


def order_program():
    src = " ".join([
        place_nat("דגל", 2),
        "ועתה אם " + index_lt(general_index(-1), general_index(1)) +
        " " + replace_nat("דגל", num(1)) +
        " ואם לא " + replace_nat("דגל", num(2)),
    ])
    c = compile_source(src)
    assert c.valid, [d.to_dict() for d in c.diagnostics]
    assert isinstance(c.ir.principal, I.IRConditional)
    assert isinstance(c.ir.principal.proposition, I.IRIndexLTProposition)
    return c


def _resign(obj):
    payload = json.dumps(
        obj["program"],
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    obj["payload_sha256"] = hashlib.sha256(payload).hexdigest()
    return json.dumps(
        obj,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8") + b"\n"


def _walk(obj):
    if isinstance(obj, dict):
        yield obj
        for value in obj.values():
            yield from _walk(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from _walk(value)


def test_index_lt_artifact_roundtrip_is_explicit_and_canonical():
    c = order_program()
    restored = verify_artifact(c.artifact)
    assert isinstance(restored.principal, I.IRConditional)
    assert isinstance(restored.principal.proposition, I.IRIndexLTProposition)


def test_artifact_and_ir_06_are_stale_not_silently_reinterpreted():
    c = order_program()
    obj = json.loads(c.artifact)
    obj["artifact_version"] = "core-artifact-0.6-candidate-1"
    with pytest.raises(ArtifactVerificationError, match="artifact version"):
        verify_artifact(json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()+b"\n")

    obj = json.loads(c.artifact)
    obj["ir_version"] = "core-ir-0.6-candidate-1"
    with pytest.raises(ArtifactVerificationError, match="IR version"):
        verify_artifact(json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()+b"\n")


@pytest.mark.parametrize("mutation,needle", [
    ("unknown_tag", "unknown artifact tag"),
    ("extra_field", "wrong fields"),
    ("missing_field", "wrong fields"),
    ("node_substitution", "IR_NATURAL_GT_DOMAIN"),
    ("malformed_span", "source point"),
    ("span_extra_field", "source point fields"),
    ("span_wrong_type", "source point line"),
    ("span_reversed", "source span is reversed"),
])
def test_index_lt_artifact_forgery_is_rejected(mutation, needle):
    c = order_program()
    obj = artifact_dict(c.ir, language_edition=LANGUAGE_EDITION)
    node = next(x for x in _walk(obj["program"]) if x.get("tag") == "IRIndexLTProposition")
    if mutation == "unknown_tag":
        node["tag"] = "IRGenericOrderProposition"
    elif mutation == "extra_field":
        node["profile"] = "general"
    elif mutation == "missing_field":
        del node["right"]
    elif mutation == "node_substitution":
        node["tag"] = "IRNaturalGTProposition"
    elif mutation == "malformed_span":
        del node["source_span"]["$span"]["start"]["line"]
    elif mutation == "span_extra_field":
        node["source_span"]["$span"]["start"]["profile"] = "general"
    elif mutation == "span_wrong_type":
        node["source_span"]["$span"]["start"]["line"] = "1"
    else:
        start = node["source_span"]["$span"]["start"]
        end = node["source_span"]["$span"]["end"]
        start["char_offset"], end["char_offset"] = end["char_offset"] + 1, start["char_offset"]
        start["byte_offset"], end["byte_offset"] = end["byte_offset"] + 1, start["byte_offset"]
    with pytest.raises(ArtifactVerificationError, match=needle):
        verify_artifact(_resign(obj))


def test_direct_ir_wrong_domain_operand_is_rejected_before_artifact_encoding():
    c = order_program()
    prop = c.ir.principal.proposition
    bad_prop = dataclasses.replace(prop, right=I.IRNatural(prop.source_span, 1))
    bad = dataclasses.replace(
        c.ir,
        principal=dataclasses.replace(c.ir.principal, proposition=bad_prop),
    )
    with pytest.raises(ArtifactVerificationError, match="IR_INDEX_LT_DOMAIN"):
        verify_ir(bad)


def test_current_artifact_identity_is_07():
    assert ARTIFACT_FORMAT_VERSION == "core-artifact-0.7-candidate-1"
