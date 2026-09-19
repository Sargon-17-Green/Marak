"""Post-audit semantic substrate justified independently by B7/B8.

These models are semantic capabilities, not surface syntax and not a mandate
for any particular runtime representation.  In particular they do not expose
variables/cells or Boolean data values.
"""
from compiler.semantic_core.from_hast import number_term_from_hast, proposition_from_hast
from compiler.semantic_core.performance import (
    CompletedPerformance, DescribedActId, PerformanceIssue, PerformanceOccurrence,
    PerformanceOccurrenceId, RoleAssociation, RoleId, begin_performance,
    complete_performance, denote_immediate_result, produce_number, with_successor_snapshot,
)
from compiler.semantic_core.recurrence import OccurrenceDue, RecurrenceComplete, begin_after_gated, checkpoint_until
from compiler.semantic_core.state import (
    NUMBER_ASPECT,
    CurrentObservation,
    MissingCurrentFact,
    SemanticSnapshot,
    StateAspect,
    StateReferentId,
)
from compiler.semantic_core.truth import (
    AddNumber,
    ConsequenceSelection,
    CurrentNumber,
    EqualNumberProposition,
    IntegerNumber,
    NumberIssue,
    Satisfaction,
    SubtractNumber,
    ZeroProposition,
    denote_number,
    judge_proposition,
    select_consequence,
)

__all__ = [
    "NUMBER_ASPECT", "CurrentObservation", "MissingCurrentFact", "SemanticSnapshot",
    "StateAspect", "StateReferentId", "AddNumber", "ConsequenceSelection", "CurrentNumber",
    "EqualNumberProposition", "IntegerNumber", "NumberIssue", "Satisfaction", "SubtractNumber",
    "ZeroProposition", "denote_number", "judge_proposition", "select_consequence",
    "number_term_from_hast", "proposition_from_hast",
    "OccurrenceDue", "RecurrenceComplete", "begin_after_gated", "checkpoint_until",
    "CompletedPerformance", "DescribedActId", "PerformanceIssue", "PerformanceOccurrence",
    "PerformanceOccurrenceId", "RoleAssociation", "RoleId", "begin_performance",
    "complete_performance", "denote_immediate_result", "produce_number", "with_successor_snapshot",
]
