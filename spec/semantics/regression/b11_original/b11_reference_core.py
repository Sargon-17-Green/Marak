#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

class SemanticError(Exception): pass
class SourceInvalid(SemanticError): pass
class ProductReferenceError(SemanticError): pass

@dataclass(frozen=True, order=True)
class Referent:
    id:str

@dataclass(frozen=True)
class Integer:
    value:int

NUMBER="number"

@dataclass(frozen=True)
class Snapshot:
    facts:tuple
    @staticmethod
    def empty():
        return Snapshot(tuple())
    def _d(self):
        return dict(self.facts)
    def establish(self,r,v):
        d=self._d()
        if (r,NUMBER) in d:
            raise SourceInvalid("already established")
        d[(r,NUMBER)]=v
        return Snapshot(tuple(sorted(d.items(),key=lambda x:x[0][0].id)))
    def query(self,r):
        return self._d()[(r,NUMBER)]
    def replace(self,r,v):
        d=self._d()
        if (r,NUMBER) not in d:
            raise SourceInvalid("missing current fact")
        d[(r,NUMBER)]=v
        return Snapshot(tuple(sorted(d.items(),key=lambda x:x[0][0].id)))

# Numeric terms
@dataclass(frozen=True)
class Lit: n:int
@dataclass(frozen=True)
class Current: r:Referent
@dataclass(frozen=True)
class RoleNum: role:str
@dataclass(frozen=True)
class Add: a:Any; b:Any
@dataclass(frozen=True)
class Sub: a:Any; b:Any
@dataclass(frozen=True)
class Mul: a:Any; b:Any
@dataclass(frozen=True)
class Rem: a:Any; b:Any
@dataclass(frozen=True)
class RecentResult: act_id:str

# Propositions
@dataclass(frozen=True)
class Equal: a:Any; b:Any
@dataclass(frozen=True)
class Zero: a:Any
@dataclass(frozen=True)
class Greater: a:Any; b:Any

# Executable units
@dataclass(frozen=True)
class Replace: r:Referent; term:Any
@dataclass(frozen=True)
class Conditional: p:Any; yes:Any; no:Any
@dataclass(frozen=True)
class FixedRepeat: count:int; action:Any
@dataclass(frozen=True)
class PostRepeatUntil: action:Any; predicate:Any
@dataclass(frozen=True)
class Perform:
    act_id:str
    associations:tuple[tuple[str,Any],...]=()
@dataclass(frozen=True)
class Produce: term:Any
@dataclass(frozen=True)
class NoOp: pass

@dataclass(frozen=True)
class ActDef:
    roles:frozenset[str]
    body:tuple[Any,...]

@dataclass(frozen=True)
class Outcome:
    occurrence:int
    act_id:str
    state:Snapshot
    result:Integer|None

@dataclass(frozen=True)
class Recent:
    outcome:Outcome

@dataclass
class Occurrence:
    id:int
    act_id:str
    roles:dict[str,Integer]
    result:Integer|None=None

class Runtime:
    def __init__(self,acts=None):
        self.acts=acts or {}
        self.next_occ=1
    def denote(self,t,s,occ=None,recent=None):
        if isinstance(t,Lit): return Integer(t.n)
        if isinstance(t,Current): return s.query(t.r)
        if isinstance(t,RoleNum):
            if occ is None or t.role not in occ.roles: raise SourceInvalid("role unavailable")
            return occ.roles[t.role]
        if isinstance(t,(Add,Sub,Mul,Rem)):
            a=self.denote(t.a,s,occ,recent).value
            b=self.denote(t.b,s,occ,recent).value
            if isinstance(t,Add): return Integer(a+b)
            if isinstance(t,Sub): return Integer(a-b)
            if isinstance(t,Mul): return Integer(a*b)
            if b==0: raise SemanticError("division by zero")
            return Integer(a % abs(b))
        if isinstance(t,RecentResult):
            if recent is None: raise ProductReferenceError("no immediate result")
            if recent.outcome.act_id != t.act_id: raise ProductReferenceError("act mismatch")
            if recent.outcome.result is None: raise ProductReferenceError("no result")
            return recent.outcome.result
        raise SourceInvalid(f"unknown term {t!r}")
    def holds(self,p,s,occ=None,recent=None):
        if isinstance(p,Equal):
            return self.denote(p.a,s,occ,recent).value == self.denote(p.b,s,occ,recent).value
        if isinstance(p,Zero):
            return self.denote(p.a,s,occ,recent).value == 0
        if isinstance(p,Greater):
            return self.denote(p.a,s,occ,recent).value > self.denote(p.b,s,occ,recent).value
        raise SourceInvalid("unknown proposition")
    def _new_occ(self,act_id,roles):
        o=Occurrence(self.next_occ,act_id,dict(roles))
        self.next_occ+=1
        return o
    def perform(self,act_id,assocs,s,caller_occ=None,recent=None):
        act=self.acts[act_id]
        names=[n for n,_ in assocs]
        if len(names)!=len(set(names)) or set(names)!=set(act.roles):
            raise SourceInvalid("role association invalid")
        # Pure associations, all against same incoming snapshot and caller context.
        roles={n:self.denote(t,s,caller_occ,recent) for n,t in assocs}
        occ=self._new_occ(act_id,roles)
        st=s
        recent_local=None
        for u in act.body:
            st,recent_local=self.exec_unit(u,st,occ,recent_local)
        return Outcome(occ.id,act_id,st,occ.result)
    def exec_unit(self,u,s,occ=None,recent=None):
        if isinstance(u,NoOp):
            return s,None
        if isinstance(u,Replace):
            v=self.denote(u.term,s,occ,recent)
            return s.replace(u.r,v),None
        if isinstance(u,Conditional):
            chosen=u.yes if self.holds(u.p,s,occ,recent) else u.no
            return self.exec_unit(chosen,s,occ,recent)
        if isinstance(u,FixedRepeat):
            if u.count<0: raise SourceInvalid("negative repeat count")
            st=s
            for _ in range(u.count):
                st,_=self.exec_unit(u.action,st,occ,None)
            return st,None
        if isinstance(u,PostRepeatUntil):
            st=s
            while True:
                st,_=self.exec_unit(u.action,st,occ,None)
                if self.holds(u.predicate,st,occ,None):
                    return st,None
        if isinstance(u,Perform):
            out=self.perform(u.act_id,u.associations,s,occ,recent)
            return out.state,Recent(out)
        if isinstance(u,Produce):
            if occ is None: raise SourceInvalid("output outside performance")
            if occ.result is not None: raise SourceInvalid("A12 second output")
            occ.result=self.denote(u.term,s,occ,recent)
            return s,None
        raise SourceInvalid(f"unknown unit {u!r}")

def run_units(rt,units,s):
    st=s
    recent=None
    for u in units:
        st,recent=rt.exec_unit(u,st,None,recent)
    return st,recent
