from __future__ import annotations

import dataclasses
import hashlib
import json

import pytest

from compiler.api import compile_source
from compiler.artifact.format import ArtifactVerificationError, artifact_dict, verify_artifact
from compiler.models import ir as I
from compiler.models.domains import NATURAL, SymbolDomainId, SymbolMemberId
from tests.test_c5_2_surface_pipeline import current, num, place_nat, replace_nat


def source_program() -> I.IRProgram:
    action=replace_nat("מונה",f"המספר הנחשב בהוסיף את {num(1)} על {current('מונה')}")
    src=" ".join([place_nat("מונה",1),"ועתה שלש פעמים "+action])
    c=compile_source(src)
    assert c.valid,[d.to_dict() for d in c.diagnostics]
    assert isinstance(c.ir.principal,I.IRRepeatExactly)
    return c.ir


def malicious_bytes(program: I.IRProgram) -> bytes:
    obj=artifact_dict(program,language_edition="core-0.1-integration-candidate-a13-b12")
    return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False).encode()+b"\n"


def raw_mutation(mutator) -> bytes:
    c=compile_source(" ".join([
        place_nat("מונה",1),
        "ועתה שלש פעמים "+replace_nat("מונה",f"המספר הנחשב בהוסיף את {num(1)} על {current('מונה')}"),
    ]))
    assert c.valid and c.artifact
    obj=json.loads(c.artifact)
    mutator(obj)
    obj["payload_sha256"]=hashlib.sha256(
        json.dumps(obj["program"],ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False).encode()
    ).hexdigest()
    return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False).encode()+b"\n"


@pytest.mark.parametrize("bad_count",[
    lambda sp: I.IRIndexValue(sp,"zero",0),
    lambda sp: I.IRCollectionValue(sp,NATURAL,()),
    lambda sp: I.IRSymbolValue(sp,SymbolDomainId(991,"זר"),SymbolMemberId(992,"א"),"א"),
])
def test_valid_digest_non_natural_count_operands_rejected(bad_count):
    p=source_program()
    bad=dataclasses.replace(p,principal=dataclasses.replace(p.principal,count=bad_count(p.source_span)))
    with pytest.raises(ArtifactVerificationError,match="RECURRENCE_COUNT_DOMAIN_ERROR"):
        verify_artifact(malicious_bytes(bad))


def test_multiple_or_composite_repeated_body_is_rejected():
    p=source_program()
    atom=p.principal.action
    forged=I.IRThen(p.source_span,(atom,atom))
    bad=dataclasses.replace(p,principal=dataclasses.replace(p.principal,action=forged))
    with pytest.raises(ArtifactVerificationError,match="repeated atomic action"):
        verify_artifact(malicious_bytes(bad))


def test_unknown_recurrence_tag_is_rejected_after_valid_digest():
    def mutate(obj):
        node=next(x for x in _walk(obj["program"]) if x.get("tag")=="IRRepeatExactly")
        node["tag"]="IRRepeatMaybe"
    with pytest.raises(ArtifactVerificationError,match="unknown artifact tag"):
        verify_artifact(raw_mutation(mutate))


def test_missing_count_is_rejected_after_valid_digest():
    def mutate(obj):
        node=next(x for x in _walk(obj["program"]) if x.get("tag")=="IRRepeatExactly")
        del node["count"]
    with pytest.raises(ArtifactVerificationError,match="wrong fields"):
        verify_artifact(raw_mutation(mutate))


def test_forged_reevaluation_metadata_is_rejected_after_valid_digest():
    def mutate(obj):
        node=next(x for x in _walk(obj["program"]) if x.get("tag")=="IRRepeatExactly")
        node["reevaluate_each_iteration"]=True
    with pytest.raises(ArtifactVerificationError,match="wrong fields"):
        verify_artifact(raw_mutation(mutate))


def test_artifact_04_cannot_silently_reinterpret_repeat_exactly():
    c=compile_source(" ".join([
        place_nat("מונה",1),
        "ועתה שלש פעמים "+replace_nat("מונה",f"המספר הנחשב בהוסיף את {num(1)} על {current('מונה')}"),
    ]))
    obj=json.loads(c.artifact)
    obj["artifact_version"]="core-artifact-0.4-candidate-1"
    bad=json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()+b"\n"
    with pytest.raises(ArtifactVerificationError,match="artifact version"):
        verify_artifact(bad)


def test_direct_produce_repeat_preserves_existing_zero_one_output_rule_at_runtime():
    # Source grammar never makes Produce an AtomicAction. This verifier-level case
    # proves that if a valid canonical body contains direct RepeatExactly(2,Produce),
    # no implicit output collection appears: the second Produce hits the existing
    # one-output-per-occurrence rule.
    worker="פולט"
    c=compile_source(f"יהי מעשה ושמו {worker} זה דבר המעשה אשר שמו {worker} הוצא מן המעשה הזה את {num(1)} עד הנה דבר המעשה אשר שמו {worker} ועתה עשה את המעשה אשר שמו {worker}")
    assert c.valid
    actdef=c.ir.acts[0]
    produce=actdef.body
    repeat=I.IRRepeatExactly(produce.source_span,I.IRNatural(produce.source_span,2),produce)
    bad_program=dataclasses.replace(c.ir,acts=(dataclasses.replace(actdef,body=repeat),))
    # The canonical representation is admitted; runtime cardinality is the existing error.
    from compiler.artifact.format import verify_ir
    verify_ir(bad_program)
    from compiler.runtime.ir_reference import execute_reference_ir, IRReferenceErrorOutcome
    from compiler.backend.portable import execute_ir, VMErrorOutcome
    a=execute_reference_ir(bad_program); b=execute_ir(bad_program)
    assert isinstance(a,IRReferenceErrorOutcome) and a.error.code=="CORE_OUTPUT_CARDINALITY_ERROR"
    assert isinstance(b,VMErrorOutcome) and b.error.code=="CORE_OUTPUT_CARDINALITY_ERROR"
    assert len(a.products)==len(b.products)==1


def _walk(obj):
    if isinstance(obj,dict):
        yield obj
        for v in obj.values():
            yield from _walk(v)
    elif isinstance(obj,list):
        for v in obj:
            yield from _walk(v)
