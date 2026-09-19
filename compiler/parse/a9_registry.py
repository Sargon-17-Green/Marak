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

# A9 is a consolidation milestone.  This registry intentionally contains only
# the retained stable subset that C can encode without resolving A9's reopened
# state/reusable-computation/result questions.
A9_LANGUAGE_EDITION = "core-0.1-draft-a9-b8-review"
SEQ = (WordTerminal("ואחרי"), WordTerminal("כן"))


def _count_prod(pid: str, word: str) -> Production:
    return Production(
        production_id=pid,
        construction_id="A9.COUNTED_RECURRENCE",
        lhs="RepeatCount",
        rhs=(WordTerminal(word), WordTerminal("פעמים")),
        semantic_id="A9.EXACT_REPEAT_COUNT",
    )


A9_REGISTRY = ConstructionRegistry(
    language_edition=A9_LANGUAGE_EDITION,
    registry_version="a9.1-c-stable-subset",
    source_snapshot="A9_Surface_Consolidation_Handoff",
    declarations=(
        ConstructionDeclaration(
            "A9.EXPLICIT_SEQUENCE",
            ConstructionKind.POSITIVE,
            SpecStatus.NORMATIVE,
            ("A-CORE-005",),
            "Where order matters, the retained overt temporal relation is ואחרי כן; source order and bare waw do not create sequence.",
        ),
        ConstructionDeclaration(
            "A9.NUMERIC_LITERAL_FRAME",
            ConstructionKind.POSITIVE,
            SpecStatus.NORMATIVE,
            ("A-CORE-006", "A-CORE-007"),
            "Numeric values may be denoted by המספר אשר הוא NUMERAL. C currently encodes only the proved אחד atom while the productive magnitude grammar beyond the former finite fixture ceiling remains open.",
        ),
        ConstructionDeclaration(
            "A9.PURE_ADDITION_FRAME",
            ConstructionKind.POSITIVE,
            SpecStatus.NORMATIVE,
            ("A-CORE-006",),
            "Pure addition uses the explicit Biblical-Hebrew valency frame המספר הנחשב בהוסיף את A על B.",
        ),
        ConstructionDeclaration(
            "A9.PURE_SUBTRACTION_FRAME",
            ConstructionKind.POSITIVE,
            SpecStatus.NORMATIVE,
            ("A-CORE-006",),
            "Pure subtraction uses the explicit Biblical-Hebrew valency frame המספר הנחשב בגרע את A מן B.",
        ),
        ConstructionDeclaration(
            "A9.NUMERIC_IDENTITY",
            ConstructionKind.POSITIVE,
            SpecStatus.NORMATIVE,
            ("A-CORE-006",),
            "VALUE_A הוא VALUE_B is the retained exact numeric identity proposition in the controlled numeric frame.",
        ),
        ConstructionDeclaration(
            "A9.PAIRED_CONDITIONAL",
            ConstructionKind.POSITIVE,
            SpecStatus.NORMATIVE,
            ("A-CORE-008",),
            "Conditional consequence uses the paired Hebrew shell אם P A ואם לא B; no dangling-else convention is available.",
        ),
        ConstructionDeclaration(
            "A9.COUNTED_RECURRENCE",
            ConstructionKind.POSITIVE,
            SpecStatus.NORMATIVE,
            ("A-CORE-009",),
            "Exact N פעמים recurrence is admitted only for counts whose morphology and repeated material are structurally closed.",
        ),
        ConstructionDeclaration(
            "A9.NO_HIDDEN_DEREFERENCE",
            ConstructionKind.NEGATIVE,
            SpecStatus.NORMATIVE,
            ("A-CORE-002", "A9-STABLE-NEGATIVE"),
            "A referent is not silently replaced by its current content merely because an implementation stores content in a cell.",
        ),
        ConstructionDeclaration(
            "A9.UNTIL_NOT_GENERIC_LOOP",
            ConstructionKind.NEGATIVE,
            SpecStatus.NORMATIVE,
            ("A-CORE-010",),
            "Bare עד אשר does not select a conventional pre-test or post-test recurrence model.",
        ),
        ConstructionDeclaration(
            "A9.NO_POSITIONAL_INPUT_CONVENTION",
            ConstructionKind.NEGATIVE,
            SpecStatus.NORMATIVE,
            ("A9-STABLE-NEGATIVE",),
            "Positional argument matching is unavailable unless linguistic role marking later licenses it.",
        ),
    ),
    productions=(
        # A9 reopens the former arbitrary finite fixture maximum.  C therefore does not
        # install a fake closed decimal-style literal grammar.  The atom אחד is
        # sufficient to exercise the stable frame and to derive zero exactly.
        Production(
            "A9.NUMBER.LITERAL.ONE",
            "A9.NUMERIC_LITERAL_FRAME",
            "NumberValue",
            (WordTerminal("המספר"), WordTerminal("אשר"), WordTerminal("הוא"), WordTerminal("אחד")),
            "A9.NUMERIC_LITERAL",
        ),
        Production(
            "A9.NUMBER.ADD",
            "A9.PURE_ADDITION_FRAME",
            "NumberValue",
            (
                WordTerminal("המספר"), WordTerminal("הנחשב"), WordTerminal("בהוסיף"), WordTerminal("את"),
                Nonterminal("NumberValue"), WordTerminal("על"), Nonterminal("NumberValue"),
            ),
            "A9.PURE_ADDITION",
        ),
        Production(
            "A9.NUMBER.SUBTRACT",
            "A9.PURE_SUBTRACTION_FRAME",
            "NumberValue",
            (
                WordTerminal("המספר"), WordTerminal("הנחשב"), WordTerminal("בגרע"), WordTerminal("את"),
                Nonterminal("NumberValue"), WordTerminal("מן"), Nonterminal("NumberValue"),
            ),
            "A9.PURE_SUBTRACTION",
        ),
        Production(
            "A9.PROPOSITION.NUMERIC_IDENTITY",
            "A9.NUMERIC_IDENTITY",
            "Proposition",
            (Nonterminal("NumberValue"), WordTerminal("הוא"), Nonterminal("NumberValue")),
            "A9.NUMERIC_IDENTITY",
        ),
        # The shell is normative, but no current A9 production supplies
        # AdmittedConsequence.  Keeping the missing leaf explicit prevents C
        # from reviving A8's now-reopened מצוה call ontology.
        Production(
            "A9.CONDITIONAL.PAIRED",
            "A9.PAIRED_CONDITIONAL",
            "ConditionalConsequence",
            (
                WordTerminal("אם"), Nonterminal("Proposition"), Nonterminal("AdmittedConsequence"),
                WordTerminal("ואם"), WordTerminal("לא"), Nonterminal("AdmittedConsequence"),
            ),
            "A9.PAIRED_CONDITIONAL",
            root=True,
        ),
        Production(
            "A9.SEQUENCE.TWO",
            "A9.EXPLICIT_SEQUENCE",
            "OrderedSequence",
            (Nonterminal("AdmittedConsequence"), *SEQ, Nonterminal("AdmittedConsequence")),
            "A9.EXPLICIT_SEQUENCE",
            root=True,
        ),
        Production(
            "A9.SEQUENCE.MORE",
            "A9.EXPLICIT_SEQUENCE",
            "OrderedSequence",
            (Nonterminal("OrderedSequence"), *SEQ, Nonterminal("AdmittedConsequence")),
            "A9.EXPLICIT_SEQUENCE",
            root=True,
        ),
        _count_prod("A9.REPEAT.COUNT.3", "שלש"),
        _count_prod("A9.REPEAT.COUNT.4", "ארבע"),
        _count_prod("A9.REPEAT.COUNT.5", "חמש"),
        _count_prod("A9.REPEAT.COUNT.6", "שש"),
        _count_prod("A9.REPEAT.COUNT.7", "שבע"),
        _count_prod("A9.REPEAT.COUNT.8", "שמנה"),
        _count_prod("A9.REPEAT.COUNT.9", "תשע"),
        Production(
            "A9.REPEAT.ADMITTED_CONSEQUENCE",
            "A9.COUNTED_RECURRENCE",
            "CountedConsequence",
            (Nonterminal("RepeatCount"), Nonterminal("AdmittedConsequence")),
            "A9.COUNTED_RECURRENCE",
            root=True,
        ),
    ),
)

__all__ = ["A9_LANGUAGE_EDITION", "A9_REGISTRY"]
