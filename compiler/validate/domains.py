from __future__ import annotations

from dataclasses import dataclass

from compiler.models import hast as h
from compiler.models import ir as i
from compiler.models.domains import (
    BIDIRECTIONAL_INDEX, NATURAL, CollectionDomain, Domain, SymbolDomain,
    require_domain,
)
from compiler.diagnostics.catalog import (
    DOMAIN_COLLECTION_ELEMENT, DOMAIN_CONTRACT_INCOMPLETE,
    DOMAIN_EQUALITY_MISMATCH, DOMAIN_NATURAL_OPERATION,
    DOMAIN_OUTPUT_MISMATCH, DOMAIN_PLACE_INITIALIZER,
    DOMAIN_PLACE_REPLACEMENT, DOMAIN_PROGRAM_INPUT_CONTRACT,
    DOMAIN_RESULT_HEAD_MISMATCH, DOMAIN_ROLE_ASSOCIATION,
    DOMAIN_TYPED_REFERENCE, DOMAIN_UNRESOLVED_EXPRESSION,
)


def _diagnostic_code(semantic_code: str) -> str:
    if "UNRESOLVED_EXPRESSION" in semantic_code:
        return DOMAIN_UNRESOLVED_EXPRESSION
    if "PLACE_INITIALIZER" in semantic_code:
        return DOMAIN_PLACE_INITIALIZER
    if "PLACE_REPLACEMENT" in semantic_code:
        return DOMAIN_PLACE_REPLACEMENT
    if "ROLE_ASSOCIATION" in semantic_code:
        return DOMAIN_ROLE_ASSOCIATION
    if "OUTPUT" in semantic_code or semantic_code == "MIXED_OUTPUT_DOMAINS":
        return DOMAIN_OUTPUT_MISMATCH
    if "RESULT" in semantic_code:
        return DOMAIN_RESULT_HEAD_MISMATCH
    if "COLLECTION" in semantic_code:
        return DOMAIN_COLLECTION_ELEMENT
    if "PROGRAM_INPUT" in semantic_code:
        return DOMAIN_PROGRAM_INPUT_CONTRACT
    if "ARITHMETIC" in semantic_code:
        return DOMAIN_NATURAL_OPERATION
    if "EQUALITY" in semantic_code:
        return DOMAIN_EQUALITY_MISMATCH
    if "TYPED_HEAD" in semantic_code or "UNRESOLVED_PLACE" in semantic_code or "UNRESOLVED_ROLE" in semantic_code:
        return DOMAIN_TYPED_REFERENCE
    return DOMAIN_CONTRACT_INCOMPLETE


@dataclass(frozen=True, slots=True)
class DomainIssue:
    code: str
    diagnostic_code: str
    detail: str


class DomainValidationError(ValueError):
    def __init__(self, issue: DomainIssue):
        super().__init__(f"{issue.code}: {issue.detail}")
        self.issue = issue


def _fail(code: str, detail: str):
    raise DomainValidationError(DomainIssue(code, _diagnostic_code(code), detail))


def hast_value_domain(node: h.HastValue) -> Domain:
    if isinstance(node, h.HastNumber):
        return NATURAL
    if isinstance(node, h.HastSymbolValue):
        return SymbolDomain(node.domain_id)
    if isinstance(node, h.HastIndexValue):
        return BIDIRECTIONAL_INDEX
    if isinstance(node, h.HastCollectionValue):
        require_domain(node.element_domain)
        for item in node.items:
            if hast_value_domain(item) != node.element_domain:
                _fail("DOMAIN_COLLECTION_ELEMENT", "collection literal element has incompatible domain")
        return CollectionDomain(node.element_domain)
    if isinstance(node, h.HastCurrentValue):
        return require_domain(node.domain)
    if isinstance(node, h.HastCurrentRoleValue):
        return require_domain(node.domain)
    if isinstance(node, h.HastRecentTypedResult):
        return require_domain(node.domain)
    _fail("DOMAIN_UNRESOLVED_EXPRESSION", f"no independent domain for {type(node).__name__}")


def ir_value_domain(
    node: i.IRValue,
    *,
    place_domains: dict[int, Domain],
    role_domains: dict[int, Domain],
    output_domains: dict[int, Domain | None],
) -> Domain:
    if isinstance(node, i.IRNatural):
        return NATURAL
    if isinstance(node, i.IRReadCurrentFact):
        actual = place_domains.get(node.place)
        if actual != NATURAL:
            _fail("IR_DOMAIN_TYPED_HEAD", "numeric current-fact read requires a Natural place contract")
        return NATURAL
    if isinstance(node, i.IRReadRoleNumber):
        actual = role_domains.get(node.role)
        if actual != NATURAL:
            _fail("IR_DOMAIN_TYPED_HEAD", "numeric role read requires a Natural role contract")
        return NATURAL
    if isinstance(node, i.IRRecentResult):
        actual = output_domains.get(node.act)
        # Frozen B12 permits a structurally immediate numeric reference after
        # an act with no syntactic output site; execution then raises the
        # existing RESULT_PROVENANCE_ERROR.  Post-M2 typed heads are stricter.
        if actual is not None and actual != NATURAL:
            _fail("IR_DOMAIN_RESULT_HEAD", "numeric immediate-result read requires Natural act output")
        return NATURAL
    if isinstance(node, i.IRAddNatural):
        if ir_value_domain(node.addend, place_domains=place_domains, role_domains=role_domains, output_domains=output_domains) != NATURAL:
            _fail("IR_DOMAIN_ARITHMETIC", "Natural addition addend is not Natural")
        if ir_value_domain(node.augend, place_domains=place_domains, role_domains=role_domains, output_domains=output_domains) != NATURAL:
            _fail("IR_DOMAIN_ARITHMETIC", "Natural addition augend is not Natural")
        return NATURAL
    if isinstance(node, i.IRCheckedSubtractNatural):
        if ir_value_domain(node.amount, place_domains=place_domains, role_domains=role_domains, output_domains=output_domains) != NATURAL:
            _fail("IR_DOMAIN_ARITHMETIC", "Natural subtraction amount is not Natural")
        if ir_value_domain(node.source, place_domains=place_domains, role_domains=role_domains, output_domains=output_domains) != NATURAL:
            _fail("IR_DOMAIN_ARITHMETIC", "Natural subtraction source is not Natural")
        return NATURAL
    if isinstance(node, i.IRSymbolValue):
        return SymbolDomain(node.domain_id)
    if isinstance(node, i.IRIndexValue):
        return BIDIRECTIONAL_INDEX
    if isinstance(node, i.IRCollectionValue):
        require_domain(node.element_domain)
        for item in node.items:
            if ir_value_domain(item, place_domains=place_domains, role_domains=role_domains, output_domains=output_domains) != node.element_domain:
                _fail("IR_DOMAIN_COLLECTION_ELEMENT", "collection element metadata is incompatible with its value domain")
        return CollectionDomain(node.element_domain)
    if isinstance(node, i.IRReadCurrentValue):
        actual = place_domains.get(node.place)
        if actual is None:
            _fail("IR_DOMAIN_UNRESOLVED_PLACE", "typed current-value read references a place without a domain contract")
        if actual != node.domain:
            _fail("IR_DOMAIN_TYPED_HEAD", "typed current-value head disagrees with the place domain")
        return actual
    if isinstance(node, i.IRReadRoleValue):
        actual = role_domains.get(node.role)
        if actual is None:
            _fail("IR_DOMAIN_UNRESOLVED_ROLE", "typed role read references a role without a domain contract")
        if actual != node.domain:
            _fail("IR_DOMAIN_TYPED_HEAD", "typed role head disagrees with the role domain")
        return actual
    if isinstance(node, i.IRRecentTypedResult):
        actual = output_domains.get(node.act)
        if actual is None:
            _fail("IR_DOMAIN_RESULT_NONE", "typed immediate-result read references an act without an output domain")
        if actual != node.domain:
            _fail("IR_DOMAIN_RESULT_HEAD", "typed immediate-result head disagrees with act output domain")
        return actual
    _fail("IR_DOMAIN_UNRESOLVED_EXPRESSION", f"no independent domain for {type(node).__name__}")


def validate_hast_domains(program: h.HastCoreProgram) -> None:
    places = {x.place: require_domain(x.domain) for x in program.place_domains}
    roles = {x.role: require_domain(x.domain) for x in program.role_domains}
    outputs = {x.act: None if x.domain is None else require_domain(x.domain) for x in program.act_output_domains}

    if set(places) != set(program.places):
        _fail("DOMAIN_PLACE_CONTRACT", "every place requires exactly one static domain contract")
    if set(roles) != set(program.roles):
        _fail("DOMAIN_ROLE_CONTRACT", "every role requires exactly one static domain contract")
    if set(outputs) != set(program.acts):
        _fail("DOMAIN_OUTPUT_CONTRACT", "every act requires an explicit none-or-domain output contract")
    if len(program.program_input_domains) != len({x.input_id for x in program.program_input_domains}):
        _fail("DOMAIN_PROGRAM_INPUT_DUPLICATE", "duplicate Program Input identity")
    for x in program.program_input_domains:
        require_domain(x.domain)

    def value(node: h.HastValue) -> Domain:
        d = hast_value_domain(node)
        if isinstance(node, h.HastCurrentFact):
            if places.get(node.place) != NATURAL:
                _fail("DOMAIN_TYPED_HEAD", "numeric current-fact reference requires a Natural place")
        elif isinstance(node, h.HastCurrentValue):
            if places.get(node.place) != node.domain:
                _fail("DOMAIN_TYPED_HEAD", "typed current-value reference disagrees with the place contract")
        elif isinstance(node, h.HastCurrentRoleNumber):
            if roles.get(node.role) != NATURAL:
                _fail("DOMAIN_TYPED_HEAD", "numeric role reference requires a Natural role")
        elif isinstance(node, h.HastCurrentRoleValue):
            if roles.get(node.role) != node.domain:
                _fail("DOMAIN_TYPED_HEAD", "typed role reference disagrees with the role contract")
        elif isinstance(node, h.HastRecentResult):
            actual_output = outputs.get(node.act)
            if actual_output is not None and actual_output != NATURAL:
                _fail("DOMAIN_RESULT_HEAD", "numeric immediate-result reference requires Natural output")
        elif isinstance(node, h.HastRecentTypedResult):
            if outputs.get(node.act) != node.domain:
                _fail("DOMAIN_RESULT_HEAD", "typed immediate-result reference disagrees with act output domain")
        if isinstance(node, h.HastAddNatural):
            if value(node.addend) != NATURAL or value(node.augend) != NATURAL:
                _fail("DOMAIN_ARITHMETIC", "Natural addition operands must independently resolve to Natural")
        if isinstance(node, h.HastSubtractNatural):
            if value(node.amount) != NATURAL or value(node.source) != NATURAL:
                _fail("DOMAIN_ARITHMETIC", "Natural subtraction operands must independently resolve to Natural")
        if isinstance(node, h.HastCollectionValue):
            for item in node.items:
                value(item)
        return d

    def action(node: h.HastExecutable, current_act=None) -> None:
        if isinstance(node, h.HastReplaceCurrentFact):
            actual = value(node.value)
            if places.get(node.place) != actual:
                _fail("DOMAIN_PLACE_REPLACEMENT", "replacement value domain does not equal the fixed place domain")
        elif isinstance(node, h.HastPerformAct):
            for assoc in node.associations:
                actual = value(assoc.value)
                if roles.get(assoc.role) != actual:
                    _fail("DOMAIN_ROLE_ASSOCIATION", "role association value domain does not equal the declared role domain")
        elif isinstance(node, h.HastProduceResult):
            actual = value(node.value)
            expected = outputs.get(current_act)
            if expected is None or expected != actual:
                _fail("MIXED_OUTPUT_DOMAINS", "result production disagrees with the act's static output domain")
        elif isinstance(node, h.HastThen):
            for x in node.actions:
                action(x, current_act)
        elif isinstance(node, h.HastConditional):
            if isinstance(node.proposition, h.HastEqualProposition):
                if value(node.proposition.left) != NATURAL or value(node.proposition.right) != NATURAL:
                    _fail("DOMAIN_EQUALITY", "Core numeric equality remains Natural-specialized")
            action(node.if_holds, current_act)
            action(node.if_not, current_act)
        elif isinstance(node, (h.HastFixedRecurrence, h.HastPostActionRecurrence)):
            action(node.action, current_act)

    for prep in program.preparation:
        if isinstance(prep, h.HastPlaceIntroduction):
            if value(prep.initial_fact) != places[prep.place]:
                _fail("DOMAIN_PLACE_INITIALIZER", "place initializer domain does not equal the fixed place domain")
        elif isinstance(prep, h.HastActBody):
            action(prep.body, prep.act)
    action(program.principal, None)


__all__ = [
    "DomainIssue", "DomainValidationError", "hast_value_domain", "ir_value_domain",
    "validate_hast_domains",
]
