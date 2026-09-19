"""Canonical validated IR for A13/B12 Core v0.1 integration candidate."""
from __future__ import annotations
from dataclasses import dataclass
from compiler.source.source_map import OriginalSpan

IR_VERSION = "core-ir-0.1-candidate-1"

@dataclass(frozen=True, slots=True)
class IRNode: source_span: OriginalSpan
@dataclass(frozen=True, slots=True)
class IRNumber(IRNode): pass
@dataclass(frozen=True, slots=True)
class IRProposition(IRNode): pass
@dataclass(frozen=True, slots=True)
class IRAction(IRNode): pass

@dataclass(frozen=True, slots=True)
class IRNatural(IRNumber):
    value:int
    def __post_init__(self):
        if type(self.value) is not int or self.value < 0: raise ValueError("negative Natural in canonical IR")
@dataclass(frozen=True, slots=True)
class IRReadCurrentFact(IRNumber): place:int
@dataclass(frozen=True, slots=True)
class IRReadRoleNumber(IRNumber): role:int
@dataclass(frozen=True, slots=True)
class IRRecentResult(IRNumber): act:int
@dataclass(frozen=True, slots=True)
class IRAddNatural(IRNumber): addend:IRNumber; augend:IRNumber
@dataclass(frozen=True, slots=True)
class IRCheckedSubtractNatural(IRNumber): amount:IRNumber; source:IRNumber; error_code:str="ARITHMETIC_DOMAIN_ERROR"
@dataclass(frozen=True, slots=True)
class IREqualProposition(IRProposition): left:IRNumber; right:IRNumber

@dataclass(frozen=True, slots=True)
class IRRoleAssociation(IRNode): role:int; value:IRNumber
@dataclass(frozen=True, slots=True)
class IRReplaceCurrentFact(IRAction): place:int; value:IRNumber
@dataclass(frozen=True, slots=True)
class IRPerformAct(IRAction): act:int; associations:tuple[IRRoleAssociation,...]=()
@dataclass(frozen=True, slots=True)
class IRProduceResult(IRAction): value:IRNumber
@dataclass(frozen=True, slots=True)
class IRThen(IRAction): actions:tuple[IRAction,...]
@dataclass(frozen=True, slots=True)
class IRConditional(IRAction): proposition:IRProposition; if_holds:IRAction; if_not:IRAction
@dataclass(frozen=True, slots=True)
class IRFixedRecurrence(IRAction): count:int; action:IRAction
@dataclass(frozen=True, slots=True)
class IRPostActionRecurrence(IRAction): action:IRAction; proposition:IRProposition

@dataclass(frozen=True, slots=True)
class IRInitialFact(IRNode): place:int; value:IRNumber
@dataclass(frozen=True, slots=True)
class IRActDefinition(IRNode): act:int; roles:tuple[int,...]; body:IRAction
@dataclass(frozen=True, slots=True)
class IRSymbol(IRNode): kind:str; serial:int; spelling:str; owner:int|None=None

@dataclass(frozen=True, slots=True)
class IRProgram:
    source_span:OriginalSpan
    ir_version:str
    symbols:tuple[IRSymbol,...]
    initial_facts:tuple[IRInitialFact,...]
    acts:tuple[IRActDefinition,...]
    principal:IRAction

__all__=[n for n in globals() if n.startswith("IR")]
