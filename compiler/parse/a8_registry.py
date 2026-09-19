from __future__ import annotations

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

SEQ = (WordTerminal("ואחרי"), WordTerminal("כן"))
ACTION_REF = (
    WordTerminal("את"),
    WordTerminal("המצוה"),
    WordTerminal("אשר"),
    WordTerminal("שמה"),
    NameTerminal("ActionName"),
)


def _count_prod(pid: str, word: str) -> Production:
    return Production(
        production_id=pid,
        construction_id="A3.COUNTED_ATOMIC_REPEAT",
        lhs="RepeatCount",
        rhs=(WordTerminal(word), WordTerminal("פעמים")),
        semantic_id="A3.REPEAT_COUNT",
    )


A8_REGISTRY = ConstructionRegistry(
    language_edition="core-0.1-draft-a8-b6-review",
    registry_version="a8.1-c-safe-subset",
    source_snapshot="A8_Anti_Imitation_Audit_Handoff",
    declarations=(
        ConstructionDeclaration(
            "A2.EXPLICIT_SEQUENCE",
            ConstructionKind.POSITIVE,
            SpecStatus.NORMATIVE,
            ("A-SEQ-003", "A-SEQ-004"),
            "Overt temporal sequencing uses ואחרי כן; source order alone is not sequencing.",
        ),
        ConstructionDeclaration(
            "A3.COUNTED_ATOMIC_REPEAT",
            ConstructionKind.POSITIVE,
            SpecStatus.NORMATIVE,
            ("A-REP-001", "A-REP-002", "A-REP-003"),
            "Exact counted repetition 3..9 consumes one admitted atomic action.",
        ),
        ConstructionDeclaration(
            "A8.REUSABLE_ACTION_PERFORMANCE",
            ConstructionKind.POSITIVE,
            SpecStatus.NORMATIVE,
            ("A-CALL-004", "A-AUDIT-001", "A-AUDIT-005"),
            "A8 retains עשה/לעשות את המצוה אשר שמה NAME as a Hebrew-derived reusable-action surface family; B6 reopens its call/input/result ontology.",
        ),
        ConstructionDeclaration(
            "A8.NO_BARE_NAME_REFERENCE",
            ConstructionKind.NEGATIVE,
            SpecStatus.NORMATIVE,
            ("A-NAME-008",),
            "A bare coined word does not become a program reference; namehood is licensed by an explicit name slot.",
        ),
        ConstructionDeclaration(
            "A8.NO_RESERVED_WORD_FILTER_BY_CONVENTION",
            ConstructionKind.CONSTRAINT,
            SpecStatus.NORMATIVE,
            ("A-NAME-009", "A-AUDIT-005"),
            "A8 reopens keyword-style reserved-name exclusion; C does not reject a name merely because its consonants equal a grammar word.",
        ),
        ConstructionDeclaration(
            "A8.NO_IMPLICIT_SOURCE_ORDER",
            ConstructionKind.NEGATIVE,
            SpecStatus.NORMATIVE,
            ("A-SEQ-001", "A-AUDIT-001"),
            "Two adjacent clauses do not acquire execution order from layout/source order alone.",
        ),
        ConstructionDeclaration(
            "A8.UNTIL_NOT_WHILE",
            ConstructionKind.NEGATIVE,
            SpecStatus.NORMATIVE,
            ("A-REP-006", "A-REP-007", "A-AUDIT-003"),
            "עד אשר is not silently assigned a conventional pre/post-test loop semantics.",
        ),
    ),
    productions=(
        Production(
            "A8.ACTION.CALL.IMPERATIVE",
            "A8.REUSABLE_ACTION_PERFORMANCE",
            "AtomicAction",
            (WordTerminal("עשה"), *ACTION_REF),
            "A8.ACTION_PERFORMANCE",
            root=True,
        ),
        Production(
            "A8.ACTION.CALL.INFINITIVE",
            "A8.REUSABLE_ACTION_PERFORMANCE",
            "InfinitiveAction",
            (WordTerminal("לעשות"), *ACTION_REF),
            "A8.ACTION_PERFORMANCE",
        ),
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
    semantic_gates=(
        ConstructionSemanticGate(
            "A8.REUSABLE_ACTION_PERFORMANCE",
            SemanticReadiness.BLOCKED_ON_SPEC,
            "B6 reopened reusable-computation, input association/evaluation, state visibility, and result/completion semantics. Surface recognition must not reinstate B4 call semantics.",
            ("B-AI-Q04", "B-AI-Q05", "B-AI-Q06", "B-AI-Q07", "B-AI-Q08"),
        ),
    ),
)

__all__ = ["A8_REGISTRY"]
