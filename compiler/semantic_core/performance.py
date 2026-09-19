from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

from compiler.semantic_core.state import SemanticSnapshot


@dataclass(frozen=True, slots=True, order=True)
class DescribedActId:
    """Opaque resolved identity of a reusable described מעשה."""

    key: str

    def __post_init__(self) -> None:
        if not self.key:
            raise ValueError("described-act identity must be non-empty")


@dataclass(frozen=True, slots=True, order=True)
class RoleId:
    """A named semantic role belonging to one described act; never positional."""

    act: DescribedActId
    key: str

    def __post_init__(self) -> None:
        if not self.key:
            raise ValueError("role identity must be non-empty")


@dataclass(frozen=True, slots=True, order=True)
class PerformanceOccurrenceId:
    """Semantic identity of one performance occurrence, not a stack frame."""

    key: str

    def __post_init__(self) -> None:
        if not self.key:
            raise ValueError("performance occurrence identity must be non-empty")


@dataclass(frozen=True, slots=True)
class RoleAssociation:
    role: RoleId
    value: int

    def __post_init__(self) -> None:
        if type(self.value) is not int:
            raise TypeError("role association requires an exact integer value")


@dataclass(frozen=True, slots=True)
class PerformanceIssue:
    code: str
    detail: str


@dataclass(frozen=True, slots=True)
class PerformanceOccurrence:
    """B10/B11 semantic occurrence while its described act is being carried out.

    This is a semantic relation bundle, not a call frame.  Association ordering
    is canonicalized because A12 explicitly denies positional force.
    """

    identity: PerformanceOccurrenceId
    act: DescribedActId
    incoming_snapshot: SemanticSnapshot
    current_snapshot: SemanticSnapshot
    associations: tuple[RoleAssociation, ...]
    produced_number: int | None = None

    def __post_init__(self) -> None:
        seen: set[RoleId] = set()
        for association in self.associations:
            if association.role.act != self.act:
                raise ValueError("role association belongs to a different described act")
            if association.role in seen:
                raise ValueError("duplicate role association")
            seen.add(association.role)
        canonical = tuple(sorted(self.associations, key=lambda a: (a.role.act.key, a.role.key)))
        if canonical != self.associations:
            object.__setattr__(self, "associations", canonical)
        if self.produced_number is not None and type(self.produced_number) is not int:
            raise TypeError("produced number must be an exact integer")

    def value_for_role(self, role: RoleId) -> int | PerformanceIssue:
        if role.act != self.act:
            return PerformanceIssue("UNDECLARED_ROLE", "role belongs to a different described act")
        for association in self.associations:
            if association.role == role:
                return association.value
        return PerformanceIssue("MISSING_ROLE_ASSOCIATION", f"no association for role {role.key}")


@dataclass(frozen=True, slots=True)
class CompletedPerformance:
    """Successful completed performance with provenance and optional A12 output."""

    identity: PerformanceOccurrenceId
    act: DescribedActId
    snapshot: SemanticSnapshot
    produced_number: int | None

    def __post_init__(self) -> None:
        if self.produced_number is not None and type(self.produced_number) is not int:
            raise TypeError("completed output must be an exact integer")


PerformanceStart: TypeAlias = PerformanceOccurrence | PerformanceIssue
ImmediateResult: TypeAlias = int | PerformanceIssue


def begin_performance(
    identity: PerformanceOccurrenceId,
    act: DescribedActId,
    *,
    required_roles: tuple[RoleId, ...],
    associations: tuple[RoleAssociation, ...],
    incoming_snapshot: SemanticSnapshot,
) -> PerformanceStart:
    """Create one semantic performance occurrence from explicit named roles.

    This operation assumes Value descriptions have already been denoted against
    the same incoming snapshot, per B10/B11.  The tuple order has no matching or
    timing force.
    """
    if len(set(required_roles)) != len(required_roles):
        return PerformanceIssue("DUPLICATE_REQUIRED_ROLE", "described act repeats a required role identity")
    if any(role.act != act for role in required_roles):
        return PerformanceIssue("UNDECLARED_ROLE", "a required role belongs to a different described act")

    by_role: dict[RoleId, int] = {}
    for association in associations:
        if association.role.act != act or association.role not in required_roles:
            return PerformanceIssue("UNDECLARED_ROLE_ASSOCIATION", f"role {association.role.key} is not required by this act")
        if association.role in by_role:
            return PerformanceIssue("DUPLICATE_ROLE_ASSOCIATION", f"role {association.role.key} is associated more than once")
        by_role[association.role] = association.value

    missing = [role.key for role in required_roles if role not in by_role]
    if missing:
        return PerformanceIssue("MISSING_ROLE_ASSOCIATION", "missing role association(s): " + ", ".join(sorted(missing)))

    canonical = tuple(RoleAssociation(role, by_role[role]) for role in sorted(required_roles))
    return PerformanceOccurrence(identity, act, incoming_snapshot, incoming_snapshot, canonical)


def with_successor_snapshot(occurrence: PerformanceOccurrence, snapshot: SemanticSnapshot) -> PerformanceOccurrence:
    """Carry a committed successor semantic state without affecting role values/output."""
    return PerformanceOccurrence(
        occurrence.identity,
        occurrence.act,
        occurrence.incoming_snapshot,
        snapshot,
        occurrence.associations,
        occurrence.produced_number,
    )


def produce_number(occurrence: PerformanceOccurrence, value: int) -> PerformanceOccurrence | PerformanceIssue:
    """Record the A12 output without completing the performance."""
    if type(value) is not int:
        raise TypeError("A12 numeric output requires an exact integer")
    if occurrence.produced_number is not None:
        return PerformanceIssue("SECOND_OUTPUT_OUTSIDE_A12_CORE", "A12 Core permits at most one numeric output")
    return PerformanceOccurrence(
        occurrence.identity,
        occurrence.act,
        occurrence.incoming_snapshot,
        occurrence.current_snapshot,
        occurrence.associations,
        value,
    )


def complete_performance(occurrence: PerformanceOccurrence) -> CompletedPerformance:
    """Ordinary successful completion by body exhaustion (or separately licensed cessation)."""
    return CompletedPerformance(
        occurrence.identity,
        occurrence.act,
        occurrence.current_snapshot,
        occurrence.produced_number,
    )


def denote_immediate_result(completed: CompletedPerformance) -> ImmediateResult:
    """Denote an explicitly supplied just-completed performance's sole result.

    No history/global 'last result' exists here.  Source resolution must prove
    that the passed completion is exactly the A12 immediate antecedent.
    """
    if completed.produced_number is None:
        return PerformanceIssue("NO_NUMERIC_OUTPUT", "the completed performance produced no numeric output")
    return completed.produced_number


__all__ = [
    "DescribedActId", "RoleId", "PerformanceOccurrenceId", "RoleAssociation",
    "PerformanceIssue", "PerformanceOccurrence", "CompletedPerformance",
    "PerformanceStart", "ImmediateResult", "begin_performance", "with_successor_snapshot",
    "produce_number", "complete_performance", "denote_immediate_result",
]
