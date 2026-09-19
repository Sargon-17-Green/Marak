"""Independent reference evaluator for canonical validated Core IR.

Act recursion is executed with explicit continuations rather than Python call
recursion.  Those continuations are implementation-only and are not Marak
language stack frames.
"""
from __future__ import annotations

from dataclasses import dataclass

from compiler.models import ir as i
from compiler.version import IR_REFERENCE_VERSION

IMPLEMENTATION_RESOURCE_EXHAUSTION = "IMPLEMENTATION_RESOURCE_EXHAUSTION"
DEFAULT_MAX_ACTIVE_PERFORMANCES = None


@dataclass(frozen=True, slots=True)
class IRReferenceError:
    code: str
    phase: str
    detail: str = ""


@dataclass(frozen=True, slots=True)
class IRReferenceProduct:
    occurrence: int
    act: int
    value: int


@dataclass(frozen=True, slots=True)
class IRReferenceNormal:
    facts: tuple[tuple[int, int], ...]
    products: tuple[IRReferenceProduct, ...]
    place_names: tuple[tuple[int, str], ...] = ()
    act_names: tuple[tuple[int, str], ...] = ()


@dataclass(frozen=True, slots=True)
class IRReferenceErrorOutcome:
    facts: tuple[tuple[int, int], ...]
    error: IRReferenceError
    products: tuple[IRReferenceProduct, ...]
    place_names: tuple[tuple[int, str], ...] = ()
    act_names: tuple[tuple[int, str], ...] = ()


@dataclass(frozen=True, slots=True)
class IRReferenceDivergence:
    products: tuple[IRReferenceProduct, ...]
    harness_reason: str = "fuel-exhausted"
    place_names: tuple[tuple[int, str], ...] = ()
    act_names: tuple[tuple[int, str], ...] = ()


@dataclass(frozen=True, slots=True)
class IRReferenceResourceExhaustion:
    facts: tuple[tuple[int, int], ...]
    products: tuple[IRReferenceProduct, ...]
    category: str = IMPLEMENTATION_RESOURCE_EXHAUSTION
    detail: str = "implementation activation budget exhausted"
    place_names: tuple[tuple[int, str], ...] = ()
    act_names: tuple[tuple[int, str], ...] = ()


@dataclass(slots=True)
class _Occurrence:
    identity: int
    act: int
    roles: dict[int, int]
    output: int | None = None


@dataclass(frozen=True, slots=True)
class _Provenance:
    occurrence: int
    act: int
    output: int | None


@dataclass(frozen=True, slots=True)
class _NormalStep:
    facts: tuple[tuple[int, int], ...]
    provenance: _Provenance | None = None


@dataclass(frozen=True, slots=True)
class _ErrorStep:
    facts: tuple[tuple[int, int], ...]
    error: IRReferenceError


@dataclass(frozen=True, slots=True)
class _DivergenceStep:
    pass


@dataclass(frozen=True, slots=True)
class _ResourceStep:
    facts: tuple[tuple[int, int], ...]
    detail: str


@dataclass(frozen=True, slots=True)
class _ThenFrame:
    remaining: tuple[i.IRAction, ...]
    occurrence: _Occurrence | None


@dataclass(frozen=True, slots=True)
class _ClearFrame:
    pass


@dataclass(frozen=True, slots=True)
class _FixedFrame:
    remaining: int
    action: i.IRAction
    occurrence: _Occurrence | None


@dataclass(frozen=True, slots=True)
class _PostFrame:
    action: i.IRAction
    proposition: i.IRProposition
    occurrence: _Occurrence | None


@dataclass(frozen=True, slots=True)
class _PerformanceFrame:
    child: _Occurrence


class _TermFault(Exception):
    def __init__(self, code: str, detail: str = ""):
        super().__init__(code)
        self.code = code
        self.detail = detail


def _facts_dict(facts: tuple[tuple[int, int], ...]) -> dict[int, int]:
    return dict(facts)


def _freeze_facts(facts: dict[int, int]) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(facts.items()))


class IRReferenceEvaluator:
    def __init__(
        self,
        program: i.IRProgram,
        *,
        fuel: int | None = None,
        max_active_performances: int | None = DEFAULT_MAX_ACTIVE_PERFORMANCES,
    ):
        if program.ir_version != i.IR_VERSION:
            raise ValueError("unsupported IR version")
        self.program = program
        self.fuel = fuel
        self.max_active_performances = max_active_performances
        self.active_performances = 0
        self._next_occurrence = 1
        self._products: list[IRReferenceProduct] = []
        self._acts = {definition.act: definition for definition in program.acts}
        self._place_names = tuple(sorted((x.serial, x.spelling) for x in program.symbols if x.kind == "place"))
        self._act_names = tuple(sorted((x.serial, x.spelling) for x in program.symbols if x.kind == "act"))

    def _consume(self) -> bool:
        if self.fuel is None:
            return True
        if self.fuel <= 0:
            return False
        self.fuel -= 1
        return True

    def number(self, node: i.IRNumber, facts: tuple[tuple[int, int], ...], occurrence: _Occurrence | None, provenance: _Provenance | None) -> int:
        state = _facts_dict(facts)
        if isinstance(node, i.IRNatural):
            return node.value
        if isinstance(node, i.IRReadCurrentFact):
            try:
                return state[node.place]
            except KeyError as exc:
                raise _TermFault("INTERNAL_UNESTABLISHED_PLACE") from exc
        if isinstance(node, i.IRReadRoleNumber):
            if occurrence is None or node.role not in occurrence.roles:
                raise _TermFault("ROLE_VALUE_OUTSIDE_PERFORMANCE")
            return occurrence.roles[node.role]
        if isinstance(node, i.IRRecentResult):
            if provenance is None or provenance.act != node.act or provenance.output is None:
                raise _TermFault("RESULT_PROVENANCE_ERROR")
            return provenance.output
        if isinstance(node, i.IRAddNatural):
            return self.number(node.addend, facts, occurrence, provenance) + self.number(node.augend, facts, occurrence, provenance)
        if isinstance(node, i.IRCheckedSubtractNatural):
            amount = self.number(node.amount, facts, occurrence, provenance)
            source = self.number(node.source, facts, occurrence, provenance)
            if amount > source:
                raise _TermFault(node.error_code, f"{source}-{amount}")
            return source - amount
        raise _TermFault("INTERNAL_UNKNOWN_NUMBER")

    def holds(self, proposition: i.IRProposition, facts: tuple[tuple[int, int], ...], occurrence: _Occurrence | None, provenance: _Provenance | None) -> bool:
        if isinstance(proposition, i.IREqualProposition):
            return self.number(proposition.left, facts, occurrence, provenance) == self.number(proposition.right, facts, occurrence, provenance)
        raise _TermFault("INTERNAL_UNKNOWN_PROPOSITION")

    def action(self, action: i.IRAction, facts: tuple[tuple[int, int], ...], occurrence: _Occurrence | None = None, provenance: _Provenance | None = None):
        frames: list[object] = []
        current_action: i.IRAction | None = action
        current_facts = facts
        current_occ = occurrence
        current_prov = provenance
        step: _NormalStep | _ErrorStep | _DivergenceStep | _ResourceStep | None = None

        while True:
            if current_action is not None:
                if not self._consume():
                    step = _DivergenceStep(); current_action = None; continue
                a = current_action
                if isinstance(a, i.IRReplaceCurrentFact):
                    try:
                        value = self.number(a.value, current_facts, current_occ, current_prov)
                    except _TermFault as exc:
                        step = _ErrorStep(current_facts, IRReferenceError(exc.code, "EXECUTION", exc.detail)); current_action=None; continue
                    state = _facts_dict(current_facts)
                    if a.place not in state:
                        step = _ErrorStep(current_facts, IRReferenceError("INTERNAL_UNESTABLISHED_PLACE", "EXECUTION")); current_action=None; continue
                    state[a.place] = value
                    step = _NormalStep(_freeze_facts(state), None); current_action=None; continue

                if isinstance(a, i.IRThen):
                    frames.append(_ThenFrame(tuple(a.actions[1:]), current_occ))
                    current_action = a.actions[0]
                    continue

                if isinstance(a, i.IRConditional):
                    try:
                        selected = a.if_holds if self.holds(a.proposition, current_facts, current_occ, current_prov) else a.if_not
                    except _TermFault as exc:
                        step = _ErrorStep(current_facts, IRReferenceError(exc.code, "EXECUTION", exc.detail)); current_action=None; continue
                    frames.append(_ClearFrame()); current_action=selected; continue

                if isinstance(a, i.IRFixedRecurrence):
                    frames.append(_FixedFrame(a.count-1, a.action, current_occ))
                    current_action=a.action; current_prov=None; continue

                if isinstance(a, i.IRPostActionRecurrence):
                    frames.append(_PostFrame(a.action, a.proposition, current_occ))
                    current_action=a.action; current_prov=None; continue

                if isinstance(a, i.IRPerformAct):
                    try:
                        role_values={assoc.role:self.number(assoc.value,current_facts,current_occ,current_prov) for assoc in a.associations}
                    except _TermFault as exc:
                        step=_ErrorStep(current_facts,IRReferenceError(exc.code,"EXECUTION",exc.detail)); current_action=None; continue
                    definition=self._acts.get(a.act)
                    if definition is None:
                        step=_ErrorStep(current_facts,IRReferenceError("INTERNAL_UNRESOLVED_ACT","EXECUTION")); current_action=None; continue
                    if self.max_active_performances is not None and self.active_performances >= self.max_active_performances:
                        step=_ResourceStep(current_facts,f"caller-imposed active performance budget {self.max_active_performances} exhausted"); current_action=None; continue
                    child=_Occurrence(self._next_occurrence,a.act,role_values); self._next_occurrence += 1
                    self.active_performances += 1
                    frames.append(_PerformanceFrame(child))
                    current_action=definition.body; current_occ=child; current_prov=None; continue

                if isinstance(a, i.IRProduceResult):
                    if current_occ is None:
                        step=_ErrorStep(current_facts,IRReferenceError("OUTPUT_OUTSIDE_PERFORMANCE","EXECUTION")); current_action=None; continue
                    try:
                        value=self.number(a.value,current_facts,current_occ,current_prov)
                    except _TermFault as exc:
                        step=_ErrorStep(current_facts,IRReferenceError(exc.code,"EXECUTION",exc.detail)); current_action=None; continue
                    if current_occ.output is not None:
                        step=_ErrorStep(current_facts,IRReferenceError("CORE_OUTPUT_CARDINALITY_ERROR","EXECUTION"))
                    else:
                        current_occ.output=value
                        self._products.append(IRReferenceProduct(current_occ.identity,current_occ.act,value))
                        step=_NormalStep(current_facts,None)
                    current_action=None; continue

                step=_ErrorStep(current_facts,IRReferenceError("INTERNAL_UNKNOWN_ACTION","EXECUTION")); current_action=None; continue

            assert step is not None
            if not isinstance(step,_NormalStep):
                return step
            if not frames:
                return step
            frame=frames.pop(); current_facts=step.facts
            if isinstance(frame,_ThenFrame):
                if frame.remaining:
                    current_occ=frame.occurrence; current_prov=step.provenance
                    current_action=frame.remaining[0]
                    frames.append(_ThenFrame(frame.remaining[1:],frame.occurrence)); step=None; continue
                continue
            if isinstance(frame,_ClearFrame):
                step=_NormalStep(current_facts,None); continue
            if isinstance(frame,_FixedFrame):
                if frame.remaining>0:
                    current_occ=frame.occurrence; current_prov=None; current_action=frame.action
                    frames.append(_FixedFrame(frame.remaining-1,frame.action,frame.occurrence)); step=None; continue
                step=_NormalStep(current_facts,None); continue
            if isinstance(frame,_PostFrame):
                try:
                    stop=self.holds(frame.proposition,current_facts,frame.occurrence,step.provenance)
                except _TermFault as exc:
                    step=_ErrorStep(current_facts,IRReferenceError(exc.code,"EXECUTION",exc.detail)); continue
                if stop:
                    step=_NormalStep(current_facts,None); continue
                current_occ=frame.occurrence; current_prov=None; current_action=frame.action; frames.append(frame); step=None; continue
            if isinstance(frame,_PerformanceFrame):
                self.active_performances -= 1
                child=frame.child
                step=_NormalStep(current_facts,_Provenance(child.identity,child.act,child.output)); continue
            return _ErrorStep(current_facts,IRReferenceError("INTERNAL_UNKNOWN_CONTINUATION","EXECUTION"))

    def prepare(self) -> _NormalStep | _ErrorStep:
        facts: tuple[tuple[int, int], ...] = ()
        for initial in self.program.initial_facts:
            try:
                value = self.number(initial.value, facts, None, None)
            except _TermFault as exc:
                return _ErrorStep(facts, IRReferenceError(exc.code, "PREPARATION", exc.detail))
            state = _facts_dict(facts)
            if initial.place in state:
                return _ErrorStep(facts, IRReferenceError("INTERNAL_DUPLICATE_INITIAL_FACT", "PREPARATION"))
            state[initial.place] = value
            facts = _freeze_facts(state)
        return _NormalStep(facts, None)

    def run(self):
        try:
            prepared=self.prepare()
            if isinstance(prepared,_ErrorStep):
                return IRReferenceErrorOutcome(prepared.facts,prepared.error,tuple(self._products),self._place_names,self._act_names)
            step=self.action(self.program.principal,prepared.facts,None,None)
            if isinstance(step,_NormalStep):
                return IRReferenceNormal(step.facts,tuple(self._products),self._place_names,self._act_names)
            if isinstance(step,_ErrorStep):
                return IRReferenceErrorOutcome(step.facts,step.error,tuple(self._products),self._place_names,self._act_names)
            if isinstance(step,_ResourceStep):
                return IRReferenceResourceExhaustion(step.facts,tuple(self._products),detail=step.detail,place_names=self._place_names,act_names=self._act_names)
            return IRReferenceDivergence(tuple(self._products),"fuel-exhausted",self._place_names,self._act_names)
        except (MemoryError,RecursionError) as exc:
            return IRReferenceResourceExhaustion((),tuple(self._products),detail=type(exc).__name__,place_names=self._place_names,act_names=self._act_names)


def execute_reference_ir(program:i.IRProgram,*,fuel:int|None=None,max_active_performances:int|None=DEFAULT_MAX_ACTIVE_PERFORMANCES):
    return IRReferenceEvaluator(program,fuel=fuel,max_active_performances=max_active_performances).run()


__all__=[
    "IR_REFERENCE_VERSION","IMPLEMENTATION_RESOURCE_EXHAUSTION","DEFAULT_MAX_ACTIVE_PERFORMANCES",
    "IRReferenceError","IRReferenceProduct","IRReferenceNormal","IRReferenceErrorOutcome",
    "IRReferenceDivergence","IRReferenceResourceExhaustion","IRReferenceEvaluator","execute_reference_ir",
]
