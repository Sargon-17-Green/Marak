from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TypeAlias

from compiler.source.source_map import OriginalSpan


@dataclass(frozen=True, slots=True)
class ParseLeaf:
    token_index: int
    text: str
    normalized_start: int
    normalized_end: int
    original: OriginalSpan
    morphology_rule_id: str | None = None
    lemma: str | None = None
    features: tuple[tuple[str, str], ...] = ()
    terminal_role: str | None = None
    numeric_value: int | None = None


@dataclass(frozen=True, slots=True)
class ParseNode:
    production_id: str
    construction_id: str
    symbol: str
    token_start: int
    token_end: int
    normalized_start: int | None
    normalized_end: int | None
    original: OriginalSpan | None
    children: tuple["ParseElement", ...] = ()


ParseElement: TypeAlias = ParseLeaf | ParseNode


@dataclass(frozen=True, slots=True)
class ParseAlternative:
    root: ParseNode
    semantic_id: str
    # Filled only by a later spec-grounded semantic/resolution step. Parser code
    # must not manufacture equivalence merely because semantic_id strings match.
    semantic_fingerprint: str | None = None


class AmbiguityStatus(str, Enum):
    EMPTY = "empty"
    UNIQUE = "unique"
    UNRESOLVED_MULTIPLE = "unresolved-multiple"
    PROVEN_EQUIVALENT = "proven-equivalent"
    PROVEN_DISTINCT = "proven-distinct"


@dataclass(frozen=True, slots=True)
class ParseForest:
    alternatives: tuple[ParseAlternative, ...]

    @property
    def structurally_ambiguous(self) -> bool:
        return len(self.alternatives) > 1

    @property
    def ambiguity_status(self) -> AmbiguityStatus:
        if not self.alternatives:
            return AmbiguityStatus.EMPTY
        if len(self.alternatives) == 1:
            return AmbiguityStatus.UNIQUE
        fingerprints = [a.semantic_fingerprint for a in self.alternatives]
        if any(f is None for f in fingerprints):
            return AmbiguityStatus.UNRESOLVED_MULTIPLE
        return (
            AmbiguityStatus.PROVEN_EQUIVALENT
            if len(set(fingerprints)) == 1
            else AmbiguityStatus.PROVEN_DISTINCT
        )

    @property
    def requires_disambiguation(self) -> bool:
        return self.ambiguity_status in {
            AmbiguityStatus.UNRESOLVED_MULTIPLE,
            AmbiguityStatus.PROVEN_DISTINCT,
        }


__all__ = [
    "ParseLeaf",
    "ParseNode",
    "ParseElement",
    "ParseAlternative",
    "AmbiguityStatus",
    "ParseForest",
]
