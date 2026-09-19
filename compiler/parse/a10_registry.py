from __future__ import annotations

from compiler.parse.a9_registry import A9_REGISTRY
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

A10_LANGUAGE_EDITION = "core-0.1-draft-a10-b9-review"

# Keep the stable A9 number/proposition/count pieces but replace its root shells
# so they compose with A10's newly admitted atomic-action surface.
_REPLACED_A9_ROOTS = {
    "A9.CONDITIONAL.PAIRED",
    "A9.SEQUENCE.TWO",
    "A9.SEQUENCE.MORE",
    "A9.REPEAT.ADMITTED_CONSEQUENCE",
}
_BASE_PRODUCTIONS = tuple(p for p in A9_REGISTRY.productions if p.production_id not in _REPLACED_A9_ROOTS)

ACTION_REF = (
    WordTerminal("את"), WordTerminal("המעשה"), WordTerminal("אשר"), WordTerminal("שמו"),
    NameTerminal("ActionName"),
)
PLACE_REF = (
    WordTerminal("מקום"), WordTerminal("אשר"), WordTerminal("שמו"), NameTerminal("PlaceName"),
)


A10_REGISTRY = ConstructionRegistry(
    language_edition=A10_LANGUAGE_EDITION,
    registry_version="a10.1-c-stable-subset",
    source_snapshot="A10_Surface_Language_Handoff+B9_UNBOUNDED_RECURRENCE",
    declarations=A9_REGISTRY.declarations + (
        ConstructionDeclaration(
            "A10.NAMED_ACT_IDENTITY",
            ConstructionKind.POSITIVE,
            SpecStatus.NORMATIVE,
            ("A-ACT-021", "A-ACT-023", "A-ACT-024"),
            "Reusable described computation is named as מעשה; introduction uses יהי מעשה ושמו NAME and reference uses המעשה אשר שמו NAME.",
        ),
        ConstructionDeclaration(
            "A10.NAMED_ACT_PERFORMANCE",
            ConstructionKind.POSITIVE,
            SpecStatus.NORMATIVE,
            ("A-ACT-026",),
            "Explicit performance is עשה את המעשה אשר שמו NAME; a bare name is never invocation.",
        ),
        ConstructionDeclaration(
            "A10.RESULT_PROVENANCE_NUMBER",
            ConstructionKind.POSITIVE,
            SpecStatus.NORMATIVE,
            ("A-RESULT-006", "A-RESULT-007", "A-RESULT-008"),
            "A numeric result is identified by provenance המספר אשר יצא מן המעשה אשר שמו NAME; production and cessation are separate.",
        ),
        ConstructionDeclaration(
            "A10.NAMED_PLACE_STATE",
            ConstructionKind.POSITIVE,
            SpecStatus.NORMATIVE,
            ("A-STATE-001", "A-STATE-002", "A-STATE-006"),
            "מקום is a source-semantic changeable-state holder, distinct from its current numeric occupant and from implementation memory.",
        ),
        ConstructionDeclaration(
            "A10.PLACE_INTRODUCTION",
            ConstructionKind.POSITIVE,
            SpecStatus.NORMATIVE,
            ("A-STATE-003",),
            "Initialized place introduction explicitly names the place and states its sole current numeric occupant.",
        ),
        ConstructionDeclaration(
            "A10.PLACE_REPLACEMENT",
            ConstructionKind.POSITIVE,
            SpecStatus.NORMATIVE,
            ("A-STATE-004", "A-STATE-005"),
            "Replacement explicitly names destination, new occupant, and displaced current numeric occupant.",
        ),
        ConstructionDeclaration(
            "A10.AFTER_GATED_RECURRENCE",
            ConstructionKind.POSITIVE,
            SpecStatus.NORMATIVE,
            ("A-REP-009", "A-REP-010", "A-REP-011", "A-REP-012", "A-REP-013"),
            "ATOMIC_ACTION וכן תעשה עד אשר P performs the action once, then checks P after each occurrence and repeats the same atomic act until P holds.",
        ),
        ConstructionDeclaration(
            "A10.NO_MITZVAH_CORE_CALL",
            ConstructionKind.NEGATIVE,
            SpecStatus.NORMATIVE,
            ("A-ACT-022",),
            "מצוה is superseded as the primary Core reusable-computation abstraction; C must not preserve A8 syntax for compatibility.",
        ),
        ConstructionDeclaration(
            "A10.NO_BARE_UNTIL_RECURRENCE",
            ConstructionKind.NEGATIVE,
            SpecStatus.NORMATIVE,
            ("A-REP-009", "A-REP-013"),
            "ACTION עד אשר P and ACTION וכן עשה עד אשר P are not the canonical Core recurrence; the admitted form contains וכן תעשה.",
        ),
    ),
    productions=_BASE_PRODUCTIONS + (
        # Additional proven atoms used by A10's own normative state fixtures.
        Production(
            "A10.NUMBER.LITERAL.THREE", "A9.NUMERIC_LITERAL_FRAME", "NumberValue",
            (WordTerminal("המספר"), WordTerminal("אשר"), WordTerminal("הוא"), WordTerminal("שלשה")),
            "A9.NUMERIC_LITERAL",
        ),
        Production(
            "A10.NUMBER.LITERAL.FOUR", "A9.NUMERIC_LITERAL_FRAME", "NumberValue",
            (WordTerminal("המספר"), WordTerminal("אשר"), WordTerminal("הוא"), WordTerminal("ארבעה")),
            "A9.NUMERIC_LITERAL",
        ),
        Production(
            "A10.ACT.IDENTITY", "A10.NAMED_ACT_IDENTITY", "NamedActIdentity",
            (WordTerminal("יהי"), WordTerminal("מעשה"), WordTerminal("ושמו"), NameTerminal("ActionName")),
            "A10.NAMED_ACT_IDENTITY",
        ),
        Production(
            "A10.ACT.PERFORM", "A10.NAMED_ACT_PERFORMANCE", "AtomicAction",
            (WordTerminal("עשה"), *ACTION_REF),
            "A10.NAMED_ACT_PERFORMANCE", root=True,
        ),
        Production(
            "A10.RESULT.NUMBER", "A10.RESULT_PROVENANCE_NUMBER", "NumberValue",
            (
                WordTerminal("המספר"), WordTerminal("אשר"), WordTerminal("יצא"), WordTerminal("מן"),
                WordTerminal("המעשה"), WordTerminal("אשר"), WordTerminal("שמו"), NameTerminal("ActionName"),
            ),
            "A10.RESULT_PROVENANCE_NUMBER",
        ),
        Production(
            "A10.PLACE.CURRENT_NUMBER", "A10.NAMED_PLACE_STATE", "NumberValue",
            (
                WordTerminal("המספר"), WordTerminal("אשר"), WordTerminal("במקום"), WordTerminal("אשר"),
                WordTerminal("שמו"), NameTerminal("PlaceName"),
            ),
            "A10.CURRENT_PLACE_NUMBER",
        ),
        Production(
            "A10.PLACE.INTRODUCE", "A10.PLACE_INTRODUCTION", "AtomicAction",
            (
                WordTerminal("יהי"), WordTerminal("מקום"), WordTerminal("ושמו"), NameTerminal("PlaceName"),
                WordTerminal("ובמקום"), WordTerminal("אשר"), WordTerminal("שמו"), NameTerminal("PlaceName"),
                WordTerminal("יהי"), Nonterminal("NumberValue"), WordTerminal("לבדו"),
            ),
            "A10.PLACE_INTRODUCTION", root=True,
        ),
        Production(
            "A10.PLACE.REPLACE", "A10.PLACE_REPLACEMENT", "AtomicAction",
            (
                WordTerminal("שים"), WordTerminal("במקום"), WordTerminal("אשר"), WordTerminal("שמו"), NameTerminal("PlaceName"),
                WordTerminal("את"), Nonterminal("NumberValue"),
                WordTerminal("תחת"), WordTerminal("המספר"), WordTerminal("אשר"), WordTerminal("במקום"), WordTerminal("אשר"),
                WordTerminal("שמו"), NameTerminal("PlaceName"),
            ),
            "A10.PLACE_REPLACEMENT", root=True,
        ),
        Production(
            "A10.SEQUENCE.TWO", "A9.EXPLICIT_SEQUENCE", "OrderedSequence",
            (Nonterminal("AtomicAction"), WordTerminal("ואחרי"), WordTerminal("כן"), Nonterminal("AtomicAction")),
            "A9.EXPLICIT_SEQUENCE", root=True,
        ),
        Production(
            "A10.SEQUENCE.MORE", "A9.EXPLICIT_SEQUENCE", "OrderedSequence",
            (Nonterminal("OrderedSequence"), WordTerminal("ואחרי"), WordTerminal("כן"), Nonterminal("AtomicAction")),
            "A9.EXPLICIT_SEQUENCE", root=True,
        ),
        Production(
            "A10.REPEAT.COUNTED", "A9.COUNTED_RECURRENCE", "CountedConsequence",
            (Nonterminal("RepeatCount"), Nonterminal("AtomicAction")),
            "A9.COUNTED_RECURRENCE", root=True,
        ),
        Production(
            "A10.CONDITIONAL.PAIRED", "A9.PAIRED_CONDITIONAL", "ConditionalConsequence",
            (
                WordTerminal("אם"), Nonterminal("Proposition"), Nonterminal("AtomicAction"),
                WordTerminal("ואם"), WordTerminal("לא"), Nonterminal("AtomicAction"),
            ),
            "A9.PAIRED_CONDITIONAL", root=True,
        ),
        Production(
            "A10.RECURRENCE.AFTER_UNTIL", "A10.AFTER_GATED_RECURRENCE", "AfterGatedRecurrence",
            (
                Nonterminal("AtomicAction"), WordTerminal("וכן"), WordTerminal("תעשה"),
                WordTerminal("עד"), WordTerminal("אשר"), Nonterminal("Proposition"),
            ),
            "A10.AFTER_GATED_RECURRENCE", root=True,
        ),
    ),
    semantic_gates=(
        ConstructionSemanticGate(
            "A10.NAMED_ACT_PERFORMANCE", SemanticReadiness.BLOCKED_ON_SPEC,
            "A10 closes the performance wording but A11 still owes act-body closure and varying input/result semantics; historical B4 Call/Return cannot fill that gap.",
            ("A11 act body/input/result", "post-audit reusable-computation semantics"),
        ),
        ConstructionSemanticGate(
            "A10.RESULT_PROVENANCE_NUMBER", SemanticReadiness.BLOCKED_ON_SPEC,
            "A provenance phrase requires a resolved act specification that proves exactly one matching numeric result; A11 has not yet closed that model.",
            ("A11 result multiplicity/act specification",),
        ),
        ConstructionSemanticGate(
            "A10.NAMED_PLACE_STATE", SemanticReadiness.BLOCKED_ON_SPEC,
            "A10+B7 close place/current-fact meaning, but source visibility/lifetime and resolver ownership remain open for canonical lowering.",
            ("A11 local state ownership/reference visibility",),
        ),
        ConstructionSemanticGate(
            "A10.PLACE_INTRODUCTION", SemanticReadiness.BLOCKED_ON_SPEC,
            "State establishment meaning is known, but canonical source identity/lifetime resolution is not yet closed.",
            ("A11 local state ownership/reference visibility",),
        ),
        ConstructionSemanticGate(
            "A10.PLACE_REPLACEMENT", SemanticReadiness.BLOCKED_ON_SPEC,
            "B7 replacement semantics is known, but canonical source identity/lifetime resolution is not yet closed.",
            ("A11 local state ownership/reference visibility",),
        ),
    ),
)

__all__ = ["A10_LANGUAGE_EDITION", "A10_REGISTRY"]
