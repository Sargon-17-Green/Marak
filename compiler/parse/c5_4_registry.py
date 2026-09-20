from __future__ import annotations

"""C5.4 production registry: general exact counted recurrence only."""

from compiler.parse.c5_3_registry import C5_3_REGISTRY
from compiler.parse.a15_numerals import A15_FEMININE_COUNT_LEXICON_ID
from compiler.parse.grammar import (
    ConstructionDeclaration, ConstructionKind, ConstructionRegistry,
    Nonterminal, NumeralTerminal, Production, SpecStatus, WordTerminal,
)

LANGUAGE_EDITION = C5_3_REGISTRY.language_edition
REGISTRY_VERSION = "c5.4-a15-b13.1"

def W(text: str) -> WordTerminal:
    return WordTerminal(text)

# A13's 3..9 spelling overlaps the A15 productive profile exactly.  Replace
# only the current production; the frozen historical registry stays immutable.
_BASE = tuple(
    p for p in C5_3_REGISTRY.productions
    if p.production_id != "A10.REPEAT.COUNTED"
)

_DECLS = C5_3_REGISTRY.declarations + (
    ConstructionDeclaration(
        "C54.EXACT_COUNTED_RECURRENCE",
        ConstructionKind.POSITIVE,
        SpecStatus.NORMATIVE,
        ("A15_COUNTED_RECURRENCE", "B-REP-R06"),
        "RepeatExactly determines one Natural count once at entry and repeats exactly one atomic action; no iterator or implicit result collection exists.",
    ),
    ConstructionDeclaration(
        "C54.COUNT_AS_NUMBER",
        ConstructionKind.POSITIVE,
        SpecStatus.NORMATIVE,
        ("A15_COUNTED_RECURRENCE",),
        "Dynamic counts are existing Natural Value descriptions with only their initial numeric head inflected to כמספר.",
    ),
)

_count_as = []
COUNT_AS_NUMBER_ORIGINS: dict[str, str] = {}
for p in C5_3_REGISTRY.productions:
    if p.lhs != "NumberValue" or not p.rhs or not isinstance(p.rhs[0], WordTerminal):
        continue
    head = p.rhs[0].text
    if head not in {"המספר", "מספר"}:
        continue
    if head == "מספר" and p.production_id != "C53.COUNT":
        continue
    derived_id = "C54.COUNT_AS." + p.production_id.replace(".", "_")
    _count_as.append(Production(
        derived_id,
        "C54.COUNT_AS_NUMBER",
        "CountAsNumber",
        (W("כמספר"), *p.rhs[1:]),
        "C54.COUNT_AS_NUMBER",
    ))
    COUNT_AS_NUMBER_ORIGINS[derived_id] = p.production_id

_PRODS = _BASE + tuple(_count_as) + (
    Production(
        "C54.REPEAT.ONE", "C54.EXACT_COUNTED_RECURRENCE", "CountedConsequence",
        (W("פעם"), W("אחת"), Nonterminal("AtomicAction")),
        "C54.REPEAT_EXACTLY",
    ),
    Production(
        "C54.REPEAT.TWO", "C54.EXACT_COUNTED_RECURRENCE", "CountedConsequence",
        (W("שתי"), W("פעמים"), Nonterminal("AtomicAction")),
        "C54.REPEAT_EXACTLY",
    ),
    Production(
        "C54.REPEAT.MANY", "C54.EXACT_COUNTED_RECURRENCE", "CountedConsequence",
        (NumeralTerminal(A15_FEMININE_COUNT_LEXICON_ID), W("פעמים"), Nonterminal("AtomicAction")),
        "C54.REPEAT_EXACTLY",
    ),
    Production(
        "C54.REPEAT.DYNAMIC", "C54.EXACT_COUNTED_RECURRENCE", "CountedConsequence",
        (W("פעמים"), Nonterminal("CountAsNumber"), Nonterminal("AtomicAction")),
        "C54.REPEAT_EXACTLY",
    ),
)

C5_4_REGISTRY = ConstructionRegistry(
    language_edition=LANGUAGE_EDITION,
    registry_version=REGISTRY_VERSION,
    source_snapshot="C5.3+A15 counted recurrence+B13 RepeatExactly production integration",
    declarations=_DECLS,
    productions=_PRODS,
    semantic_gates=C5_3_REGISTRY.semantic_gates,
)

__all__ = [
    "C5_4_REGISTRY", "COUNT_AS_NUMBER_ORIGINS", "REGISTRY_VERSION", "LANGUAGE_EDITION",
]
