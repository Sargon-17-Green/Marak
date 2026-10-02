#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class NameKind(Enum):
    ACT = "act"
    PLACE = "place"
    ROLE = "role"
    PROGRAM_INPUT = "program-input"
    SYMBOL_DOMAIN = "symbol-domain"
    SYMBOL_MEMBER = "symbol-member"


OWNER_REQUIRED = frozenset({
    NameKind.ROLE,
    NameKind.PROGRAM_INPUT,
    NameKind.SYMBOL_MEMBER,
})

FORBIDDEN_RESOLUTION_POLICIES = frozenset({
    "longest-match",
    "expected-type-rescue",
    "declaration-known-tokenization",
    "nearest-declaration",
    "welded-spaced-alias",
    "visible-label-alias",
    "runtime-name-lookup",
})


@dataclass(frozen=True, order=True)
class CanonicalSourceName:
    words: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.words:
            raise ValueError("SOURCE_NAME_EMPTY")
        for word in self.words:
            if not isinstance(word, str) or not word or " " in word:
                raise ValueError("SOURCE_NAME_WORD_NOT_CANONICAL")

    @property
    def spelling(self) -> str:
        return " ".join(self.words)


def simple_name(word: str) -> CanonicalSourceName:
    return CanonicalSourceName((word,))


def counted_name(count: int, words: tuple[str, ...]) -> CanonicalSourceName:
    if type(count) is not int or count < 2:
        raise ValueError("COUNTED_SOURCE_NAME_COUNT")
    if count != len(words):
        raise ValueError("COUNTED_SOURCE_NAME_ARITY")
    return CanonicalSourceName(words)


@dataclass(frozen=True, order=True)
class SourceIdentityKey:
    kind: NameKind
    owner: object | None
    name: CanonicalSourceName

    def __post_init__(self) -> None:
        if self.kind in OWNER_REQUIRED and self.owner is None:
            raise ValueError("SOURCE_NAME_OWNER_REQUIRED")
        if self.kind not in OWNER_REQUIRED and self.owner is not None:
            raise ValueError("SOURCE_NAME_UNEXPECTED_OWNER")


@dataclass(frozen=True)
class ResolvedIdentity:
    serial: int
    key: SourceIdentityKey

    def __post_init__(self) -> None:
        if type(self.serial) is not int or self.serial <= 0:
            raise ValueError("SOURCE_ID_SERIAL")


class StaticNameEnvironment:
    def __init__(self) -> None:
        self._next = 1
        self._declared: dict[SourceIdentityKey, ResolvedIdentity] = {}

    def declare(self, key: SourceIdentityKey) -> ResolvedIdentity:
        if key in self._declared:
            raise ValueError("DUPLICATE_SOURCE_NAME")
        out = ResolvedIdentity(self._next, key)
        self._next += 1
        self._declared[key] = out
        return out

    def resolve(self, key: SourceIdentityKey) -> ResolvedIdentity:
        try:
            return self._declared[key]
        except KeyError as exc:
            raise ValueError("REFERENCE_BEFORE_DECLARATION") from exc


def program_input_semantic_material(owner_contract: str, name: CanonicalSourceName) -> tuple:
    if not owner_contract:
        raise ValueError("PROGRAM_CONTRACT_REQUIRED")
    return ("ProgramInputId", owner_contract, name.spelling)


def symbol_source_material(domain_owner: object, name: CanonicalSourceName) -> tuple:
    return ("SymbolMemberId", domain_owner, name.spelling)


__all__ = [
    "NameKind", "CanonicalSourceName", "SourceIdentityKey", "ResolvedIdentity",
    "StaticNameEnvironment", "simple_name", "counted_name",
    "program_input_semantic_material", "symbol_source_material",
    "FORBIDDEN_RESOLUTION_POLICIES",
]
