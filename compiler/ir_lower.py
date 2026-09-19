from __future__ import annotations
from compiler.models import hast as h
from compiler.models import ir as i

def num(n:h.HastNumber)->i.IRNumber:
    if isinstance(n,h.HastExactNatural): return i.IRNatural(n.source_span,n.value)
    if isinstance(n,h.HastCurrentFact): return i.IRReadCurrentFact(n.source_span,n.place.serial)
    if isinstance(n,h.HastCurrentRoleNumber): return i.IRReadRoleNumber(n.source_span,n.role.serial)
    if isinstance(n,h.HastRecentResult): return i.IRRecentResult(n.source_span,n.act.serial)
    if isinstance(n,h.HastAddNatural): return i.IRAddNatural(n.source_span,num(n.addend),num(n.augend))
    if isinstance(n,h.HastSubtractNatural): return i.IRCheckedSubtractNatural(n.source_span,num(n.amount),num(n.source))
    raise TypeError(type(n).__name__)

def prop(p:h.HastProposition)->i.IRProposition:
    if isinstance(p,h.HastEqualProposition): return i.IREqualProposition(p.source_span,num(p.left),num(p.right))
    raise TypeError(type(p).__name__)

def action(a:h.HastExecutable)->i.IRAction:
    if isinstance(a,h.HastReplaceCurrentFact): return i.IRReplaceCurrentFact(a.source_span,a.place.serial,num(a.value))
    if isinstance(a,h.HastPerformAct): return i.IRPerformAct(a.source_span,a.act.serial,tuple(i.IRRoleAssociation(x.source_span,x.role.serial,num(x.value)) for x in a.associations))
    if isinstance(a,h.HastProduceResult): return i.IRProduceResult(a.source_span,num(a.value))
    if isinstance(a,h.HastThen): return i.IRThen(a.source_span,tuple(action(x) for x in a.actions))
    if isinstance(a,h.HastConditional): return i.IRConditional(a.source_span,prop(a.proposition),action(a.if_holds),action(a.if_not))
    if isinstance(a,h.HastFixedRecurrence): return i.IRFixedRecurrence(a.source_span,a.count,action(a.action))
    if isinstance(a,h.HastPostActionRecurrence): return i.IRPostActionRecurrence(a.source_span,action(a.action),prop(a.proposition))
    raise TypeError(type(a).__name__)

def lower_validated_hast(program:h.HastCoreProgram)->i.IRProgram:
    symbols=[]
    for p in program.places: symbols.append(i.IRSymbol(program.source_span,"place",p.serial,p.spelling,None))
    for a in program.acts: symbols.append(i.IRSymbol(program.source_span,"act",a.serial,a.spelling,None))
    for r in program.roles: symbols.append(i.IRSymbol(program.source_span,"role",r.serial,r.spelling,r.owner.serial))
    inits=tuple(i.IRInitialFact(x.source_span,x.place.serial,num(x.initial_fact)) for x in program.preparation if isinstance(x,h.HastPlaceIntroduction))
    body={x.act:x for x in program.preparation if isinstance(x,h.HastActBody)}
    acts=tuple(i.IRActDefinition(body[a].source_span,a.serial,tuple(r.serial for r in program.roles if r.owner==a),action(body[a].body)) for a in program.acts)
    return i.IRProgram(program.source_span,i.IR_VERSION,tuple(sorted(symbols,key=lambda s:s.serial)),inits,acts,action(program.principal))

__all__=["lower_validated_hast"]
