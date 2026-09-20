"""Canonical HAST for the frozen Core plus Post-M2 typed-domain infrastructure."""
from __future__ import annotations

from dataclasses import dataclass

from compiler.models.domains import (
    BIDIRECTIONAL_INDEX, NATURAL, CollectionDomain, Domain, ProgramInputId,
    SymbolDomain, SymbolDomainId, SymbolMemberId,
)
from compiler.models.symbols import ActId, PlaceId, RoleId
from compiler.source.source_map import OriginalSpan

HAST_VERSION = "core-hast-0.2-candidate-1"


@dataclass(frozen=True, slots=True)
class HastNode:
    source_span: OriginalSpan


@dataclass(frozen=True, slots=True)
class HastValue(HastNode):
    pass


@dataclass(frozen=True, slots=True)
class HastNumber(HastValue):
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
class HastSymbolValue(HastValue):
    domain_id: SymbolDomainId
    member_id: SymbolMemberId
    external_label: str


@dataclass(frozen=True, slots=True)
class HastIndexValue(HastValue):
    side: str
    magnitude: int = 0
    def __post_init__(self) -> None:
        if self.side not in {"before", "zero", "after"}:
            raise ValueError("index side must be before/zero/after")
        if type(self.magnitude) is not int or self.magnitude < 0:
            raise ValueError("index magnitude must be a Natural")
        if (self.side == "zero") != (self.magnitude == 0):
            raise ValueError("zero index alone has magnitude zero")


@dataclass(frozen=True, slots=True)
class HastCollectionValue(HastValue):
    element_domain: Domain
    items: tuple[HastValue, ...]


@dataclass(frozen=True, slots=True)
class HastCurrentFact(HastNumber):
    place: PlaceId


@dataclass(frozen=True, slots=True)
class HastCurrentValue(HastValue):
    place: PlaceId
    domain: Domain


@dataclass(frozen=True, slots=True)
class HastCurrentRoleNumber(HastNumber):
    role: RoleId


@dataclass(frozen=True, slots=True)
class HastCurrentRoleValue(HastValue):
    role: RoleId
    domain: Domain


@dataclass(frozen=True, slots=True)
class HastRecentResult(HastNumber):
    act: ActId


@dataclass(frozen=True, slots=True)
class HastRecentTypedResult(HastValue):
    act: ActId
    domain: Domain


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
    value: HastValue


@dataclass(frozen=True, slots=True)
class HastReplaceCurrentFact(HastExecutable):
    place: PlaceId
    value: HastValue


@dataclass(frozen=True, slots=True)
class HastPerformAct(HastExecutable):
    act: ActId
    associations: tuple[HastRoleAssociation, ...] = ()


@dataclass(frozen=True, slots=True)
class HastProduceResult(HastExecutable):
    value: HastValue


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
    initial_fact: HastValue


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
class HastPlaceDomain:
    place: PlaceId
    domain: Domain


@dataclass(frozen=True, slots=True)
class HastRoleDomain:
    role: RoleId
    domain: Domain


@dataclass(frozen=True, slots=True)
class HastActOutputDomain:
    act: ActId
    domain: Domain | None


@dataclass(frozen=True, slots=True)
class HastProgramInputDomain:
    input_id: ProgramInputId
    domain: Domain


@dataclass(frozen=True, slots=True)
class HastCoreProgram(HastNode):
    preparation: tuple[HastPreparatory, ...]
    principal: HastExecutable
    places: tuple[PlaceId, ...]
    acts: tuple[ActId, ...]
    roles: tuple[RoleId, ...]
    place_domains: tuple[HastPlaceDomain, ...] = ()
    role_domains: tuple[HastRoleDomain, ...] = ()
    act_output_domains: tuple[HastActOutputDomain, ...] = ()
    program_input_domains: tuple[HastProgramInputDomain, ...] = ()


# Historical fragment model retained for regression/constituent tools.
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
