from __future__ import annotations

"""C5.5 production registry: Program Input declaration and typed reads only."""

from compiler.parse.c5_4_registry import C5_4_REGISTRY, COUNT_AS_NUMBER_ORIGINS
from compiler.parse.grammar import (
    ConstructionDeclaration, ConstructionKind, ConstructionRegistry,
    NameTerminal, Nonterminal, Production, SpecStatus, WordTerminal,
)

LANGUAGE_EDITION = C5_4_REGISTRY.language_edition
REGISTRY_VERSION = "c5.5-a15-b13.1"

def W(text: str) -> WordTerminal:
    return WordTerminal(text)

def N(role: str) -> NameTerminal:
    return NameTerminal(role)

_COMMON_DECL_PREFIX = (
    W("יהי"), W("למלאכה"), W("הזאת"), W("דבר"), W("ושמו"), N("ProgramInputRoleName"),
    W("ובטרם"), W("תחל"), W("המלאכה"), W("הזאת"), W("יעמד"),
)
_COMMON_DECL_SUFFIX = (
    W("תחת"), W("הדבר"), W("אשר"), W("למלאכה"), W("הזאת"), W("שמו"),
    N("ProgramInputRoleName"),
)

_DECLS = C5_4_REGISTRY.declarations + (
    ConstructionDeclaration(
        "C55.PROGRAM_INPUT_DECLARATION", ConstructionKind.POSITIVE, SpecStatus.NORMATIVE,
        ("A15_PROGRAM_INPUT_ROLES", "B13_EXTERNAL_BINDING_MODEL", "B15_DOMAIN_FLOW_SEMANTICS"),
        "A required Program Input Role is top-level preparatory contract metadata, not an executable action or mutable place.",
    ),
    ConstructionDeclaration(
        "C55.PROGRAM_INPUT_REFERENCE", ConstructionKind.POSITIVE, SpecStatus.NORMATIVE,
        ("A15_PROGRAM_INPUT_ROLES", "B13_EXTERNAL_BINDING_MODEL", "B15_DOMAIN_FLOW_SEMANTICS"),
        "Program Input reads resolve by semantic identity and independently declared domain; no positional, spelling-based, transport, optional, or default convention exists.",
    ),
)

_PRODS = C5_4_REGISTRY.productions + (
    Production("C55.INPUT.DECLARE.NATURAL","C55.PROGRAM_INPUT_DECLARATION","PreparatoryUnit",
        (*_COMMON_DECL_PREFIX,W("מספר"),*_COMMON_DECL_SUFFIX),"C55.PROGRAM_INPUT_DECLARATION"),
    Production("C55.INPUT.DECLARE.SYMBOL","C55.PROGRAM_INPUT_DECLARATION","PreparatoryUnit",
        (*_COMMON_DECL_PREFIX,W("שם"),W("ממשפחת"),W("השמות"),W("אשר"),W("שמה"),N("SymbolDomainName"),*_COMMON_DECL_SUFFIX),"C55.PROGRAM_INPUT_DECLARATION"),
    Production("C55.INPUT.DECLARE.INDEX","C55.PROGRAM_INPUT_DECLARATION","PreparatoryUnit",
        (*_COMMON_DECL_PREFIX,W("מספר"),W("שנה"),*_COMMON_DECL_SUFFIX),"C55.PROGRAM_INPUT_DECLARATION"),
    Production("C55.INPUT.DECLARE.COLLECTION","C55.PROGRAM_INPUT_DECLARATION","PreparatoryUnit",
        (*_COMMON_DECL_PREFIX,Nonterminal("CollectionKind"),*_COMMON_DECL_SUFFIX),"C55.PROGRAM_INPUT_DECLARATION"),
    Production("C55.INPUT.READ.NATURAL","C55.PROGRAM_INPUT_REFERENCE","NumberValue",
        (W("המספר"),W("אשר"),W("עומד"),W("תחת"),W("הדבר"),W("אשר"),W("למלאכה"),W("הזאת"),W("שמו"),N("ProgramInputRoleName")),"C55.PROGRAM_INPUT_READ_NATURAL"),
    Production("C55.INPUT.READ.SYMBOL","C55.PROGRAM_INPUT_REFERENCE","SymbolValue",
        (W("השם"),W("אשר"),W("במשפחת"),W("השמות"),W("אשר"),W("שמה"),N("SymbolDomainName"),W("עומד"),W("תחת"),W("הדבר"),W("אשר"),W("למלאכה"),W("הזאת"),W("שמו"),N("ProgramInputRoleName")),"C55.PROGRAM_INPUT_READ_SYMBOL"),
    Production("C55.INPUT.READ.INDEX","C55.PROGRAM_INPUT_REFERENCE","IndexValue",
        (W("מספר"),W("השנה"),W("אשר"),W("עומד"),W("תחת"),W("הדבר"),W("אשר"),W("למלאכה"),W("הזאת"),W("שמו"),N("ProgramInputRoleName")),"C55.PROGRAM_INPUT_READ_INDEX"),
    Production("C55.INPUT.READ.COLLECTION","C55.PROGRAM_INPUT_REFERENCE","CollectionValue",
        (W("הספר"),W("אשר"),W("עומד"),W("תחת"),W("הדבר"),W("אשר"),W("למלאכה"),W("הזאת"),W("שמו"),N("ProgramInputRoleName")),"C55.PROGRAM_INPUT_READ_COLLECTION"),
)

C5_5_REGISTRY = ConstructionRegistry(
    language_edition=LANGUAGE_EDITION,
    registry_version=REGISTRY_VERSION,
    source_snapshot="C5.4+A15 Program Input Roles+B13 external binding+B15 domain-flow production integration",
    declarations=_DECLS, productions=_PRODS, semantic_gates=C5_4_REGISTRY.semantic_gates,
)

__all__=["C5_5_REGISTRY","COUNT_AS_NUMBER_ORIGINS","REGISTRY_VERSION","LANGUAGE_EDITION"]
