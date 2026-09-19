from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

from compiler.semantic_core.state import SemanticSnapshot
from compiler.semantic_core.truth import NumberIssue, Proposition, Satisfaction, judge_proposition


@dataclass(frozen=True, slots=True)
class OccurrenceDue:
    """Meta-semantic phase: the admitted repeated occurrence is due to execute.

    No iteration number or hidden counter is carried.
    """
    snapshot: SemanticSnapshot


@dataclass(frozen=True, slots=True)
class RecurrenceComplete:
    snapshot: SemanticSnapshot


AfterCheckpointResult: TypeAlias = OccurrenceDue | RecurrenceComplete | NumberIssue


def begin_after_gated(snapshot: SemanticSnapshot) -> OccurrenceDue:
    """A10/B9 recurrence always begins with the explicit initial occurrence."""
    return OccurrenceDue(snapshot)


def checkpoint_until(proposition: Proposition, snapshot_after_occurrence: SemanticSnapshot) -> AfterCheckpointResult:
    """After one completed occurrence, cease exactly when the proposition holds."""
    judgment = judge_proposition(proposition, snapshot_after_occurrence)
    if isinstance(judgment, NumberIssue):
        return judgment
    if judgment.outcome is Satisfaction.HOLDS:
        return RecurrenceComplete(snapshot_after_occurrence)
    return OccurrenceDue(snapshot_after_occurrence)


__all__ = ["OccurrenceDue", "RecurrenceComplete", "AfterCheckpointResult", "begin_after_gated", "checkpoint_until"]
