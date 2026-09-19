from __future__ import annotations

from dataclasses import dataclass

from compiler.parse.forest import ParseElement, ParseLeaf, ParseNode
from compiler.source.source_map import OriginalSpan


@dataclass(frozen=True, slots=True)
class A10ConstraintIssue:
    code: str
    message_en: str
    message_he: str
    source_span: OriginalSpan | None
    metadata: dict[str, object]


def find_a10_constraint_issues(root: ParseNode) -> tuple[A10ConstraintIssue, ...]:
    out: list[A10ConstraintIssue] = []
    _visit(root, out)
    return tuple(out)


def _visit(node: ParseNode, out: list[A10ConstraintIssue]) -> None:
    if node.production_id in {"A10.PLACE.INTRODUCE", "A10.PLACE.REPLACE"}:
        names = [c for c in node.children if isinstance(c, ParseLeaf) and c.terminal_role == "PlaceName"]
        if len(names) == 2 and names[0].text != names[1].text:
            out.append(A10ConstraintIssue(
                "REF0001",
                "This A10 construction grammatically requires its two place descriptions to co-refer; the explicit names differ.",
                "במבנה A10 זה שני תיאורי המקום חייבים להתייחס לאותו מקום; השמות המפורשים שונים.",
                names[1].original,
                {
                    "production_id": node.production_id,
                    "first_name": names[0].text,
                    "second_name": names[1].text,
                    "rule": "explicit-required-co-reference",
                },
            ))
    for child in node.children:
        if isinstance(child, ParseNode):
            _visit(child, out)


__all__ = ["A10ConstraintIssue", "find_a10_constraint_issues"]
