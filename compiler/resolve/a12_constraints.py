from __future__ import annotations

from dataclasses import dataclass

from compiler.parse.forest import ParseElement, ParseLeaf, ParseNode
from compiler.source.source_map import OriginalSpan


@dataclass(frozen=True, slots=True)
class A12ConstraintIssue:
    code: str
    message_en: str
    message_he: str
    source_span: OriginalSpan | None
    metadata: dict[str, object]


def _direct_leaves(node: ParseNode, role: str) -> tuple[ParseLeaf, ...]:
    return tuple(
        child for child in node.children
        if isinstance(child, ParseLeaf) and child.terminal_role == role
    )


def find_a12_constraint_issues(root: ParseNode) -> tuple[A12ConstraintIssue, ...]:
    out: list[A12ConstraintIssue] = []
    _visit(root, out)
    return tuple(out)


def _visit(node: ParseNode, out: list[A12ConstraintIssue]) -> None:
    if node.production_id == "A12.BODY.DEFINITION":
        names = _direct_leaves(node, "BodyActionName")
        if len(names) == 2 and names[0].text != names[1].text:
            out.append(A12ConstraintIssue(
                "REF0021",
                "The frozen A12 body opener and closer must explicitly name the same act; no nearest-open-body convention repairs a mismatch.",
                "פותח הגוף וסוגר הגוף הקפואים של A12 חייבים לנקוב במפורש באותו מעשה; אין כלל של 'הגוף הפתוח הקרוב ביותר' המתקן אי־התאמה.",
                names[1].original,
                {
                    "rule": "a12-body-opener-closer-explicit-co-reference",
                    "expected_name": names[0].text,
                    "actual_name": names[1].text,
                },
            ))
    for child in node.children:
        if isinstance(child, ParseNode):
            _visit(child, out)


__all__ = ["A12ConstraintIssue", "find_a12_constraint_issues"]
