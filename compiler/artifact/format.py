from __future__ import annotations
import dataclasses, hashlib, json
from dataclasses import fields
from compiler.models import ir as irm
from compiler.source.source_map import OriginalPoint, OriginalSpan
from compiler.version import LANGUAGE_EDITION
from compiler.validate.ir_canonical import CanonicalIRValidationError, validate_canonical_ir

ARTIFACT_FORMAT_VERSION="core-artifact-0.1-candidate-1"

_IR_CLASSES=(
 irm.IRProgram,irm.IRSymbol,irm.IRInitialFact,irm.IRActDefinition,
 irm.IRNatural,irm.IRReadCurrentFact,irm.IRReadRoleNumber,irm.IRRecentResult,
 irm.IRAddNatural,irm.IRCheckedSubtractNatural,irm.IREqualProposition,
 irm.IRRoleAssociation,irm.IRReplaceCurrentFact,irm.IRPerformAct,irm.IRProduceResult,
 irm.IRThen,irm.IRConditional,irm.IRFixedRecurrence,irm.IRPostActionRecurrence,
)
_CLASS_BY_TAG={c.__name__:c for c in _IR_CLASSES}

class ArtifactVerificationError(ValueError): pass

def _point(p:OriginalPoint): return {"file":p.file,"char_offset":p.char_offset,"byte_offset":p.byte_offset,"line":p.line,"column":p.column}
def _span(s:OriginalSpan): return {"start":_point(s.start),"end":_point(s.end)}
def _encode(x):
    if isinstance(x,OriginalSpan): return {"$span":_span(x)}
    if isinstance(x,tuple): return [_encode(y) for y in x]
    if dataclasses.is_dataclass(x) and type(x) in _IR_CLASSES:
        return {"tag":type(x).__name__,**{f.name:_encode(getattr(x,f.name)) for f in fields(x)}}
    if x is None or isinstance(x,(str,int,bool)): return x
    raise TypeError(f"artifact cannot encode {type(x).__name__}")

def _decode_span(obj):
    def p(d): return OriginalPoint(d["file"],d["char_offset"],d["byte_offset"],d["line"],d["column"])
    d=obj["$span"]; return OriginalSpan(p(d["start"]),p(d["end"]))
def _decode(x):
    if isinstance(x,list): return tuple(_decode(y) for y in x)
    if isinstance(x,dict):
        if "$span" in x: return _decode_span(x)
        tag=x.get("tag")
        if tag is None: raise ArtifactVerificationError("object without explicit artifact tag")
        cls=_CLASS_BY_TAG.get(tag)
        if cls is None: raise ArtifactVerificationError(f"unknown artifact tag: {tag}")
        expected={f.name for f in fields(cls)}
        actual=set(x)-{"tag"}
        if actual!=expected: raise ArtifactVerificationError(f"wrong fields for {tag}: expected {sorted(expected)}, got {sorted(actual)}")
        return cls(**{name:_decode(x[name]) for name in expected})
    return x

def _canonical(obj)->bytes: return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False).encode("utf-8")

def artifact_dict(program:irm.IRProgram,*,language_edition:str)->dict:
    pobj=_encode(program)
    ph=hashlib.sha256(_canonical(pobj)).hexdigest()
    return {"artifact_version":ARTIFACT_FORMAT_VERSION,"ir_version":program.ir_version,"language_edition":language_edition,"payload_sha256":ph,"program":pobj}

def serialize_artifact(program:irm.IRProgram,*,language_edition:str)->bytes:
    return _canonical(artifact_dict(program,language_edition=language_edition))+b"\n"

def _walk_ir(node):
    yield node
    if dataclasses.is_dataclass(node):
        for f in fields(node):
            v=getattr(node,f.name)
            if isinstance(v,tuple):
                for x in v:
                    if dataclasses.is_dataclass(x): yield from _walk_ir(x)
            elif dataclasses.is_dataclass(v) and not isinstance(v,OriginalSpan): yield from _walk_ir(v)

def verify_ir(program:irm.IRProgram)->None:
    if not isinstance(program, irm.IRProgram): raise ArtifactVerificationError("payload is not IRProgram")
    if program.ir_version!=irm.IR_VERSION: raise ArtifactVerificationError("unsupported IR version")
    if not isinstance(program.principal, irm.IRAction): raise ArtifactVerificationError("principal is not an IR action")
    if not all(isinstance(x, irm.IRInitialFact) and isinstance(x.value, irm.IRNumber) for x in program.initial_facts):
        raise ArtifactVerificationError("invalid initial-fact semantic kind")
    if not all(isinstance(x, irm.IRActDefinition) and isinstance(x.body, irm.IRAction) for x in program.acts):
        raise ArtifactVerificationError("invalid act-definition semantic kind")
    serials=[s.serial for s in program.symbols]
    if any(type(x) is not int or x <= 0 for x in serials): raise ArtifactVerificationError("identity serial must be a positive integer")
    if len(serials)!=len(set(serials)): raise ArtifactVerificationError("duplicate identity serial")
    by={s.serial:s for s in program.symbols}
    places={s.serial for s in program.symbols if s.kind=="place"}
    acts={s.serial for s in program.symbols if s.kind=="act"}
    roles={s.serial for s in program.symbols if s.kind=="role"}
    if any(s.kind not in {"place","act","role"} for s in program.symbols): raise ArtifactVerificationError("unknown semantic identity kind")
    for s in program.symbols:
        if s.kind=="role" and s.owner not in acts: raise ArtifactVerificationError("role owner is not an act")
        if s.kind!="role" and s.owner is not None: raise ArtifactVerificationError("non-role identity has owner")
    init_places=[x.place for x in program.initial_facts]
    if len(init_places)!=len(set(init_places)) or set(init_places)!=places: raise ArtifactVerificationError("invalid initial-fact/place structure")
    act_ids=[a.act for a in program.acts]
    if len(act_ids)!=len(set(act_ids)) or set(act_ids)!=acts: raise ArtifactVerificationError("invalid act-definition structure")
    for a in program.acts:
        if len(a.roles)!=len(set(a.roles)): raise ArtifactVerificationError("duplicate role in act profile")
        for r in a.roles:
            if r not in roles or by[r].owner!=a.act: raise ArtifactVerificationError("invalid role reference in act profile")
    for n in _walk_ir(program):
        if not isinstance(getattr(n, "source_span", program.source_span), OriginalSpan): raise ArtifactVerificationError("invalid source span")
        if isinstance(n,irm.IRNatural) and (type(n.value) is not int or n.value<0): raise ArtifactVerificationError("negative/invalid Natural")
        if isinstance(n,irm.IRAddNatural) and (not isinstance(n.addend,irm.IRNumber) or not isinstance(n.augend,irm.IRNumber)): raise ArtifactVerificationError("invalid addition operand kind")
        if isinstance(n,irm.IRCheckedSubtractNatural) and (not isinstance(n.amount,irm.IRNumber) or not isinstance(n.source,irm.IRNumber)): raise ArtifactVerificationError("invalid subtraction operand kind")
        if isinstance(n,irm.IREqualProposition) and (not isinstance(n.left,irm.IRNumber) or not isinstance(n.right,irm.IRNumber)): raise ArtifactVerificationError("invalid proposition operand kind")
        if isinstance(n,irm.IRRoleAssociation) and not isinstance(n.value,irm.IRNumber): raise ArtifactVerificationError("invalid role value kind")
        if isinstance(n,irm.IRReplaceCurrentFact) and not isinstance(n.value,irm.IRNumber): raise ArtifactVerificationError("invalid replacement value kind")
        if isinstance(n,irm.IRPerformAct) and not all(isinstance(x,irm.IRRoleAssociation) for x in n.associations): raise ArtifactVerificationError("invalid role association kind")
        if isinstance(n,irm.IRProduceResult) and not isinstance(n.value,irm.IRNumber): raise ArtifactVerificationError("invalid result value kind")
        if isinstance(n,irm.IRThen) and (not n.actions or not all(isinstance(x,irm.IRAction) for x in n.actions)): raise ArtifactVerificationError("invalid explicit sequence")
        if isinstance(n,irm.IRConditional) and (not isinstance(n.proposition,irm.IRProposition) or not isinstance(n.if_holds,irm.IRAction) or not isinstance(n.if_not,irm.IRAction)): raise ArtifactVerificationError("invalid conditional semantic kind")
        if isinstance(n,irm.IRFixedRecurrence) and (type(n.count) is not int or n.count <= 0 or not isinstance(n.action,irm.IRAction)): raise ArtifactVerificationError("invalid fixed recurrence")
        if isinstance(n,irm.IRPostActionRecurrence) and (not isinstance(n.action,irm.IRAction) or not isinstance(n.proposition,irm.IRProposition)): raise ArtifactVerificationError("invalid post-action recurrence")
        if isinstance(n,(irm.IRReadCurrentFact,irm.IRReplaceCurrentFact,irm.IRInitialFact)) and n.place not in places: raise ArtifactVerificationError("unresolved place identity")
        if isinstance(n,irm.IRReadRoleNumber) and n.role not in roles: raise ArtifactVerificationError("unresolved role identity")
        if isinstance(n,irm.IRRecentResult) and n.act not in acts: raise ArtifactVerificationError("unresolved result act identity")
        if isinstance(n,irm.IRPerformAct):
            if n.act not in acts: raise ArtifactVerificationError("unresolved performed act")
            seen=[]
            for x in n.associations:
                if x.role not in roles or by[x.role].owner!=n.act: raise ArtifactVerificationError("invalid role association")
                seen.append(x.role)
            required=next(a.roles for a in program.acts if a.act==n.act)
            if set(seen)!=set(required) or len(seen)!=len(set(seen)): raise ArtifactVerificationError("role association profile mismatch")
        if isinstance(n,irm.IRCheckedSubtractNatural) and n.error_code!="ARITHMETIC_DOMAIN_ERROR": raise ArtifactVerificationError("unchecked/unknown subtraction failure code")
    try:
        validate_canonical_ir(program)
    except CanonicalIRValidationError as e:
        raise ArtifactVerificationError(f"canonical IR semantic validation failed: {e.issue.code}: {e.issue.detail}") from e

def verify_artifact(data:bytes, *, expected_language_edition:str=LANGUAGE_EDITION)->irm.IRProgram:
    try: obj=json.loads(data.decode("utf-8"))
    except Exception as e: raise ArtifactVerificationError("artifact is not canonical JSON data") from e
    if not isinstance(obj,dict) or set(obj)!={"artifact_version","ir_version","language_edition","payload_sha256","program"}: raise ArtifactVerificationError("artifact top-level fields invalid")
    if obj["artifact_version"]!=ARTIFACT_FORMAT_VERSION: raise ArtifactVerificationError("unknown artifact version")
    if obj["ir_version"]!=irm.IR_VERSION: raise ArtifactVerificationError("unknown IR version")
    if obj["language_edition"]!=expected_language_edition: raise ArtifactVerificationError("incompatible language edition")
    if hashlib.sha256(_canonical(obj["program"])).hexdigest()!=obj["payload_sha256"]: raise ArtifactVerificationError("artifact payload digest mismatch")
    try:
        program=_decode(obj["program"])
    except ArtifactVerificationError:
        raise
    except Exception as e:
        raise ArtifactVerificationError("malformed artifact payload") from e
    if not isinstance(program,irm.IRProgram): raise ArtifactVerificationError("artifact payload is not IRProgram")
    verify_ir(program)
    return program

__all__=["ARTIFACT_FORMAT_VERSION","ArtifactVerificationError","artifact_dict","serialize_artifact","verify_ir","verify_artifact"]
