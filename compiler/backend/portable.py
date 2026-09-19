from __future__ import annotations
from dataclasses import dataclass
from compiler.models import ir as i

BACKEND_VERSION="portable-ir-vm-0.1-candidate-3"
IMPLEMENTATION_RESOURCE_EXHAUSTION="IMPLEMENTATION_RESOURCE_EXHAUSTION"
DEFAULT_MAX_ACTIVE_PERFORMANCES=None

@dataclass(frozen=True,slots=True)
class VMError: code:str; phase:str; detail:str=""
@dataclass(frozen=True,slots=True)
class VMProduct: occurrence:int; act:int; value:int
@dataclass(frozen=True,slots=True)
class VMNormal: facts:tuple[tuple[int,int],...]; products:tuple[VMProduct,...]; place_names:tuple[tuple[int,str],...]=(); act_names:tuple[tuple[int,str],...]=()
@dataclass(frozen=True,slots=True)
class VMErrorOutcome: facts:tuple[tuple[int,int],...]; error:VMError; products:tuple[VMProduct,...]; place_names:tuple[tuple[int,str],...]=(); act_names:tuple[tuple[int,str],...]=()
@dataclass(frozen=True,slots=True)
class VMDivergence: products:tuple[VMProduct,...]; place_names:tuple[tuple[int,str],...]=(); act_names:tuple[tuple[int,str],...]=()
@dataclass(frozen=True,slots=True)
class VMResourceExhaustion: facts:tuple[tuple[int,int],...]; products:tuple[VMProduct,...]; category:str=IMPLEMENTATION_RESOURCE_EXHAUSTION; detail:str="implementation activation budget exhausted"; place_names:tuple[tuple[int,str],...]=(); act_names:tuple[tuple[int,str],...]=()

@dataclass
class _Occ: token:int; act:int; roles:dict[int,int]; output:int|None=None
@dataclass(frozen=True)
class _Prov: token:int; act:int; output:int|None
@dataclass(frozen=True)
class _Then: remaining:tuple[i.IRAction,...]; occ:_Occ|None
@dataclass(frozen=True)
class _Clear: pass
@dataclass(frozen=True)
class _Fixed: remaining:int; action:i.IRAction; occ:_Occ|None
@dataclass(frozen=True)
class _Post: action:i.IRAction; proposition:i.IRProposition; occ:_Occ|None
@dataclass(frozen=True)
class _Perf: child:_Occ
class _Fault(Exception):
    def __init__(self,code,detail=""): self.code=code; self.detail=detail

class PortableVM:
    def __init__(self,program:i.IRProgram,*,fuel:int|None=None,max_active_performances:int|None=DEFAULT_MAX_ACTIVE_PERFORMANCES):
        if program.ir_version!=i.IR_VERSION: raise ValueError("unsupported IR version")
        self.p=program; self.fuel=fuel; self.next_occ=1; self.products=[]
        self.max_active_performances=max_active_performances; self.active_performances=0
        self.acts={a.act:a for a in program.acts}
        self.place_names=tuple(sorted((x.serial,x.spelling) for x in program.symbols if x.kind=="place"))
        self.act_names=tuple(sorted((x.serial,x.spelling) for x in program.symbols if x.kind=="act"))
    def consume(self):
        if self.fuel is None:return True
        if self.fuel<=0:return False
        self.fuel-=1;return True
    def number(self,n,state,occ,prov):
        if isinstance(n,i.IRNatural):return n.value
        if isinstance(n,i.IRReadCurrentFact):return state[n.place]
        if isinstance(n,i.IRReadRoleNumber):
            if occ is None or n.role not in occ.roles:raise _Fault("ROLE_VALUE_OUTSIDE_PERFORMANCE")
            return occ.roles[n.role]
        if isinstance(n,i.IRRecentResult):
            if prov is None or prov.act!=n.act or prov.output is None:raise _Fault("RESULT_PROVENANCE_ERROR")
            return prov.output
        if isinstance(n,i.IRAddNatural):return self.number(n.addend,state,occ,prov)+self.number(n.augend,state,occ,prov)
        if isinstance(n,i.IRCheckedSubtractNatural):
            a=self.number(n.amount,state,occ,prov);b=self.number(n.source,state,occ,prov)
            if a>b:raise _Fault(n.error_code,f"{b}-{a}")
            return b-a
        raise _Fault("INTERNAL_UNKNOWN_NUMBER")
    def holds(self,p,state,occ,prov):
        if isinstance(p,i.IREqualProposition):return self.number(p.left,state,occ,prov)==self.number(p.right,state,occ,prov)
        raise _Fault("INTERNAL_UNKNOWN_PROPOSITION")
    def action(self,a,state,occ=None,prov=None):
        frames=[]; current=a; cur=dict(state); current_occ=occ; current_prov=prov; step=None
        while True:
            if current is not None:
                if not self.consume(): step=("div",cur,None);current=None;continue
                x=current
                if isinstance(x,i.IRReplaceCurrentFact):
                    try:v=self.number(x.value,cur,current_occ,current_prov)
                    except _Fault as e:step=("err",cur,VMError(e.code,"EXECUTION",e.detail));current=None;continue
                    ns=dict(cur);ns[x.place]=v;step=("ok",ns,None);current=None;continue
                if isinstance(x,i.IRThen):
                    frames.append(_Then(tuple(x.actions[1:]),current_occ));current=x.actions[0];continue
                if isinstance(x,i.IRConditional):
                    try:yes=self.holds(x.proposition,cur,current_occ,current_prov)
                    except _Fault as e:step=("err",cur,VMError(e.code,"EXECUTION",e.detail));current=None;continue
                    frames.append(_Clear());current=x.if_holds if yes else x.if_not;continue
                if isinstance(x,i.IRFixedRecurrence):
                    frames.append(_Fixed(x.count-1,x.action,current_occ));current=x.action;current_prov=None;continue
                if isinstance(x,i.IRPostActionRecurrence):
                    frames.append(_Post(x.action,x.proposition,current_occ));current=x.action;current_prov=None;continue
                if isinstance(x,i.IRPerformAct):
                    try:vals={z.role:self.number(z.value,cur,current_occ,current_prov) for z in x.associations}
                    except _Fault as e:step=("err",cur,VMError(e.code,"EXECUTION",e.detail));current=None;continue
                    if self.max_active_performances is not None and self.active_performances>=self.max_active_performances:
                        step=("resource",cur,f"caller-imposed active performance budget {self.max_active_performances} exhausted");current=None;continue
                    child=_Occ(self.next_occ,x.act,vals);self.next_occ+=1;self.active_performances+=1
                    frames.append(_Perf(child));current=self.acts[x.act].body;current_occ=child;current_prov=None;continue
                if isinstance(x,i.IRProduceResult):
                    if current_occ is None:step=("err",cur,VMError("OUTPUT_OUTSIDE_PERFORMANCE","EXECUTION"));current=None;continue
                    try:v=self.number(x.value,cur,current_occ,current_prov)
                    except _Fault as e:step=("err",cur,VMError(e.code,"EXECUTION",e.detail));current=None;continue
                    if current_occ.output is not None:step=("err",cur,VMError("CORE_OUTPUT_CARDINALITY_ERROR","EXECUTION"))
                    else:
                        current_occ.output=v;self.products.append(VMProduct(current_occ.token,current_occ.act,v));step=("ok",dict(cur),None)
                    current=None;continue
                step=("err",cur,VMError("INTERNAL_UNKNOWN_ACTION","EXECUTION"));current=None;continue

            k,cur,z=step
            if k!="ok":return (k,cur,z)
            if not frames:return step
            frame=frames.pop()
            if isinstance(frame,_Then):
                if frame.remaining:
                    current_occ=frame.occ;current_prov=z;current=frame.remaining[0];frames.append(_Then(frame.remaining[1:],frame.occ));step=None;continue
                continue
            if isinstance(frame,_Clear):step=("ok",cur,None);continue
            if isinstance(frame,_Fixed):
                if frame.remaining>0:
                    current_occ=frame.occ;current_prov=None;current=frame.action;frames.append(_Fixed(frame.remaining-1,frame.action,frame.occ));step=None;continue
                step=("ok",cur,None);continue
            if isinstance(frame,_Post):
                try:stop=self.holds(frame.proposition,cur,frame.occ,z)
                except _Fault as e:step=("err",cur,VMError(e.code,"EXECUTION",e.detail));continue
                if stop:step=("ok",cur,None);continue
                current_occ=frame.occ;current_prov=None;current=frame.action;frames.append(frame);step=None;continue
            if isinstance(frame,_Perf):
                self.active_performances-=1; child=frame.child;step=("ok",cur,_Prov(child.token,child.act,child.output));continue
            return ("err",cur,VMError("INTERNAL_UNKNOWN_CONTINUATION","EXECUTION"))
    def run(self):
        state={}
        try:
            for x in self.p.initial_facts:
                try:v=self.number(x.value,state,None,None)
                except _Fault as e:return VMErrorOutcome(tuple(sorted(state.items())),VMError(e.code,"PREPARATION",e.detail),tuple(self.products),self.place_names,self.act_names)
                state[x.place]=v
            k,state,z=self.action(self.p.principal,state,None,None);facts=tuple(sorted(state.items()))
            if k=="ok":return VMNormal(facts,tuple(self.products),self.place_names,self.act_names)
            if k=="err":return VMErrorOutcome(facts,z,tuple(self.products),self.place_names,self.act_names)
            if k=="resource":return VMResourceExhaustion(facts,tuple(self.products),detail=z,place_names=self.place_names,act_names=self.act_names)
            return VMDivergence(tuple(self.products),self.place_names,self.act_names)
        except (MemoryError,RecursionError) as exc:
            return VMResourceExhaustion(tuple(sorted(state.items())),tuple(self.products),detail=type(exc).__name__,place_names=self.place_names,act_names=self.act_names)

def execute_ir(program:i.IRProgram,*,fuel:int|None=None,max_active_performances:int|None=DEFAULT_MAX_ACTIVE_PERFORMANCES):
    return PortableVM(program,fuel=fuel,max_active_performances=max_active_performances).run()
