from __future__ import annotations

"""C5.7 production registry: A18/B17 counted multi-word SourceName integration."""

from dataclasses import replace

from compiler.parse.a15_numerals import A15_DIRECT_NUMERAL_LEXICON_ID
from compiler.parse.c5_6_registry import (
    C5_6_REGISTRY,
    COUNT_AS_NUMBER_ORIGINS as C5_6_COUNT_AS_NUMBER_ORIGINS,
)
from compiler.parse.grammar import (
    ConstructionRegistry,
    NameTerminal,
    SourceNameTerminal,
)

LANGUAGE_EDITION = C5_6_REGISTRY.language_edition
REGISTRY_VERSION = "c5.7-a18-b17.1"


def _migrate_source_name_symbol(symbol):
    if isinstance(symbol, NameTerminal):
        return SourceNameTerminal(symbol.role, A15_DIRECT_NUMERAL_LEXICON_ID)
    return symbol

_PRODUCTIONS = tuple(
    replace(
        production,
        rhs=tuple(_migrate_source_name_symbol(symbol) for symbol in production.rhs),
    )
    for production in C5_6_REGISTRY.productions
)

COUNT_AS_NUMBER_ORIGINS = dict(C5_6_COUNT_AS_NUMBER_ORIGINS)

C5_7_REGISTRY = ConstructionRegistry(
    language_edition=LANGUAGE_EDITION,
    registry_version=REGISTRY_VERSION,
    source_snapshot="C5.6+A18 counted SourceName+B17 semantic integration",
    declarations=C5_6_REGISTRY.declarations,
    productions=_PRODUCTIONS,
    semantic_gates=C5_6_REGISTRY.semantic_gates,
)

__all__ = [
    "C5_7_REGISTRY",
    "COUNT_AS_NUMBER_ORIGINS",
    "REGISTRY_VERSION",
    "LANGUAGE_EDITION",
]
