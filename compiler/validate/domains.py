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
    if isinstance(node, (h.HastIndexSuccessor, h.HastIndexPredecessor)):
        if hast_value_domain(node.operand) != BIDIRECTIONAL_INDEX:
            _fail("DOMAIN_INDEX_OPERAND", "BidirectionalIndex successor/predecessor operand is not BidirectionalIndex")
        return BIDIRECTIONAL_INDEX
    if isinstance(node, h.HastCollectionValue):
        require_domain(node.element_domain)
        for item in node.items:
            if hast_value_domain(item) != node.element_domain:
                _fail("DOMAIN_COLLECTION_ELEMENT", "collection literal element has incompatible domain")
        return CollectionDomain(node.element_domain)
    if isinstance(node, h.HastCollectionAppend):
        require_domain(node.element_domain)
        if hast_value_domain(node.collection) != CollectionDomain(node.element_domain):
            _fail("DOMAIN_COLLECTION_APPEND", "append source book has a different element domain")
        if hast_value_domain(node.item) != node.element_domain:
            _fail("DOMAIN_COLLECTION_ELEMENT", "append item has a different element domain")
        return CollectionDomain(node.element_domain)
    if isinstance(node, h.HastCollectionCount):
        if not isinstance(hast_value_domain(node.collection), CollectionDomain):
            _fail("DOMAIN_COLLECTION_COUNT", "count operand is not a Collection")
        return NATURAL
    if isinstance(node, h.HastCollectionSelectNatural):
        if hast_value_domain(node.collection) != CollectionDomain(NATURAL):
            _fail("DOMAIN_COLLECTION_SELECT", "Natural element head requires Collection<Natural>")
        if node.position is not None and hast_value_domain(node.position) != NATURAL:
            _fail("DOMAIN_COLLECTION_POSITION", "Collection position must independently be Natural")
        return NATURAL
    if isinstance(node, h.HastCollectionSelectValue):
        require_domain(node.element_domain)
        if hast_value_domain(node.collection) != CollectionDomain(node.element_domain):
            _fail("DOMAIN_COLLECTION_SELECT", "typed element head disagrees with the book element domain")
        if node.position is not None and hast_value_domain(node.position) != NATURAL:
            _fail("DOMAIN_COLLECTION_POSITION", "Collection position must independently be Natural")
        return node.element_domain
    if isinstance(node, h.HastCollectionOrder):
        require_domain(node.element_domain)
        if hast_value_domain(node.collection) != CollectionDomain(node.element_domain):
            _fail("DOMAIN_COLLECTION_ORDER", "Collection order profile disagrees with the book element domain")
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
    if isinstance(node, (i.IRIndexSuccessor, i.IRIndexPredecessor)):
        if ir_value_domain(node.operand, place_domains=place_domains, role_domains=role_domains, output_domains=output_domains) != BIDIRECTIONAL_INDEX:
            _fail("IR_DOMAIN_INDEX_OPERAND", "BidirectionalIndex successor/predecessor operand is not BidirectionalIndex")
        return BIDIRECTIONAL_INDEX
    if isinstance(node, i.IRCollectionValue):
        require_domain(node.element_domain)
        for item in node.items:
            if ir_value_domain(item, place_domains=place_domains, role_domains=role_domains, output_domains=output_domains) != node.element_domain:
                _fail("IR_DOMAIN_COLLECTION_ELEMENT", "collection element metadata is incompatible with its value domain")
        return CollectionDomain(node.element_domain)
    if isinstance(node, i.IRCollectionAppend):
        require_domain(node.element_domain)
        if ir_value_domain(node.collection, place_domains=place_domains, role_domains=role_domains, output_domains=output_domains) != CollectionDomain(node.element_domain):
            _fail("IR_DOMAIN_COLLECTION_APPEND", "append source book has a different element domain")
        if ir_value_domain(node.item, place_domains=place_domains, role_domains=role_domains, output_domains=output_domains) != node.element_domain:
            _fail("IR_DOMAIN_COLLECTION_ELEMENT", "append item has a different element domain")
        return CollectionDomain(node.element_domain)
    if isinstance(node, i.IRCollectionCount):
        if not isinstance(ir_value_domain(node.collection, place_domains=place_domains, role_domains=role_domains, output_domains=output_domains), CollectionDomain):
            _fail("IR_DOMAIN_COLLECTION_COUNT", "count operand is not a Collection")
        return NATURAL
    if isinstance(node, i.IRCollectionSelectNatural):
        if ir_value_domain(node.collection, place_domains=place_domains, role_domains=role_domains, output_domains=output_domains) != CollectionDomain(NATURAL):
            _fail("IR_DOMAIN_COLLECTION_SELECT", "Natural element head requires Collection<Natural>")
        if node.position is not None and ir_value_domain(node.position, place_domains=place_domains, role_domains=role_domains, output_domains=output_domains) != NATURAL:
            _fail("IR_DOMAIN_COLLECTION_POSITION", "Collection position must be Natural")
        return NATURAL
    if isinstance(node, i.IRCollectionSelectValue):
        require_domain(node.element_domain)
        if ir_value_domain(node.collection, place_domains=place_domains, role_domains=role_domains, output_domains=output_domains) != CollectionDomain(node.element_domain):
            _fail("IR_DOMAIN_COLLECTION_SELECT", "typed element head disagrees with the book element domain")
        if node.position is not None and ir_value_domain(node.position, place_domains=place_domains, role_domains=role_domains, output_domains=output_domains) != NATURAL:
            _fail("IR_DOMAIN_COLLECTION_POSITION", "Collection position must be Natural")
        return node.element_domain
    if isinstance(node, i.IRCollectionOrder):
        require_domain(node.element_domain)
        if ir_value_domain(node.collection, place_domains=place_domains, role_domains=role_domains, output_domains=output_domains) != CollectionDomain(node.element_domain):
            _fail("IR_DOMAIN_COLLECTION_ORDER", "Collection order profile disagrees with the book element domain")
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
    place_ids = [x.place for x in program.place_domains]
    role_ids = [x.role for x in program.role_domains]
    output_ids = [x.act for x in program.act_output_domains]
    input_ids = [x.input_id for x in program.program_input_domains]

    if len(place_ids) != len(set(place_ids)):
        _fail("DOMAIN_PLACE_CONTRACT", "duplicate place domain contract")
    if len(role_ids) != len(set(role_ids)):
        _fail("DOMAIN_ROLE_CONTRACT", "duplicate role domain contract")
    if len(output_ids) != len(set(output_ids)):
        _fail("DOMAIN_OUTPUT_CONTRACT", "duplicate act output-domain contract")
    if len(input_ids) != len(set(input_ids)):
        _fail("DOMAIN_PROGRAM_INPUT_DUPLICATE", "duplicate Program Input domain contract")

    symbol_domain_nodes = [x for x in program.preparation if isinstance(x, h.HastSymbolDomainDeclaration)]
    symbol_member_nodes = [x for x in program.preparation if isinstance(x, h.HastSymbolMemberDeclaration)]
    symbol_order_nodes = [x for x in program.preparation if isinstance(x, h.HastSymbolOrderAdjacent)]
    domain_ids = [x.domain_id for x in symbol_domain_nodes]
    if len(domain_ids) != len(set(domain_ids)):
        _fail("DOMAIN_SYMBOL_DECLARATION", "duplicate Symbol domain declaration")
    declared_domains = set(domain_ids)
    member_keys = [(x.domain_id, x.member_id) for x in symbol_member_nodes]
    if len(member_keys) != len(set(member_keys)):
        _fail("DOMAIN_SYMBOL_MEMBER", "duplicate Symbol member identity")
    member_labels = {}
    members_by_domain = {}
    for x in symbol_member_nodes:
        if x.domain_id not in declared_domains:
            _fail("DOMAIN_SYMBOL_MEMBER", "Symbol member belongs to an undeclared domain")
        if not x.external_label:
            _fail("DOMAIN_SYMBOL_MEMBER", "Symbol member canonical external label is empty")
        member_labels[(x.domain_id, x.member_id)] = x.external_label
        members_by_domain.setdefault(x.domain_id, set()).add(x.member_id)

    edges_by_domain = {}
    for x in symbol_order_nodes:
        if x.domain_id not in declared_domains:
            _fail("DOMAIN_SYMBOL_ORDER", "Symbol order references undeclared domain")
        members = members_by_domain.get(x.domain_id, set())
        if x.before_member_id not in members or x.after_member_id not in members:
            _fail("DOMAIN_SYMBOL_ORDER", "Symbol order references unknown member")
        if x.before_member_id == x.after_member_id:
            _fail("DOMAIN_SYMBOL_ORDER", "Symbol order self edge")
        edges_by_domain.setdefault(x.domain_id, []).append((x.before_member_id, x.after_member_id))
    for domain_id, edges in edges_by_domain.items():
        if len(edges) != len(set(edges)):
            _fail("DOMAIN_SYMBOL_ORDER", "duplicate Symbol adjacency fact")
        members = members_by_domain.get(domain_id, set())
        outgoing = {}
        incoming = {}
        for before, after in edges:
            if before in outgoing or after in incoming:
                _fail("DOMAIN_SYMBOL_ORDER", "Symbol order contains fork or merge")
            outgoing[before] = after
            incoming[after] = before
        if len(edges) != max(0, len(members)-1):
            _fail("DOMAIN_SYMBOL_ORDER", "Symbol order profile is incomplete")
        starts = [m for m in members if m not in incoming]
        if len(starts) != 1:
            _fail("DOMAIN_SYMBOL_ORDER", "Symbol order does not have exactly one chain start")
        seen=set(); cur=starts[0]
        while cur not in seen:
            seen.add(cur)
            if cur not in outgoing:
                break
            cur=outgoing[cur]
        if seen != members:
            _fail("DOMAIN_SYMBOL_ORDER", "Symbol order is cyclic or disconnected")

    places = {x.place: require_domain(x.domain) for x in program.place_domains}
    roles = {x.role: require_domain(x.domain) for x in program.role_domains}
    outputs = {x.act: None if x.domain is None else require_domain(x.domain) for x in program.act_output_domains}

    if set(places) != set(program.places):
        _fail("DOMAIN_PLACE_CONTRACT", "every place requires exactly one static domain contract")
    if set(roles) != set(program.roles):
        _fail("DOMAIN_ROLE_CONTRACT", "every role requires exactly one static domain contract")
    if set(outputs) != set(program.acts):
        _fail("DOMAIN_OUTPUT_CONTRACT", "every act requires an explicit none-or-domain output contract")
    for x in program.program_input_domains:
        require_domain(x.domain)

    def value(node: h.HastValue) -> Domain:
        d = hast_value_domain(node)
        if isinstance(node, h.HastSymbolValue):
            expected_label = member_labels.get((node.domain_id, node.member_id))
            if expected_label is None:
                _fail("DOMAIN_SYMBOL_VALUE", "Symbol Value references undeclared domain/member identity")
            if expected_label != node.external_label:
                _fail("DOMAIN_SYMBOL_LABEL", "Symbol Value label does not match declared canonical member label")
        elif isinstance(node, (h.HastIndexSuccessor, h.HastIndexPredecessor)):
            if value(node.operand) != BIDIRECTIONAL_INDEX:
                _fail("DOMAIN_INDEX_OPERAND", "Index successor/predecessor requires BidirectionalIndex operand")
        elif isinstance(node, h.HastCurrentFact):
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
        if isinstance(node, h.HastCollectionAppend):
            value(node.collection)
            value(node.item)
        if isinstance(node, h.HastCollectionCount):
            value(node.collection)
        if isinstance(node, (h.HastCollectionSelectNatural, h.HastCollectionSelectValue)):
            value(node.collection)
            if node.position is not None:
                value(node.position)
        if isinstance(node, h.HastCollectionOrder):
            value(node.collection)
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
            elif isinstance(node.proposition, h.HastNaturalGTProposition):
                if value(node.proposition.left) != NATURAL or value(node.proposition.right) != NATURAL:
                    _fail("DOMAIN_NATURAL_GT", "Natural strict ordering requires two independently Natural operands")
            elif isinstance(node.proposition, h.HastSymbolEqualProposition):
                left_domain=value(node.proposition.left)
                right_domain=value(node.proposition.right)
                expected=SymbolDomain(node.proposition.domain_id)
                if left_domain != expected or right_domain != expected:
                    _fail("DOMAIN_SYMBOL_EQUALITY", "Symbol equality operands must belong to the same declared Symbol domain")
            elif isinstance(node.proposition, h.HastCollectionMembershipProposition):
                collection_domain=value(node.proposition.collection)
                item_domain=value(node.proposition.item)
                expected=CollectionDomain(node.proposition.element_domain)
                if collection_domain != expected or item_domain != node.proposition.element_domain:
                    _fail("DOMAIN_COLLECTION_MEMBERSHIP", "membership operands do not share the book element domain")
            else:
                _fail("DOMAIN_PROPOSITION", f"unsupported proposition {type(node.proposition).__name__}")
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
