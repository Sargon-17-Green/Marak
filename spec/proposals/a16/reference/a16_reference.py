#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass, replace as dc_replace
from types import MappingProxyType
from typing import Any, Callable, Iterable, Optional

from spec.proposals.a15.tools.a15_reference import (
    Symbol, SymbolDomain, BidirectionalIndex, Collection, SurfaceError, normalize
)

class A16Error(SurfaceError):
    pass

PLACE_DOMAIN_MISMATCH='PLACE_DOMAIN_MISMATCH'
PLACE_HEAD_DOMAIN_MISMATCH='PLACE_HEAD_DOMAIN_MISMATCH'
ROLE_DOMAIN_MISMATCH='ROLE_DOMAIN_MISMATCH'
ROLE_BINDING_ERROR='ROLE_BINDING_ERROR'
OUTPUT_DOMAIN_MISMATCH='OUTPUT_DOMAIN_MISMATCH'
MIXED_OUTPUT_DOMAINS='MIXED_OUTPUT_DOMAINS'
SECOND_OUTPUT='SECOND_OUTPUT'
NO_OUTPUT='NO_OUTPUT'
STALE_IMMEDIATE_RESULT='STALE_IMMEDIATE_RESULT'
IMMEDIATE_RESULT_HEAD_MISMATCH='IMMEDIATE_RESULT_HEAD_MISMATCH'
SYMBOL_EQUALITY_DOMAIN_MISMATCH='SYMBOL_EQUALITY_DOMAIN_MISMATCH'
INDEX_OPERAND_DOMAIN_MISMATCH='INDEX_OPERAND_DOMAIN_MISMATCH'

def value_domain(value: Any) -> str:
    if isinstance(value, bool):
        raise A16Error('VALUE_DOMAIN_MISMATCH')
    if isinstance(value, int) and value >= 0:
        return 'Natural'
    if isinstance(value, Symbol):
        return f'Symbol:{value.domain}'
    if isinstance(value, BidirectionalIndex):
        return 'BidirectionalIndex'
    if isinstance(value, Collection):
        return f'Collection<{value.domain}>'
    raise A16Error('VALUE_DOMAIN_MISMATCH')

def accepts(domain: str, value: Any) -> bool:
    try:
        return value_domain(value) == domain
    except A16Error:
        return False

@dataclass(frozen=True)
class Place:
    name: str
    domain: str

@dataclass(frozen=True)
class State:
    values: tuple[tuple[Place, Any], ...] = ()
    def get(self, place: Place) -> Any:
        data=dict(self.values)
        if place not in data:
            raise A16Error('UNKNOWN_PLACE')
        return data[place]
    def put(self, place: Place, value: Any) -> 'State':
        data=dict(self.values)
        data[place]=value
        return State(tuple(data.items()))

def initialize_place(name: str, initial_value: Any) -> tuple[Place, State]:
    domain=value_domain(initial_value)
    place=Place(name,domain)
    return place, State(((place,initial_value),))

def merge_states(*states: State) -> State:
    data={}
    for state in states:
        for place,value in state.values:
            if place in data:
                raise A16Error('DUPLICATE_PLACE')
            data[place]=value
    return State(tuple(data.items()))

def current_place_value(state: State, place: Place, typed_head_domain: Optional[str]=None) -> Any:
    if typed_head_domain is not None and typed_head_domain != place.domain:
        raise A16Error(PLACE_HEAD_DOMAIN_MISMATCH)
    value=state.get(place)
    if not accepts(place.domain,value):
        raise A16Error(PLACE_DOMAIN_MISMATCH)
    return value

def replace_place(state: State, place: Place, rhs_eval: Callable[[],Any],
                  displaced_head_domain: Optional[str]=None) -> State:
    if displaced_head_domain is not None and displaced_head_domain != place.domain:
        raise A16Error(PLACE_HEAD_DOMAIN_MISMATCH)
    _=current_place_value(state,place,place.domain)
    new_value=rhs_eval()
    if not accepts(place.domain,new_value):
        raise A16Error(PLACE_DOMAIN_MISMATCH)
    return state.put(place,new_value)

@dataclass(frozen=True)
class Role:
    act: str
    name: str
    domain: str

def bind_roles(required: Iterable[Role], supplied: Iterable[tuple[Role,Any]]):
    required=tuple(required)
    supplied=tuple(supplied)
    req={(r.act,r.name):r for r in required}
    out={}
    for role,value in supplied:
        key=(role.act,role.name)
        if key in out or key not in req or req[key] != role:
            raise A16Error(ROLE_BINDING_ERROR)
        if not accepts(role.domain,value):
            raise A16Error(ROLE_DOMAIN_MISMATCH)
        out[key]=value
    if set(out) != set(req):
        raise A16Error(ROLE_BINDING_ERROR)
    return MappingProxyType(dict(out))

def current_role_value(bindings, role: Role, typed_head_domain: Optional[str]=None):
    if typed_head_domain is not None and typed_head_domain != role.domain:
        raise A16Error(ROLE_DOMAIN_MISMATCH)
    key=(role.act,role.name)
    if key not in bindings:
        raise A16Error(ROLE_BINDING_ERROR)
    value=bindings[key]
    if not accepts(role.domain,value):
        raise A16Error(ROLE_DOMAIN_MISMATCH)
    return value

def resolve_output_domain(site_domains: Iterable[str]) -> Optional[str]:
    domains=tuple(site_domains)
    if not domains:
        return None
    first=domains[0]
    if any(d != first for d in domains[1:]):
        raise A16Error(MIXED_OUTPUT_DOMAINS)
    return first

@dataclass
class Occurrence:
    act: str
    output_domain: Optional[str]
    output: Any=None
    output_count: int=0
    later_actions: int=0
    def emit(self, value: Any) -> None:
        if self.output_count:
            raise A16Error(SECOND_OUTPUT)
        if self.output_domain is None or not accepts(self.output_domain,value):
            raise A16Error(OUTPUT_DOMAIN_MISMATCH)
        self.output=value
        self.output_count=1
    def later_action(self) -> None:
        self.later_actions += 1
    def complete(self) -> 'ImmediateResult':
        if self.output_count != 1:
            raise A16Error(NO_OUTPUT)
        return ImmediateResult(self.act,self.output_domain,self.output,True)

@dataclass(frozen=True)
class ImmediateResult:
    act: str
    domain: str
    value: Any
    fresh: bool=True

def invalidate_immediate(result: ImmediateResult) -> ImmediateResult:
    return dc_replace(result,fresh=False)

def read_immediate(result: ImmediateResult, act: str, typed_head_domain: str):
    if not result.fresh or result.act != act:
        raise A16Error(STALE_IMMEDIATE_RESULT)
    if result.domain != typed_head_domain:
        raise A16Error(IMMEDIATE_RESULT_HEAD_MISMATCH)
    return result.value

def _index_from_key(z: int) -> BidirectionalIndex:
    if z == 0:
        return BidirectionalIndex.zero()
    return BidirectionalIndex.after(z) if z > 0 else BidirectionalIndex.before(-z)

def index_successor(value: Any) -> BidirectionalIndex:
    if not isinstance(value,BidirectionalIndex):
        raise A16Error(INDEX_OPERAND_DOMAIN_MISMATCH)
    return _index_from_key(value.key()+1)

def index_predecessor(value: Any) -> BidirectionalIndex:
    if not isinstance(value,BidirectionalIndex):
        raise A16Error(INDEX_OPERAND_DOMAIN_MISMATCH)
    return _index_from_key(value.key()-1)

def symbol_equal_proposition(a: Any, b: Any) -> bool:
    if not isinstance(a,Symbol) or not isinstance(b,Symbol):
        raise A16Error('SYMBOL_EQUALITY_OPERAND_DOMAIN_MISMATCH')
    if a.domain != b.domain:
        raise A16Error(SYMBOL_EQUALITY_DOMAIN_MISMATCH)
    return a.member == b.member
