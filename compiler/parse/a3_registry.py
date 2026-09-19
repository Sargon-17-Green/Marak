from __future__ import annotations

from compiler.parse.grammar import (
    ConstructionDeclaration,
    ConstructionKind,
    ConstructionRegistry,
    Nonterminal,
    Production,
    SpecStatus,
    WordTerminal,
)
A3_LANGUAGE_EDITION = "core-0.1-draft-a3-b4-review"


SEQ = (WordTerminal("ואחרי"), WordTerminal("כן"))


def _count_prod(pid: str, word: str) -> Production:
    return Production(
        production_id=pid,
        construction_id="A3.COUNTED_ATOMIC_REPEAT",
        lhs="RepeatCount",
        rhs=(WordTerminal(word), WordTerminal("פעמים")),
        semantic_id="A3.REPEAT_COUNT",
    )


A3_REGISTRY = ConstructionRegistry(
    language_edition=A3_LANGUAGE_EDITION,
    registry_version="a3.1",
    source_snapshot="A3_Surface_Language_Handoff",
    declarations=(
        ConstructionDeclaration(
            "A2.EXPLICIT_SEQUENCE",
            ConstructionKind.POSITIVE,
            SpecStatus.NORMATIVE,
            ("A-SEQ-003", "A-SEQ-004"),
            "Flat temporal sequencing uses the overt Biblical-Hebrew marker ואחרי כן.",
        ),
        ConstructionDeclaration(
            "A3.COUNTED_ATOMIC_REPEAT",
            ConstructionKind.POSITIVE,
            SpecStatus.NORMATIVE,
            ("A-REP-001", "A-REP-002", "A-REP-003"),
            "Exact counted repetition 3..9 consumes exactly one admitted atomic action.",
        ),
        ConstructionDeclaration(
            "A2.BINARY_CONDITIONAL_SHELL",
            ConstructionKind.POSITIVE,
            SpecStatus.PROPOSED,
            ("A-COND-001",),
            "Binary conditional shell remains proposed because the predicate layer is not yet fixed.",
        ),
        ConstructionDeclaration(
            "A3.NO_GENERIC_END",
            ConstructionKind.NEGATIVE,
            SpecStatus.NORMATIVE,
            ("A-SCOPE-001", "A-SCOPE-002", "A-SCOPE-003"),
            "No compiler-only generic END or nearest-open-block closer is admitted.",
        ),
        ConstructionDeclaration(
            "A3.UNTIL_NOT_WHILE",
            ConstructionKind.NEGATIVE,
            SpecStatus.NORMATIVE,
            ("A-REP-006", "A-REP-007"),
            "עד אשר is not silently assigned while/do-while/repeat-until test-point semantics.",
        ),
    ),
    productions=(
        Production(
            "A2.SEQUENCE.TWO",
            "A2.EXPLICIT_SEQUENCE",
            "Sequence",
            (Nonterminal("AtomicAction"), *SEQ, Nonterminal("AtomicAction")),
            "A2.EXPLICIT_SEQUENCE",
            root=True,
        ),
        Production(
            "A2.SEQUENCE.MORE",
            "A2.EXPLICIT_SEQUENCE",
            "Sequence",
            (Nonterminal("Sequence"), *SEQ, Nonterminal("AtomicAction")),
            "A2.EXPLICIT_SEQUENCE",
            root=True,
        ),
        _count_prod("A3.REPEAT.COUNT.3", "שלש"),
        _count_prod("A3.REPEAT.COUNT.4", "ארבע"),
        _count_prod("A3.REPEAT.COUNT.5", "חמש"),
        _count_prod("A3.REPEAT.COUNT.6", "שש"),
        _count_prod("A3.REPEAT.COUNT.7", "שבע"),
        _count_prod("A3.REPEAT.COUNT.8", "שמנה"),
        _count_prod("A3.REPEAT.COUNT.9", "תשע"),
        Production(
            "A3.REPEAT.ATOMIC",
            "A3.COUNTED_ATOMIC_REPEAT",
            "CountedAtomicAction",
            (Nonterminal("RepeatCount"), Nonterminal("AtomicAction")),
            "A3.COUNTED_ATOMIC_REPEAT",
            root=True,
        ),
    ),
)


__all__ = ["A3_REGISTRY"]
