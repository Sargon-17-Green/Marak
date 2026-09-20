#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass, replace
from typing import Any, Callable, Optional

class InvalidProgram(Exception):
    def __init__(self, code:str): super().__init__(code); self.code=code
class RuntimeFault(Exception):
    def __init__(self, code:str): super().__init__(code); self.code=code
class Diverged(Exception): pass

RESULT_PROVENANCE_ERROR="RESULT_PROVENANCE_ERROR"
CORE_OUTPUT_CARDINALITY_ERROR="CORE_OUTPUT_CARDINALITY_ERROR"
VALUE_DOMAIN_MISMATCH="VALUE_DOMAIN_MISMATCH"
UNRESOLVED_VALUE_DOMAIN="UNRESOLVED_VALUE_DOMAIN"
MIXED_OUTPUT_DOMAINS="MIXED_OUTPUT_DOMAINS"
IMMEDIATE_RESULT_HEAD_MISMATCH="IMMEDIATE_RESULT_HEAD_MISMATCH"
STALE_RESULT_REFERENCE="STALE_RESULT_REFERENCE"
ROLE_DOMAIN_MISMATCH="ROLE_DOMAIN_MISMATCH"
PLACE_DOMAIN_MISMATCH="PLACE_DOMAIN_MISMATCH"
INDEX_OPERAND_DOMAIN_MISMATCH="INDEX_OPERAND_DOMAIN_MISMATCH"
SYMBOL_EQUALITY_DOMAIN_MISMATCH="SYMBOL_EQUALITY_DOMAIN_MISMATCH"

@dataclass(frozen=True)
class Expr:
    domain: Optional[str]
    evaluate: Callable[[],Any]

def require_domain(expr:Expr, expected:str, code:str=VALUE_DOMAIN_MISMATCH):
    if expr.domain is None:
        raise InvalidProgram(UNRESOLVED_VALUE_DOMAIN)
    if expr.domain != expected:
        raise InvalidProgram(code)

@dataclass(frozen=True)
class PlaceContract:
    place_id:str
    domain:str

@dataclass(frozen=True)
class State:
    values:tuple[tuple[str,Any],...]=()
    def has(self,p:PlaceContract): return p.place_id in dict(self.values)
    def get(self,p:PlaceContract):
        d=dict(self.values)
        if p.place_id not in d: raise RuntimeFault("UNESTABLISHED_PLACE")
        return d[p.place_id]
    def put(self,p:PlaceContract,v:Any):
        d=dict(self.values); d[p.place_id]=v
        return State(tuple(d.items()))

def declare_place(place_id:str, initializer:Expr)->PlaceContract:
    if initializer.domain is None:
        raise InvalidProgram(UNRESOLVED_VALUE_DOMAIN)
    return PlaceContract(place_id,initializer.domain)

def establish_place(state:State, contract:PlaceContract, initializer:Expr)->State:
    require_domain(initializer,contract.domain,PLACE_DOMAIN_MISMATCH)
    v=initializer.evaluate()
    return state.put(contract,v)

def current_place(state:State, contract:PlaceContract, typed_head_domain:str):
    if typed_head_domain != contract.domain:
        raise InvalidProgram(PLACE_DOMAIN_MISMATCH)
    return state.get(contract)

def replace_place(state:State, contract:PlaceContract, rhs:Expr, typed_current_domain:str)->State:
    if typed_current_domain != contract.domain:
        raise InvalidProgram(PLACE_DOMAIN_MISMATCH)
    require_domain(rhs,contract.domain,PLACE_DOMAIN_MISMATCH)
    v=rhs.evaluate()
    return state.put(contract,v)

@dataclass(frozen=True)
class RoleContract:
    act_id:str
    role_id:str
    domain:str

@dataclass(frozen=True)
class Occurrence:
    token:int
    act_id:str
    associations:tuple[tuple[tuple[str,str],Any],...]
    output_contract:Optional[str]=None
    output:Any=None
    output_count:int=0
    completed_actions:int=0
    def role_value(self,role:RoleContract,typed_head_domain:str):
        if role.act_id != self.act_id:
            raise InvalidProgram("ROLE_OWNER_MISMATCH")
        if typed_head_domain != role.domain:
            raise InvalidProgram(ROLE_DOMAIN_MISMATCH)
        d=dict(self.associations)
        key=(role.act_id,role.role_id)
        if key not in d: raise RuntimeFault("ROLE_ASSOCIATION_MISSING")
        return d[key]

def start_occurrence(token:int, act_id:str, required:tuple[RoleContract,...],
                     supplied:tuple[tuple[RoleContract,Expr],...],
                     output_contract:Optional[str]=None)->Occurrence:
    req={(r.act_id,r.role_id):r for r in required}
    seen={}
    for role,expr in supplied:
        key=(role.act_id,role.role_id)
        if key not in req or req[key] != role or key in seen:
            raise InvalidProgram("ROLE_BINDING_ERROR")
        require_domain(expr,role.domain,ROLE_DOMAIN_MISMATCH)
        seen[key]=expr
    if set(seen)!=set(req): raise InvalidProgram("ROLE_BINDING_ERROR")
    vals=[]
    for key,role in req.items():
        vals.append((key,seen[key].evaluate()))
    return Occurrence(token,act_id,tuple(vals),output_contract)

def resolve_output_contract(site_domains:tuple[Optional[str],...])->Optional[str]:
    if not site_domains: return None
    if any(d is None for d in site_domains):
        raise InvalidProgram(UNRESOLVED_VALUE_DOMAIN)
    d=site_domains[0]
    if any(x!=d for x in site_domains[1:]):
        raise InvalidProgram(MIXED_OUTPUT_DOMAINS)
    return d

def emit(occ:Occurrence,expr:Expr)->Occurrence:
    if occ.output_contract is None:
        raise InvalidProgram("OUTPUT_WITHOUT_DECLARED_DOMAIN")
    require_domain(expr,occ.output_contract,"OUTPUT_DOMAIN_MISMATCH")
    if occ.output_count:
        raise RuntimeFault(CORE_OUTPUT_CARDINALITY_ERROR)
    v=expr.evaluate()
    return replace(occ,output=v,output_count=1)

def later_action(occ:Occurrence)->Occurrence:
    return replace(occ,completed_actions=occ.completed_actions+1)

@dataclass(frozen=True)
class Provenance:
    act_id:str
    output_domain:Optional[str]
    output:Any
    fresh:bool=True

def complete_occurrence(occ:Occurrence)->Provenance:
    return Provenance(occ.act_id,occ.output_contract,occ.output if occ.output_count else None,True)

def validate_immediate_reference(output_domain:Optional[str],typed_head_domain:str,structurally_adjacent:bool=True):
    if output_domain is None:
        raise InvalidProgram("ACT_HAS_NO_OUTPUT_DOMAIN")
    if typed_head_domain != output_domain:
        raise InvalidProgram(IMMEDIATE_RESULT_HEAD_MISMATCH)
    if not structurally_adjacent:
        raise InvalidProgram(STALE_RESULT_REFERENCE)

def read_immediate(prov:Provenance,act_id:str,typed_head_domain:str):
    if not prov.fresh or prov.act_id!=act_id or prov.output is None:
        raise RuntimeFault(RESULT_PROVENANCE_ERROR)
    if prov.output_domain != typed_head_domain:
        raise RuntimeFault(RESULT_PROVENANCE_ERROR)
    return prov.output

def invalidate(prov:Provenance)->Provenance:
    return replace(prov,fresh=False)

def index_succ(value:Any,domain:str,from_math:Callable[[int],Any],key:Callable[[Any],int]):
    if domain!="BidirectionalIndex": raise InvalidProgram(INDEX_OPERAND_DOMAIN_MISMATCH)
    return from_math(key(value)+1)

def index_pred(value:Any,domain:str,from_math:Callable[[int],Any],key:Callable[[Any],int]):
    if domain!="BidirectionalIndex": raise InvalidProgram(INDEX_OPERAND_DOMAIN_MISMATCH)
    return from_math(key(value)-1)

def symbol_equal(a:Any,b:Any,left_domain:str,right_domain:str,identity:Callable[[Any],tuple]):
    if left_domain!=right_domain or not left_domain.startswith("Symbol:"):
        raise InvalidProgram(SYMBOL_EQUALITY_DOMAIN_MISMATCH)
    return identity(a)==identity(b)

D_ADEQUACY={str(i).zfill(3):"EXECUTABLE_AFTER_INTEGRATION" for i in range(1,8)}
