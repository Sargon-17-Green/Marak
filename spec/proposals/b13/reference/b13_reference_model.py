from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable

class SemanticFailure(Exception):
    def __init__(self, code: str): super().__init__(code); self.code=code
class InvalidInvocation(Exception):
    def __init__(self, code: str): super().__init__(code); self.code=code

VALUE_DOMAIN_MISMATCH='VALUE_DOMAIN_MISMATCH'
INDEX_TO_NATURAL_DOMAIN_ERROR='INDEX_TO_NATURAL_DOMAIN_ERROR'
COLLECTION_POSITION_ERROR='COLLECTION_POSITION_ERROR'
COLLECTION_ELEMENT_DOMAIN_ERROR='COLLECTION_ELEMENT_DOMAIN_ERROR'
ORDER_RELATION_ERROR='ORDER_RELATION_ERROR'
RECURRENCE_COUNT_DOMAIN_ERROR='RECURRENCE_COUNT_DOMAIN_ERROR'
MISSING_INPUT_BINDING='MISSING_INPUT_BINDING'
EXTRA_INPUT_BINDING='EXTRA_INPUT_BINDING'
DUPLICATE_INPUT_BINDING='DUPLICATE_INPUT_BINDING'
INPUT_DOMAIN_MISMATCH='INPUT_DOMAIN_MISMATCH'

@dataclass(frozen=True)
class Natural:
    n:int
    def __post_init__(self):
        if type(self.n) is not int or self.n < 0: raise SemanticFailure(VALUE_DOMAIN_MISMATCH)

@dataclass(frozen=True)
class SymbolDomain: serial:int; name:str
@dataclass(frozen=True)
class SymbolMember: domain:SymbolDomain; serial:int; label:str

def symbol_equal(a,b):
    return isinstance(a,SymbolMember) and isinstance(b,SymbolMember) and a.domain.serial==b.domain.serial and a.serial==b.serial

class Side(Enum): BEFORE='before'; ZERO='zero'; AFTER='after'
@dataclass(frozen=True)
class BidirectionalIndex:
    side:Side; magnitude:int=0
    def __post_init__(self):
        if self.side is Side.ZERO:
            if self.magnitude!=0: raise SemanticFailure(VALUE_DOMAIN_MISMATCH)
        elif type(self.magnitude) is not int or self.magnitude<1:
            raise SemanticFailure(VALUE_DOMAIN_MISMATCH)
    def math(self): return 0 if self.side is Side.ZERO else (self.magnitude if self.side is Side.AFTER else -self.magnitude)
    def succ(self): return from_math_index(self.math()+1)
    def pred(self): return from_math_index(self.math()-1)
    def distance(self,other): return Natural(abs(self.math()-other.math()))
    def to_natural(self):
        if self.side is Side.BEFORE: raise SemanticFailure(INDEX_TO_NATURAL_DOMAIN_ERROR)
        return Natural(self.math())

def from_math_index(z):
    if z==0:return BidirectionalIndex(Side.ZERO,0)
    return BidirectionalIndex(Side.AFTER,z) if z>0 else BidirectionalIndex(Side.BEFORE,-z)
def index_from_natural(n): return from_math_index(n.n)
def index_lt(a,b): return a.math()<b.math()
def nat_lt(a,b): return a.n<b.n
def nat_gt(a,b): return a.n>b.n
def nat_le(a,b): return a.n<=b.n
def nat_ge(a,b): return a.n>=b.n

@dataclass(frozen=True)
class Domain:
    key:str; accepts:Callable[[Any],bool]; equal:Callable[[Any,Any],bool]
NAT_DOMAIN=Domain('Natural',lambda v:isinstance(v,Natural),lambda a,b:a==b)
INDEX_DOMAIN=Domain('BidirectionalIndex',lambda v:isinstance(v,BidirectionalIndex),lambda a,b:a==b)
def symbol_domain(d): return Domain(f'Symbol:{d.serial}',lambda v:isinstance(v,SymbolMember) and v.domain.serial==d.serial,symbol_equal)

@dataclass(frozen=True)
class FiniteOrderedCollection:
    element_domain:Domain; items:tuple
    def __post_init__(self):
        if any(not self.element_domain.accepts(x) for x in self.items): raise SemanticFailure(COLLECTION_ELEMENT_DOMAIN_ERROR)
    def append(self,x):
        if not self.element_domain.accepts(x): raise SemanticFailure(COLLECTION_ELEMENT_DOMAIN_ERROR)
        return FiniteOrderedCollection(self.element_domain,self.items+(x,))
    def count(self): return Natural(len(self.items))
    def select(self,pos):
        if not isinstance(pos,Natural) or pos.n<1 or pos.n>len(self.items): raise SemanticFailure(COLLECTION_POSITION_ERROR)
        return self.items[pos.n-1]
    def contains(self,x):
        return self.element_domain.accepts(x) and any(self.element_domain.equal(x,y) for y in self.items)

def collection_domain(elem):
    def accepts(v): return isinstance(v,FiniteOrderedCollection) and v.element_domain.key==elem.key
    def equal(a,b): return accepts(a) and accepts(b) and len(a.items)==len(b.items) and all(elem.equal(x,y) for x,y in zip(a.items,b.items))
    return Domain(f'Collection<{elem.key}>',accepts,equal)

def order_collection(c,lt):
    out=[]
    for x in c.items:
        put=False
        for i,y in enumerate(out):
            xy,yx,eq=lt(x,y),lt(y,x),c.element_domain.equal(x,y)
            if (xy and yx) or (not xy and not yx and not eq): raise SemanticFailure(ORDER_RELATION_ERROR)
            if xy: out.insert(i,x); put=True; break
        if not put: out.append(x)
    return FiniteOrderedCollection(c.element_domain,tuple(out))

def lex_lt(elem,lt,a,b):
    if a.element_domain.key!=elem.key or b.element_domain.key!=elem.key: raise SemanticFailure(VALUE_DOMAIN_MISMATCH)
    for x,y in zip(a.items,b.items):
        if elem.equal(x,y): continue
        xy,yx=lt(x,y),lt(y,x)
        if xy==yx: raise SemanticFailure(ORDER_RELATION_ERROR)
        return xy
    return len(a.items)<len(b.items)

@dataclass(frozen=True)
class StepNormal: state:int; outputs:tuple=()
@dataclass(frozen=True)
class StepError: state:int; code:str; outputs:tuple=()
@dataclass(frozen=True)
class StepDivergence: outputs:tuple=()

def repeat_exactly(count_eval,action,initial_state):
    c=count_eval()
    if not isinstance(c,Natural): return StepError(initial_state,RECURRENCE_COUNT_DOMAIN_ERROR,())
    state=initial_state; outputs=[]
    for i in range(c.n):
        r=action(state,i+1)
        if isinstance(r,StepNormal): state=r.state; outputs.extend(r.outputs); continue
        if isinstance(r,StepError): return StepError(r.state,r.code,tuple(outputs)+r.outputs)
        if isinstance(r,StepDivergence): return StepDivergence(tuple(outputs)+r.outputs)
        raise AssertionError('unknown outcome')
    return StepNormal(state,tuple(outputs))

@dataclass(frozen=True)
class ProgramInputId: serial:int; name:str; domain:Domain
@dataclass(frozen=True)
class ProgramContract: inputs:tuple
@dataclass(frozen=True)
class InvocationBindings:
    values:tuple
    def get(self,inp):
        return dict(self.values)[inp]

def bind_invocation(contract,supplied):
    serials=[k.serial for k,_ in supplied]
    if len(serials)!=len(set(serials)): raise InvalidInvocation(DUPLICATE_INPUT_BINDING)
    required={x.serial:x for x in contract.inputs}; given={k.serial:k for k,_ in supplied}
    if not set(required)<=set(given): raise InvalidInvocation(MISSING_INPUT_BINDING)
    if not set(given)<=set(required): raise InvalidInvocation(EXTRA_INPUT_BINDING)
    by={k.serial:(k,v) for k,v in supplied}; out=[]
    for inp in contract.inputs:
        k,v=by[inp.serial]
        if k!=inp or not inp.domain.accepts(v): raise InvalidInvocation(INPUT_DOMAIN_MISMATCH)
        out.append((inp,v))
    return InvocationBindings(tuple(out))
