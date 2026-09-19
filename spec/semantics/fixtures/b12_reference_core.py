#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional

ARITHMETIC_DOMAIN_ERROR = "ARITHMETIC_DOMAIN_ERROR"
REFERENCE_BEFORE_INTRODUCTION = "REFERENCE_BEFORE_INTRODUCTION"
DUPLICATE_PLACE = "DUPLICATE_PLACE"
DUPLICATE_ACT = "DUPLICATE_ACT"
DUPLICATE_ROLE = "DUPLICATE_ROLE"
DUPLICATE_BODY = "DUPLICATE_BODY"
ROLE_OWNER_NOT_INTRODUCED = "ROLE_OWNER_NOT_INTRODUCED"
ROLE_AFTER_BODY = "ROLE_AFTER_BODY"
BODY_OWNER_NOT_INTRODUCED = "BODY_OWNER_NOT_INTRODUCED"
ROLE_ASSOCIATION_INVALID = "ROLE_ASSOCIATION_INVALID"
ROLE_VALUE_OUTSIDE_PERFORMANCE = "ROLE_VALUE_OUTSIDE_PERFORMANCE"
RESULT_PROVENANCE_ERROR = "RESULT_PROVENANCE_ERROR"
CORE_OUTPUT_CARDINALITY_ERROR = "CORE_OUTPUT_CARDINALITY_ERROR"
MISSING_ACT_BODY = "MISSING_ACT_BODY"

class InvalidProgram(Exception):
    def __init__(self, code, detail=""):
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code=code
        self.detail=detail

@dataclass(frozen=True)
class ErrorRecord:
    code:str
    phase:str
    detail:str=""

@dataclass(frozen=True, order=True)
class EntityId:
    kind:str
    serial:int
    spelling:str
    owner_serial:int|None=None

@dataclass(frozen=True)
class SemanticState:
    facts:tuple[tuple[EntityId,int],...]

    @staticmethod
    def empty():
        return SemanticState(tuple())

    def as_dict(self):
        return dict(self.facts)

    def get(self,p:EntityId):
        return self.as_dict()[p]

    def establish(self,p:EntityId,n:int):
        assert p.kind=="place" and type(n) is int and n>=0
        d=self.as_dict()
        if p in d:
            raise InvalidProgram(DUPLICATE_PLACE)
        d[p]=n
        return SemanticState(tuple(sorted(d.items(), key=lambda kv:(kv[0].kind,kv[0].serial))))

    def replace(self,p:EntityId,n:int):
        assert p.kind=="place" and type(n) is int and n>=0
        d=self.as_dict()
        if p not in d:
            raise InvalidProgram(REFERENCE_BEFORE_INTRODUCTION)
        d[p]=n
        return SemanticState(tuple(sorted(d.items(), key=lambda kv:(kv[0].kind,kv[0].serial))))

@dataclass(frozen=True)
class Production:
    act:EntityId
    value:int

@dataclass(frozen=True)
class NormalOutcome:
    state:SemanticState
    productions:tuple[Production,...]

@dataclass(frozen=True)
class ErrorOutcome:
    state:SemanticState
    error:ErrorRecord
    productions:tuple[Production,...]

@dataclass(frozen=True)
class DivergenceOutcome:
    productions:tuple[Production,...]

# -------- unresolved abstract source objects (not parser syntax) --------
@dataclass(frozen=True)
class ULit: n:int
@dataclass(frozen=True)
class UCurrent: place:str
@dataclass(frozen=True)
class URoleValue: act:str; role:str
@dataclass(frozen=True)
class UAdd: a:Any; b:Any
@dataclass(frozen=True)
class USubtractFrom: subtrahend:Any; minuend:Any
@dataclass(frozen=True)
class URecentResult: act:str

@dataclass(frozen=True)
class UEqual: a:Any; b:Any

@dataclass(frozen=True)
class UReplace: place:str; term:Any
@dataclass(frozen=True)
class USequence: actions:tuple[Any,...]
@dataclass(frozen=True)
class UConditional: proposition:Any; if_holds:Any; if_not:Any
@dataclass(frozen=True)
class UPostActionUntil: action:Any; proposition:Any
@dataclass(frozen=True)
class UFixedRepeat: count:int; action:Any
@dataclass(frozen=True)
class UPerform: act:str; associations:tuple[tuple[str,Any],...]=()
@dataclass(frozen=True)
class UProduce: term:Any

@dataclass(frozen=True)
class PlaceIntro: name:str; initializer:Any
@dataclass(frozen=True)
class ActIntro: name:str
@dataclass(frozen=True)
class RoleIntro: act:str; role:str
@dataclass(frozen=True)
class BodyDef: act:str; body:Any
@dataclass(frozen=True)
class ProgramSpec:
    preparation:tuple[Any,...]
    principal:Any

# -------- resolved semantic AST --------
@dataclass(frozen=True)
class Nat: n:int
@dataclass(frozen=True)
class Current: place:EntityId
@dataclass(frozen=True)
class RoleValue: role:EntityId
@dataclass(frozen=True)
class Add: a:Any; b:Any
@dataclass(frozen=True)
class SubtractFrom: subtrahend:Any; minuend:Any
@dataclass(frozen=True)
class RecentResult: act:EntityId
@dataclass(frozen=True)
class Equal: a:Any; b:Any

@dataclass(frozen=True)
class Replace: place:EntityId; term:Any
@dataclass(frozen=True)
class Sequence: actions:tuple[Any,...]
@dataclass(frozen=True)
class Conditional: proposition:Any; if_holds:Any; if_not:Any
@dataclass(frozen=True)
class PostActionUntil: action:Any; proposition:Any
@dataclass(frozen=True)
class FixedRepeat: count:int; action:Any
@dataclass(frozen=True)
class Perform: act:EntityId; associations:tuple[tuple[EntityId,Any],...]
@dataclass(frozen=True)
class Produce: term:Any

@dataclass(frozen=True)
class RPlaceInit: place:EntityId; initializer:Any
@dataclass(frozen=True)
class RActIntro: act:EntityId
@dataclass(frozen=True)
class RRoleIntro: role:EntityId
@dataclass(frozen=True)
class RBodyDef: act:EntityId; body:Any

@dataclass(frozen=True)
class ActDefinition:
    act:EntityId
    roles:tuple[EntityId,...]
    body:Any

@dataclass(frozen=True)
class ResolvedProgram:
    preparation:tuple[Any,...]
    principal:Any
    acts:tuple[ActDefinition,...]
    places:tuple[EntityId,...]
    roles:tuple[EntityId,...]

@dataclass
class ResolverEnv:
    next_serial:int=1
    places:dict[str,EntityId]=None
    acts:dict[str,EntityId]=None
    roles:dict[tuple[int,str],EntityId]=None
    bodies:set[int]=None

    def __post_init__(self):
        self.places={} if self.places is None else self.places
        self.acts={} if self.acts is None else self.acts
        self.roles={} if self.roles is None else self.roles
        self.bodies=set() if self.bodies is None else self.bodies

    def new(self,kind,spelling,owner=None):
        e=EntityId(kind,self.next_serial,spelling,owner.serial if owner else None)
        self.next_serial+=1
        return e

def _const_eval(t):
    if isinstance(t,Nat):
        return t.n
    if isinstance(t,Add):
        a=_const_eval(t.a); b=_const_eval(t.b)
        return None if a is None or b is None else a+b
    if isinstance(t,SubtractFrom):
        a=_const_eval(t.subtrahend); b=_const_eval(t.minuend)
        if a is None or b is None:
            return None
        if a>b:
            raise InvalidProgram(ARITHMETIC_DOMAIN_ERROR,"statically provable Natural subtraction underflow")
        return b-a
    return None

def _resolve_term(t,env:ResolverEnv,current_act:EntityId|None):
    if isinstance(t,ULit):
        if type(t.n) is not int or t.n<0:
            raise InvalidProgram(ARITHMETIC_DOMAIN_ERROR,"negative Core literal not admitted")
        r=Nat(t.n)
    elif isinstance(t,UCurrent):
        if t.place not in env.places:
            raise InvalidProgram(REFERENCE_BEFORE_INTRODUCTION,f"place {t.place}")
        r=Current(env.places[t.place])
    elif isinstance(t,URoleValue):
        if t.act not in env.acts:
            raise InvalidProgram(REFERENCE_BEFORE_INTRODUCTION,f"act {t.act}")
        a=env.acts[t.act]
        key=(a.serial,t.role)
        if key not in env.roles:
            raise InvalidProgram(REFERENCE_BEFORE_INTRODUCTION,f"role {t.act}.{t.role}")
        if current_act is None or current_act != a:
            raise InvalidProgram(ROLE_VALUE_OUTSIDE_PERFORMANCE,f"{t.act}.{t.role}")
        r=RoleValue(env.roles[key])
    elif isinstance(t,UAdd):
        r=Add(_resolve_term(t.a,env,current_act),_resolve_term(t.b,env,current_act))
    elif isinstance(t,USubtractFrom):
        r=SubtractFrom(_resolve_term(t.subtrahend,env,current_act),_resolve_term(t.minuend,env,current_act))
    elif isinstance(t,URecentResult):
        if t.act not in env.acts:
            raise InvalidProgram(REFERENCE_BEFORE_INTRODUCTION,f"act {t.act}")
        r=RecentResult(env.acts[t.act])
    else:
        raise InvalidProgram("UNKNOWN_TERM",repr(t))
    _const_eval(r)  # mandatory rejection when this reference validator can prove underflow
    return r

def _resolve_prop(p,env,current_act):
    if isinstance(p,UEqual):
        return Equal(_resolve_term(p.a,env,current_act),_resolve_term(p.b,env,current_act))
    raise InvalidProgram("UNKNOWN_PROPOSITION",repr(p))

def _resolve_action(a,env,current_act):
    if isinstance(a,UReplace):
        if a.place not in env.places:
            raise InvalidProgram(REFERENCE_BEFORE_INTRODUCTION,f"place {a.place}")
        return Replace(env.places[a.place],_resolve_term(a.term,env,current_act))
    if isinstance(a,USequence):
        return Sequence(tuple(_resolve_action(x,env,current_act) for x in a.actions))
    if isinstance(a,UConditional):
        return Conditional(_resolve_prop(a.proposition,env,current_act),
                           _resolve_action(a.if_holds,env,current_act),
                           _resolve_action(a.if_not,env,current_act))
    if isinstance(a,UPostActionUntil):
        return PostActionUntil(_resolve_action(a.action,env,current_act),
                               _resolve_prop(a.proposition,env,current_act))
    if isinstance(a,UFixedRepeat):
        if type(a.count) is not int or a.count<0:
            raise InvalidProgram(ARITHMETIC_DOMAIN_ERROR,"negative repeat count")
        return FixedRepeat(a.count,_resolve_action(a.action,env,current_act))
    if isinstance(a,UPerform):
        if a.act not in env.acts:
            raise InvalidProgram(REFERENCE_BEFORE_INTRODUCTION,f"act {a.act}")
        act=env.acts[a.act]
        pairs=[]
        names=[]
        for role_name,term in a.associations:
            key=(act.serial,role_name)
            if key not in env.roles:
                raise InvalidProgram(REFERENCE_BEFORE_INTRODUCTION,f"role {a.act}.{role_name}")
            names.append(role_name)
            pairs.append((env.roles[key],_resolve_term(term,env,current_act)))
        required={rid.spelling for (owner,_),rid in env.roles.items() if owner==act.serial}
        if len(names)!=len(set(names)) or set(names)!=required:
            raise InvalidProgram(ROLE_ASSOCIATION_INVALID,a.act)
        return Perform(act,tuple(pairs))
    if isinstance(a,UProduce):
        if current_act is None:
            raise InvalidProgram("OUTPUT_OUTSIDE_PERFORMANCE")
        return Produce(_resolve_term(a.term,env,current_act))
    raise InvalidProgram("UNKNOWN_ACTION",repr(a))

def _potential_outputs(a):
    if isinstance(a,Produce): return 1
    if isinstance(a,Replace): return 0
    if isinstance(a,Perform): return 0  # child output belongs to child
    if isinstance(a,Sequence):
        return sum(_potential_outputs(x) for x in a.actions)
    if isinstance(a,Conditional):
        return max(_potential_outputs(a.if_holds),_potential_outputs(a.if_not))
    if isinstance(a,FixedRepeat):
        c=_potential_outputs(a.action)
        return c*a.count
    if isinstance(a,PostActionUntil):
        return 2 if _potential_outputs(a.action)>0 else 0
    return 0

def resolve_program(spec:ProgramSpec)->ResolvedProgram:
    env=ResolverEnv()
    rprep=[]
    body_map={}
    places=[]
    roles=[]

    for u in spec.preparation:
        if isinstance(u,PlaceIntro):
            if u.name in env.places:
                raise InvalidProgram(DUPLICATE_PLACE,u.name)
            # not visible in its own initializer
            init=_resolve_term(u.initializer,env,None)
            pid=env.new("place",u.name)
            env.places[u.name]=pid
            places.append(pid)
            rprep.append(RPlaceInit(pid,init))
        elif isinstance(u,ActIntro):
            if u.name in env.acts:
                raise InvalidProgram(DUPLICATE_ACT,u.name)
            aid=env.new("act",u.name)
            env.acts[u.name]=aid
            rprep.append(RActIntro(aid))
        elif isinstance(u,RoleIntro):
            if u.act not in env.acts:
                raise InvalidProgram(ROLE_OWNER_NOT_INTRODUCED,u.act)
            aid=env.acts[u.act]
            if aid.serial in env.bodies:
                raise InvalidProgram(ROLE_AFTER_BODY,f"{u.act}.{u.role}")
            key=(aid.serial,u.role)
            if key in env.roles:
                raise InvalidProgram(DUPLICATE_ROLE,f"{u.act}.{u.role}")
            rid=env.new("role",u.role,aid)
            env.roles[key]=rid
            roles.append(rid)
            rprep.append(RRoleIntro(rid))
        elif isinstance(u,BodyDef):
            if u.act not in env.acts:
                raise InvalidProgram(BODY_OWNER_NOT_INTRODUCED,u.act)
            aid=env.acts[u.act]
            if aid.serial in env.bodies:
                raise InvalidProgram(DUPLICATE_BODY,u.act)
            body=_resolve_action(u.body,env,aid)
            if _potential_outputs(body)>1:
                raise InvalidProgram(CORE_OUTPUT_CARDINALITY_ERROR,u.act)
            env.bodies.add(aid.serial)
            body_map[aid.serial]=body
            rprep.append(RBodyDef(aid,body))
        else:
            raise InvalidProgram("UNKNOWN_PREPARATORY_UNIT",repr(u))

    if set(a.serial for a in env.acts.values()) != env.bodies:
        missing=[a.spelling for a in env.acts.values() if a.serial not in env.bodies]
        raise InvalidProgram(MISSING_ACT_BODY,",".join(missing))

    principal=_resolve_action(spec.principal,env,None)

    actdefs=[]
    for aid in env.acts.values():
        owned=tuple(sorted((rid for (owner,_),rid in env.roles.items() if owner==aid.serial), key=lambda x:x.serial))
        actdefs.append(ActDefinition(aid,owned,body_map[aid.serial]))
    return ResolvedProgram(tuple(rprep),principal,tuple(actdefs),tuple(places),tuple(roles))

@dataclass
class Occurrence:
    token:int
    act:EntityId
    roles:dict[EntityId,int]
    output:Optional[int]=None

@dataclass(frozen=True)
class Provenance:
    act:EntityId
    output:Optional[int]
    token:int

@dataclass(frozen=True)
class StepNormal:
    state:SemanticState
    provenance:Optional[Provenance]=None

@dataclass(frozen=True)
class StepError:
    state:SemanticState
    error:ErrorRecord

@dataclass(frozen=True)
class StepDivergence:
    pass

class TermFault(Exception):
    def __init__(self,code,detail=""):
        super().__init__(code)
        self.code=code; self.detail=detail

class Evaluator:
    def __init__(self,program:ResolvedProgram,debug_trace=False,fuel:Optional[int]=None):
        self.program=program
        self.actdefs={a.act:a for a in program.acts}
        self.debug_trace_enabled=debug_trace
        self.trace=[]
        self.productions=[]
        self.next_occ=1
        self.fuel=fuel
        self.occurrence_log=[]

    def _event(self,*x):
        if self.debug_trace_enabled:
            self.trace.append(tuple(x))

    def _consume_fuel(self):
        if self.fuel is None:
            return True
        if self.fuel<=0:
            return False
        self.fuel-=1
        return True

    def eval_term(self,t,state:SemanticState,occ:Optional[Occurrence],prov:Optional[Provenance]):
        if isinstance(t,Nat): return t.n
        if isinstance(t,Current): return state.get(t.place)
        if isinstance(t,RoleValue):
            if occ is None or t.role not in occ.roles:
                raise TermFault(ROLE_VALUE_OUTSIDE_PERFORMANCE)
            return occ.roles[t.role]
        if isinstance(t,Add):
            return self.eval_term(t.a,state,occ,prov)+self.eval_term(t.b,state,occ,prov)
        if isinstance(t,SubtractFrom):
            a=self.eval_term(t.subtrahend,state,occ,prov)
            b=self.eval_term(t.minuend,state,occ,prov)
            if a>b:
                raise TermFault(ARITHMETIC_DOMAIN_ERROR,f"{b}-{a}")
            return b-a
        if isinstance(t,RecentResult):
            if prov is None or prov.act!=t.act or prov.output is None:
                raise TermFault(RESULT_PROVENANCE_ERROR)
            return prov.output
        raise TermFault("UNKNOWN_TERM")

    def holds(self,p,state,occ,prov):
        if isinstance(p,Equal):
            return self.eval_term(p.a,state,occ,prov)==self.eval_term(p.b,state,occ,prov)
        raise TermFault("UNKNOWN_PROPOSITION")

    def exec_action(self,a,state,occ=None,prov=None):
        if not self._consume_fuel():
            return StepDivergence()
        self._event("action",type(a).__name__)

        if isinstance(a,Replace):
            try:
                n=self.eval_term(a.term,state,occ,prov)
            except TermFault as e:
                return StepError(state,ErrorRecord(e.code,"EXECUTION",e.detail))
            return StepNormal(state.replace(a.place,n),None)

        if isinstance(a,Sequence):
            cur=state
            recent=prov
            for x in a.actions:
                r=self.exec_action(x,cur,occ,recent)
                if not isinstance(r,StepNormal):
                    return r
                cur=r.state
                recent=r.provenance
            return StepNormal(cur,recent)

        if isinstance(a,Conditional):
            try:
                yes=self.holds(a.proposition,state,occ,prov)
            except TermFault as e:
                return StepError(state,ErrorRecord(e.code,"EXECUTION",e.detail))
            r=self.exec_action(a.if_holds if yes else a.if_not,state,occ,prov)
            if isinstance(r,StepNormal):
                # compound conditional itself is not a direct performance provenance source
                return StepNormal(r.state,None)
            return r

        if isinstance(a,FixedRepeat):
            cur=state
            for _ in range(a.count):
                r=self.exec_action(a.action,cur,occ,None)
                if not isinstance(r,StepNormal):
                    return r
                cur=r.state
            return StepNormal(cur,None)

        if isinstance(a,PostActionUntil):
            cur=state
            while True:
                r=self.exec_action(a.action,cur,occ,None)
                if not isinstance(r,StepNormal):
                    return r
                cur=r.state
                try:
                    stop=self.holds(a.proposition,cur,occ,None)
                except TermFault as e:
                    return StepError(cur,ErrorRecord(e.code,"EXECUTION",e.detail))
                if stop:
                    return StepNormal(cur,None)

        if isinstance(a,Perform):
            try:
                vals={}
                # all pure association terms observe same incoming state
                for rid,t in a.associations:
                    vals[rid]=self.eval_term(t,state,occ,prov)
            except TermFault as e:
                return StepError(state,ErrorRecord(e.code,"EXECUTION",e.detail))

            child=Occurrence(self.next_occ,a.act,vals)
            self.next_occ+=1
            self.occurrence_log.append((child.token,child.act,tuple(sorted((r.serial,n) for r,n in vals.items()))))
            body=self.actdefs[a.act].body
            r=self.exec_action(body,state,child,None)
            if isinstance(r,StepNormal):
                return StepNormal(r.state,Provenance(a.act,child.output,child.token))
            return r

        if isinstance(a,Produce):
            if occ is None:
                return StepError(state,ErrorRecord("OUTPUT_OUTSIDE_PERFORMANCE","EXECUTION"))
            try:
                n=self.eval_term(a.term,state,occ,prov)
            except TermFault as e:
                return StepError(state,ErrorRecord(e.code,"EXECUTION",e.detail))
            if occ.output is not None:
                return StepError(state,ErrorRecord(CORE_OUTPUT_CARDINALITY_ERROR,"EXECUTION"))
            occ.output=n
            self.productions.append(Production(occ.act,n))
            return StepNormal(state,None)

        return StepError(state,ErrorRecord("UNKNOWN_ACTION","EXECUTION"))

    def prepare(self):
        state=SemanticState.empty()
        for u in self.program.preparation:
            if isinstance(u,RPlaceInit):
                try:
                    n=self.eval_term(u.initializer,state,None,None)
                except TermFault as e:
                    return StepError(state,ErrorRecord(e.code,"PREPARATION",e.detail))
                state=state.establish(u.place,n)
            else:
                # act/role/body establishment is semantic metadata, not execution
                pass
        return StepNormal(state,None)

    def run(self):
        p=self.prepare()
        if isinstance(p,StepError):
            return ErrorOutcome(p.state,p.error,tuple(self.productions))
        if isinstance(p,StepDivergence):
            return DivergenceOutcome(tuple(self.productions))
        r=self.exec_action(self.program.principal,p.state,None,None)
        if isinstance(r,StepNormal):
            return NormalOutcome(r.state,tuple(self.productions))
        if isinstance(r,StepError):
            return ErrorOutcome(r.state,r.error,tuple(self.productions))
        return DivergenceOutcome(tuple(self.productions))

def observable(outcome):
    # Trace, occurrence tokens, stack shape and evaluator internals are intentionally absent.
    return outcome
