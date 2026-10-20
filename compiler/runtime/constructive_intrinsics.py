"""Semantics-preserving accelerators for canonical constructive arithmetic.

These helpers do not replace Marak arithmetic with an oracle.  They collapse
specific constructive implementations while returning the exact language-
observable product sequence that the slow implementation emits.  Runtime
integration is opt-in and disabled whenever a fuel budget is present, so fuel
remains a step-by-step diagnostic of the baseline evaluator.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


MULTIPLY_ACT = "לקחת מספר פעמים"
REMAINDER_ACT = "הנותר בדרך הקצרה"
ADD_ACT = "חיבור"


@dataclass(frozen=True, slots=True)
class ConstructiveIntrinsicTrace:
    result: int
    fact_updates: tuple[tuple[str, int], ...]
    products: tuple[tuple[str, int], ...]


def _natural(roles: Mapping[str, object], name: str) -> int | None:
    value = roles.get(name)
    if type(value) is not int or value < 0:
        return None
    return value


def _multiply_trace(roles: Mapping[str, object]) -> ConstructiveIntrinsicTrace | None:
    number = _natural(roles, "מספר")
    count = _natural(roles, "מנין")
    if number is None or count is None:
        return None

    remaining = count
    product = 0
    emitted: list[tuple[str, int]] = []

    if count:
        bit = 1 << (count.bit_length() - 1)
        while bit:
            if bit <= remaining:
                remaining -= bit
                product += number * bit
                emitted.append((ADD_ACT, product))
            bit >>= 1

    assert remaining == 0
    emitted.append((MULTIPLY_ACT, product))
    return ConstructiveIntrinsicTrace(
        result=product,
        fact_updates=(("מכפלה", product), ("מנין הכפל הנותר", 0)),
        products=tuple(emitted),
    )


def _remainder_trace(roles: Mapping[str, object]) -> ConstructiveIntrinsicTrace | None:
    number = _natural(roles, "מספר")
    divisor = _natural(roles, "מחלק")
    if number is None or divisor is None or divisor == 0:
        return None

    products: list[tuple[str, int]] = []
    levels: list[int] = []
    current = divisor

    # This is the exact descent performed by "רד בדרך הקצרה": each level
    # first performs חיבור(divisor, divisor), then recurses with the doubled
    # divisor until the divisor is greater than the number.
    while current <= number:
        levels.append(current)
        current += current
        products.append((ADD_ACT, current))

    # Base "הנותר בדרך הקצרה" call: divisor > number.
    result = number
    products.append((REMAINDER_ACT, result))

    # Exact unwind order.  Every recursive "הנותר בדרך הקצרה" emits its
    # result after optionally subtracting that level's divisor.
    for level in reversed(levels):
        if level <= result:
            result -= level
        products.append((REMAINDER_ACT, result))

    return ConstructiveIntrinsicTrace(
        result=result,
        fact_updates=(("תוצאת הדרך הקצרה", result),),
        products=tuple(products),
    )


def constructive_intrinsic_trace(
    act_name: str,
    roles: Mapping[str, object],
) -> ConstructiveIntrinsicTrace | None:
    if act_name == MULTIPLY_ACT:
        return _multiply_trace(roles)
    if act_name == REMAINDER_ACT:
        return _remainder_trace(roles)
    return None


__all__ = [
    "ADD_ACT",
    "MULTIPLY_ACT",
    "REMAINDER_ACT",
    "ConstructiveIntrinsicTrace",
    "constructive_intrinsic_trace",
]
