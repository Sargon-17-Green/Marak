from __future__ import annotations

import dataclasses
from dataclasses import asdict, dataclass
from typing import Any

from compiler.artifact.format import serialize_artifact, verify_artifact
from compiler.backend.portable import execute_ir
from compiler.diagnostics.catalog import (
    AMBIG_SEMANTIC, AMBIG_UNRESOLVED, PARSE_NO_MATCH, PARSE_SPEC_NOT_READY,
    PROGRAM_MULTIPLE_PRINCIPAL, PROGRAM_NO_PRINCIPAL,
    PROGRAM_PREPARATION_AFTER_PRINCIPAL, PROGRAM_UNSEQUENCED_PRINCIPAL,
    SEM_SPEC_NOT_READY,
)
from compiler.ir_lower import lower_validated_hast
from compiler.lex.words import WordToken, lex_words
from compiler.models.diagnostics import Diagnostic, Severity
from compiler.models.hast import HastCoreProgram
from compiler.models.ir import IRProgram
from compiler.morphology.api import MorphologyEngine
from compiler.normalize.code import NormalizationResult, normalize_code
from compiler.parse.current_registry import CURRENT_REGISTRY
from compiler.resolve.current_constraints import find_current_constraint_issues
from compiler.resolve.a13_program import A13ResolutionError, resolve_a13_program
from compiler.validate.a12_rules import find_a12_validation_issues
from compiler.validate.a13_b12_rules import validate_a13_b12
from compiler.validate.ir_canonical import validate_canonical_ir
from compiler.validate.domains import DomainValidationError, validate_hast_domains
from compiler.parse.grammar import ConstructionRegistry
from compiler.parse.forest import AmbiguityStatus, ParseElement, ParseForest, ParseLeaf, ParseNode
from compiler.parse.parser import ParseResult, Parser
from compiler.runtime.reference import execute_reference
from compiler.runtime.invocation import InputBinding, ValidatedInvocation
from compiler.source.text import SourceText
from compiler.source.unicode_policy import DEFAULT_WHITESPACE_POLICY, WhitespacePolicy


@dataclass(frozen=True, slots=True)
class ParsePipelineResult:
    normalized: NormalizationResult
    tokens: tuple[WordToken, ...]
    morphology: dict[int, tuple]
    parse_result: ParseResult
    @property
    def forest(self) -> ParseForest: return self.parse_result.forest


@dataclass(frozen=True, slots=True)
class CheckResult:
    valid: bool
    diagnostics: tuple[Diagnostic, ...]
    normalized: NormalizationResult
    tokens: tuple[WordToken, ...]
    forest: ParseForest
    parse_result: ParseResult
    hast: HastCoreProgram | None = None


@dataclass(frozen=True, slots=True)
class CompilationResult:
    valid: bool
    diagnostics: tuple[Diagnostic, ...]
    hast: HastCoreProgram | None
    ir: IRProgram | None
    artifact: bytes | None
    check_result: CheckResult


@dataclass(frozen=True, slots=True)
class RunResult:
    compilation: CompilationResult
    outcome: object | None


@dataclass(frozen=True, slots=True)
class ToolRuntimeFailure:
    """Public API infrastructure failure; never a Marak language outcome."""
    category: str = "IMPLEMENTATION_INTERNAL_FAILURE"
    host_exception_type: str = "Exception"


def normalize(source: str | SourceText, *, file: str="<memory>", whitespace_policy:WhitespacePolicy=DEFAULT_WHITESPACE_POLICY)->NormalizationResult:
    return normalize_code(source,file=file,whitespace_policy=whitespace_policy)

def lex(source: str | SourceText, *, file: str="<memory>", whitespace_policy:WhitespacePolicy=DEFAULT_WHITESPACE_POLICY)->tuple[WordToken,...]:
    return lex_words(normalize(source,file=file,whitespace_policy=whitespace_policy))

def parse(source: str | SourceText, *, file: str="<memory>", registry:ConstructionRegistry=CURRENT_REGISTRY, whitespace_policy:WhitespacePolicy=DEFAULT_WHITESPACE_POLICY, start_lhs:str|None=None)->ParsePipelineResult:
    n=normalize(source,file=file,whitespace_policy=whitespace_policy)
    tokens=lex_words(n)
    morphology=dict(MorphologyEngine().analyze(tokens))
    parsed=Parser(registry).parse(tokens,morphology,source_map=n.source_map,start_lhs=start_lhs)
    return ParsePipelineResult(n,tokens,morphology,parsed)

def _construction_ids(element:ParseElement)->set[str]:
    if isinstance(element,ParseLeaf): return set()
    out={element.construction_id}
    for child in element.children: out.update(_construction_ids(child))
    return out

def _is_a13(registry:ConstructionRegistry)->bool:
    return registry.registry_version.startswith(("a13-b12","c5.2-","c5.3-","c5.4-","c5.5-"))

def _slice_parses_as(tokens, registry: ConstructionRegistry, lhs: str) -> bool:
    if not tokens:
        return False
    morphology=dict(MorphologyEngine().analyze(tokens))
    parsed=Parser(registry).parse(tokens,morphology,start_lhs=lhs)
    return bool(parsed.forest.alternatives)

def _program_parse_diagnostic(tokens, parsed, n, registry: ConstructionRegistry):
    # Diagnose root transitions structurally.  The word ועתה is not globally
    # reserved: it may occur in an explicit Name slot.  A top-level principal
    # transition is therefore a token whose prefix is a complete Preparation
    # (or empty), not merely any matching normalized token (E-FIND-022).
    if tokens and _slice_parses_as(tokens, registry, "Preparation"):
        return Diagnostic(PROGRAM_NO_PRINCIPAL,Severity.ERROR,"parse","Core program requires exactly one top-level ועתה transition.","תוכנית Core דורשת מעבר עליון אחד בדיוק באמצעות ועתה.",source_span=n.source_map.span(0,len(n.text)),metadata={"marker_count":0,"count_basis":"top-level-grammar"})

    raw_positions=[i for i,t in enumerate(tokens) if t.text=="ועתה"]
    top_level=[]
    for idx in raw_positions:
        if idx==0 or _slice_parses_as(tokens[:idx], registry, "Preparation"):
            top_level.append(idx)

    if not top_level:
        return Diagnostic(PROGRAM_NO_PRINCIPAL,Severity.ERROR,"parse","Core program requires exactly one top-level ועתה transition.","תוכנית Core דורשת מעבר עליון אחד בדיוק באמצעות ועתה.",source_span=n.source_map.span(0,len(n.text)),metadata={"marker_count":0,"count_basis":"top-level-grammar"})

    first=top_level[0]
    # A second raw ועתה is a second top-level transition only when the material
    # between it and the first transition is itself a complete executable
    # sequence.  Name-slot occurrences inside that sequence do not qualify.
    secondaries=[]
    for idx in raw_positions:
        if idx<=first:
            continue
        if _slice_parses_as(tokens[first+1:idx], registry, "ExecutableSequence"):
            secondaries.append(idx)
    marker_count=1+len(secondaries)
    if marker_count>1:
        span=tokens[secondaries[0]].original
        return Diagnostic(PROGRAM_MULTIPLE_PRINCIPAL,Severity.ERROR,"parse","Core program contains more than one top-level ועתה transition.","תוכנית Core מכילה יותר ממעבר ועתה עליון אחד.",source_span=span,metadata={"marker_count":marker_count,"count_basis":"top-level-grammar"})

    idx=first
    # A13 preparation has explicit linguistic openers. Detect those openers
    # anywhere after the top-level transition before diagnosing a generic
    # unsequenced executable tail.
    prep_prefixes=(("יהי","מקום","ושמו"),("יהי","מעשה","ושמו"),("יהי","במעשה","אשר"),("זה","דבר","המעשה","אשר"))
    texts=[t.text for t in tokens]
    for j in range(idx+1,len(tokens)):
        for prefix in prep_prefixes:
            if tuple(texts[j:j+len(prefix)])==prefix:
                return Diagnostic(PROGRAM_PREPARATION_AFTER_PRINCIPAL,Severity.ERROR,"parse","Preparatory material cannot occur after the principal ועתה transition.","חומר הכנה אינו יכול להופיע לאחר מעבר ועתה אל הביצוע העיקרי.",source_span=tokens[j].original,metadata={"preparation_start_token":j})
    failure=parsed.failure
    if failure and "word:ואחרי" in failure.expected and failure.furthest_token < len(tokens):
        return Diagnostic(PROGRAM_UNSEQUENCED_PRINCIPAL,Severity.ERROR,"parse","Adjacent principal executable material is not sequenced; Core requires explicit ואחרי כן.","חומר ביצוע עיקרי צמוד אינו יוצר סדר; Core דורש ואחרי כן במפורש.",source_span=tokens[failure.furthest_token].original,metadata={"furthest_token":failure.furthest_token})
    return None

def check(source: str | SourceText, *, file: str="<memory>", registry:ConstructionRegistry=CURRENT_REGISTRY, whitespace_policy:WhitespacePolicy=DEFAULT_WHITESPACE_POLICY)->CheckResult:
    pipeline=parse(source,file=file,registry=registry,whitespace_policy=whitespace_policy)
    n,tokens,parsed=pipeline.normalized,pipeline.tokens,pipeline.parse_result
    forest=parsed.forest; diagnostics=[]; hast=None
    if not parsed.grammar_available:
        span=n.source_map.span(0,len(n.text)) if n.text else n.source_map.span(0,0)
        diagnostics.append(Diagnostic(PARSE_SPEC_NOT_READY,Severity.ERROR,"parse","The selected specification snapshot contains no admitted root production; proposed syntax is not guessed.","בתמונת המפרט שנבחרה אין הפקת־שורש מותרת; המנתח אינו מנחש תחביר שמעמדו PROPOSED.",source_span=span,normalized_span=(0,len(n.text)),metadata={"blocked_on":["A positive NORMATIVE construction","B semantics for that construction"],"registry_version":registry.registry_version,"proposed_positive":[d.construction_id for d in registry.declarations if d.kind.value=="positive" and d.status.value=="proposed"]}))
    elif not forest.alternatives:
        targeted=_program_parse_diagnostic(tokens,parsed,n,registry) if _is_a13(registry) else None
        if targeted: diagnostics.append(targeted)
        failure=parsed.failure; token_at=failure.furthest_token if failure else 0
        span=tokens[token_at].original if token_at<len(tokens) else n.source_map.span(len(n.text),len(n.text))
        norm_span=(tokens[token_at].normalized_start,tokens[token_at].normalized_end) if token_at<len(tokens) else (len(n.text),len(n.text))
        diagnostics.append(Diagnostic(PARSE_NO_MATCH,Severity.ERROR,"parse","The source does not match any admitted normative construction.","המקור אינו תואם שום מבנה נורמטיבי מותר.",source_span=span,normalized_span=norm_span,metadata={"furthest_token":failure.furthest_token if failure else None,"expected":list(failure.expected) if failure else []}))

    if forest.alternatives:
        for alternative in forest.alternatives:
            for issue in find_current_constraint_issues(alternative.root):
                diagnostics.append(Diagnostic(issue.code,Severity.ERROR,"resolve",issue.message_en,issue.message_he,source_span=issue.source_span,metadata=issue.metadata))
        for alternative in forest.alternatives:
            for issue in find_a12_validation_issues(alternative.root):
                diagnostics.append(Diagnostic(issue.code,Severity.ERROR,"semantic",issue.message_en,issue.message_he,source_span=issue.source_span,metadata=issue.metadata))
        blocked={}
        for alternative in forest.alternatives:
            for cid in sorted(_construction_ids(alternative.root)):
                gate=registry.semantic_gate(cid)
                if gate is not None and gate.status.value=="blocked_on_spec": blocked[cid]=gate
        if blocked:
            diagnostics.append(Diagnostic(SEM_SPEC_NOT_READY,Severity.ERROR,"semantic","The source has a normative surface parse, but parsed constructions remain blocked by the selected semantic baseline.","למקור יש קריאה תחבירית נורמטיבית, אך מבנים שנקראו עדיין חסומים לפי קו הבסיס הסמנטי שנבחר.",metadata={"blocked_constructions":[{"construction_id":cid,"reason":blocked[cid].reason,"dependencies":list(blocked[cid].dependencies)} for cid in sorted(blocked)],"surface_parse_preserved":True,"reference_model_not_normative":True}))

    if forest.ambiguity_status is AmbiguityStatus.UNRESOLVED_MULTIPLE:
        diagnostics.append(Diagnostic(AMBIG_UNRESOLVED,Severity.ERROR,"ambiguity","Multiple legal parses remain and no spec-grounded semantic equivalence proof is available.","נותרו כמה קריאות חוקיות ואין הוכחת שקילות סמנטית המבוססת על המפרט.",metadata={"alternative_count":len(forest.alternatives),"semantic_ids":sorted({a.semantic_id for a in forest.alternatives})}))
    elif forest.ambiguity_status is AmbiguityStatus.PROVEN_DISTINCT:
        diagnostics.append(Diagnostic(AMBIG_SEMANTIC,Severity.ERROR,"ambiguity","Multiple legal parses have proven distinct computational semantics.","לכמה קריאות חוקיות הוכחו משמעויות חישוביות שונות.",metadata={"alternative_count":len(forest.alternatives)}))

    if _is_a13(registry) and len(forest.alternatives)==1 and not diagnostics:
        try:
            hast=resolve_a13_program(forest.alternatives[0].root)
        except A13ResolutionError as exc:
            x=exc.issue; diagnostics.append(Diagnostic(x.code,Severity.ERROR,"resolve",x.message_en,x.message_he,source_span=x.source_span,metadata=x.metadata))
        if hast is not None:
            for x in validate_a13_b12(hast):
                diagnostics.append(Diagnostic(x.code,Severity.ERROR,"semantic",x.message_en,x.message_he,source_span=x.source_span,metadata={"semantic_code":x.semantic_code,**x.metadata}))
            try:
                validate_hast_domains(hast)
            except DomainValidationError as exc:
                diagnostics.append(Diagnostic(
                    exc.issue.diagnostic_code,
                    Severity.ERROR,
                    "semantic",
                    exc.issue.detail,
                    exc.issue.detail,
                    source_span=hast.source_span,
                    metadata={"semantic_code":exc.issue.code},
                ))
    return CheckResult(not diagnostics,tuple(diagnostics),n,tokens,forest,parsed,hast)

def compile_source(source: str|SourceText, *, file:str="<memory>", registry:ConstructionRegistry=CURRENT_REGISTRY, whitespace_policy:WhitespacePolicy=DEFAULT_WHITESPACE_POLICY)->CompilationResult:
    c=check(source,file=file,registry=registry,whitespace_policy=whitespace_policy)
    if not c.valid or c.hast is None: return CompilationResult(False,c.diagnostics,c.hast,None,None,c)
    ir=lower_validated_hast(c.hast)
    validate_canonical_ir(ir)
    artifact=serialize_artifact(ir,language_edition=registry.language_edition)
    verify_artifact(artifact)
    return CompilationResult(True,(),c.hast,ir,artifact,c)

def run_source(source: str|SourceText, *, file:str="<memory>", registry:ConstructionRegistry=CURRENT_REGISTRY, whitespace_policy:WhitespacePolicy=DEFAULT_WHITESPACE_POLICY, fuel:int|None=None, bindings:tuple[InputBinding,...]|ValidatedInvocation=())->RunResult:
    comp=compile_source(source,file=file,registry=registry,whitespace_policy=whitespace_policy)
    if not comp.valid or comp.artifact is None:return RunResult(comp,None)
    try:
        ir=verify_artifact(comp.artifact)
        return RunResult(comp,execute_ir(ir,fuel=fuel,bindings=bindings))
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as exc:
        return RunResult(comp,ToolRuntimeFailure(host_exception_type=type(exc).__name__))

def run_reference(source: str|SourceText, *, file:str="<memory>", registry:ConstructionRegistry=CURRENT_REGISTRY, whitespace_policy:WhitespacePolicy=DEFAULT_WHITESPACE_POLICY, fuel:int|None=None, bindings:tuple[InputBinding,...]|ValidatedInvocation=()):
    c=check(source,file=file,registry=registry,whitespace_policy=whitespace_policy)
    if not c.valid or c.hast is None:return c,None
    return c,execute_reference(c.hast,fuel=fuel,bindings=bindings)

def _span_dict(span):
    if span is None:return None
    def p(x):return {"file":x.file,"char_offset":x.char_offset,"byte_offset":x.byte_offset,"line":x.line,"column":x.column}
    return {"start":p(span.start),"end":p(span.end)}
def _tree_dict(element:ParseElement)->dict[str,Any]:
    if isinstance(element,ParseLeaf):return {"kind":"leaf","token_index":element.token_index,"text":element.text,"normalized_span":[element.normalized_start,element.normalized_end],"source_span":_span_dict(element.original),"terminal_role":element.terminal_role,"numeric_value":element.numeric_value}
    return {"kind":"node","production_id":element.production_id,"construction_id":element.construction_id,"symbol":element.symbol,"token_span":[element.token_start,element.token_end],"normalized_span":None if element.normalized_start is None else [element.normalized_start,element.normalized_end],"source_span":_span_dict(element.original),"children":[_tree_dict(c) for c in element.children]}
def _semantic_obj(x):
    if dataclasses.is_dataclass(x):
        d={"kind":type(x).__name__}
        for f in dataclasses.fields(x):
            v=getattr(x,f.name)
            if f.name=="source_span": d[f.name]=_span_dict(v)
            elif isinstance(v,tuple): d[f.name]=[_semantic_obj(y) for y in v]
            elif dataclasses.is_dataclass(v): d[f.name]=_semantic_obj(v)
            else:d[f.name]=v
        return d
    return x

def _walk_hast(node):
    if dataclasses.is_dataclass(node):
        yield node
        for f in dataclasses.fields(node):
            if f.name == "source_span":
                continue
            value = getattr(node, f.name)
            if isinstance(value, tuple):
                for child in value:
                    if dataclasses.is_dataclass(child):
                        yield from _walk_hast(child)
            elif dataclasses.is_dataclass(value):
                yield from _walk_hast(value)


def _resolved_explanation(program: HastCoreProgram) -> dict[str, Any]:
    from compiler.models.hast import (
        HastActBody, HastActIntroduction, HastPlaceIntroduction, HastRecentResult,
        HastRecentTypedResult, HastRoleDeclaration, HastSymbolDomainDeclaration,
        HastSymbolMemberDeclaration, HastSymbolOrderAdjacent,
    )
    visibility=[]
    body_ownership=[]
    symbol_domains=[]
    symbol_members=[]
    symbol_order=[]
    for index, unit in enumerate(program.preparation):
        if isinstance(unit, HastPlaceIntroduction):
            visibility.append({"kind":"place","id":unit.place.serial,"spelling":unit.place.spelling,"visible_after_preparation_index":index})
        elif isinstance(unit, HastActIntroduction):
            visibility.append({"kind":"act","id":unit.act.serial,"spelling":unit.act.spelling,"visible_after_preparation_index":index})
        elif isinstance(unit, HastRoleDeclaration):
            visibility.append({"kind":"role","id":unit.role.serial,"spelling":unit.role.spelling,"owner_act_id":unit.role.owner.serial,"visible_after_preparation_index":index})
        elif isinstance(unit, HastActBody):
            body_ownership.append({"act_id":unit.act.serial,"act":unit.act.spelling,"preparation_index":index,"source_span":_span_dict(unit.source_span)})
        elif isinstance(unit,HastSymbolDomainDeclaration):
            symbol_domains.append({"domain_id":unit.domain_id.serial,"source_name":unit.domain_id.spelling,"debug_only_internal_identity":True})
        elif isinstance(unit,HastSymbolMemberDeclaration):
            symbol_members.append({
                "domain_id":unit.domain_id.serial,"member_id":unit.member_id.serial,
                "source_name":unit.member_id.spelling,"canonical_external_label":unit.external_label,
                "debug_only_internal_identity":True,
            })
        elif isinstance(unit,HastSymbolOrderAdjacent):
            symbol_order.append({
                "domain_id":unit.domain_id.serial,"before_member_id":unit.before_member_id.serial,
                "after_member_id":unit.after_member_id.serial,"relation":"adjacent-before",
                "debug_only_internal_identity":True,
            })
    recent=[]
    for node in _walk_hast(program):
        if isinstance(node,(HastRecentResult,HastRecentTypedResult)):
            recent.append({"act_id":node.act.serial,"act":node.act.spelling,"source_span":_span_dict(node.source_span),"relation":"just-completed direct performance; intervening executable expires provenance","typed":isinstance(node,HastRecentTypedResult)})
    return {
        "program_division": {
            "preparation": [type(x).__name__ for x in program.preparation],
            "principal": type(program.principal).__name__,
            "entry_is_surface_transition": "ועתה",
            "entry_is_not_magic_main": True,
        },
        "identities": {
            "places": [{"id":x.serial,"spelling":x.spelling} for x in program.places],
            "acts": [{"id":x.serial,"spelling":x.spelling} for x in program.acts],
            "roles": [{"id":x.serial,"spelling":x.spelling,"owner_act_id":x.owner.serial,"owner_act":x.owner.spelling} for x in program.roles],
            "symbol_domains_debug":symbol_domains,
            "symbol_members_debug":symbol_members,
        },
        "static_domains": {
            "places":[{"place_id":x.place.serial,"domain":_semantic_obj(x.domain)} for x in program.place_domains],
            "roles":[{"role_id":x.role.serial,"domain":_semantic_obj(x.domain)} for x in program.role_domains],
            "act_outputs":[{"act_id":x.act.serial,"domain":None if x.domain is None else _semantic_obj(x.domain)} for x in program.act_output_domains],
        },
        "symbol_order_debug":symbol_order,
        "visibility": visibility,
        "ownership": {"roles": [{"role_id":x.serial,"owner_act_id":x.owner.serial} for x in program.roles],"bodies":body_ownership},
        "immediate_result_provenance": recent,
    }

def explain(source: str|SourceText, *, file:str="<memory>", level:str="all", registry:ConstructionRegistry=CURRENT_REGISTRY, whitespace_policy:WhitespacePolicy=DEFAULT_WHITESPACE_POLICY)->dict[str,Any]:
    result=check(source,file=file,registry=registry,whitespace_policy=whitespace_policy)
    pipeline=parse(source,file=file,registry=registry,whitespace_policy=whitespace_policy)
    parsed=pipeline.parse_result
    base={"language_edition":registry.language_edition,"registry_version":registry.registry_version,"registry":registry.to_dict(),"diagnostics":[d.to_dict() for d in result.diagnostics]}
    if level in {"normalization","all","parse","resolve","semantic"}:
        base.update({"normalized_source":result.normalized.text,"whitespace_policy":result.normalized.whitespace_policy_id,"tokens":[{"index":t.index,"text":t.text,"normalized_span":[t.normalized_start,t.normalized_end],"source_span":_span_dict(t.original)} for t in result.tokens]})
    if level in {"parse","all","resolve","semantic"}:
        base["parse"]={"grammar_available":parsed.grammar_available,"ambiguity_status":parsed.forest.ambiguity_status.value,"metrics":asdict(parsed.metrics),"failure":None if parsed.failure is None else asdict(parsed.failure),"alternatives":[{"semantic_id":a.semantic_id,"semantic_fingerprint":a.semantic_fingerprint,"tree":_tree_dict(a.root)} for a in parsed.forest.alternatives]}
    if level in {"resolve","semantic","all"}:
        base["hast"]=None if result.hast is None else _semantic_obj(result.hast)
        if result.hast is not None:
            base.update(_resolved_explanation(result.hast))
        if result.hast is not None and not result.diagnostics:
            base["validated_ir"]=_semantic_obj(lower_validated_hast(result.hast))
    return base
