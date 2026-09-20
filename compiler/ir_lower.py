from __future__ import annotations

from compiler.models import hast as h
from compiler.models import ir as i
from compiler.validate.domains import validate_hast_domains


def value(n: h.HastValue) -> i.IRValue:
    if isinstance(n, h.HastExactNatural):
        return i.IRNatural(n.source_span, n.value)
    if isinstance(n, h.HastSymbolValue):
        return i.IRSymbolValue(n.source_span, n.domain_id, n.member_id, n.external_label)
    if isinstance(n, h.HastIndexValue):
        return i.IRIndexValue(n.source_span, n.side, n.magnitude)
    if isinstance(n, h.HastCollectionValue):
        return i.IRCollectionValue(n.source_span, n.element_domain, tuple(value(x) for x in n.items))
    if isinstance(n, h.HastIndexSuccessor):
        return i.IRIndexSuccessor(n.source_span, value(n.operand))
    if isinstance(n, h.HastIndexPredecessor):
        return i.IRIndexPredecessor(n.source_span, value(n.operand))
    if isinstance(n, h.HastCurrentFact):
        return i.IRReadCurrentFact(n.source_span, n.place.serial)
    if isinstance(n, h.HastCurrentValue):
        return i.IRReadCurrentValue(n.source_span, n.place.serial, n.domain)
    if isinstance(n, h.HastCurrentRoleNumber):
        return i.IRReadRoleNumber(n.source_span, n.role.serial)
    if isinstance(n, h.HastCurrentRoleValue):
        return i.IRReadRoleValue(n.source_span, n.role.serial, n.domain)
    if isinstance(n, h.HastRecentResult):
        return i.IRRecentResult(n.source_span, n.act.serial)
    if isinstance(n, h.HastRecentTypedResult):
        return i.IRRecentTypedResult(n.source_span, n.act.serial, n.domain)
    if isinstance(n, h.HastAddNatural):
        return i.IRAddNatural(n.source_span, num(n.addend), num(n.augend))
    if isinstance(n, h.HastSubtractNatural):
        return i.IRCheckedSubtractNatural(n.source_span, num(n.amount), num(n.source))
    raise TypeError(type(n).__name__)


def num(n: h.HastNumber) -> i.IRNumber:
    out = value(n)
    if not isinstance(out, i.IRNumber):
        raise TypeError("Natural expression lowered to non-Natural IR value")
    return out


def prop(p: h.HastProposition) -> i.IRProposition:
    if isinstance(p, h.HastEqualProposition):
        return i.IREqualProposition(p.source_span, num(p.left), num(p.right))
    if isinstance(p, h.HastNaturalGTProposition):
        return i.IRNaturalGTProposition(p.source_span, num(p.left), num(p.right))
    if isinstance(p, h.HastSymbolEqualProposition):
        return i.IRSymbolEqualProposition(p.source_span, value(p.left), value(p.right), p.domain_id)
    raise TypeError(type(p).__name__)


def action(a: h.HastExecutable) -> i.IRAction:
    if isinstance(a, h.HastReplaceCurrentFact):
        return i.IRReplaceCurrentFact(a.source_span, a.place.serial, value(a.value))
    if isinstance(a, h.HastPerformAct):
        return i.IRPerformAct(
            a.source_span, a.act.serial,
            tuple(i.IRRoleAssociation(x.source_span, x.role.serial, value(x.value)) for x in a.associations),
        )
    if isinstance(a, h.HastProduceResult):
        return i.IRProduceResult(a.source_span, value(a.value))
    if isinstance(a, h.HastThen):
        return i.IRThen(a.source_span, tuple(action(x) for x in a.actions))
    if isinstance(a, h.HastConditional):
        return i.IRConditional(a.source_span, prop(a.proposition), action(a.if_holds), action(a.if_not))
    if isinstance(a, h.HastFixedRecurrence):
        return i.IRFixedRecurrence(a.source_span, a.count, action(a.action))
    if isinstance(a, h.HastPostActionRecurrence):
        return i.IRPostActionRecurrence(a.source_span, action(a.action), prop(a.proposition))
    raise TypeError(type(a).__name__)


def lower_validated_hast(program: h.HastCoreProgram) -> i.IRProgram:
    validate_hast_domains(program)
    symbols = []
    for p in program.places:
        symbols.append(i.IRSymbol(program.source_span, "place", p.serial, p.spelling, None))
    for a in program.acts:
        symbols.append(i.IRSymbol(program.source_span, "act", a.serial, a.spelling, None))
    for r in program.roles:
        symbols.append(i.IRSymbol(program.source_span, "role", r.serial, r.spelling, r.owner.serial))
    inits = tuple(
        i.IRInitialFact(x.source_span, x.place.serial, value(x.initial_fact))
        for x in program.preparation if isinstance(x, h.HastPlaceIntroduction)
    )
    body = {x.act: x for x in program.preparation if isinstance(x, h.HastActBody)}
    acts = tuple(
        i.IRActDefinition(
            body[a].source_span, a.serial,
            tuple(r.serial for r in program.roles if r.owner == a),
            action(body[a].body),
        )
        for a in program.acts
    )
    return i.IRProgram(
        program.source_span,
        i.IR_VERSION,
        tuple(sorted(symbols, key=lambda s: s.serial)),
        inits,
        acts,
        action(program.principal),
        tuple(i.IRPlaceDomain(program.source_span, x.place.serial, x.domain) for x in program.place_domains),
        tuple(i.IRRoleDomain(program.source_span, x.role.serial, x.domain) for x in program.role_domains),
        tuple(i.IRActOutputDomain(program.source_span, x.act.serial, x.domain) for x in program.act_output_domains),
        tuple(i.IRProgramInputDomain(program.source_span, x.input_id, x.domain) for x in program.program_input_domains),
        tuple(i.IRSymbolDomainDeclaration(x.source_span, x.domain_id) for x in program.preparation if isinstance(x, h.HastSymbolDomainDeclaration)),
        tuple(i.IRSymbolMemberDeclaration(x.source_span, x.domain_id, x.member_id, x.external_label) for x in program.preparation if isinstance(x, h.HastSymbolMemberDeclaration)),
        tuple(i.IRSymbolOrderAdjacent(x.source_span, x.domain_id, x.before_member_id, x.after_member_id) for x in program.preparation if isinstance(x, h.HastSymbolOrderAdjacent)),
    )


__all__ = ["value", "num", "action", "lower_validated_hast"]
