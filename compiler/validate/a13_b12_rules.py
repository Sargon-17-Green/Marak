from __future__ import annotations

from dataclasses import dataclass

from compiler.models.hast import (
    HastActBody, HastAddNatural, HastConditional, HastCoreProgram, HastExactNatural,
    HastExecutable, HastFixedRecurrence, HastNumber, HastPostActionRecurrence,
    HastProduceResult, HastSubtractNatural, HastThen,
)
from compiler.source.source_map import OriginalSpan


@dataclass(frozen=True, slots=True)
class A13B12ValidationIssue:
    code: str
    semantic_code: str
    message_en: str
    message_he: str
    source_span: OriginalSpan | None
    metadata: dict[str, object]


def const_natural(node: HastNumber) -> int | None:
    if isinstance(node, HastExactNatural):
        return node.value
    if isinstance(node, HastAddNatural):
        a, b = const_natural(node.addend), const_natural(node.augend)
        return None if a is None or b is None else a + b
    if isinstance(node, HastSubtractNatural):
        a, b = const_natural(node.amount), const_natural(node.source)
        if a is None or b is None:
            return None
        if a > b:
            return None
        return b - a
    return None


def _numbers(node) -> list[HastNumber]:
    out: list[HastNumber] = []
    if isinstance(node, HastNumber):
        out.append(node)
    fields = getattr(node, "__dataclass_fields__", {})
    for name in fields:
        if name == "source_span":
            continue
        value = getattr(node, name)
        if isinstance(value, tuple):
            for x in value:
                if hasattr(x, "__dataclass_fields__"):
                    out.extend(_numbers(x))
        elif hasattr(value, "__dataclass_fields__"):
            out.extend(_numbers(value))
    return out


def _count_outputs(action: HastExecutable) -> int:
    if isinstance(action, HastProduceResult):
        return 1
    if isinstance(action, HastThen):
        return sum(_count_outputs(x) for x in action.actions)
    if isinstance(action, HastConditional):
        return max(_count_outputs(action.if_holds), _count_outputs(action.if_not))
    if isinstance(action, HastFixedRecurrence):
        return action.count * _count_outputs(action.action)
    if isinstance(action, HastPostActionRecurrence):
        # Any output in an unbounded recurrence can occur more than once.
        return 2 if _count_outputs(action.action) else 0
    return 0


def validate_a13_b12(program: HastCoreProgram) -> tuple[A13B12ValidationIssue, ...]:
    issues: list[A13B12ValidationIssue] = []
    for number in _numbers(program):
        if isinstance(number, HastSubtractNatural):
            amount = const_natural(number.amount)
            source = const_natural(number.source)
            if amount is not None and source is not None and amount > source:
                issues.append(A13B12ValidationIssue(
                    "SEM0201", "ARITHMETIC_DOMAIN_ERROR",
                    "Natural subtraction underflow is statically provable: the amount removed is larger than the source.",
                    "ניתן להוכיח מראש חריגה מתחום החיסור הטבעי: הכמות הנגרעת גדולה מן המקור.",
                    number.source_span,
                    {"amount": amount, "source": source, "phase": "static-validation"},
                ))
    for prep in program.preparation:
        if isinstance(prep, HastActBody) and _count_outputs(prep.body) > 1:
            issues.append(A13B12ValidationIssue(
                "SEM0012", "CORE_OUTPUT_CARDINALITY_ERROR",
                "Core v0.1 permits at most one numeric result production per performance path.",
                "Core v0.1 מתיר לכל היותר הפקת תוצאה מספרית אחת במסלול ביצוע.",
                prep.source_span,
                {"act": prep.act.spelling},
            ))
    return tuple(issues)


__all__ = ["A13B12ValidationIssue", "const_natural", "validate_a13_b12"]
