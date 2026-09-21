from __future__ import annotations

from dataclasses import dataclass

from compiler.models.hast import (
    HastActBody, HastAddNatural, HastConditional, HastCoreProgram, HastCurrentFact,
    HastCurrentRoleNumber, HastEqualProposition, HastExactNatural, HastExecutable,
    HastFixedRecurrence, HastRepeatExactly, HastNumber, HastValue, HastSymbolValue, HastIndexValue, HastCollectionValue, HastCurrentValue, HastCurrentRoleValue, HastRecentTypedResult, HastIndexSuccessor, HastIndexPredecessor, HastNaturalGTProposition, HastIndexLTProposition, HastSymbolEqualProposition, HastPerformAct, HastPlaceIntroduction,
    HastPostActionRecurrence, HastProduceResult, HastProposition, HastRecentResult,
    HastReplaceCurrentFact, HastSubtractNatural, HastThen,
    HastCollectionAppend, HastCollectionCount, HastCollectionSelectNatural,
    HastCollectionSelectValue, HastCollectionOrder, HastCollectionMembershipProposition,
    HastSymbolMemberDeclaration, HastSymbolOrderAdjacent,
    HastProgramInputNumber, HastProgramInputValue,
)
from compiler.models.symbols import ActId, OccurrenceId, PlaceId, RoleId
from compiler.models.domains import NATURAL, CollectionDomain, Domain
from compiler.models.values import SymbolValue, BidirectionalIndexValue, CollectionValue, NaturalValue, index_successor, index_predecessor, index_lt, symbol_identity_equal, semantic_value_equal, value_domain
from compiler.runtime.invocation import InputBinding, InvalidInvocation, ValidatedInvocation, prepare_invocation, runtime_input_values

ARITHMETIC_DOMAIN_ERROR = "ARITHMETIC_DOMAIN_ERROR"
RESULT_PROVENANCE_ERROR = "RESULT_PROVENANCE_ERROR"
CORE_OUTPUT_CARDINALITY_ERROR = "CORE_OUTPUT_CARDINALITY_ERROR"
ROLE_VALUE_OUTSIDE_PERFORMANCE = "ROLE_VALUE_OUTSIDE_PERFORMANCE"
COLLECTION_POSITION_ERROR = "COLLECTION_POSITION_ERROR"
ORDER_RELATION_ERROR = "ORDER_RELATION_ERROR"
RECURRENCE_COUNT_DOMAIN_ERROR = "RECURRENCE_COUNT_DOMAIN_ERROR"
IMPLEMENTATION_RESOURCE_EXHAUSTION = "IMPLEMENTATION_RESOURCE_EXHAUSTION"
DEFAULT_MAX_ACTIVE_PERFORMANCES = None


@dataclass(frozen=True, slots=True)
class RuntimeErrorRecord:
    code: str
    phase: str
    detail: str = ""


@dataclass(frozen=True, slots=True)
class SemanticState:
    facts: tuple[tuple[PlaceId, object], ...] = ()

    def as_dict(self) -> dict[PlaceId, object]:
        return dict(self.facts)

    def read(self, place: PlaceId) -> object:
        return self.as_dict()[place]

    def establish(self, place: PlaceId, value: object) -> "SemanticState":
        d = self.as_dict()
        if place in d:
            raise RuntimeError("internal duplicate initial establishment")
        d[place] = value
        return SemanticState(tuple(sorted(d.items(), key=lambda kv: kv[0].serial)))

    def replace(self, place: PlaceId, value: object) -> "SemanticState":
        d = self.as_dict()
        if place not in d:
            raise RuntimeError("internal unresolved place reached runtime")
        d[place] = value
        return SemanticState(tuple(sorted(d.items(), key=lambda kv: kv[0].serial)))


@dataclass(frozen=True, slots=True)
class Product:
    occurrence: OccurrenceId
    act: ActId
    value: object


@dataclass(frozen=True, slots=True)
class NormalOutcome:
    state: SemanticState
    products: tuple[Product, ...]


@dataclass(frozen=True, slots=True)
class ErrorOutcome:
    state: SemanticState
    error: RuntimeErrorRecord
    products: tuple[Product, ...]


@dataclass(frozen=True, slots=True)
class DivergenceOutcome:
    products: tuple[Product, ...]
    harness_reason: str = "fuel-exhausted"


@dataclass(frozen=True, slots=True)
class ResourceExhaustionOutcome:
    state: SemanticState
    products: tuple[Product, ...]
    category: str = IMPLEMENTATION_RESOURCE_EXHAUSTION
    detail: str = "implementation activation budget exhausted"


Outcome = NormalOutcome | ErrorOutcome | DivergenceOutcome | ResourceExhaustionOutcome


@dataclass(slots=True)
class _Occurrence:
    identity: OccurrenceId
    act: ActId
    roles: dict[RoleId, object]
    output: object | None = None


@dataclass(frozen=True, slots=True)
class _Provenance:
    occurrence: OccurrenceId
    act: ActId
    output: object | None


@dataclass(frozen=True, slots=True)
class _StepNormal:
    state: SemanticState
    provenance: _Provenance | None = None


@dataclass(frozen=True, slots=True)
class _StepError:
    state: SemanticState
    error: RuntimeErrorRecord


@dataclass(frozen=True, slots=True)
class _StepDivergence:
    pass


@dataclass(frozen=True, slots=True)
class _StepResource:
    state: SemanticState
    detail: str


@dataclass(frozen=True, slots=True)
class _ThenFrame:
    remaining: tuple[HastExecutable, ...]
    occurrence: _Occurrence | None


@dataclass(frozen=True, slots=True)
class _ClearProvenanceFrame:
    pass


@dataclass(frozen=True, slots=True)
class _FixedFrame:
    remaining: int
    action: HastExecutable
    occurrence: _Occurrence | None


@dataclass(frozen=True, slots=True)
class _RepeatExactlyFrame:
    remaining: int
    action: HastExecutable
    occurrence: _Occurrence | None


@dataclass(frozen=True, slots=True)
class _PostFrame:
    action: HastExecutable
    proposition: HastProposition
    occurrence: _Occurrence | None


@dataclass(frozen=True, slots=True)
class _PerformanceFrame:
    child: _Occurrence


class _TermFault(Exception):
    def __init__(self, code: str, detail: str = ""):
        super().__init__(code)
        self.code = code
        self.detail = detail


class ReferenceEvaluator:
    """HAST semantic reference evaluator using explicit continuations.

    ``_Occurrence`` and continuation frames are implementation machinery only;
    they do not establish a user-visible Marak call-stack ontology.
    """

    def __init__(
        self,
        program: HastCoreProgram,
        *,
        fuel: int | None = None,
        debug_trace: bool = False,
        max_active_performances: int | None = DEFAULT_MAX_ACTIVE_PERFORMANCES,
        invocation: ValidatedInvocation | None = None,
    ):
        self.program = program
        self.input_values = runtime_input_values(invocation or ValidatedInvocation(()))
        self.fuel = fuel
        self.debug_trace_enabled = debug_trace
        self.trace: list[tuple] = []
        self.products: list[Product] = []
        self.next_occurrence = 1
        self.max_active_performances = max_active_performances
        self.active_performances = 0
        self.body_by_act = {p.act: p.body for p in program.preparation if isinstance(p, HastActBody)}
        self.roles_by_act: dict[ActId, tuple[RoleId, ...]] = {}
        for role in program.roles:
            self.roles_by_act.setdefault(role.owner, tuple())
        for act in program.acts:
            self.roles_by_act[act] = tuple(sorted((r for r in program.roles if r.owner == act), key=lambda r: r.serial))
        self.symbol_order_rank = {}
        members_by_domain = {}
        edges_by_domain = {}
        for unit in program.preparation:
            if isinstance(unit,HastSymbolMemberDeclaration):
                members_by_domain.setdefault(unit.domain_id,set()).add(unit.member_id)
            elif isinstance(unit,HastSymbolOrderAdjacent):
                edges_by_domain.setdefault(unit.domain_id,{})[unit.before_member_id]=unit.after_member_id
        for domain_id,members in members_by_domain.items():
            if not members:
                continue
            outgoing=edges_by_domain.get(domain_id,{})
            incoming=set(outgoing.values())
            starts=[m for m in members if m not in incoming]
            if len(starts)==1:
                rank={}; cur=starts[0]
                while cur not in rank:
                    rank[cur]=len(rank)
                    if cur not in outgoing:
                        break
                    cur=outgoing[cur]
                if set(rank)==members:
                    self.symbol_order_rank[domain_id]=rank

    def _event(self, *parts) -> None:
        if self.debug_trace_enabled:
            self.trace.append(tuple(parts))

    def _consume(self) -> bool:
        if self.fuel is None:
            return True
        if self.fuel <= 0:
            return False
        self.fuel -= 1
        return True

    def _semantic_item(self, value: object, domain: Domain):
        if domain == NATURAL:
            if type(value) is not int:
                raise _TermFault("INTERNAL_DOMAIN_GUARD")
            return NaturalValue(value)
        if not isinstance(value,(SymbolValue,BidirectionalIndexValue,CollectionValue)) or value_domain(value)!=domain:
            raise _TermFault("INTERNAL_DOMAIN_GUARD")
        return value

    def _selected_runtime_value(self, item):
        return item.value if isinstance(item,NaturalValue) else item

    def _select_collection(self, collection: CollectionValue, mode: str, position: int | None):
        if mode=="first":
            k=1
        elif mode=="last":
            k=len(collection.items)
        elif mode=="ordinal":
            if position is None:
                raise _TermFault("INTERNAL_DOMAIN_GUARD")
            k=position
        else:
            raise _TermFault("INTERNAL_DOMAIN_GUARD")
        if k<1 or k>len(collection.items):
            raise _TermFault(COLLECTION_POSITION_ERROR,f"position={k}, count={len(collection.items)}")
        return self._selected_runtime_value(collection.items[k-1])

    def _order_collection(self, collection: CollectionValue, kind: str, symbol_domain_id):
        try:
            if kind=="natural":
                return CollectionValue(collection.element_domain,tuple(sorted(collection.items,key=lambda x:x.value)))
            if kind=="symbol":
                rank=self.symbol_order_rank[symbol_domain_id]
                return CollectionValue(collection.element_domain,tuple(sorted(collection.items,key=lambda x:rank[x.member_id])))
            if kind=="lex-natural":
                return CollectionValue(collection.element_domain,tuple(sorted(collection.items,key=lambda x:tuple(v.value for v in x.items))))
            if kind=="lex-symbol":
                rank=self.symbol_order_rank[symbol_domain_id]
                return CollectionValue(collection.element_domain,tuple(sorted(collection.items,key=lambda x:tuple(rank[v.member_id] for v in x.items))))
        except (KeyError,AttributeError,TypeError):
            raise _TermFault(ORDER_RELATION_ERROR)
        raise _TermFault(ORDER_RELATION_ERROR)

    def eval_value(self, node: HastValue, state: SemanticState, occ: _Occurrence | None, prov: _Provenance | None) -> object:
        if isinstance(node, HastSymbolValue):
            return SymbolValue(node.domain_id, node.member_id, node.external_label)
        if isinstance(node, HastIndexValue):
            return BidirectionalIndexValue(node.side, node.magnitude)
        if isinstance(node, HastIndexSuccessor):
            operand=self.eval_value(node.operand,state,occ,prov)
            if not isinstance(operand,BidirectionalIndexValue): raise _TermFault("INTERNAL_DOMAIN_GUARD")
            return index_successor(operand)
        if isinstance(node, HastIndexPredecessor):
            operand=self.eval_value(node.operand,state,occ,prov)
            if not isinstance(operand,BidirectionalIndexValue): raise _TermFault("INTERNAL_DOMAIN_GUARD")
            return index_predecessor(operand)
        if isinstance(node, HastCollectionValue):
            items=[]
            for child in node.items:
                v=self.eval_value(child,state,occ,prov)
                if node.element_domain == NATURAL:
                    if type(v) is not int:
                        raise _TermFault("INTERNAL_DOMAIN_GUARD", "validated Natural collection element produced a non-Natural value")
                    items.append(NaturalValue(v))
                else:
                    items.append(v)
            return CollectionValue(node.element_domain,tuple(items))
        if isinstance(node,HastCollectionAppend):
            # Collapse a left-associated pure append chain so immutable tuple
            # materialization is linear rather than repeatedly copying every prefix.
            chain=[]
            current=node
            while isinstance(current,HastCollectionAppend):
                chain.append(current)
                current=current.collection
            collection=self.eval_value(current,state,occ,prov)
            if not isinstance(collection,CollectionValue):
                raise _TermFault("INTERNAL_DOMAIN_GUARD")
            items=list(collection.items)
            for append in reversed(chain):
                if collection.element_domain!=append.element_domain:
                    raise _TermFault("INTERNAL_DOMAIN_GUARD")
                items.append(self._semantic_item(self.eval_value(append.item,state,occ,prov),append.element_domain))
            return CollectionValue(node.element_domain,tuple(items))
        if isinstance(node,HastCollectionCount):
            collection=self.eval_value(node.collection,state,occ,prov)
            if not isinstance(collection,CollectionValue):
                raise _TermFault("INTERNAL_DOMAIN_GUARD")
            return len(collection.items)
        if isinstance(node,HastCollectionSelectNatural):
            collection=self.eval_value(node.collection,state,occ,prov)
            if not isinstance(collection,CollectionValue):
                raise _TermFault("INTERNAL_DOMAIN_GUARD")
            pos=None if node.position is None else self.eval_number(node.position,state,occ,prov)
            selected=self._select_collection(collection,node.mode,pos)
            if type(selected) is not int:
                raise _TermFault("INTERNAL_DOMAIN_GUARD")
            return selected
        if isinstance(node,HastCollectionSelectValue):
            collection=self.eval_value(node.collection,state,occ,prov)
            if not isinstance(collection,CollectionValue):
                raise _TermFault("INTERNAL_DOMAIN_GUARD")
            pos=None if node.position is None else self.eval_number(node.position,state,occ,prov)
            return self._select_collection(collection,node.mode,pos)
        if isinstance(node,HastCollectionOrder):
            collection=self.eval_value(node.collection,state,occ,prov)
            if not isinstance(collection,CollectionValue):
                raise _TermFault("INTERNAL_DOMAIN_GUARD")
            return self._order_collection(collection,node.order_kind,node.symbol_domain_id)
        if isinstance(node, HastProgramInputValue):
            try:
                return self.input_values[node.input_id]
            except KeyError:
                raise _TermFault("INTERNAL_INVOCATION_GUARD")
        if isinstance(node, HastCurrentValue):
            return state.read(node.place)
        if isinstance(node, HastCurrentRoleValue):
            if occ is None or node.role not in occ.roles:
                raise _TermFault(ROLE_VALUE_OUTSIDE_PERFORMANCE)
            return occ.roles[node.role]
        if isinstance(node, HastRecentTypedResult):
            if prov is None or prov.act != node.act or prov.output is None:
                raise _TermFault(RESULT_PROVENANCE_ERROR)
            return prov.output
        if isinstance(node, HastNumber):
            return self.eval_number(node,state,occ,prov)
        raise _TermFault("INTERNAL_UNKNOWN_VALUE")

    def eval_number(self, node: HastNumber, state: SemanticState, occ: _Occurrence | None, prov: _Provenance | None) -> int:
        if isinstance(node,(HastCollectionCount,HastCollectionSelectNatural)):
            value=self.eval_value(node,state,occ,prov)
            if type(value) is not int:
                raise _TermFault("INTERNAL_DOMAIN_GUARD")
            return value
        if isinstance(node, HastExactNatural):
            return node.value
        if isinstance(node, HastProgramInputNumber):
            try:
                value = self.input_values[node.input_id]
            except KeyError:
                raise _TermFault("INTERNAL_INVOCATION_GUARD")
            if type(value) is not int:
                raise _TermFault("INTERNAL_DOMAIN_GUARD")
            return value
        if isinstance(node, HastCurrentFact):
            return state.read(node.place)
        if isinstance(node, HastCurrentRoleNumber):
            if occ is None or node.role not in occ.roles:
                raise _TermFault(ROLE_VALUE_OUTSIDE_PERFORMANCE)
            return occ.roles[node.role]
        if isinstance(node, HastRecentResult):
            if prov is None or prov.act != node.act or prov.output is None:
                raise _TermFault(RESULT_PROVENANCE_ERROR)
            return prov.output
        if isinstance(node, HastAddNatural):
            return self.eval_number(node.addend, state, occ, prov) + self.eval_number(node.augend, state, occ, prov)
        if isinstance(node, HastSubtractNatural):
            amount = self.eval_number(node.amount, state, occ, prov)
            source = self.eval_number(node.source, state, occ, prov)
            if amount > source:
                raise _TermFault(ARITHMETIC_DOMAIN_ERROR, f"{source}-{amount}")
            return source - amount
        raise _TermFault("INTERNAL_UNKNOWN_NUMBER")

    def holds(self, proposition: HastProposition, state: SemanticState, occ: _Occurrence | None, prov: _Provenance | None) -> bool:
        if isinstance(proposition, HastEqualProposition):
            return self.eval_number(proposition.left, state, occ, prov) == self.eval_number(proposition.right, state, occ, prov)
        if isinstance(proposition,HastNaturalGTProposition):
            return self.eval_number(proposition.left,state,occ,prov) > self.eval_number(proposition.right,state,occ,prov)
        if isinstance(proposition,HastIndexLTProposition):
            left=self.eval_value(proposition.left,state,occ,prov)
            right=self.eval_value(proposition.right,state,occ,prov)
            if not isinstance(left,BidirectionalIndexValue) or not isinstance(right,BidirectionalIndexValue):
                raise _TermFault("INTERNAL_DOMAIN_GUARD")
            return index_lt(left,right)
        if isinstance(proposition,HastSymbolEqualProposition):
            left=self.eval_value(proposition.left,state,occ,prov); right=self.eval_value(proposition.right,state,occ,prov)
            if not isinstance(left,SymbolValue) or not isinstance(right,SymbolValue): raise _TermFault("INTERNAL_DOMAIN_GUARD")
            return symbol_identity_equal(left,right)
        if isinstance(proposition,HastCollectionMembershipProposition):
            collection=self.eval_value(proposition.collection,state,occ,prov)
            if not isinstance(collection,CollectionValue):
                raise _TermFault("INTERNAL_DOMAIN_GUARD")
            item=self._semantic_item(self.eval_value(proposition.item,state,occ,prov),proposition.element_domain)
            return any(semantic_value_equal(item,x) for x in collection.items)
        raise _TermFault("INTERNAL_UNKNOWN_PROPOSITION")

    def execute(self, action: HastExecutable, state: SemanticState, occ: _Occurrence | None = None, prov: _Provenance | None = None):
        frames: list[object] = []
        current_action: HastExecutable | None = action
        current_state = state
        current_occ = occ
        current_prov = prov
        step: _StepNormal | _StepError | _StepDivergence | _StepResource | None = None

        while True:
            if current_action is not None:
                if not self._consume():
                    step = _StepDivergence()
                    current_action = None
                    continue
                self._event("execute", type(current_action).__name__)
                a = current_action

                if isinstance(a, HastReplaceCurrentFact):
                    try:
                        value = self.eval_value(a.value, current_state, current_occ, current_prov)
                        step = _StepNormal(current_state.replace(a.place, value), None)
                    except _TermFault as e:
                        step = _StepError(current_state, RuntimeErrorRecord(e.code, "EXECUTION", e.detail))
                    current_action = None
                    continue

                if isinstance(a, HastThen):
                    frames.append(_ThenFrame(tuple(a.actions[1:]), current_occ))
                    current_action = a.actions[0]
                    continue

                if isinstance(a, HastConditional):
                    try:
                        selected = a.if_holds if self.holds(a.proposition, current_state, current_occ, current_prov) else a.if_not
                    except _TermFault as e:
                        step = _StepError(current_state, RuntimeErrorRecord(e.code, "EXECUTION", e.detail))
                        current_action = None
                        continue
                    frames.append(_ClearProvenanceFrame())
                    current_action = selected
                    continue

                if isinstance(a, HastFixedRecurrence):
                    frames.append(_FixedFrame(a.count - 1, a.action, current_occ))
                    current_action = a.action
                    current_prov = None
                    continue

                if isinstance(a, HastRepeatExactly):
                    try:
                        count = self.eval_value(a.count, current_state, current_occ, current_prov)
                        if type(count) is not int or count < 0:
                            raise _TermFault(RECURRENCE_COUNT_DOMAIN_ERROR)
                    except _TermFault as e:
                        step = _StepError(current_state, RuntimeErrorRecord(e.code, "EXECUTION", e.detail))
                        current_action = None
                        continue
                    if count == 0:
                        step = _StepNormal(current_state, None)
                        current_action = None
                        continue
                    frames.append(_RepeatExactlyFrame(count - 1, a.action, current_occ))
                    current_action = a.action
                    current_prov = None
                    continue

                if isinstance(a, HastPostActionRecurrence):
                    frames.append(_PostFrame(a.action, a.proposition, current_occ))
                    current_action = a.action
                    current_prov = None
                    continue

                if isinstance(a, HastPerformAct):
                    try:
                        values: dict[RoleId, object] = {}
                        for assoc in a.associations:
                            values[assoc.role] = self.eval_value(assoc.value, current_state, current_occ, current_prov)
                    except _TermFault as e:
                        step = _StepError(current_state, RuntimeErrorRecord(e.code, "EXECUTION", e.detail))
                        current_action = None
                        continue
                    if self.max_active_performances is not None and self.active_performances >= self.max_active_performances:
                        step = _StepResource(current_state, f"caller-imposed active performance budget {self.max_active_performances} exhausted")
                        current_action = None
                        continue
                    child = _Occurrence(OccurrenceId(self.next_occurrence), a.act, values)
                    self.next_occurrence += 1
                    self.active_performances += 1
                    frames.append(_PerformanceFrame(child))
                    current_action = self.body_by_act[a.act]
                    current_occ = child
                    current_prov = None
                    continue

                if isinstance(a, HastProduceResult):
                    if current_occ is None:
                        step = _StepError(current_state, RuntimeErrorRecord("OUTPUT_OUTSIDE_PERFORMANCE", "EXECUTION"))
                        current_action = None
                        continue
                    try:
                        value = self.eval_value(a.value, current_state, current_occ, current_prov)
                    except _TermFault as e:
                        step = _StepError(current_state, RuntimeErrorRecord(e.code, "EXECUTION", e.detail))
                        current_action = None
                        continue
                    if current_occ.output is not None:
                        step = _StepError(current_state, RuntimeErrorRecord(CORE_OUTPUT_CARDINALITY_ERROR, "EXECUTION"))
                    else:
                        current_occ.output = value
                        self.products.append(Product(current_occ.identity, current_occ.act, value))
                        step = _StepNormal(current_state, None)
                    current_action = None
                    continue

                step = _StepError(current_state, RuntimeErrorRecord("INTERNAL_UNKNOWN_ACTION", "EXECUTION"))
                current_action = None
                continue

            assert step is not None
            if not isinstance(step, _StepNormal):
                return step
            if not frames:
                return step

            frame = frames.pop()
            current_state = step.state

            if isinstance(frame, _ThenFrame):
                if frame.remaining:
                    current_occ = frame.occurrence
                    current_prov = step.provenance
                    current_action = frame.remaining[0]
                    frames.append(_ThenFrame(frame.remaining[1:], frame.occurrence))
                    step = None
                    continue
                # A completed sequence exposes the provenance of its last unit.
                continue

            if isinstance(frame, _ClearProvenanceFrame):
                step = _StepNormal(current_state, None)
                continue

            if isinstance(frame, _FixedFrame):
                if frame.remaining > 0:
                    current_occ = frame.occurrence
                    current_prov = None
                    current_action = frame.action
                    frames.append(_FixedFrame(frame.remaining - 1, frame.action, frame.occurrence))
                    step = None
                    continue
                step = _StepNormal(current_state, None)
                continue

            if isinstance(frame, _RepeatExactlyFrame):
                if frame.remaining > 0:
                    current_occ = frame.occurrence
                    current_prov = None
                    current_action = frame.action
                    frames.append(_RepeatExactlyFrame(frame.remaining - 1, frame.action, frame.occurrence))
                    step = None
                    continue
                step = _StepNormal(current_state, None)
                continue

            if isinstance(frame, _PostFrame):
                try:
                    stop = self.holds(frame.proposition, current_state, frame.occurrence, step.provenance)
                except _TermFault as e:
                    step = _StepError(current_state, RuntimeErrorRecord(e.code, "EXECUTION", e.detail))
                    continue
                if stop:
                    step = _StepNormal(current_state, None)
                    continue
                current_occ = frame.occurrence
                current_prov = None
                current_action = frame.action
                frames.append(frame)
                step = None
                continue

            if isinstance(frame, _PerformanceFrame):
                self.active_performances -= 1
                child = frame.child
                step = _StepNormal(current_state, _Provenance(child.identity, child.act, child.output))
                continue

            return _StepError(current_state, RuntimeErrorRecord("INTERNAL_UNKNOWN_CONTINUATION", "EXECUTION"))

    def prepare(self):
        state = SemanticState()
        for prep in self.program.preparation:
            if not isinstance(prep, HastPlaceIntroduction):
                continue
            try:
                value = self.eval_value(prep.initial_fact, state, None, None)
            except _TermFault as e:
                return _StepError(state, RuntimeErrorRecord(e.code, "PREPARATION", e.detail))
            state = state.establish(prep.place, value)
        return _StepNormal(state, None)

    def run(self) -> Outcome:
        try:
            prep = self.prepare()
            if isinstance(prep, _StepError):
                return ErrorOutcome(prep.state, prep.error, tuple(self.products))
            step = self.execute(self.program.principal, prep.state, None, None)
            if isinstance(step, _StepNormal):
                return NormalOutcome(step.state, tuple(self.products))
            if isinstance(step, _StepError):
                return ErrorOutcome(step.state, step.error, tuple(self.products))
            if isinstance(step, _StepResource):
                return ResourceExhaustionOutcome(step.state, tuple(self.products), detail=step.detail)
            return DivergenceOutcome(tuple(self.products))
        except (MemoryError, RecursionError) as exc:
            # A host resource failure is tooling/runtime infrastructure status,
            # never a Marak language runtime error.
            return ResourceExhaustionOutcome(SemanticState(), tuple(self.products), detail=type(exc).__name__)


def execute_reference(
    program: HastCoreProgram,
    *,
    fuel: int | None = None,
    debug_trace: bool = False,
    max_active_performances: int | None = DEFAULT_MAX_ACTIVE_PERFORMANCES,
    bindings: tuple[InputBinding, ...] | ValidatedInvocation = (),
):
    invocation = prepare_invocation(program, bindings)
    if isinstance(invocation, InvalidInvocation):
        return invocation
    return ReferenceEvaluator(
        program,
        fuel=fuel,
        debug_trace=debug_trace,
        max_active_performances=max_active_performances,
        invocation=invocation,
    ).run()


__all__ = [
    "ARITHMETIC_DOMAIN_ERROR", "RESULT_PROVENANCE_ERROR", "CORE_OUTPUT_CARDINALITY_ERROR",
    "COLLECTION_POSITION_ERROR", "ORDER_RELATION_ERROR", "RECURRENCE_COUNT_DOMAIN_ERROR",
    "ROLE_VALUE_OUTSIDE_PERFORMANCE", "IMPLEMENTATION_RESOURCE_EXHAUSTION",
    "DEFAULT_MAX_ACTIVE_PERFORMANCES", "RuntimeErrorRecord", "SemanticState", "Product",
    "NormalOutcome", "ErrorOutcome", "DivergenceOutcome", "ResourceExhaustionOutcome", "Outcome",
    "ReferenceEvaluator", "execute_reference",
]
