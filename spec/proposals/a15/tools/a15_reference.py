#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Iterable
import re

HEBREW=set('אבגדהוזחטיכךלמםנןסעפףצץקרשת')
WS=set(chr(cp) for cp in list(range(0x9,0xE))+[0x20,0x85,0xA0,0x1680]+list(range(0x2000,0x200B))+[0x2028,0x2029,0x202F,0x205F,0x3000])

class SurfaceError(ValueError): pass
class CollectionPositionError(SurfaceError): pass
class InputBindingError(SurfaceError): pass


def normalize(source: str) -> str:
    out=[]; pending=False
    for c in source:
        if c in HEBREW:
            if pending and out: out.append(' ')
            pending=False; out.append(c)
        elif c in WS:
            pending=True
    return re.sub(r' +',' ',''.join(out)).strip()

@dataclass(frozen=True)
class Symbol:
    domain: str
    member: str

class SymbolDomain:
    def __init__(self, source_id: str):
        self.source_id=source_id
        self._labels: dict[str, tuple[str,...]]={}
        self._next: dict[str,str]={}
    def declare(self, member: str, visible_words: Iterable[str]):
        words=tuple(visible_words)
        if not words: raise SurfaceError('SYMBOL_LABEL_EMPTY')
        if member in self._labels: raise SurfaceError('DUPLICATE_SYMBOL_MEMBER')
        for w in words:
            nw=normalize(w)
            if not nw or ' ' in nw: raise SurfaceError('SYMBOL_LABEL_WORD_INVALID')
        self._labels[member]=tuple(normalize(w) for w in words)
        return Symbol(self.source_id,member)
    def value(self, member: str) -> Symbol:
        if member not in self._labels: raise SurfaceError('UNKNOWN_SYMBOL_MEMBER')
        return Symbol(self.source_id,member)
    def visible(self, value: Symbol) -> str:
        if value.domain != self.source_id or value.member not in self._labels: raise SurfaceError('SYMBOL_DOMAIN_MISMATCH')
        return ' '.join(self._labels[value.member])
    def establish_adjacent_order(self, members: list[str]):
        if set(members) != set(self._labels) or len(members)!=len(self._labels): raise SurfaceError('SYMBOL_ORDER_NOT_TOTAL')
        self._next={a:b for a,b in zip(members,members[1:])}
        self._rank={m:i for i,m in enumerate(members)}
    def order_key(self, value: Symbol):
        if value.domain != self.source_id or not hasattr(self,'_rank') or value.member not in self._rank: raise SurfaceError('SYMBOL_ORDER_UNAVAILABLE')
        return self._rank[value.member]

@dataclass(frozen=True, order=False)
class BidirectionalIndex:
    side: int
    magnitude: int=0
    def __post_init__(self):
        if self.side not in (-1,0,1): raise SurfaceError('INDEX_SIDE')
        if self.side==0 and self.magnitude!=0: raise SurfaceError('INDEX_ZERO_MAGNITUDE')
        if self.side!=0 and self.magnitude<1: raise SurfaceError('INDEX_POSITIVE_MAGNITUDE_REQUIRED')
    @staticmethod
    def zero(): return BidirectionalIndex(0,0)
    @staticmethod
    def before(n:int): return BidirectionalIndex(-1,n)
    @staticmethod
    def after(n:int): return BidirectionalIndex(1,n)
    def key(self):
        if self.side<0: return -self.magnitude
        if self.side==0: return 0
        return self.magnitude
    def __lt__(self,other):
        if not isinstance(other,BidirectionalIndex): return NotImplemented
        return self.key()<other.key()

@dataclass(frozen=True)
class Collection:
    domain: str
    items: tuple[Any,...]=()
    def append(self,item: Any): return Collection(self.domain,self.items+(item,))
    def count(self): return len(self.items)
    def contains(self,item: Any): return item in self.items
    def first(self): return self.select(1)
    def last(self): return self.select(len(self.items))
    def select(self,position: int):
        if not 1 <= position <= len(self.items): raise CollectionPositionError('COLLECTION_POSITION_ERROR')
        return self.items[position-1]
    def successor_at(self,position:int): return self.select(position+1)
    def ordered(self,key: Callable[[Any],Any]): return Collection(self.domain,tuple(sorted(self.items,key=key)))


def repeat_exactly(count_observer: Callable[[],int], action: Callable[[],None]):
    n=count_observer()
    if not isinstance(n,int) or isinstance(n,bool) or n<0: raise SurfaceError('RECURRENCE_COUNT_DOMAIN_ERROR')
    for _ in range(n): action()

class ProgramInputContract:
    def __init__(self, roles: dict[str,str]): self.roles=dict(roles)
    def bind(self, associations: Iterable[tuple[str,str,Any]]):
        bound={}
        for identity,domain,value in associations:
            if identity in bound: raise InputBindingError('DUPLICATE_INPUT_BINDING')
            if identity not in self.roles: raise InputBindingError('EXTRA_INPUT_BINDING')
            if self.roles[identity] != domain: raise InputBindingError('INPUT_DOMAIN_MISMATCH')
            bound[identity]=value
        missing=set(self.roles)-set(bound)
        if missing: raise InputBindingError('MISSING_INPUT_BINDING')
        return bound
