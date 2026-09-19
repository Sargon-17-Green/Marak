"""Normative Core v0.1 Unicode policy from A13.

Outside future strings, only the exact 27 Hebrew letter forms and the closed
A13 whitespace set are lexically significant.  No host Unicode/locale
predicate is a source of truth.
"""
from __future__ import annotations

from dataclasses import dataclass

HEBREW_LETTERS_27: tuple[str, ...] = tuple("אבגדהוזחטיכךלמםנןסעפףצץקרשת")
HEBREW_LETTER_SET = frozenset(HEBREW_LETTERS_27)
assert len(HEBREW_LETTERS_27) == 27
assert len(HEBREW_LETTER_SET) == 27

A13_NORMATIVE_WHITESPACE_CODEPOINTS: tuple[int, ...] = (
    *range(0x0009, 0x000E),
    0x0020,
    0x0085,
    0x00A0,
    0x1680,
    *range(0x2000, 0x200B),
    0x2028,
    0x2029,
    0x202F,
    0x205F,
    0x3000,
)
A13_NORMATIVE_WHITESPACE = frozenset(chr(cp) for cp in A13_NORMATIVE_WHITESPACE_CODEPOINTS)
# Historical name retained as a compatibility alias for C test/tool imports only.
# The language definition is A13, not the Unicode White_Space property.
UNICODE_WHITE_SPACE_15_1 = A13_NORMATIVE_WHITESPACE


@dataclass(frozen=True, slots=True)
class WhitespacePolicy:
    policy_id: str
    code_points: frozenset[str]

    def __post_init__(self) -> None:
        if not self.policy_id:
            raise ValueError("whitespace policy id must be non-empty")
        if any(len(ch) != 1 for ch in self.code_points):
            raise ValueError("whitespace policy entries must be single Unicode scalar values")

    def contains(self, ch: str) -> bool:
        return ch in self.code_points


A13_NORMATIVE_WHITESPACE_POLICY = WhitespacePolicy(
    "a13-core-v0.1-normative-whitespace",
    A13_NORMATIVE_WHITESPACE,
)
DEFAULT_WHITESPACE_POLICY = A13_NORMATIVE_WHITESPACE_POLICY
WHITESPACE_POLICY_ID = DEFAULT_WHITESPACE_POLICY.policy_id


def is_code_whitespace(ch: str, policy: WhitespacePolicy = DEFAULT_WHITESPACE_POLICY) -> bool:
    return policy.contains(ch)


__all__ = [
    "HEBREW_LETTERS_27",
    "HEBREW_LETTER_SET",
    "A13_NORMATIVE_WHITESPACE_CODEPOINTS",
    "A13_NORMATIVE_WHITESPACE",
    "A13_NORMATIVE_WHITESPACE_POLICY",
    "UNICODE_WHITE_SPACE_15_1",
    "WhitespacePolicy",
    "DEFAULT_WHITESPACE_POLICY",
    "WHITESPACE_POLICY_ID",
    "is_code_whitespace",
]
