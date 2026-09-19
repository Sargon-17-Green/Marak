from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TypeAlias

from compiler.semantic_core.state import (
    NUMBER_ASPECT,
    CurrentObservation,
    SemanticSnapshot,
    StateReferentId,
)


@dataclass(frozen=True, slots=True)
class IntegerNumber:
    value: int

    def __post_init__(self) -> None:
        if type(self.value) is not int:
            raise TypeError("IntegerNumber requires an exact integer, not host bool/coercions")


@dataclass(frozen=True, slots=True)
class CurrentNumber:
    referent: StateReferentId


@dataclass(frozen=True, slots=True)
class AddNumber:
    left: "NumberTerm"
    right: "NumberTerm"


@dataclass(frozen=True, slots=True)
class SubtractNumber:
    left: "NumberTerm"
    right: "NumberTerm"


NumberTerm: TypeAlias = IntegerNumber | CurrentNumber | AddNumber | SubtractNumber


@dataclass(frozen=True, slots=True)
class NumberObservation:
    value: int


@dataclass(frozen=True, slots=True)
class NumberIssue:
    code: str
    detail: str


NumberResult: TypeAlias = NumberObservation | NumberIssue


def denote_number(term: NumberTerm, snapshot: SemanticSnapshot) -> NumberResult:
    if isinstance(term, IntegerNumber):
        return NumberObservation(term.value)
    if isinstance(term, CurrentNumber):
        observed = snapshot.current_of(term.referent, NUMBER_ASPECT)
        if isinstance(observed, CurrentObservation):
            return NumberObservation(observed.value)
        return NumberIssue("NO_CURRENT_NUMBER", f"no current number for referent {term.referent.key}")
    if isinstance(term, (AddNumber, SubtractNumber)):
        left = denote_number(term.left, snapshot)
        if isinstance(left, NumberIssue):
            return left
        right = denote_number(term.right, snapshot)
        if isinstance(right, NumberIssue):
            return right
        value = left.value + right.value if isinstance(term, AddNumber) else left.value - right.value
        return NumberObservation(value)
    raise TypeError(f"unsupported NumberTerm: {type(term)!r}")


@dataclass(frozen=True, slots=True)
class EqualNumberProposition:
    left: NumberTerm
    right: NumberTerm


@dataclass(frozen=True, slots=True)
class ZeroProposition:
    number: NumberTerm


Proposition: TypeAlias = EqualNumberProposition | ZeroProposition


class Satisfaction(str, Enum):
    """Meta-semantic judgment outcome; deliberately not a language data Value."""

    HOLDS = "holds"
    DOES_NOT_HOLD = "does_not_hold"


@dataclass(frozen=True, slots=True)
class PropositionJudgment:
    outcome: Satisfaction


PropositionResult: TypeAlias = PropositionJudgment | NumberIssue


def judge_proposition(proposition: Proposition, snapshot: SemanticSnapshot) -> PropositionResult:
    if isinstance(proposition, EqualNumberProposition):
        left = denote_number(proposition.left, snapshot)
        if isinstance(left, NumberIssue):
            return left
        right = denote_number(proposition.right, snapshot)
        if isinstance(right, NumberIssue):
            return right
        return PropositionJudgment(
            Satisfaction.HOLDS if left.value == right.value else Satisfaction.DOES_NOT_HOLD
        )
    if isinstance(proposition, ZeroProposition):
        number = denote_number(proposition.number, snapshot)
        if isinstance(number, NumberIssue):
            return number
        return PropositionJudgment(
            Satisfaction.HOLDS if number.value == 0 else Satisfaction.DOES_NOT_HOLD
        )
    raise TypeError(f"unsupported Proposition: {type(proposition)!r}")


class ConsequenceSelection(str, Enum):
    HOLDS_CONSEQUENCE = "holds_consequence"
    DOES_NOT_HOLD_CONSEQUENCE = "does_not_hold_consequence"


SelectionResult: TypeAlias = ConsequenceSelection | NumberIssue


def select_consequence(proposition: Proposition, snapshot: SemanticSnapshot) -> SelectionResult:
    """Select a consequence without imposing any action/block/call representation."""
    result = judge_proposition(proposition, snapshot)
    if isinstance(result, NumberIssue):
        return result
    if result.outcome is Satisfaction.HOLDS:
        return ConsequenceSelection.HOLDS_CONSEQUENCE
    return ConsequenceSelection.DOES_NOT_HOLD_CONSEQUENCE


__all__ = [
    "IntegerNumber", "CurrentNumber", "AddNumber", "SubtractNumber", "NumberTerm",
    "NumberObservation", "NumberIssue", "NumberResult", "denote_number",
    "EqualNumberProposition", "ZeroProposition", "Proposition", "Satisfaction",
    "PropositionJudgment", "PropositionResult", "judge_proposition",
    "ConsequenceSelection", "SelectionResult", "select_consequence",
]
