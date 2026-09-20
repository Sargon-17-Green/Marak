"""Reference evaluator for canonical validated IR with typed Values."""
from __future__ import annotations

from dataclasses import dataclass

from compiler.models import ir as i
from compiler.models.domains import NATURAL, Domain
from compiler.models.values import (
    BidirectionalIndexValue, CollectionValue, NaturalValue, SemanticValue, SymbolValue,
    index_successor, index_predecessor, symbol_identity_equal,
    semantic_value_equal, value_domain,
)
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
    value: object


@dataclass(frozen=True, slots=True)
class IRReferenceNormal:
    facts: tuple[tuple[int, object], ...]
    products: tuple[IRReferenceProduct, ...]
    place_names: tuple[tuple[int, str], ...] = ()
    act_names: tuple[tuple[int, str], ...] = ()


@dataclass(frozen=True, slots=True)
class IRReferenceErrorOutcome:
    facts: tuple[tuple[int, object], ...]
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
    facts: tuple[tuple[int, object], ...]
    products: tuple[IRReferenceProduct, ...]
    category: str = IMPLEMENTATION_RESOURCE_EXHAUSTION
    detail: str = "implementation activation budget exhausted"
    place_names: tuple[tuple[int, str], ...] = ()
    act_names: tuple[tuple[int, str], ...] = ()


@dataclass
class _Occurrence:
    identity: int
    act: int
    roles: dict[int, object]
    output: object | None = None


@dataclass(frozen=True)
class _Provenance:
    occurrence: int
    act: int
    output: object | None


@dataclass(frozen=True)
class _Then:
    remaining: tuple[i.IRAction, ...]
    occ: _Occurrence | None


@dataclass(frozen=True)
class _Clear:
    pass


@dataclass(frozen=True)
class _Fixed:
    remaining: int
    action: i.IRAction
    occ: _Occurrence | None


@dataclass(frozen=True)
class _Post:
    action: i.IRAction
    proposition: i.IRProposition
    occ: _Occurrence | None


@dataclass(frozen=True)
class _Perf:
    child: _Occurrence


class _Fault(Exception):
    def __init__(self, code: str, detail: str = ""):
        self.code = code
        self.detail = detail


def _natural(value: object) -> int:
    if type(value) is not int:
        raise _Fault("INTERNAL_DOMAIN_GUARD")
    return value


def _public(value: object):
    return value


class IRReferenceEvaluator:
    def __init__(self, program: i.IRProgram, *, fuel: int | None = None, max_active_performances: int | None = DEFAULT_MAX_ACTIVE_PERFORMANCES):
        if program.ir_version != i.IR_VERSION:
            raise ValueError("unsupported IR version")
        self.program = program
        self.fuel = fuel
        self.max_active_performances = max_active_performances
        self.active_performances = 0
        self.next_occurrence = 1
        self.products: list[IRReferenceProduct] = []
        self.acts = {x.act: x for x in program.acts}
        self.place_names = tuple(sorted((x.serial, x.spelling) for x in program.symbols if x.kind == "place"))
        self.act_names = tuple(sorted((x.serial, x.spelling) for x in program.symbols if x.kind == "act"))
        self.symbol_order_rank = {}
        members_by_domain = {}
        outgoing_by_domain = {}
        for m in program.symbol_members:
            members_by_domain.setdefault(m.domain_id,set()).add(m.member_id)
        for edge in program.symbol_order_edges:
            outgoing_by_domain.setdefault(edge.domain_id,{})[edge.before_member_id]=edge.after_member_id
        for domain_id,members in members_by_domain.items():
            outgoing=outgoing_by_domain.get(domain_id,{})
            incoming=set(outgoing.values())
            starts=[m for m in members if m not in incoming]
            if len(starts)==1:
                rank={}; cur=starts[0]
                while cur not in rank:
                    rank[cur]=len(rank)
                    if cur not in outgoing: break
                    cur=outgoing[cur]
                if set(rank)==members:
                    self.symbol_order_rank[domain_id]=rank

    def consume(self) -> bool:
        if self.fuel is None:
            return True
        if self.fuel <= 0:
            return False
        self.fuel -= 1
        return True

    def _semantic_item(self,value: object,domain: Domain):
        if domain==NATURAL:
            if type(value) is not int: raise _Fault("INTERNAL_DOMAIN_GUARD")
            return NaturalValue(value)
        if not isinstance(value,(SymbolValue,BidirectionalIndexValue,CollectionValue)) or value_domain(value)!=domain:
            raise _Fault("INTERNAL_DOMAIN_GUARD")
        return value

    def _select(self,collection: CollectionValue,mode: str,position: int | None):
        k=1 if mode=="first" else len(collection.items) if mode=="last" else position
        if type(k) is not int or k<1 or k>len(collection.items):
            raise _Fault("COLLECTION_POSITION_ERROR",f"position={k}, count={len(collection.items)}")
        item=collection.items[k-1]
        return item.value if isinstance(item,NaturalValue) else item

    def _order(self,collection: CollectionValue,kind: str,symbol_domain_id):
        try:
            if kind=="natural":
                items=sorted(collection.items,key=lambda x:x.value)
            elif kind=="symbol":
                rank=self.symbol_order_rank[symbol_domain_id]; items=sorted(collection.items,key=lambda x:rank[x.member_id])
            elif kind=="lex-natural":
                items=sorted(collection.items,key=lambda x:tuple(v.value for v in x.items))
            elif kind=="lex-symbol":
                rank=self.symbol_order_rank[symbol_domain_id]; items=sorted(collection.items,key=lambda x:tuple(rank[v.member_id] for v in x.items))
            else:
                raise KeyError(kind)
            return CollectionValue(collection.element_domain,tuple(items))
        except (KeyError,AttributeError,TypeError):
            raise _Fault("ORDER_RELATION_ERROR")

    def value(self, node: i.IRValue, state: dict[int, object], occ: _Occurrence | None, prov: _Provenance | None) -> object:
        if isinstance(node, i.IRNatural):
            return node.value
        if isinstance(node, i.IRSymbolValue):
            return SymbolValue(node.domain_id, node.member_id, node.external_label)
        if isinstance(node, i.IRIndexValue):
            return BidirectionalIndexValue(node.side, node.magnitude)
        if isinstance(node, i.IRIndexSuccessor):
            operand=self.value(node.operand,state,occ,prov)
            if not isinstance(operand,BidirectionalIndexValue): raise _Fault("INTERNAL_DOMAIN_GUARD")
            return index_successor(operand)
        if isinstance(node, i.IRIndexPredecessor):
            operand=self.value(node.operand,state,occ,prov)
            if not isinstance(operand,BidirectionalIndexValue): raise _Fault("INTERNAL_DOMAIN_GUARD")
            return index_predecessor(operand)
        if isinstance(node, i.IRCollectionValue):
            items=[]
            for child in node.items:
                v=self.value(child,state,occ,prov)
                if node.element_domain == NATURAL:
                    if type(v) is not int:
                        raise _Fault("INTERNAL_DOMAIN_GUARD", "validated Natural collection element produced a non-Natural value")
                    items.append(NaturalValue(v))
                else:
                    items.append(v)
            return CollectionValue(node.element_domain,tuple(items))
        if isinstance(node,i.IRCollectionAppend):
            collection=self.value(node.collection,state,occ,prov)
            if not isinstance(collection,CollectionValue): raise _Fault("INTERNAL_DOMAIN_GUARD")
            item=self._semantic_item(self.value(node.item,state,occ,prov),node.element_domain)
            return CollectionValue(node.element_domain,collection.items+(item,))
        if isinstance(node,i.IRCollectionCount):
            collection=self.value(node.collection,state,occ,prov)
            if not isinstance(collection,CollectionValue): raise _Fault("INTERNAL_DOMAIN_GUARD")
            return len(collection.items)
        if isinstance(node,i.IRCollectionSelectNatural):
            collection=self.value(node.collection,state,occ,prov)
            if not isinstance(collection,CollectionValue): raise _Fault("INTERNAL_DOMAIN_GUARD")
            pos=None if node.position is None else _natural(self.value(node.position,state,occ,prov))
            selected=self._select(collection,node.mode,pos)
            if type(selected) is not int: raise _Fault("INTERNAL_DOMAIN_GUARD")
            return selected
        if isinstance(node,i.IRCollectionSelectValue):
            collection=self.value(node.collection,state,occ,prov)
            if not isinstance(collection,CollectionValue): raise _Fault("INTERNAL_DOMAIN_GUARD")
            pos=None if node.position is None else _natural(self.value(node.position,state,occ,prov))
            return self._select(collection,node.mode,pos)
        if isinstance(node,i.IRCollectionOrder):
            collection=self.value(node.collection,state,occ,prov)
            if not isinstance(collection,CollectionValue): raise _Fault("INTERNAL_DOMAIN_GUARD")
            return self._order(collection,node.order_kind,node.symbol_domain_id)
        if isinstance(node, (i.IRReadCurrentFact, i.IRReadCurrentValue)):
            return state[node.place]
        if isinstance(node, (i.IRReadRoleNumber, i.IRReadRoleValue)):
            if occ is None or node.role not in occ.roles:
                raise _Fault("ROLE_VALUE_OUTSIDE_PERFORMANCE")
            return occ.roles[node.role]
        if isinstance(node, (i.IRRecentResult, i.IRRecentTypedResult)):
            if prov is None or prov.act != node.act or prov.output is None:
                raise _Fault("RESULT_PROVENANCE_ERROR")
            return prov.output
        if isinstance(node, i.IRAddNatural):
            return _natural(self.value(node.addend, state, occ, prov)) + _natural(self.value(node.augend, state, occ, prov))
        if isinstance(node, i.IRCheckedSubtractNatural):
            amount = _natural(self.value(node.amount, state, occ, prov))
            source = _natural(self.value(node.source, state, occ, prov))
            if amount > source:
                raise _Fault(node.error_code, f"{source}-{amount}")
            return source - amount
        raise _Fault("INTERNAL_UNKNOWN_VALUE")

    def holds(self, proposition, state, occ, prov):
        if isinstance(proposition, i.IREqualProposition):
            return _natural(self.value(proposition.left, state, occ, prov)) == _natural(self.value(proposition.right, state, occ, prov))
        if isinstance(proposition,i.IRNaturalGTProposition):
            return _natural(self.value(proposition.left,state,occ,prov)) > _natural(self.value(proposition.right,state,occ,prov))
        if isinstance(proposition,i.IRSymbolEqualProposition):
            left=self.value(proposition.left,state,occ,prov); right=self.value(proposition.right,state,occ,prov)
            if not isinstance(left,SymbolValue) or not isinstance(right,SymbolValue): raise _Fault("INTERNAL_DOMAIN_GUARD")
            return symbol_identity_equal(left,right)
        if isinstance(proposition,i.IRCollectionMembershipProposition):
            collection=self.value(proposition.collection,state,occ,prov)
            if not isinstance(collection,CollectionValue): raise _Fault("INTERNAL_DOMAIN_GUARD")
            item=self._semantic_item(self.value(proposition.item,state,occ,prov),proposition.element_domain)
            return any(semantic_value_equal(item,x) for x in collection.items)
        raise _Fault("INTERNAL_UNKNOWN_PROPOSITION")

    def action(self, action, state, occ=None, prov=None):
        frames = []
        current = action
        current_state = dict(state)
        current_occ = occ
        current_prov = prov
        step = None
        while True:
            if current is not None:
                if not self.consume():
                    step = ("div", current_state, None); current = None; continue
                node = current
                if isinstance(node, i.IRReplaceCurrentFact):
                    try:
                        v = self.value(node.value, current_state, current_occ, current_prov)
                    except _Fault as e:
                        step = ("err", current_state, IRReferenceError(e.code, "EXECUTION", e.detail)); current = None; continue
                    ns = dict(current_state); ns[node.place] = v; step = ("ok", ns, None); current = None; continue
                if isinstance(node, i.IRThen):
                    frames.append(_Then(tuple(node.actions[1:]), current_occ)); current = node.actions[0]; continue
                if isinstance(node, i.IRConditional):
                    try:
                        selected = node.if_holds if self.holds(node.proposition, current_state, current_occ, current_prov) else node.if_not
                    except _Fault as e:
                        step = ("err", current_state, IRReferenceError(e.code, "EXECUTION", e.detail)); current = None; continue
                    frames.append(_Clear()); current = selected; continue
                if isinstance(node, i.IRFixedRecurrence):
                    frames.append(_Fixed(node.count - 1, node.action, current_occ)); current = node.action; current_prov = None; continue
                if isinstance(node, i.IRPostActionRecurrence):
                    frames.append(_Post(node.action, node.proposition, current_occ)); current = node.action; current_prov = None; continue
                if isinstance(node, i.IRPerformAct):
                    try:
                        vals = {x.role: self.value(x.value, current_state, current_occ, current_prov) for x in node.associations}
                    except _Fault as e:
                        step = ("err", current_state, IRReferenceError(e.code, "EXECUTION", e.detail)); current = None; continue
                    if self.max_active_performances is not None and self.active_performances >= self.max_active_performances:
                        step = ("resource", current_state, f"caller-imposed active performance budget {self.max_active_performances} exhausted"); current = None; continue
                    child = _Occurrence(self.next_occurrence, node.act, vals)
                    self.next_occurrence += 1; self.active_performances += 1
                    frames.append(_Perf(child)); current = self.acts[node.act].body; current_occ = child; current_prov = None; continue
                if isinstance(node, i.IRProduceResult):
                    if current_occ is None:
                        step = ("err", current_state, IRReferenceError("OUTPUT_OUTSIDE_PERFORMANCE", "EXECUTION")); current = None; continue
                    try:
                        v = self.value(node.value, current_state, current_occ, current_prov)
                    except _Fault as e:
                        step = ("err", current_state, IRReferenceError(e.code, "EXECUTION", e.detail)); current = None; continue
                    if current_occ.output is not None:
                        step = ("err", current_state, IRReferenceError("CORE_OUTPUT_CARDINALITY_ERROR", "EXECUTION"))
                    else:
                        current_occ.output = v
                        self.products.append(IRReferenceProduct(current_occ.identity, current_occ.act, _public(v)))
                        step = ("ok", dict(current_state), None)
                    current = None; continue
                step = ("err", current_state, IRReferenceError("INTERNAL_UNKNOWN_ACTION", "EXECUTION")); current = None; continue

            kind, current_state, payload = step
            if kind != "ok":
                return step
            if not frames:
                return step
            frame = frames.pop()
            if isinstance(frame, _Then):
                if frame.remaining:
                    current_occ = frame.occ; current_prov = payload; current = frame.remaining[0]
                    frames.append(_Then(frame.remaining[1:], frame.occ)); step = None; continue
                continue
            if isinstance(frame, _Clear):
                step = ("ok", current_state, None); continue
            if isinstance(frame, _Fixed):
                if frame.remaining > 0:
                    current_occ = frame.occ; current_prov = None; current = frame.action
                    frames.append(_Fixed(frame.remaining - 1, frame.action, frame.occ)); step = None; continue
                step = ("ok", current_state, None); continue
            if isinstance(frame, _Post):
                try:
                    stop = self.holds(frame.proposition, current_state, frame.occ, payload)
                except _Fault as e:
                    step = ("err", current_state, IRReferenceError(e.code, "EXECUTION", e.detail)); continue
                if stop:
                    step = ("ok", current_state, None); continue
                current_occ = frame.occ; current_prov = None; current = frame.action; frames.append(frame); step = None; continue
            if isinstance(frame, _Perf):
                self.active_performances -= 1
                child = frame.child
                step = ("ok", current_state, _Provenance(child.identity, child.act, child.output)); continue
            return ("err", current_state, IRReferenceError("INTERNAL_UNKNOWN_CONTINUATION", "EXECUTION"))

    def facts(self, state):
        return tuple((k, _public(v)) for k, v in sorted(state.items()))

    def run(self):
        state: dict[int, object] = {}
        try:
            for initial in self.program.initial_facts:
                try:
                    value = self.value(initial.value, state, None, None)
                except _Fault as e:
                    return IRReferenceErrorOutcome(self.facts(state), IRReferenceError(e.code, "PREPARATION", e.detail), tuple(self.products), self.place_names, self.act_names)
                state[initial.place] = value
            kind, state, payload = self.action(self.program.principal, state)
            facts = self.facts(state)
            if kind == "ok":
                return IRReferenceNormal(facts, tuple(self.products), self.place_names, self.act_names)
            if kind == "err":
                return IRReferenceErrorOutcome(facts, payload, tuple(self.products), self.place_names, self.act_names)
            if kind == "resource":
                return IRReferenceResourceExhaustion(facts, tuple(self.products), detail=payload, place_names=self.place_names, act_names=self.act_names)
            return IRReferenceDivergence(tuple(self.products), place_names=self.place_names, act_names=self.act_names)
        except (MemoryError, RecursionError) as exc:
            return IRReferenceResourceExhaustion(self.facts(state), tuple(self.products), detail=type(exc).__name__, place_names=self.place_names, act_names=self.act_names)


def execute_ir_reference(program: i.IRProgram, *, fuel: int | None = None, max_active_performances: int | None = DEFAULT_MAX_ACTIVE_PERFORMANCES):
    return IRReferenceEvaluator(program, fuel=fuel, max_active_performances=max_active_performances).run()


# Stable M4 public name retained for compatibility.
execute_reference_ir = execute_ir_reference


__all__ = [
    "IR_REFERENCE_VERSION", "IRReferenceError", "IRReferenceProduct", "IRReferenceNormal",
    "IRReferenceErrorOutcome", "IRReferenceDivergence", "IRReferenceResourceExhaustion",
    "IRReferenceEvaluator", "execute_ir_reference", "execute_reference_ir",
]
