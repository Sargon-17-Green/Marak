from __future__ import annotations

from dataclasses import dataclass

from compiler.parse.forest import ParseElement, ParseLeaf, ParseNode
from compiler.source.source_map import OriginalSpan


@dataclass(frozen=True, slots=True)
class A12ValidationIssue:
    code: str
    message_en: str
    message_he: str
    source_span: OriginalSpan | None
    metadata: dict[str, object]


def _nodes(element: ParseElement, production_id: str) -> tuple[ParseNode, ...]:
    if isinstance(element, ParseLeaf):
        return ()
    out = [element] if element.production_id == production_id else []
    for child in element.children:
        out.extend(_nodes(child, production_id))
    return tuple(out)


def find_a12_validation_issues(root: ParseNode) -> tuple[A12ValidationIssue, ...]:
    issues: list[A12ValidationIssue] = []
    for body in _nodes(root, "A12.BODY.DEFINITION"):
        outputs = _nodes(body, "A12.RESULT.PRODUCE")
        if len(outputs) > 1:
            issues.append(A12ValidationIssue(
                "SEM0012",
                "Frozen A-Core v0.1 permits at most one numeric output production in one act performance.",
                "A-Core v0.1 הקפוא מתיר לכל היותר הפקת תוצאה מספרית אחת בביצוע אחד של מעשה.",
                outputs[1].original,
                {
                    "rule": "a12-at-most-one-numeric-output",
                    "output_count": len(outputs),
                    "a11_multiple_results_removed": True,
                },
            ))
    return tuple(issues)


__all__ = ["A12ValidationIssue", "find_a12_validation_issues"]
