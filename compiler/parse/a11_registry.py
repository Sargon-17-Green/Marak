from __future__ import annotations

from compiler.parse.a10_registry import A10_REGISTRY
from compiler.parse.grammar import (
    ConstructionDeclaration,
    ConstructionKind,
    ConstructionRegistry,
    ConstructionSemanticGate,
    NameTerminal,
    Nonterminal,
    Production,
    SemanticReadiness,
    SpecStatus,
    WordTerminal,
)

A11_LANGUAGE_EDITION = "core-0.1-candidate-a11-b9-review"

# A11 supersedes A10's free provenance-result phrase.  Current result reference
# now requires עתה and, for multiple results, an ordinal.  Preserve the rest of
# A10 while preventing the superseded A10 result production from remaining live.
_BASE_DECLARATIONS = tuple(
    d for d in A10_REGISTRY.declarations
    if d.construction_id != "A10.RESULT_PROVENANCE_NUMBER"
)
_BASE_PRODUCTIONS = tuple(
    p for p in A10_REGISTRY.productions
    if p.construction_id != "A10.RESULT_PROVENANCE_NUMBER"
)
# Replace stale A10 blockers whose source questions A11 has answered.  Global
# מקום semantics is now A10+B7+A11-ready; reusable-performance semantics is not.
_BASE_GATES = tuple(
    g for g in A10_REGISTRY.semantic_gates
    if g.construction_id not in {
        "A10.NAMED_ACT_PERFORMANCE",
        "A10.RESULT_PROVENANCE_NUMBER",
        "A10.NAMED_PLACE_STATE",
        "A10.PLACE_INTRODUCTION",
        "A10.PLACE_REPLACEMENT",
    }
)


def W(text: str) -> WordTerminal:
    return WordTerminal(text)


_DECLARATIONS = _BASE_DECLARATIONS + (
    ConstructionDeclaration(
        "A11.BODY_SCOPE", ConstructionKind.POSITIVE, SpecStatus.NORMATIVE,
        ("A-BODY-001", "A-BODY-002", "A-BODY-003", "A-BODY-004", "A-BODY-005"),
        "Named act bodies use explicit אלה דברי המעשה... / עד הנה דברי המעשה... boundaries; the closer repeats the same explicit act name and body units use overt relations.",
    ),
    ConstructionDeclaration(
        "A11.INPUT_ROLE", ConstructionKind.POSITIVE, SpecStatus.NORMATIVE,
        ("A-ROLE-001", "A-ROLE-002", "A-ROLE-005", "A-ROLE-006"),
        "A numeric input role is a named דבר owned by a named מעשה; role identity is explicit and never positional.",
    ),
    ConstructionDeclaration(
        "A11.ROLE_ASSOCIATION", ConstructionKind.POSITIVE, SpecStatus.NORMATIVE,
        ("A-ROLE-003", "A-ROLE-004"),
        "Performance associates a pure numeric Value with an explicitly named role via בהיות VALUE תחת ROLE; source order does not establish matching.",
    ),
    ConstructionDeclaration(
        "A11.CURRENT_PERFORMANCE", ConstructionKind.POSITIVE, SpecStatus.NORMATIVE,
        ("A-CURRENT-001", "A-CURRENT-002", "A-CURRENT-003"),
        "המעשה הזה is the current performance occurrence only inside an act body; it is a source deictic, not a stack-frame lookup rule.",
    ),
    ConstructionDeclaration(
        "A11.RESULT_PRODUCTION", ConstructionKind.POSITIVE, SpecStatus.NORMATIVE,
        ("A-OUT-001", "A-OUT-002", "A-OUT-003", "A-OUT-007"),
        "הוצא מן המעשה הזה את VALUE produces one ordered numeric result and does not itself terminate the performance.",
    ),
    ConstructionDeclaration(
        "A11.IMMEDIATE_RESULT_REFERENCE", ConstructionKind.POSITIVE, SpecStatus.NORMATIVE,
        ("A-OUT-004", "A-OUT-005", "A-OUT-006"),
        "Immediate result reference requires עתה; unqualified reference requires exactly one result, while ordinal forms distinguish multiple results.",
    ),
    ConstructionDeclaration(
        "A11.PERFORMANCE_LOCAL_STATE", ConstructionKind.POSITIVE, SpecStatus.NORMATIVE,
        ("A-LOCAL-001", "A-LOCAL-002", "A-LOCAL-003", "A-LOCAL-004", "A-LOCAL-005"),
        "Performance-owned מקום explicitly includes המעשה הזה in its referent; same spelling in recursive performances does not imply same state referent.",
    ),
    ConstructionDeclaration(
        "A11.NO_POSITIONAL_ROLE_MATCHING", ConstructionKind.NEGATIVE, SpecStatus.NORMATIVE,
        ("A11-NG-ROLE-001", "A11-NG-ROLE-002", "A11-NG-ROLE-003"),
        "Actual inputs are not matched to roles by order; every required named role must be associated exactly once.",
    ),
    ConstructionDeclaration(
        "A11.NO_IMPLICIT_RETURN", ConstructionKind.NEGATIVE, SpecStatus.NORMATIVE,
        ("A11-NG-OUT-001", "A11-NG-OUT-002", "A11-NG-LEAK-003"),
        "A final value is not an implicit result and result production is not abrupt Return/tuple-return semantics.",
    ),
    ConstructionDeclaration(
        "A11.NO_DYNAMIC_CALLER_LOCAL_LOOKUP", ConstructionKind.NEGATIVE, SpecStatus.NORMATIVE,
        ("A11-NG-LOCAL-001", "A11-NG-LOCAL-002", "A11-NG-CURRENT-002"),
        "Current-performance and local-place reference never mean runtime caller-chain or top-of-stack lookup.",
    ),
    ConstructionDeclaration(
        "A11.NO_FREE_RESULT_HISTORY", ConstructionKind.NEGATIVE, SpecStatus.NORMATIVE,
        ("A11-NG-OUT-003", "A11-NG-OUT-004"),
        "A result reference is immediate and uniquely determined; there is no hidden global last-result register or historical nearest-result lookup.",
    ),
)

_PRODUCTIONS = _BASE_PRODUCTIONS + (
    # A complete act-introduction unit.  This says nothing about adjacency or
    # execution order with other top-level discourse units.
    Production(
        "A11.TOP.ACT.IDENTITY", "A10.NAMED_ACT_IDENTITY", "TopLevelUnit",
        (Nonterminal("NamedActIdentity"),), "A10.NAMED_ACT_IDENTITY", root=True,
    ),

    # Named input role declaration.  Repeated explicit names are checked by the
    # resolver; the grammar itself never substitutes nearest or positional names.
    Production(
        "A11.ROLE.DECLARATION", "A11.INPUT_ROLE", "RoleDeclaration",
        (
            W("יהי"), W("במעשה"), W("אשר"), W("שמו"), NameTerminal("RoleOwnerActionName"),
            W("דבר"), W("ושמו"), NameTerminal("DeclaredRoleName"),
            W("ובעשות"), W("את"), W("המעשה"), W("אשר"), W("שמו"),
            NameTerminal("RoleOwnerActionName"), W("יעמד"), W("מספר"), W("תחת"), W("הדבר"),
            W("אשר"), W("במעשה"), W("אשר"), W("שמו"), NameTerminal("RoleOwnerActionName"),
            W("שמו"), NameTerminal("DeclaredRoleName"),
        ),
        "A11.INPUT_ROLE", root=True,
    ),

    # One or more explicitly named role associations on a performance.  The
    # association list has no positional matching force.
    Production(
        "A11.ROLE.ASSOCIATIONS.ONE", "A11.ROLE_ASSOCIATION", "RoleAssociations",
        (
            W("בהיות"), Nonterminal("NumberValue"), W("תחת"), W("הדבר"), W("אשר"), W("במעשה"),
            W("אשר"), W("שמו"), NameTerminal("RoleOwnerActionName"), W("שמו"), NameTerminal("AssociatedRoleName"),
        ),
        "A11.ROLE_ASSOCIATION",
    ),
    Production(
        "A11.ROLE.ASSOCIATIONS.MORE", "A11.ROLE_ASSOCIATION", "RoleAssociations",
        (
            Nonterminal("RoleAssociations"), W("ובהיות"), Nonterminal("NumberValue"), W("תחת"), W("הדבר"),
            W("אשר"), W("במעשה"), W("אשר"), W("שמו"), NameTerminal("RoleOwnerActionName"),
            W("שמו"), NameTerminal("AssociatedRoleName"),
        ),
        "A11.ROLE_ASSOCIATION",
    ),
    Production(
        "A11.ACT.PERFORM.WITH.ROLES", "A11.ROLE_ASSOCIATION", "AtomicAction",
        (
            W("עשה"), W("את"), W("המעשה"), W("אשר"), W("שמו"), NameTerminal("PerformedActionName"),
            Nonterminal("RoleAssociations"),
        ),
        "A11.ROLE_ASSOCIATION", root=True,
    ),

    # Performance-relative input value.  It is a NumberValue only within the
    # source relation that explicitly names the role and current performance.
    Production(
        "A11.NUMBER.CURRENT.ROLE", "A11.CURRENT_PERFORMANCE", "NumberValue",
        (
            W("המספר"), W("אשר"), W("במעשה"), W("הזה"), W("עומד"), W("תחת"), W("הדבר"),
            W("אשר"), W("במעשה"), W("אשר"), W("שמו"), NameTerminal("RoleOwnerActionName"),
            W("שמו"), NameTerminal("AssociatedRoleName"),
        ),
        "A11.CURRENT_ROLE_NUMBER",
    ),

    # Body-only result production.  Its distinct nonterminal prevents existing
    # top-level AtomicAction sequence grammar from licensing it outside a body.
    Production(
        "A11.RESULT.PRODUCE", "A11.RESULT_PRODUCTION", "BodyAtomicAction",
        (W("הוצא"), W("מן"), W("המעשה"), W("הזה"), W("את"), Nonterminal("NumberValue")),
        "A11.RESULT_PRODUCTION",
    ),

    # Immediate result references.  These are value constituents, never program
    # roots; adjacency/uniqueness remains a resolver/validator obligation.
    Production(
        "A11.RESULT.IMMEDIATE.SINGLE", "A11.IMMEDIATE_RESULT_REFERENCE", "NumberValue",
        (
            W("המספר"), W("אשר"), W("יצא"), W("עתה"), W("מן"), W("המעשה"), W("אשר"), W("שמו"),
            NameTerminal("ResultActionName"),
        ),
        "A11.IMMEDIATE_RESULT_SINGLE",
    ),
    Production(
        "A11.RESULT.IMMEDIATE.FIRST", "A11.IMMEDIATE_RESULT_REFERENCE", "NumberValue",
        (
            W("המספר"), W("הראשון"), W("אשר"), W("יצא"), W("עתה"), W("מן"), W("המעשה"), W("אשר"),
            W("שמו"), NameTerminal("ResultActionName"),
        ),
        "A11.IMMEDIATE_RESULT_ORDINAL",
    ),
    Production(
        "A11.RESULT.IMMEDIATE.SECOND", "A11.IMMEDIATE_RESULT_REFERENCE", "NumberValue",
        (
            W("המספר"), W("השני"), W("אשר"), W("יצא"), W("עתה"), W("מן"), W("המעשה"), W("אשר"),
            W("שמו"), NameTerminal("ResultActionName"),
        ),
        "A11.IMMEDIATE_RESULT_ORDINAL",
    ),

    # Performance-owned state: body-only establishment/replacement and a value
    # constituent for its explicitly queried current number.
    Production(
        "A11.LOCAL.CURRENT.NUMBER", "A11.PERFORMANCE_LOCAL_STATE", "NumberValue",
        (
            W("המספר"), W("אשר"), W("במקום"), W("אשר"), W("במעשה"), W("הזה"), W("שמו"),
            NameTerminal("LocalPlaceName"),
        ),
        "A11.LOCAL_CURRENT_NUMBER",
    ),
    Production(
        "A11.LOCAL.INTRODUCE", "A11.PERFORMANCE_LOCAL_STATE", "BodyAtomicAction",
        (
            W("יהי"), W("במעשה"), W("הזה"), W("מקום"), W("ושמו"), NameTerminal("LocalPlaceName"),
            W("ובמקום"), W("אשר"), W("במעשה"), W("הזה"), W("שמו"), NameTerminal("LocalPlaceName"),
            W("יהי"), Nonterminal("NumberValue"), W("לבדו"),
        ),
        "A11.LOCAL_STATE_INTRODUCTION",
    ),
    Production(
        "A11.LOCAL.REPLACE", "A11.PERFORMANCE_LOCAL_STATE", "BodyAtomicAction",
        (
            W("שים"), W("במקום"), W("אשר"), W("במעשה"), W("הזה"), W("שמו"), NameTerminal("LocalPlaceName"),
            W("את"), Nonterminal("NumberValue"), W("תחת"), W("המספר"), W("אשר"), W("במקום"),
            W("אשר"), W("במעשה"), W("הזה"), W("שמו"), NameTerminal("LocalPlaceName"),
        ),
        "A11.LOCAL_STATE_REPLACEMENT",
    ),

    # Body unit/sequence grammar.  BodyAtomicAction is separate so context-bound
    # deictic constructions cannot leak to top-level AtomicAction roots.
    Production(
        "A11.BODY.UNIT.ATOMIC", "A11.BODY_SCOPE", "BodyUnit",
        (Nonterminal("AtomicAction"),), "A11.BODY_UNIT",
    ),
    Production(
        "A11.BODY.UNIT.LOCAL", "A11.BODY_SCOPE", "BodyUnit",
        (Nonterminal("BodyAtomicAction"),), "A11.BODY_UNIT",
    ),
    Production(
        "A11.BODY.UNIT.CONDITIONAL", "A11.BODY_SCOPE", "BodyUnit",
        (Nonterminal("ConditionalConsequence"),), "A11.BODY_UNIT",
    ),
    Production(
        "A11.BODY.UNIT.RECURRENCE", "A11.BODY_SCOPE", "BodyUnit",
        (Nonterminal("AfterGatedRecurrence"),), "A11.BODY_UNIT",
    ),
    Production(
        "A11.BODY.UNIT.COUNTED", "A11.BODY_SCOPE", "BodyUnit",
        (Nonterminal("CountedConsequence"),), "A11.BODY_UNIT",
    ),
    Production(
        "A11.BODY.SEQUENCE.ONE", "A11.BODY_SCOPE", "BodySequence",
        (Nonterminal("BodyUnit"),), "A11.BODY_SEQUENCE",
    ),
    Production(
        "A11.BODY.SEQUENCE.MORE", "A11.BODY_SCOPE", "BodySequence",
        (Nonterminal("BodySequence"), W("ואחרי"), W("כן"), Nonterminal("BodyUnit")),
        "A11.BODY_SEQUENCE",
    ),
    Production(
        "A11.BODY.DEFINITION", "A11.BODY_SCOPE", "ActBodyDefinition",
        (
            W("אלה"), W("דברי"), W("המעשה"), W("אשר"), W("שמו"), NameTerminal("BodyActionName"),
            Nonterminal("BodySequence"), W("עד"), W("הנה"), W("דברי"), W("המעשה"), W("אשר"), W("שמו"),
            NameTerminal("BodyActionName"),
        ),
        "A11.BODY_SCOPE", root=True,
    ),
)

_GATES = _BASE_GATES + (
    ConstructionSemanticGate(
        "A10.NAMED_ACT_PERFORMANCE", SemanticReadiness.BLOCKED_ON_SPEC,
        "A11 closes body/input/result surface structure, but post-audit B has not yet closed reusable-performance occurrence, role association, completion and result semantics.",
        ("post-audit B reusable-performance semantics",),
    ),
    ConstructionSemanticGate(
        "A11.BODY_SCOPE", SemanticReadiness.BLOCKED_ON_SPEC,
        "A11 fixes lexical body boundaries and ordinary completion, but canonical execution of reusable performances awaits post-audit B action semantics.",
        ("post-audit B reusable-performance semantics",),
    ),
    ConstructionSemanticGate(
        "A11.INPUT_ROLE", SemanticReadiness.BLOCKED_ON_SPEC,
        "A11 fixes named role surface and valency, while B has not yet supplied the post-audit semantic relation between a performance occurrence and its role associations.",
        ("post-audit B role/performance semantics",),
    ),
    ConstructionSemanticGate(
        "A11.ROLE_ASSOCIATION", SemanticReadiness.BLOCKED_ON_SPEC,
        "A11 explicitly rejects positional/cell calling conventions; C waits for B to model the source-level Value-to-role relation without reintroducing them.",
        ("post-audit B role/performance semantics",),
    ),
    ConstructionSemanticGate(
        "A11.CURRENT_PERFORMANCE", SemanticReadiness.BLOCKED_ON_SPEC,
        "The deictic surface is closed, but its performance-occurrence identity must come from the post-audit reusable-computation model rather than a stack frame.",
        ("post-audit B performance-occurrence semantics",),
    ),
    ConstructionSemanticGate(
        "A11.RESULT_PRODUCTION", SemanticReadiness.BLOCKED_ON_SPEC,
        "A11 separates result production from cessation and permits zero/one/many results; B must still close their observable semantic carrier/order/lifetime.",
        ("post-audit B result semantics",),
    ),
    ConstructionSemanticGate(
        "A11.IMMEDIATE_RESULT_REFERENCE", SemanticReadiness.BLOCKED_ON_SPEC,
        "A11 closes the immediate reference words, but B must define result availability without a hidden last-result register.",
        ("post-audit B result semantics",),
    ),
    ConstructionSemanticGate(
        "A11.PERFORMANCE_LOCAL_STATE", SemanticReadiness.BLOCKED_ON_SPEC,
        "B7 closes state-bearing referents and A11 closes source ownership, but performance-occurrence identity is still required to form the full local referent canonically.",
        ("post-audit B performance-occurrence semantics",),
    ),
)

A11_REGISTRY = ConstructionRegistry(
    language_edition=A11_LANGUAGE_EDITION,
    registry_version="a11.1-c-surface-candidate",
    source_snapshot="A11_Surface_Language_Handoff+B7+B8+B9",
    declarations=_DECLARATIONS,
    productions=_PRODUCTIONS,
    semantic_gates=_GATES,
)

__all__ = ["A11_LANGUAGE_EDITION", "A11_REGISTRY"]
