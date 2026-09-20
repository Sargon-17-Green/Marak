from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

from compiler.models.domains import (
    BIDIRECTIONAL_INDEX, NATURAL, CollectionDomain, Domain, SymbolDomain,
    SymbolDomainId, SymbolMemberId, require_domain,
)


@dataclass(frozen=True, slots=True)
class NaturalValue:
    value: int

    def __post_init__(self) -> None:
        if type(self.value) is not int or self.value < 0:
            raise ValueError("NaturalValue requires a non-negative exact integer")


@dataclass(frozen=True, slots=True)
class SymbolValue:
    domain_id: SymbolDomainId
    member_id: SymbolMemberId
    external_label: str

    def __post_init__(self) -> None:
        if not self.external_label:
            raise ValueError("SymbolValue requires canonical visible label metadata")


@dataclass(frozen=True, slots=True)
class BidirectionalIndexValue:
    side: str
    magnitude: int = 0

    def __post_init__(self) -> None:
        if self.side not in {"before", "zero", "after"}:
            raise ValueError("BidirectionalIndex side must be before/zero/after")
        if type(self.magnitude) is not int or self.magnitude < 0:
            raise ValueError("BidirectionalIndex magnitude must be a Natural")
        if self.side == "zero" and self.magnitude != 0:
            raise ValueError("Zero index has magnitude 0")
        if self.side != "zero" and self.magnitude <= 0:
            raise ValueError("Before/After index requires positive magnitude")


@dataclass(frozen=True, slots=True)
class CollectionValue:
    element_domain: Domain
    items: tuple["SemanticValue", ...]

    def __post_init__(self) -> None:
        require_domain(self.element_domain)
        for item in self.items:
            if value_domain(item) != self.element_domain:
                raise ValueError("CollectionValue element domain mismatch")


SemanticValue: TypeAlias = NaturalValue | SymbolValue | BidirectionalIndexValue | CollectionValue


def value_domain(value: SemanticValue) -> Domain:
    if isinstance(value, NaturalValue):
        return NATURAL
    if isinstance(value, SymbolValue):
        return SymbolDomain(value.domain_id)
    if isinstance(value, BidirectionalIndexValue):
        return BIDIRECTIONAL_INDEX
    if isinstance(value, CollectionValue):
        return CollectionDomain(value.element_domain)
    raise TypeError(f"unknown Marak Value {type(value).__name__}")


def symbol_identity_equal(left: SymbolValue, right: SymbolValue) -> bool:
    return left.domain_id == right.domain_id and left.member_id == right.member_id


def index_successor(value: BidirectionalIndexValue) -> BidirectionalIndexValue:
    if value.side == "before":
        if value.magnitude == 1:
            return BidirectionalIndexValue("zero", 0)
        return BidirectionalIndexValue("before", value.magnitude - 1)
    if value.side == "zero":
        return BidirectionalIndexValue("after", 1)
    return BidirectionalIndexValue("after", value.magnitude + 1)


def index_predecessor(value: BidirectionalIndexValue) -> BidirectionalIndexValue:
    if value.side == "after":
        if value.magnitude == 1:
            return BidirectionalIndexValue("zero", 0)
        return BidirectionalIndexValue("after", value.magnitude - 1)
    if value.side == "zero":
        return BidirectionalIndexValue("before", 1)
    return BidirectionalIndexValue("before", value.magnitude + 1)


def observable_value(value: SemanticValue):
    if isinstance(value, NaturalValue):
        return value.value
    if isinstance(value, SymbolValue):
        # B13/B15 language observation is the canonical visible label only.
        # Domain/member source names and implementation identities remain
        # available to resolution/validation/debug layers but are erased here.
        return value.external_label
    if isinstance(value, BidirectionalIndexValue):
        if value.side == "zero":
            return {"index": "Zero"}
        return {"index": "BeforeZero" if value.side == "before" else "AfterZero", "magnitude": value.magnitude}
    if isinstance(value, CollectionValue):
        return [observable_value(x) for x in value.items]
    raise TypeError(type(value).__name__)


__all__ = [
    "NaturalValue", "SymbolValue", "BidirectionalIndexValue", "CollectionValue",
    "SemanticValue", "value_domain", "symbol_identity_equal",
    "index_successor", "index_predecessor", "observable_value",
]
