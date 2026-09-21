from __future__ import annotations

"""C5.6 production registry: A17/B16 general BidirectionalIndex surface."""

from compiler.parse.a15_numerals import A15_FEMININE_COUNT_LEXICON_ID
from compiler.parse.c5_5_registry import (
    C5_5_REGISTRY,
    COUNT_AS_NUMBER_ORIGINS as C5_5_COUNT_AS_NUMBER_ORIGINS,
)
from compiler.parse.grammar import (
    ConstructionDeclaration,
    ConstructionKind,
    ConstructionRegistry,
    NameTerminal,
    Nonterminal,
    NumeralTerminal,
    Production,
    SpecStatus,
    WordTerminal,
)

LANGUAGE_EDITION = C5_5_REGISTRY.language_edition
REGISTRY_VERSION = "c5.6-a17-b16.1"


def W(text: str) -> WordTerminal:
    return WordTerminal(text)


def N(role: str) -> NameTerminal:
    return NameTerminal(role)


def NT(name: str) -> Nonterminal:
    return Nonterminal(name)


_DECLS = C5_5_REGISTRY.declarations + (
    ConstructionDeclaration(
        "C56.GENERAL_INDEX_VALUE",
        ConstructionKind.POSITIVE,
        SpecStatus.NORMATIVE,
        ("A17_BIDIRECTIONAL_INDEX_SURFACE", "B16_PROFILE_IDENTITY_SEMANTICS"),
        "General/non-year source profile for the existing BidirectionalIndex domain; no profile subtype or runtime tag.",
    ),
    ConstructionDeclaration(
        "C56.GENERAL_INDEX_CARRIER",
        ConstructionKind.POSITIVE,
        SpecStatus.NORMATIVE,
        ("A17_BIDIRECTIONAL_INDEX_SURFACE", "B16_PROFILE_FLOW_MATRIX"),
        "General-profile Program Input/place/role/result carrier heads over the existing BidirectionalIndex domain.",
    ),
    ConstructionDeclaration(
        "C56.INDEX_STRICT_ORDER",
        ConstructionKind.POSITIVE,
        SpecStatus.NORMATIVE,
        ("A17_BIDIRECTIONAL_INDEX_SURFACE", "B16_INDEX_ORDER_SEMANTICS"),
        "Strict BidirectionalIndex order proposition A before B; proposition satisfaction only.",
    ),
)

P: list[Production] = []

# General-profile literals. Productive COUNT reuses the frozen A15 feminine-count lexicon.
P += [
    Production(
        "C56.INDEX.GENERAL.ZERO", "C56.GENERAL_INDEX_VALUE", "IndexValue",
        (W("מעלת"), W("היתד")), "C56.INDEX_GENERAL_ZERO",
    ),
    Production(
        "C56.INDEX.GENERAL.BEFORE.ONE", "C56.GENERAL_INDEX_VALUE", "IndexValue",
        (W("מעלה"), W("אחת"), W("לפני"), W("מעלת"), W("היתד")),
        "C56.INDEX_GENERAL_BEFORE_ONE",
    ),
    Production(
        "C56.INDEX.GENERAL.AFTER.ONE", "C56.GENERAL_INDEX_VALUE", "IndexValue",
        (W("מעלה"), W("אחת"), W("אחרי"), W("מעלת"), W("היתד")),
        "C56.INDEX_GENERAL_AFTER_ONE",
    ),
    Production(
        "C56.INDEX.GENERAL.BEFORE.TWO", "C56.GENERAL_INDEX_VALUE", "IndexValue",
        (W("שתי"), W("מעלות"), W("לפני"), W("מעלת"), W("היתד")),
        "C56.INDEX_GENERAL_BEFORE_TWO",
    ),
    Production(
        "C56.INDEX.GENERAL.AFTER.TWO", "C56.GENERAL_INDEX_VALUE", "IndexValue",
        (W("שתי"), W("מעלות"), W("אחרי"), W("מעלת"), W("היתד")),
        "C56.INDEX_GENERAL_AFTER_TWO",
    ),
    Production(
        "C56.INDEX.GENERAL.BEFORE.MANY", "C56.GENERAL_INDEX_VALUE", "IndexValue",
        (
            NumeralTerminal(A15_FEMININE_COUNT_LEXICON_ID),
            W("מעלות"), W("לפני"), W("מעלת"), W("היתד"),
        ),
        "C56.INDEX_GENERAL_BEFORE_MANY",
    ),
    Production(
        "C56.INDEX.GENERAL.AFTER.MANY", "C56.GENERAL_INDEX_VALUE", "IndexValue",
        (
            NumeralTerminal(A15_FEMININE_COUNT_LEXICON_ID),
            W("מעלות"), W("אחרי"), W("מעלת"), W("היתד"),
        ),
        "C56.INDEX_GENERAL_AFTER_MANY",
    ),
]

# General-profile typed carrier heads. All lower to existing semantic carrier nodes.
P += [
    Production(
        "C56.INPUT.DECLARE.INDEX", "C56.GENERAL_INDEX_CARRIER", "PreparatoryUnit",
        (
            W("יהי"), W("למלאכה"), W("הזאת"), W("דבר"), W("ושמו"), N("ProgramInputRoleName"),
            W("ובטרם"), W("תחל"), W("המלאכה"), W("הזאת"), W("תעמד"), W("מעלה"),
            W("תחת"), W("הדבר"), W("אשר"), W("למלאכה"), W("הזאת"), W("שמו"),
            N("ProgramInputRoleName"),
        ),
        "C56.PROGRAM_INPUT_DECLARE_INDEX",
    ),
    Production(
        "C56.INPUT.READ.INDEX", "C56.GENERAL_INDEX_CARRIER", "IndexValue",
        (
            W("המעלה"), W("אשר"), W("עומדת"), W("תחת"), W("הדבר"), W("אשר"),
            W("למלאכה"), W("הזאת"), W("שמו"), N("ProgramInputRoleName"),
        ),
        "C56.PROGRAM_INPUT_READ_INDEX",
    ),
    Production(
        "C56.INDEX.GENERAL.CURRENT.PLACE", "C56.GENERAL_INDEX_CARRIER", "IndexValue",
        (W("המעלה"), W("אשר"), W("במקום"), W("אשר"), W("שמו"), N("PlaceName")),
        "C56.INDEX_GENERAL_CURRENT_PLACE",
    ),
    Production(
        "C56.PLACE.REPLACE.INDEX", "C56.GENERAL_INDEX_CARRIER", "AtomicAction",
        (
            W("שים"), W("במקום"), W("אשר"), W("שמו"), N("PlaceName"), W("את"),
            NT("IndexValue"), W("תחת"), W("המעלה"), W("אשר"), W("במקום"), W("אשר"),
            W("שמו"), N("PlaceName"),
        ),
        "C56.REPLACE_INDEX",
    ),
    Production(
        "C56.ROLE.DECLARE.INDEX", "C56.GENERAL_INDEX_CARRIER", "PreparatoryUnit",
        (
            W("יהי"), W("במעשה"), W("אשר"), W("שמו"), N("RoleOwnerActionName"),
            W("דבר"), W("ושמו"), N("DeclaredRoleName"),
            W("ובעשות"), W("את"), W("המעשה"), W("אשר"), W("שמו"),
            N("RoleOwnerActionName"), W("תעמד"), W("מעלה"), W("תחת"), W("הדבר"),
            W("אשר"), W("במעשה"), W("אשר"), W("שמו"), N("RoleOwnerActionName"),
            W("שמו"), N("DeclaredRoleName"),
        ),
        "C56.ROLE_INDEX",
    ),
    Production(
        "C56.INDEX.GENERAL.CURRENT.ROLE", "C56.GENERAL_INDEX_CARRIER", "IndexValue",
        (
            W("המעלה"), W("אשר"), W("במעשה"), W("הזה"), W("עומדת"), W("תחת"),
            W("הדבר"), W("אשר"), W("במעשה"), W("אשר"), W("שמו"),
            N("RoleOwnerActionName"), W("שמו"), N("AssociatedRoleName"),
        ),
        "C56.INDEX_GENERAL_CURRENT_ROLE",
    ),
    Production(
        "C56.INDEX.GENERAL.IMMEDIATE", "C56.GENERAL_INDEX_CARRIER", "IndexValue",
        (
            W("המעלה"), W("אשר"), W("יצאה"), W("עתה"), W("מן"), W("המעשה"),
            W("אשר"), W("שמו"), N("ResultActionName"),
        ),
        "C56.INDEX_GENERAL_IMMEDIATE",
    ),
]

# General-profile one-step traversal reuses the existing Index semantic path.
P += [
    Production(
        "C56.INDEX.GENERAL.SUCC", "C56.GENERAL_INDEX_VALUE", "IndexValue",
        (W("המעלה"), W("אשר"), W("אחר"), NT("IndexValue")),
        "C56.INDEX_GENERAL_SUCCESSOR",
    ),
    Production(
        "C56.INDEX.GENERAL.PRED", "C56.GENERAL_INDEX_VALUE", "IndexValue",
        (W("המעלה"), W("אשר"), W("לפני"), NT("IndexValue")),
        "C56.INDEX_GENERAL_PREDECESSOR",
    ),
]

# The only genuinely new semantic operation: strict Index order proposition.
P += [
    Production(
        "C56.PROP.INDEX.LT", "C56.INDEX_STRICT_ORDER", "Proposition",
        (NT("IndexValue"), W("לפני"), NT("IndexValue")),
        "C56.INDEX_LT",
    ),
]

COUNT_AS_NUMBER_ORIGINS = dict(C5_5_COUNT_AS_NUMBER_ORIGINS)

C5_6_REGISTRY = ConstructionRegistry(
    language_edition=LANGUAGE_EDITION,
    registry_version=REGISTRY_VERSION,
    source_snapshot="C5.5+A17 general BidirectionalIndex surface+B16 semantic integration",
    declarations=_DECLS,
    productions=C5_5_REGISTRY.productions + tuple(P),
    semantic_gates=C5_5_REGISTRY.semantic_gates,
)

__all__ = [
    "C5_6_REGISTRY",
    "COUNT_AS_NUMBER_ORIGINS",
    "REGISTRY_VERSION",
    "LANGUAGE_EDITION",
]
