from __future__ import annotations

from compiler.models.hast import (
    HastAddNumber,
    HastEqualNumberProposition,
    HastExactInteger,
    HastNode,
    HastSubtractNumber,
)
from compiler.semantic_core.truth import (
    AddNumber,
    EqualNumberProposition,
    IntegerNumber,
    NumberTerm,
    Proposition,
    SubtractNumber,
)


def number_term_from_hast(node: HastNode) -> NumberTerm:
    if isinstance(node, HastExactInteger):
        return IntegerNumber(node.value)
    if isinstance(node, HastAddNumber):
        return AddNumber(number_term_from_hast(node.left), number_term_from_hast(node.right))
    if isinstance(node, HastSubtractNumber):
        return SubtractNumber(number_term_from_hast(node.left), number_term_from_hast(node.right))
    raise TypeError(f"HAST node does not denote a currently justified number: {type(node).__name__}")


def proposition_from_hast(node: HastNode) -> Proposition:
    if isinstance(node, HastEqualNumberProposition):
        return EqualNumberProposition(number_term_from_hast(node.left), number_term_from_hast(node.right))
    raise TypeError(f"HAST node is not a currently justified proposition: {type(node).__name__}")


__all__ = ["number_term_from_hast", "proposition_from_hast"]
