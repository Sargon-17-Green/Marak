from __future__ import annotations

from dataclasses import dataclass

from compiler.models import ir as i
from compiler.models.domains import NATURAL, Domain
from compiler.models.values import (
    BidirectionalIndexValue, CollectionValue, NaturalValue, SemanticValue,
    SymbolValue, index_successor, index_predecessor, symbol_identity_equal,
    semantic_value_equal, value_domain,
)

BACKEND_VERSION = "portable-ir-vm-0.4-candidate-1"
IMPLEMENTATION_RESOURCE_EXHAUSTION = "IMPLEMENTATION_RESOURCE_EXHAUSTION"
DEFAULT_MAX_ACTIVE_PERFORMANCES = None


@dataclass(frozen=True, slots=True)
class VMError:
    code: str
    phase: str
    detail: str = ""


@dataclass(frozen=True, slots=True)
class VMProduct:
    occurrence: int
    act: int
    value: object


@dataclass(frozen=True, slots=True)
class VMNormal:
    facts: tuple[tuple[int, object], ...]
    products: tuple[VMProduct, ...]
    place_names: tuple[tuple[int, str], ...] = ()
    act_names: tuple[tuple[int, str], ...] = ()


@dataclass(frozen=True, slots=True)
class VMErrorOutcome:
    facts: tuple[tuple[int, object], ...]
    error: VMError
    products: tuple[VMProduct, ...]
    place_names: tuple[tuple[int, str], ...] = ()
    act_names: tuple[tuple[int, str], ...] = ()


@dataclass(frozen=True, slots=True)
class VMDivergence:
    products: tuple[VMProduct, ...]
    place_names: tuple[tuple[int, str], ...] = ()
    act_names: tuple[tuple[int, str], ...] = ()


@dataclass(frozen=True, slots=True)
class VMResourceExhaustion:
    facts: tuple[tuple[int, object], ...]
    products: tuple[VMProduct, ...]
    category: str = IMPLEMENTATION_RESOURCE_EXHAUSTION
    detail: str = "implementation activation budget exhausted"
    place_names: tuple[tuple[int, str], ...] = ()
    act_names: tuple[tuple[int, str], ...] = ()


@dataclass
class _Occ:
    token: int
    act: int
    roles: dict[int, object]
    output: object | None = None


@dataclass(frozen=True)
class _Prov:
    token: int
    act: int
    output: object | None


@dataclass(frozen=True)
class _Then:
    remaining: tuple[i.IRAction, ...]
    occ: _Occ | None


@dataclass(frozen=True)
class _Clear:
    pass


@dataclass(frozen=True)
class _Fixed:
    remaining: int
    action: i.IRAction
    occ: _Occ | None


@dataclass(frozen=True)
class _Post:
    action: i.IRAction
    proposition: i.IRProposition
    occ: _Occ | None


@dataclass(frozen=True)
class _Perf:
    child: _Occ


class _Fault(Exception):
    def __init__(self, code, detail=""):
        self.code = code
        self.detail = detail


def _natural(value: object) -> int:
    if type(value) is not int:
        raise _Fault("INTERNAL_DOMAIN_GUARD", "validated Natural expression produced a non-Natural runtime value")
    return value


def _public(value: object):
    return value


class PortableVM:
    def __init__(self, program: i.IRProgram, *, fuel: int | None = None, max_active_performances: int | None = DEFAULT_MAX_ACTIVE_PERFORMANCES):
        if program.ir_version != i.IR_VERSION:
            raise ValueError("unsupported IR version")
        self.p = program
        self.fuel = fuel
        self.next_occ = 1
        self.products: list[VMProduct] = []
        self.max_active_performances = max_active_performances
        self.active_performances = 0
        self.acts = {a.act: a for a in program.acts}
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

    def consume(self):
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

    def value(self, n: i.IRValue, state: dict[int, object], occ: _Occ | None, prov: _Prov | None) -> object:
        if isinstance(n, i.IRNatural):
            return n.value
        if isinstance(n, i.IRSymbolValue):
            return SymbolValue(n.domain_id, n.member_id, n.external_label)
        if isinstance(n, i.IRIndexValue):
            return BidirectionalIndexValue(n.side, n.magnitude)
        if isinstance(n, i.IRIndexSuccessor):
            operand=self.value(n.operand,state,occ,prov)
            if not isinstance(operand,BidirectionalIndexValue): raise _Fault("INTERNAL_DOMAIN_GUARD")
            return index_successor(operand)
        if isinstance(n, i.IRIndexPredecessor):
            operand=self.value(n.operand,state,occ,prov)
            if not isinstance(operand,BidirectionalIndexValue): raise _Fault("INTERNAL_DOMAIN_GUARD")
            return index_predecessor(operand)
        if isinstance(n, i.IRCollectionValue):
            items=[]
            for child in n.items:
                v=self.value(child,state,occ,prov)
                if n.element_domain == NATURAL:
                    if type(v) is not int:
                        raise _Fault("INTERNAL_DOMAIN_GUARD", "validated Natural collection element produced a non-Natural value")
                    items.append(NaturalValue(v))
                else:
                    items.append(v)
            return CollectionValue(n.element_domain,tuple(items))
        if isinstance(n,i.IRCollectionAppend):
            chain=[]
            current=n
            while isinstance(current,i.IRCollectionAppend):
                chain.append(current)
                current=current.collection
            collection=self.value(current,state,occ,prov)
            if not isinstance(collection,CollectionValue): raise _Fault("INTERNAL_DOMAIN_GUARD")
            items=list(collection.items)
            for append in reversed(chain):
                if collection.element_domain!=append.element_domain: raise _Fault("INTERNAL_DOMAIN_GUARD")
                items.append(self._semantic_item(self.value(append.item,state,occ,prov),append.element_domain))
            return CollectionValue(n.element_domain,tuple(items))
        if isinstance(n,i.IRCollectionCount):
            collection=self.value(n.collection,state,occ,prov)
            if not isinstance(collection,CollectionValue): raise _Fault("INTERNAL_DOMAIN_GUARD")
            return len(collection.items)
        if isinstance(n,i.IRCollectionSelectNatural):
            collection=self.value(n.collection,state,occ,prov)
            if not isinstance(collection,CollectionValue): raise _Fault("INTERNAL_DOMAIN_GUARD")
            pos=None if n.position is None else _natural(self.value(n.position,state,occ,prov))
            selected=self._select(collection,n.mode,pos)
            if type(selected) is not int: raise _Fault("INTERNAL_DOMAIN_GUARD")
            return selected
        if isinstance(n,i.IRCollectionSelectValue):
            collection=self.value(n.collection,state,occ,prov)
            if not isinstance(collection,CollectionValue): raise _Fault("INTERNAL_DOMAIN_GUARD")
            pos=None if n.position is None else _natural(self.value(n.position,state,occ,prov))
            return self._select(collection,n.mode,pos)
        if isinstance(n,i.IRCollectionOrder):
            collection=self.value(n.collection,state,occ,prov)
            if not isinstance(collection,CollectionValue): raise _Fault("INTERNAL_DOMAIN_GUARD")
            return self._order(collection,n.order_kind,n.symbol_domain_id)
        if isinstance(n, (i.IRReadCurrentFact, i.IRReadCurrentValue)):
            return state[n.place]
        if isinstance(n, (i.IRReadRoleNumber, i.IRReadRoleValue)):
            if occ is None or n.role not in occ.roles:
                raise _Fault("ROLE_VALUE_OUTSIDE_PERFORMANCE")
            return occ.roles[n.role]
        if isinstance(n, (i.IRRecentResult, i.IRRecentTypedResult)):
            if prov is None or prov.act != n.act or prov.output is None:
                raise _Fault("RESULT_PROVENANCE_ERROR")
            return prov.output
        if isinstance(n, i.IRAddNatural):
            return _natural(self.value(n.addend, state, occ, prov)) + _natural(self.value(n.augend, state, occ, prov))
        if isinstance(n, i.IRCheckedSubtractNatural):
            amount = _natural(self.value(n.amount, state, occ, prov))
            source = _natural(self.value(n.source, state, occ, prov))
            if amount > source:
                raise _Fault(n.error_code, f"{source}-{amount}")
            return source - amount
        raise _Fault("INTERNAL_UNKNOWN_VALUE")

    def holds(self, p, state, occ, prov):
        if isinstance(p, i.IREqualProposition):
            return _natural(self.value(p.left, state, occ, prov)) == _natural(self.value(p.right, state, occ, prov))
        if isinstance(p,i.IRNaturalGTProposition):
            return _natural(self.value(p.left,state,occ,prov)) > _natural(self.value(p.right,state,occ,prov))
        if isinstance(p,i.IRSymbolEqualProposition):
            left=self.value(p.left,state,occ,prov); right=self.value(p.right,state,occ,prov)
            if not isinstance(left,SymbolValue) or not isinstance(right,SymbolValue): raise _Fault("INTERNAL_DOMAIN_GUARD")
            return symbol_identity_equal(left,right)
        if isinstance(p,i.IRCollectionMembershipProposition):
            collection=self.value(p.collection,state,occ,prov)
            if not isinstance(collection,CollectionValue): raise _Fault("INTERNAL_DOMAIN_GUARD")
            item=self._semantic_item(self.value(p.item,state,occ,prov),p.element_domain)
            return any(semantic_value_equal(item,x) for x in collection.items)
        raise _Fault("INTERNAL_UNKNOWN_PROPOSITION")

    def action(self, a, state, occ=None, prov=None):
        frames = []
        current = a
        cur = dict(state)
        current_occ = occ
        current_prov = prov
        step = None
        while True:
            if current is not None:
                if not self.consume():
                    step = ("div", cur, None)
                    current = None
                    continue
                x = current
                if isinstance(x, i.IRReplaceCurrentFact):
                    try:
                        v = self.value(x.value, cur, current_occ, current_prov)
                    except _Fault as e:
                        step = ("err", cur, VMError(e.code, "EXECUTION", e.detail)); current = None; continue
                    ns = dict(cur); ns[x.place] = v; step = ("ok", ns, None); current = None; continue
                if isinstance(x, i.IRThen):
                    frames.append(_Then(tuple(x.actions[1:]), current_occ)); current = x.actions[0]; continue
                if isinstance(x, i.IRConditional):
                    try:
                        yes = self.holds(x.proposition, cur, current_occ, current_prov)
                    except _Fault as e:
                        step = ("err", cur, VMError(e.code, "EXECUTION", e.detail)); current = None; continue
                    frames.append(_Clear()); current = x.if_holds if yes else x.if_not; continue
                if isinstance(x, i.IRFixedRecurrence):
                    frames.append(_Fixed(x.count - 1, x.action, current_occ)); current = x.action; current_prov = None; continue
                if isinstance(x, i.IRPostActionRecurrence):
                    frames.append(_Post(x.action, x.proposition, current_occ)); current = x.action; current_prov = None; continue
                if isinstance(x, i.IRPerformAct):
                    try:
                        vals = {z.role: self.value(z.value, cur, current_occ, current_prov) for z in x.associations}
                    except _Fault as e:
                        step = ("err", cur, VMError(e.code, "EXECUTION", e.detail)); current = None; continue
                    if self.max_active_performances is not None and self.active_performances >= self.max_active_performances:
                        step = ("resource", cur, f"caller-imposed active performance budget {self.max_active_performances} exhausted"); current = None; continue
                    child = _Occ(self.next_occ, x.act, vals)
                    self.next_occ += 1; self.active_performances += 1
                    frames.append(_Perf(child)); current = self.acts[x.act].body; current_occ = child; current_prov = None; continue
                if isinstance(x, i.IRProduceResult):
                    if current_occ is None:
                        step = ("err", cur, VMError("OUTPUT_OUTSIDE_PERFORMANCE", "EXECUTION")); current = None; continue
                    try:
                        v = self.value(x.value, cur, current_occ, current_prov)
                    except _Fault as e:
                        step = ("err", cur, VMError(e.code, "EXECUTION", e.detail)); current = None; continue
                    if current_occ.output is not None:
                        step = ("err", cur, VMError("CORE_OUTPUT_CARDINALITY_ERROR", "EXECUTION"))
                    else:
                        current_occ.output = v
                        self.products.append(VMProduct(current_occ.token, current_occ.act, _public(v)))
                        step = ("ok", dict(cur), None)
                    current = None; continue
                step = ("err", cur, VMError("INTERNAL_UNKNOWN_ACTION", "EXECUTION")); current = None; continue

            k, cur, z = step
            if k != "ok":
                return (k, cur, z)
            if not frames:
                return step
            frame = frames.pop()
            if isinstance(frame, _Then):
                if frame.remaining:
                    current_occ = frame.occ; current_prov = z; current = frame.remaining[0]
                    frames.append(_Then(frame.remaining[1:], frame.occ)); step = None; continue
                continue
            if isinstance(frame, _Clear):
                step = ("ok", cur, None); continue
            if isinstance(frame, _Fixed):
                if frame.remaining > 0:
                    current_occ = frame.occ; current_prov = None; current = frame.action
                    frames.append(_Fixed(frame.remaining - 1, frame.action, frame.occ)); step = None; continue
                step = ("ok", cur, None); continue
            if isinstance(frame, _Post):
                try:
                    stop = self.holds(frame.proposition, cur, frame.occ, z)
                except _Fault as e:
                    step = ("err", cur, VMError(e.code, "EXECUTION", e.detail)); continue
                if stop:
                    step = ("ok", cur, None); continue
                current_occ = frame.occ; current_prov = None; current = frame.action; frames.append(frame); step = None; continue
            if isinstance(frame, _Perf):
                self.active_performances -= 1
                child = frame.child
                step = ("ok", cur, _Prov(child.token, child.act, child.output))
                continue
            return ("err", cur, VMError("INTERNAL_UNKNOWN_CONTINUATION", "EXECUTION"))

    def _facts(self, state):
        return tuple((k, _public(v)) for k, v in sorted(state.items()))

    def run(self):
        state: dict[int, object] = {}
        try:
            for x in self.p.initial_facts:
                try:
                    v = self.value(x.value, state, None, None)
                except _Fault as e:
                    return VMErrorOutcome(self._facts(state), VMError(e.code, "PREPARATION", e.detail), tuple(self.products), self.place_names, self.act_names)
                state[x.place] = v
            k, state, z = self.action(self.p.principal, state, None, None)
            facts = self._facts(state)
            if k == "ok":
                return VMNormal(facts, tuple(self.products), self.place_names, self.act_names)
            if k == "err":
                return VMErrorOutcome(facts, z, tuple(self.products), self.place_names, self.act_names)
            if k == "resource":
                return VMResourceExhaustion(facts, tuple(self.products), detail=z, place_names=self.place_names, act_names=self.act_names)
            return VMDivergence(tuple(self.products), self.place_names, self.act_names)
        except (MemoryError, RecursionError) as exc:
            return VMResourceExhaustion(self._facts(state), tuple(self.products), detail=type(exc).__name__, place_names=self.place_names, act_names=self.act_names)


def execute_ir(program: i.IRProgram, *, fuel: int | None = None, max_active_performances: int | None = DEFAULT_MAX_ACTIVE_PERFORMANCES):
    return PortableVM(program, fuel=fuel, max_active_performances=max_active_performances).run()
