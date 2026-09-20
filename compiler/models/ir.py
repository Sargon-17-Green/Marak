"""Canonical validated IR with explicit semantic-domain contracts."""
from __future__ import annotations

from dataclasses import dataclass

from compiler.models.domains import Domain, ProgramInputId, SymbolDomainId, SymbolMemberId
from compiler.source.source_map import OriginalSpan

IR_VERSION = "core-ir-0.2-candidate-1"


@dataclass(frozen=True, slots=True)
class IRNode:
    source_span: OriginalSpan


@dataclass(frozen=True, slots=True)
class IRValue(IRNode):
    pass


@dataclass(frozen=True, slots=True)
class IRNumber(IRValue):
    pass


@dataclass(frozen=True, slots=True)
class IRProposition(IRNode):
    pass


@dataclass(frozen=True, slots=True)
class IRAction(IRNode):
    pass


@dataclass(frozen=True, slots=True)
class IRNatural(IRNumber):
    value: int
    def __post_init__(self) -> None:
        if type(self.value) is not int or self.value < 0:
            raise ValueError("negative Natural in canonical IR")


@dataclass(frozen=True, slots=True)
class IRSymbolValue(IRValue):
    domain_id: SymbolDomainId
    member_id: SymbolMemberId
    external_label: str


@dataclass(frozen=True, slots=True)
class IRIndexValue(IRValue):
    side: str
    magnitude: int = 0


@dataclass(frozen=True, slots=True)
class IRCollectionValue(IRValue):
    element_domain: Domain
    items: tuple[IRValue, ...]


@dataclass(frozen=True, slots=True)
class IRReadCurrentFact(IRNumber):
    place: int


@dataclass(frozen=True, slots=True)
class IRReadCurrentValue(IRValue):
    place: int
    domain: Domain


@dataclass(frozen=True, slots=True)
class IRReadRoleNumber(IRNumber):
    role: int


@dataclass(frozen=True, slots=True)
class IRReadRoleValue(IRValue):
    role: int
    domain: Domain


@dataclass(frozen=True, slots=True)
class IRRecentResult(IRNumber):
    act: int


@dataclass(frozen=True, slots=True)
class IRRecentTypedResult(IRValue):
    act: int
    domain: Domain


@dataclass(frozen=True, slots=True)
class IRAddNatural(IRNumber):
    addend: IRNumber
    augend: IRNumber


@dataclass(frozen=True, slots=True)
class IRCheckedSubtractNatural(IRNumber):
    amount: IRNumber
    source: IRNumber
    error_code: str = "ARITHMETIC_DOMAIN_ERROR"


@dataclass(frozen=True, slots=True)
class IREqualProposition(IRProposition):
    left: IRNumber
    right: IRNumber


@dataclass(frozen=True, slots=True)
class IRRoleAssociation(IRNode):
    role: int
    value: IRValue


@dataclass(frozen=True, slots=True)
class IRReplaceCurrentFact(IRAction):
    place: int
    value: IRValue


@dataclass(frozen=True, slots=True)
class IRPerformAct(IRAction):
    act: int
    associations: tuple[IRRoleAssociation, ...] = ()


@dataclass(frozen=True, slots=True)
class IRProduceResult(IRAction):
    value: IRValue


@dataclass(frozen=True, slots=True)
class IRThen(IRAction):
    actions: tuple[IRAction, ...]


@dataclass(frozen=True, slots=True)
class IRConditional(IRAction):
    proposition: IRProposition
    if_holds: IRAction
    if_not: IRAction


@dataclass(frozen=True, slots=True)
class IRFixedRecurrence(IRAction):
    count: int
    action: IRAction


@dataclass(frozen=True, slots=True)
class IRPostActionRecurrence(IRAction):
    action: IRAction
    proposition: IRProposition


@dataclass(frozen=True, slots=True)
class IRInitialFact(IRNode):
    place: int
    value: IRValue


@dataclass(frozen=True, slots=True)
class IRActDefinition(IRNode):
    act: int
    roles: tuple[int, ...]
    body: IRAction


@dataclass(frozen=True, slots=True)
class IRSymbol(IRNode):
    kind: str
    serial: int
    spelling: str
    owner: int | None = None


@dataclass(frozen=True, slots=True)
class IRPlaceDomain(IRNode):
    place: int
    domain: Domain


@dataclass(frozen=True, slots=True)
class IRRoleDomain(IRNode):
    role: int
    domain: Domain


@dataclass(frozen=True, slots=True)
class IRActOutputDomain(IRNode):
    act: int
    domain: Domain | None


@dataclass(frozen=True, slots=True)
class IRProgramInputDomain(IRNode):
    input_id: ProgramInputId
    domain: Domain


@dataclass(frozen=True, slots=True)
class IRProgram:
    source_span: OriginalSpan
    ir_version: str
    symbols: tuple[IRSymbol, ...]
    initial_facts: tuple[IRInitialFact, ...]
    acts: tuple[IRActDefinition, ...]
    principal: IRAction
    place_domains: tuple[IRPlaceDomain, ...] = ()
    role_domains: tuple[IRRoleDomain, ...] = ()
    act_output_domains: tuple[IRActOutputDomain, ...] = ()
    program_input_domains: tuple[IRProgramInputDomain, ...] = ()


__all__ = [n for n in globals() if n.startswith("IR")]
