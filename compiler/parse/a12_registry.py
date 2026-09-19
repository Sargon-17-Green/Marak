from __future__ import annotations

from compiler.parse.a11_registry import A11_REGISTRY
from compiler.parse.grammar import (
    ConstructionDeclaration,
    ConstructionKind,
    ConstructionRegistry,
    ConstructionSemanticGate,
    NameTerminal,
    Nonterminal,
    NumeralTerminal,
    Production,
    SemanticReadiness,
    SpecStatus,
    WordTerminal,
)
from compiler.parse.numeral_lexicons import A12_DIRECT_NUMERAL_LEXICON_ID

A12_LANGUAGE_EDITION = "core-0.1-frozen-candidate-a12-b11-review"


def W(text: str) -> WordTerminal:
    return WordTerminal(text)


# A12 freezes the direct 1..9999 numeral frontier and deliberately removes
# three A11 surface choices: plural body framing, ordinal/multiple results, and
# performance-owned mutable local places.  Historical A11 remains intact in its
# own registry; the current registry does not carry compatibility aliases.
_REMOVED_DECLARATIONS = {
    "A9.NUMERIC_LITERAL_FRAME",
    "A11.BODY_SCOPE",
    "A11.RESULT_PRODUCTION",
    "A11.IMMEDIATE_RESULT_REFERENCE",
    "A11.PERFORMANCE_LOCAL_STATE",
    "A11.NO_DYNAMIC_CALLER_LOCAL_LOOKUP",
}
_BASE_DECLARATIONS = tuple(
    d for d in A11_REGISTRY.declarations if d.construction_id not in _REMOVED_DECLARATIONS
)

_REMOVED_PRODUCTION_PREFIXES = (
    "A11.BODY.",
    "A11.RESULT.",
    "A11.LOCAL.",
)
_REMOVED_PRODUCTIONS = {
    "A9.NUMBER.LITERAL.ONE",
    "A10.NUMBER.LITERAL.THREE",
    "A10.NUMBER.LITERAL.FOUR",
}
_BASE_PRODUCTIONS = tuple(
    p for p in A11_REGISTRY.productions
    if p.production_id not in _REMOVED_PRODUCTIONS
    and not p.production_id.startswith(_REMOVED_PRODUCTION_PREFIXES)
)

_REMOVED_GATES = {
    "A10.NAMED_ACT_PERFORMANCE",
    "A11.BODY_SCOPE",
    "A11.INPUT_ROLE",
    "A11.ROLE_ASSOCIATION",
    "A11.CURRENT_PERFORMANCE",
    "A11.RESULT_PRODUCTION",
    "A11.IMMEDIATE_RESULT_REFERENCE",
    "A11.PERFORMANCE_LOCAL_STATE",
}
_BASE_GATES = tuple(
    g for g in A11_REGISTRY.semantic_gates if g.construction_id not in _REMOVED_GATES
)

_DECLARATIONS = _BASE_DECLARATIONS + (
    ConstructionDeclaration(
        "A12.DIRECT_NUMERIC_LITERAL",
        ConstructionKind.POSITIVE,
        SpecStatus.NORMATIVE,
        ("A-NUM-001", "A-NUM-002", "A-NUM-003"),
        "Core v0.1 admits exactly the frozen canonical direct numeral spellings 1..9999 inside המספר אשר הוא NUMERAL; this is a direct-literal admission frontier, not a semantic numeric bound.",
    ),
    ConstructionDeclaration(
        "A12.BODY_SCOPE",
        ConstructionKind.POSITIVE,
        SpecStatus.NORMATIVE,
        ("A-BODY-001", "A-BODY-002"),
        "A named act body is delimited by singular זה דבר המעשה אשר שמו NAME ... עד הנה דבר המעשה אשר שמו NAME; the explicit names must co-refer and layout has no boundary force.",
    ),
    ConstructionDeclaration(
        "A12.RESULT_PRODUCTION",
        ConstructionKind.POSITIVE,
        SpecStatus.NORMATIVE,
        ("A-OUT-001", "A-OUT-002"),
        "הוצא מן המעשה הזה את VALUE produces the at-most-one Core numeric output of the current performance and does not itself terminate the act.",
    ),
    ConstructionDeclaration(
        "A12.IMMEDIATE_RESULT_REFERENCE",
        ConstructionKind.POSITIVE,
        SpecStatus.NORMATIVE,
        ("A-OUT-003",),
        "The single Core result may be referred to only by the explicit immediate form המספר אשר יצא עתה מן המעשה אשר שמו ACT; no ordinal or hidden last-result convention is admitted.",
    ),
    ConstructionDeclaration(
        "A12.NO_A11_PLURAL_BODY_ALIAS",
        ConstructionKind.NEGATIVE,
        SpecStatus.NORMATIVE,
        ("A-BODY-001",),
        "A11 אלה דברי המעשה / עד הנה דברי המעשה is superseded and is not a compatibility alias in A12.",
    ),
    ConstructionDeclaration(
        "A12.NO_MULTIPLE_POSITIONAL_RESULTS",
        ConstructionKind.NEGATIVE,
        SpecStatus.NORMATIVE,
        ("A-OUT-002", "A-OUT-003"),
        "A12 Core permits zero or one numeric output and rejects A11 ordinal/positional multi-result access.",
    ),
    ConstructionDeclaration(
        "A12.NO_PERFORMANCE_LOCAL_MUTABLE_PLACE",
        ConstructionKind.NEGATIVE,
        SpecStatus.NORMATIVE,
        ("A12-FREEZE-LOCAL-STATE" ,),
        "A11 performance-owned mutable local places are not part of frozen A-Core v0.1; future local-state design remains open.",
    ),
    ConstructionDeclaration(
        "A12.NO_STACK_DEICTIC",
        ConstructionKind.NEGATIVE,
        SpecStatus.NORMATIVE,
        ("A-ROLE-003",),
        "המעשה הזה is a source deictic for the current performance occurrence, not a stack-frame or caller-chain lookup convention.",
    ),
)

_PRODUCTIONS = _BASE_PRODUCTIONS + (
    Production(
        "A12.NUMBER.LITERAL",
        "A12.DIRECT_NUMERIC_LITERAL",
        "NumberValue",
        (W("המספר"), W("אשר"), W("הוא"), NumeralTerminal(A12_DIRECT_NUMERAL_LEXICON_ID)),
        "A12.DIRECT_NUMERIC_LITERAL",
    ),
    Production(
        "A12.RESULT.PRODUCE",
        "A12.RESULT_PRODUCTION",
        "BodyAtomicAction",
        (W("הוצא"), W("מן"), W("המעשה"), W("הזה"), W("את"), Nonterminal("NumberValue")),
        "A12.RESULT_PRODUCTION",
    ),
    Production(
        "A12.RESULT.IMMEDIATE.SINGLE",
        "A12.IMMEDIATE_RESULT_REFERENCE",
        "NumberValue",
        (
            W("המספר"), W("אשר"), W("יצא"), W("עתה"), W("מן"), W("המעשה"), W("אשר"), W("שמו"),
            NameTerminal("ResultActionName"),
        ),
        "A12.IMMEDIATE_RESULT_SINGLE",
    ),
    Production(
        "A12.BODY.UNIT.ATOMIC",
        "A12.BODY_SCOPE",
        "BodyUnit",
        (Nonterminal("AtomicAction"),),
        "A12.BODY_UNIT",
    ),
    Production(
        "A12.BODY.UNIT.RESULT",
        "A12.BODY_SCOPE",
        "BodyUnit",
        (Nonterminal("BodyAtomicAction"),),
        "A12.BODY_UNIT",
    ),
    Production(
        "A12.BODY.UNIT.CONDITIONAL",
        "A12.BODY_SCOPE",
        "BodyUnit",
        (Nonterminal("ConditionalConsequence"),),
        "A12.BODY_UNIT",
    ),
    Production(
        "A12.BODY.UNIT.RECURRENCE",
        "A12.BODY_SCOPE",
        "BodyUnit",
        (Nonterminal("AfterGatedRecurrence"),),
        "A12.BODY_UNIT",
    ),
    Production(
        "A12.BODY.UNIT.COUNTED",
        "A12.BODY_SCOPE",
        "BodyUnit",
        (Nonterminal("CountedConsequence"),),
        "A12.BODY_UNIT",
    ),
    Production(
        "A12.BODY.SEQUENCE.ONE",
        "A12.BODY_SCOPE",
        "BodySequence",
        (Nonterminal("BodyUnit"),),
        "A12.BODY_SEQUENCE",
    ),
    Production(
        "A12.BODY.SEQUENCE.MORE",
        "A12.BODY_SCOPE",
        "BodySequence",
        (Nonterminal("BodySequence"), W("ואחרי"), W("כן"), Nonterminal("BodyUnit")),
        "A12.BODY_SEQUENCE",
    ),
    Production(
        "A12.BODY.DEFINITION",
        "A12.BODY_SCOPE",
        "ActBodyDefinition",
        (
            W("זה"), W("דבר"), W("המעשה"), W("אשר"), W("שמו"), NameTerminal("BodyActionName"),
            Nonterminal("BodySequence"),
            W("עד"), W("הנה"), W("דבר"), W("המעשה"), W("אשר"), W("שמו"), NameTerminal("BodyActionName"),
        ),
        "A12.BODY_SCOPE",
        root=True,
    ),
)

_GATES = _BASE_GATES + (
    ConstructionSemanticGate(
        "A10.NAMED_ACT_PERFORMANCE",
        SemanticReadiness.READY,
        "B11 maps A12 described-act performance exactly to semantic performance occurrences without requiring call frames.",
        ("B-ACT-R01/R02/R07", "B11 exact A12 mapping"),
    ),
    ConstructionSemanticGate(
        "A11.INPUT_ROLE",
        SemanticReadiness.READY,
        "B11 maps A12 named numeric roles to non-positional semantic role identities and explicit associations.",
        ("B-ROLE-R01..R05", "B11 exact A12 mapping"),
    ),
    ConstructionSemanticGate(
        "A11.ROLE_ASSOCIATION",
        SemanticReadiness.READY,
        "B11 freezes explicit non-positional Value-to-role association for each performance occurrence.",
        ("B-ROLE-R01..R05", "B11 exact A12 mapping"),
    ),
    ConstructionSemanticGate(
        "A11.CURRENT_PERFORMANCE",
        SemanticReadiness.READY,
        "B11 maps המעשה הזה to the current semantic performance occurrence, not to an observable stack frame or caller chain.",
        ("B-ACT-R02/R03", "B11 exact A12 mapping"),
    ),
    ConstructionSemanticGate(
        "A12.BODY_SCOPE",
        SemanticReadiness.READY,
        "B11 maps the frozen A12 body delimiters to described-act body execution with ordinary completion at exhaustion.",
        ("B-ACT-R04/R05", "B11 exact A12 mapping"),
    ),
    ConstructionSemanticGate(
        "A12.RESULT_PRODUCTION",
        SemanticReadiness.READY,
        "B11 freezes zero-or-one numeric output production as part of the current performance and explicitly separates output from completion.",
        ("B-OUT-R01/R04", "B11 A12 Core profile |Products|<=1"),
    ),
    ConstructionSemanticGate(
        "A12.IMMEDIATE_RESULT_REFERENCE",
        SemanticReadiness.READY,
        "B11 maps the A12 immediate single-result description to the explicitly resolved just-completed performance; no hidden last-result register exists.",
        ("B-OUT-R06/R07/R08", "B11 exact A12 mapping"),
    ),
)

A12_REGISTRY = ConstructionRegistry(
    language_edition=A12_LANGUAGE_EDITION,
    registry_version="a12.2-c-b11-mapped",
    source_snapshot="A12_A_Core_v0.1_Frozen_Candidate+B11_CORE_CLOSURE",
    declarations=_DECLARATIONS,
    productions=_PRODUCTIONS,
    semantic_gates=_GATES,
)

__all__ = ["A12_LANGUAGE_EDITION", "A12_REGISTRY"]
