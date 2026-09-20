from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias


@dataclass(frozen=True, slots=True, order=True)
class SymbolDomainId:
    serial: int
    spelling: str

    def __post_init__(self) -> None:
        if self.serial <= 0 or not self.spelling:
            raise ValueError("SymbolDomainId requires positive serial and spelling")


@dataclass(frozen=True, slots=True, order=True)
class SymbolMemberId:
    serial: int
    spelling: str

    def __post_init__(self) -> None:
        if self.serial <= 0 or not self.spelling:
            raise ValueError("SymbolMemberId requires positive serial and spelling")


@dataclass(frozen=True, slots=True, order=True)
class ProgramInputId:
    serial: int
    spelling: str

    def __post_init__(self) -> None:
        if self.serial <= 0 or not self.spelling:
            raise ValueError("ProgramInputId requires positive serial and spelling")


@dataclass(frozen=True, slots=True)
class NaturalDomain:
    pass


@dataclass(frozen=True, slots=True)
class SymbolDomain:
    identity: SymbolDomainId


@dataclass(frozen=True, slots=True)
class BidirectionalIndexDomain:
    pass


@dataclass(frozen=True, slots=True)
class CollectionDomain:
    element_domain: "Domain"


Domain: TypeAlias = NaturalDomain | SymbolDomain | BidirectionalIndexDomain | CollectionDomain

NATURAL = NaturalDomain()
BIDIRECTIONAL_INDEX = BidirectionalIndexDomain()


def domain_key(domain: Domain) -> tuple:
    if isinstance(domain, NaturalDomain):
        return ("Natural",)
    if isinstance(domain, SymbolDomain):
        return ("Symbol", domain.identity.serial, domain.identity.spelling)
    if isinstance(domain, BidirectionalIndexDomain):
        return ("BidirectionalIndex",)
    if isinstance(domain, CollectionDomain):
        return ("Collection", domain_key(domain.element_domain))
    raise TypeError(f"unknown domain {type(domain).__name__}")


def require_domain(domain: object) -> Domain:
    if isinstance(domain, (NaturalDomain, SymbolDomain, BidirectionalIndexDomain, CollectionDomain)):
        if isinstance(domain, CollectionDomain):
            require_domain(domain.element_domain)
        return domain
    raise TypeError(f"unknown Marak domain {type(domain).__name__}")


__all__ = [
    "SymbolDomainId", "SymbolMemberId", "ProgramInputId",
    "NaturalDomain", "SymbolDomain", "BidirectionalIndexDomain", "CollectionDomain",
    "Domain", "NATURAL", "BIDIRECTIONAL_INDEX", "domain_key", "require_domain",
]
