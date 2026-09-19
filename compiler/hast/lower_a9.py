from __future__ import annotations

from compiler.models.hast import (
    HastAddNumber,
    HastEqualNumberProposition,
    HastExactInteger,
    HastNode,
    HastSubtractNumber,
)
from compiler.parse.forest import ParseAlternative, ParseElement, ParseLeaf, ParseNode


class A9LoweringError(ValueError):
    """Internal C error for a parse shape outside the currently justified bridge."""


def lower_numeric_truth_fragment(alternative: ParseAlternative) -> HastNode:
    """Lower the post-audit numeric/proposition overlap into canonical HAST.

    The bridge retains historical A9 support and accepts A12 direct numerals.
    It remains intentionally partial: reusable acts, result flow and whole-
    program organization are not inferred from this numeric/truth subset.
    """
    root = alternative.root
    if root.symbol == "NumberValue":
        return _lower_number(root)
    if root.symbol == "Proposition":
        return _lower_proposition(root)
    raise A9LoweringError(f"A9 canonical lowering is not available for {root.symbol}")


def _span(node: ParseNode):
    if node.original is None:
        raise A9LoweringError("canonical lowering requires source provenance")
    return node.original


def _node_children(node: ParseNode, symbol: str) -> tuple[ParseNode, ...]:
    return tuple(
        child for child in node.children
        if isinstance(child, ParseNode) and child.symbol == symbol
    )



def _numeric_leaf_value(element: ParseElement) -> int | None:
    if isinstance(element, ParseLeaf):
        return element.numeric_value
    for child in element.children:
        value = _numeric_leaf_value(child)
        if value is not None:
            return value
    return None

def _lower_number(node: ParseNode) -> HastNode:
    if node.production_id == "A9.NUMBER.LITERAL.ONE":
        return HastExactInteger(_span(node), 1)
    if node.production_id == "A12.NUMBER.LITERAL":
        value = _numeric_leaf_value(node)
        if value is None:
            raise A9LoweringError("A12 direct numeral parse lacks numeric_value provenance")
        return HastExactInteger(_span(node), value)
    if node.production_id == "A9.NUMBER.ADD":
        children = _node_children(node, "NumberValue")
        if len(children) != 2:
            raise A9LoweringError("addition parse must contain exactly two NumberValue children")
        return HastAddNumber(_span(node), _lower_number(children[0]), _lower_number(children[1]))
    if node.production_id == "A9.NUMBER.SUBTRACT":
        children = _node_children(node, "NumberValue")
        if len(children) != 2:
            raise A9LoweringError("subtraction parse must contain exactly two NumberValue children")
        return HastSubtractNumber(_span(node), _lower_number(children[0]), _lower_number(children[1]))
    raise A9LoweringError(f"unsupported A9 NumberValue production {node.production_id}")


def _lower_proposition(node: ParseNode) -> HastNode:
    if node.production_id == "A9.PROPOSITION.NUMERIC_IDENTITY":
        children = _node_children(node, "NumberValue")
        if len(children) != 2:
            raise A9LoweringError("numeric identity parse must contain exactly two NumberValue children")
        return HastEqualNumberProposition(
            _span(node), _lower_number(children[0]), _lower_number(children[1])
        )
    raise A9LoweringError(f"unsupported A9 Proposition production {node.production_id}")


def lower_a9_fragment(alternative: ParseAlternative) -> HastNode:
    """Backward-compatible name for historical tests; uses the neutral bridge."""
    return lower_numeric_truth_fragment(alternative)


__all__ = ["A9LoweringError", "lower_numeric_truth_fragment", "lower_a9_fragment"]
