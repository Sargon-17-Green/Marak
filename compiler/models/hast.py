"""Canonical HAST ownership for the A13/B12 Core integration candidate.

The model records only distinctions justified by A13/B12.  It deliberately
avoids a conventional Statement/Expression/Function/Parameter/Return ontology.
Historical M3 fragment nodes are retained at the end for regression evidence.
"""
from __future__ import annotations

from dataclasses import dataclass

from compiler.models.symbols import ActId, PlaceId, RoleId
from compiler.source.source_map import OriginalSpan

HAST_VERSION = "core-hast-0.1-candidate-1"


@dataclass(frozen=True, slots=True)
class HastNode:
    source_span: OriginalSpan


# ---- semantic categories justified by A13/B12 ----
@dataclass(frozen=True, slots=True)
class HastNumber(HastNode):
    pass


@dataclass(frozen=True, slots=True)
class HastProposition(HastNode):
    pass


@dataclass(frozen=True, slots=True)
class HastExecutable(HastNode):
    pass


@dataclass(frozen=True, slots=True)
class HastPreparatory(HastNode):
    pass


@dataclass(frozen=True, slots=True)
class HastExactNatural(HastNumber):
    value: int

    def __post_init__(self) -> None:
        if type(self.value) is not int or self.value < 0:
            raise ValueError("Core Natural must be a non-negative exact integer")


@dataclass(frozen=True, slots=True)
class HastCurrentFact(HastNumber):
    place: PlaceId


@dataclass(frozen=True, slots=True)
class HastCurrentRoleNumber(HastNumber):
    role: RoleId


@dataclass(frozen=True, slots=True)
class HastRecentResult(HastNumber):
    act: ActId


@dataclass(frozen=True, slots=True)
class HastAddNatural(HastNumber):
    addend: HastNumber
    augend: HastNumber


@dataclass(frozen=True, slots=True)
class HastSubtractNatural(HastNumber):
    amount: HastNumber
    source: HastNumber


@dataclass(frozen=True, slots=True)
class HastEqualProposition(HastProposition):
    left: HastNumber
    right: HastNumber


@dataclass(frozen=True, slots=True)
class HastRoleAssociation(HastNode):
    role: RoleId
    value: HastNumber


@dataclass(frozen=True, slots=True)
class HastReplaceCurrentFact(HastExecutable):
    place: PlaceId
    value: HastNumber


@dataclass(frozen=True, slots=True)
class HastPerformAct(HastExecutable):
    act: ActId
    associations: tuple[HastRoleAssociation, ...] = ()


@dataclass(frozen=True, slots=True)
class HastProduceResult(HastExecutable):
    value: HastNumber


@dataclass(frozen=True, slots=True)
class HastThen(HastExecutable):
    actions: tuple[HastExecutable, ...]

    def __post_init__(self) -> None:
        if not self.actions:
            raise ValueError("HastThen requires at least one action")


@dataclass(frozen=True, slots=True)
class HastConditional(HastExecutable):
    proposition: HastProposition
    if_holds: HastExecutable
    if_not: HastExecutable


@dataclass(frozen=True, slots=True)
class HastPostActionRecurrence(HastExecutable):
    action: HastExecutable
    proposition: HastProposition


@dataclass(frozen=True, slots=True)
class HastFixedRecurrence(HastExecutable):
    count: int
    action: HastExecutable

    def __post_init__(self) -> None:
        if type(self.count) is not int or self.count < 0:
            raise ValueError("fixed recurrence count must be a Natural")


@dataclass(frozen=True, slots=True)
class HastPlaceIntroduction(HastPreparatory):
    place: PlaceId
    initial_fact: HastNumber


@dataclass(frozen=True, slots=True)
class HastActIntroduction(HastPreparatory):
    act: ActId


@dataclass(frozen=True, slots=True)
class HastRoleDeclaration(HastPreparatory):
    role: RoleId


@dataclass(frozen=True, slots=True)
class HastActBody(HastPreparatory):
    act: ActId
    body: HastExecutable


@dataclass(frozen=True, slots=True)
class HastCoreProgram(HastNode):
    preparation: tuple[HastPreparatory, ...]
    principal: HastExecutable
    places: tuple[PlaceId, ...]
    acts: tuple[ActId, ...]
    roles: tuple[RoleId, ...]


# ---- M3 historical fragment model retained for regression/constituent tools ----
@dataclass(frozen=True, slots=True)
class HastProgram:
    units: tuple[HastNode, ...]


@dataclass(frozen=True, slots=True)
class HastExactInteger(HastNode):
    value: int

    def __post_init__(self) -> None:
        if type(self.value) is not int:
            raise TypeError("HastExactInteger requires an exact integer")


@dataclass(frozen=True, slots=True)
class HastAddNumber(HastNode):
    left: HastNode
    right: HastNode


@dataclass(frozen=True, slots=True)
class HastSubtractNumber(HastNode):
    left: HastNode
    right: HastNode


@dataclass(frozen=True, slots=True)
class HastEqualNumberProposition(HastNode):
    left: HastNode
    right: HastNode


__all__ = [name for name in globals() if name.startswith("Hast")]
