"""Source-independent semantic validation for decoded canonical Marak IR."""
from __future__ import annotations

from dataclasses import dataclass

from compiler.models import ir as i
from compiler.models.domains import NATURAL, BIDIRECTIONAL_INDEX, CollectionDomain, Domain, SymbolDomain, require_domain
from compiler.validate.domains import DomainValidationError, ir_value_domain


@dataclass(frozen=True, slots=True)
class CanonicalIRIssue:
    code: str
    detail: str


class CanonicalIRValidationError(ValueError):
    def __init__(self, issue: CanonicalIRIssue):
        super().__init__(f"{issue.code}: {issue.detail}")
        self.issue = issue


def _fail(code: str, detail: str) -> None:
    raise CanonicalIRValidationError(CanonicalIRIssue(code, detail))


def _constant_natural(node: i.IRValue) -> int | None:
    if isinstance(node, i.IRNatural):
        return node.value
    if isinstance(node, i.IRAddNatural):
        a, b = _constant_natural(node.addend), _constant_natural(node.augend)
        return None if a is None or b is None else a + b
    if isinstance(node, i.IRCheckedSubtractNatural):
        amount, source = _constant_natural(node.amount), _constant_natural(node.source)
        if amount is None or source is None:
            return None
        if amount > source:
            _fail("IR_STATIC_ARITHMETIC_DOMAIN", f"constant Natural subtraction {source}-{amount} is out of domain")
        return source - amount
    return None


def validate_canonical_ir(program: i.IRProgram) -> None:
    if not isinstance(program, i.IRProgram):
        _fail("IR_NOT_PROGRAM", "payload is not IRProgram")
    if program.ir_version != i.IR_VERSION:
        _fail("IR_VERSION", "program IR version does not match this compiler")

    by = {s.serial: s for s in program.symbols}
    places = {s.serial for s in program.symbols if s.kind == "place"}
    acts = {s.serial for s in program.symbols if s.kind == "act"}
    roles = {s.serial for s in program.symbols if s.kind == "role"}
    role_owner = {s.serial: s.owner for s in program.symbols if s.kind == "role"}
    act_defs = {a.act: a for a in program.acts}

    def contract_map(records, attr: str, expected: set[int], code: str) -> dict[int, Domain]:
        keys = [getattr(x, attr) for x in records]
        if len(keys) != len(set(keys)) or set(keys) != expected:
            _fail(code, "domain contracts must cover each resolved identity exactly once")
        out = {}
        for x in records:
            try:
                out[getattr(x, attr)] = require_domain(x.domain)
            except TypeError as exc:
                _fail(code, str(exc))
        return out

    place_domains = contract_map(program.place_domains, "place", places, "IR_PLACE_DOMAIN_CONTRACT")
    role_domains = contract_map(program.role_domains, "role", roles, "IR_ROLE_DOMAIN_CONTRACT")

    output_ids = [x.act for x in program.act_output_domains]
    if len(output_ids) != len(set(output_ids)) or set(output_ids) != acts:
        _fail("IR_OUTPUT_DOMAIN_CONTRACT", "every act requires exactly one none-or-domain output contract")
    output_domains: dict[int, Domain | None] = {}
    for x in program.act_output_domains:
        if x.domain is None:
            output_domains[x.act] = None
        else:
            try:
                output_domains[x.act] = require_domain(x.domain)
            except TypeError as exc:
                _fail("IR_OUTPUT_DOMAIN_CONTRACT", str(exc))

    input_ids = [x.input_id for x in program.program_input_domains]
    if len(input_ids) != len(set(input_ids)):
        _fail("IR_PROGRAM_INPUT_DOMAIN_CONTRACT", "duplicate Program Input identity")
    for x in program.program_input_domains:
        if x.input_id.serial <= 0 or not x.input_id.spelling:
            _fail("IR_PROGRAM_INPUT_DOMAIN_CONTRACT", "invalid Program Input identity")
        try:
            require_domain(x.domain)
        except TypeError as exc:
            _fail("IR_PROGRAM_INPUT_DOMAIN_CONTRACT", str(exc))

    domain_ids=[x.domain_id for x in program.symbol_domains]
    if len(domain_ids)!=len(set(domain_ids)):
        _fail("IR_SYMBOL_DOMAIN_DUPLICATE","duplicate Symbol domain declaration")
    declared_symbol_domains=set(domain_ids)
    for d in declared_symbol_domains:
        if d.serial<=0 or not d.spelling:
            _fail("IR_SYMBOL_DOMAIN_ID","invalid Symbol domain identity")
    member_keys=[(x.domain_id,x.member_id) for x in program.symbol_members]
    if len(member_keys)!=len(set(member_keys)):
        _fail("IR_SYMBOL_MEMBER_DUPLICATE","duplicate Symbol member identity in domain")
    member_labels={}
    members_by_domain={}
    for m in program.symbol_members:
        if m.domain_id not in declared_symbol_domains:
            _fail("IR_SYMBOL_MEMBER_DOMAIN","Symbol member belongs to undeclared domain")
        if m.member_id.serial<=0 or not m.member_id.spelling or not m.external_label:
            _fail("IR_SYMBOL_MEMBER_METADATA","invalid Symbol member metadata")
        member_labels[(m.domain_id,m.member_id)]=m.external_label
        members_by_domain.setdefault(m.domain_id,set()).add(m.member_id)

    edges_by_domain={}
    for edge in program.symbol_order_edges:
        members=members_by_domain.get(edge.domain_id)
        if members is None or edge.before_member_id not in members or edge.after_member_id not in members:
            _fail("IR_SYMBOL_ORDER_MEMBER","Symbol order references unknown domain/member")
        if edge.before_member_id==edge.after_member_id:
            _fail("IR_SYMBOL_ORDER_SELF","Symbol order self edge")
        edges_by_domain.setdefault(edge.domain_id,[]).append((edge.before_member_id,edge.after_member_id))
    complete_order_domains=set()
    for domain_id,edges in edges_by_domain.items():
        if len(edges)!=len(set(edges)):
            _fail("IR_SYMBOL_ORDER_DUPLICATE","duplicate Symbol adjacency")
        members=members_by_domain[domain_id]; outgoing={}; incoming={}
        for before,after in edges:
            if before in outgoing or after in incoming:
                _fail("IR_SYMBOL_ORDER_FORK","Symbol order fork/merge")
            outgoing[before]=after; incoming[after]=before
        if len(edges)!=max(0,len(members)-1):
            _fail("IR_SYMBOL_ORDER_INCOMPLETE","Symbol order profile does not contain all members")
        starts=[m for m in members if m not in incoming]
        if len(starts)!=1:
            _fail("IR_SYMBOL_ORDER_CHAIN","Symbol order lacks unique chain start")
        seen=set(); cur=starts[0]
        while cur not in seen:
            seen.add(cur)
            if cur not in outgoing: break
            cur=outgoing[cur]
        if seen!=members:
            _fail("IR_SYMBOL_ORDER_CHAIN","Symbol order is cyclic/disconnected")
        complete_order_domains.add(domain_id)

    def ensure_declared_domain(domain: Domain, code: str) -> None:
        try:
            require_domain(domain)
        except TypeError as exc:
            _fail(code,str(exc))
        if isinstance(domain,SymbolDomain) and domain.identity not in declared_symbol_domains:
            _fail(code,"Symbol domain contract references undeclared domain identity")
        if isinstance(domain,CollectionDomain):
            element=domain.element_domain
            if isinstance(element,CollectionDomain) and isinstance(element.element_domain,CollectionDomain):
                _fail("IR_COLLECTION_DOMAIN_DEPTH","Collection nesting deeper than the admitted two levels is not canonical")
            leaf=element.element_domain if isinstance(element,CollectionDomain) else element
            if leaf not in {NATURAL,BIDIRECTIONAL_INDEX} and not isinstance(leaf,SymbolDomain):
                _fail("IR_COLLECTION_DOMAIN_LEAF","Collection domain has a non-admitted leaf domain")
            ensure_declared_domain(element,code)

    for d in place_domains.values(): ensure_declared_domain(d,"IR_PLACE_DOMAIN_CONTRACT")
    for d in role_domains.values(): ensure_declared_domain(d,"IR_ROLE_DOMAIN_CONTRACT")
    for d in output_domains.values():
        if d is not None: ensure_declared_domain(d,"IR_OUTPUT_DOMAIN_CONTRACT")
    for x in program.program_input_domains: ensure_declared_domain(x.domain,"IR_PROGRAM_INPUT_DOMAIN_CONTRACT")

    def value(
        node: i.IRValue,
        *,
        visible_places: set[int],
        current_act: int | None,
        recent_act: int | None,
        context: str,
    ) -> Domain:
        try:
            domain = ir_value_domain(
                node,
                place_domains=place_domains,
                role_domains=role_domains,
                output_domains=output_domains,
            )
        except DomainValidationError as exc:
            _fail(exc.issue.code, exc.issue.detail)

        if isinstance(node,i.IRSymbolValue):
            expected_label=member_labels.get((node.domain_id,node.member_id))
            if expected_label is None:
                _fail("IR_SYMBOL_VALUE_IDENTITY","Symbol Value references undeclared domain/member")
            if node.external_label!=expected_label:
                _fail("IR_SYMBOL_LABEL_FORGERY","Symbol Value label does not match canonical declared member label")
        elif isinstance(node,(i.IRIndexSuccessor,i.IRIndexPredecessor)):
            if value(node.operand,visible_places=visible_places,current_act=current_act,recent_act=recent_act,context=context)!=BIDIRECTIONAL_INDEX:
                _fail("IR_INDEX_OPERAND_DOMAIN","Index successor/predecessor operand is not BidirectionalIndex")
        elif isinstance(node, (i.IRReadCurrentFact, i.IRReadCurrentValue)):
            if node.place not in places:
                _fail("IR_UNRESOLVED_PLACE", "current-value read references unknown place")
            if node.place not in visible_places:
                _fail("IR_INITIALIZER_VISIBILITY", "initializer reads self or a not-yet-established place")
        elif isinstance(node, (i.IRReadRoleNumber, i.IRReadRoleValue)):
            if node.role not in roles:
                _fail("IR_UNRESOLVED_ROLE", "role read references unknown role")
            if current_act is None or role_owner[node.role] != current_act:
                _fail("IR_ROLE_OWNER_CONTEXT", "role read is not owned by the current act occurrence")
        elif isinstance(node, (i.IRRecentResult, i.IRRecentTypedResult)):
            if node.act not in acts:
                _fail("IR_UNRESOLVED_RESULT_ACT", "recent-result read references unknown act")
            if context == "initializer":
                _fail("IR_RECENT_RESULT_IN_INITIALIZER", "recent-result reference is not valid in preparation initializer")
            if recent_act != node.act:
                _fail("IR_RECENT_RESULT_PROVENANCE", "recent-result reference lacks the directly preceding matching performance")
        elif isinstance(node, i.IRAddNatural):
            value(node.addend, visible_places=visible_places, current_act=current_act, recent_act=recent_act, context=context)
            value(node.augend, visible_places=visible_places, current_act=current_act, recent_act=recent_act, context=context)
            _constant_natural(node)
        elif isinstance(node, i.IRCheckedSubtractNatural):
            if node.error_code != "ARITHMETIC_DOMAIN_ERROR":
                _fail("IR_SUBTRACTION_ERROR_CODE", "checked Natural subtraction has non-canonical error code")
            value(node.amount, visible_places=visible_places, current_act=current_act, recent_act=recent_act, context=context)
            value(node.source, visible_places=visible_places, current_act=current_act, recent_act=recent_act, context=context)
            _constant_natural(node)
        elif isinstance(node, i.IRCollectionValue):
            ensure_declared_domain(node.element_domain,"IR_COLLECTION_ELEMENT_DOMAIN")
            for item in node.items:
                child_domain=value(item, visible_places=visible_places, current_act=current_act, recent_act=recent_act, context=context)
                if child_domain!=node.element_domain:
                    _fail("IR_DOMAIN_COLLECTION_ELEMENT","serialized Collection member has the wrong domain")
        elif isinstance(node,i.IRCollectionAppend):
            ensure_declared_domain(node.element_domain,"IR_COLLECTION_ELEMENT_DOMAIN")
            source=value(node.collection,visible_places=visible_places,current_act=current_act,recent_act=recent_act,context=context)
            item=value(node.item,visible_places=visible_places,current_act=current_act,recent_act=recent_act,context=context)
            if source!=CollectionDomain(node.element_domain) or item!=node.element_domain:
                _fail("IR_DOMAIN_COLLECTION_APPEND","Collection append metadata/operand domain mismatch")
        elif isinstance(node,i.IRCollectionCount):
            actual=value(node.collection,visible_places=visible_places,current_act=current_act,recent_act=recent_act,context=context)
            if not isinstance(actual,CollectionDomain):
                _fail("IR_DOMAIN_COLLECTION_COUNT","Collection count operand is not a Collection")
        elif isinstance(node,(i.IRCollectionSelectNatural,i.IRCollectionSelectValue)):
            if isinstance(node,i.IRCollectionSelectValue):
                ensure_declared_domain(node.element_domain,"IR_COLLECTION_ELEMENT_DOMAIN")
            actual=value(node.collection,visible_places=visible_places,current_act=current_act,recent_act=recent_act,context=context)
            if node.mode not in {"first","last","ordinal"}:
                _fail("IR_COLLECTION_POSITION_MODE","unknown Collection selection mode")
            if (node.mode=="ordinal") != (node.position is not None):
                _fail("IR_COLLECTION_POSITION_MODE","Collection selection position shape does not match mode")
            if node.position is not None:
                pd=value(node.position,visible_places=visible_places,current_act=current_act,recent_act=recent_act,context=context)
                if pd!=NATURAL:
                    _fail("IR_DOMAIN_COLLECTION_POSITION","Collection position must be Natural")
            if isinstance(node,i.IRCollectionSelectNatural):
                if actual!=CollectionDomain(NATURAL):
                    _fail("IR_DOMAIN_COLLECTION_SELECT","Natural element head requires Collection<Natural>")
            elif actual!=CollectionDomain(node.element_domain):
                _fail("IR_DOMAIN_COLLECTION_SELECT","typed Collection selection head disagrees with element domain")
        elif isinstance(node,i.IRCollectionOrder):
            ensure_declared_domain(node.element_domain,"IR_COLLECTION_ELEMENT_DOMAIN")
            actual=value(node.collection,visible_places=visible_places,current_act=current_act,recent_act=recent_act,context=context)
            if actual!=CollectionDomain(node.element_domain):
                _fail("IR_DOMAIN_COLLECTION_ORDER","Collection order metadata disagrees with source book domain")
            if node.order_kind=="natural":
                if node.element_domain!=NATURAL or node.symbol_domain_id is not None:
                    _fail("IR_COLLECTION_ORDER_PROFILE","invalid Natural Collection order profile")
            elif node.order_kind=="lex-natural":
                if node.element_domain!=CollectionDomain(NATURAL) or node.symbol_domain_id is not None:
                    _fail("IR_COLLECTION_ORDER_PROFILE","invalid lexicographic Natural Collection order profile")
            elif node.order_kind=="symbol":
                if not isinstance(node.element_domain,SymbolDomain) or node.symbol_domain_id!=node.element_domain.identity:
                    _fail("IR_COLLECTION_ORDER_PROFILE","Symbol order profile/domain mismatch")
                if node.symbol_domain_id not in complete_order_domains:
                    _fail("IR_COLLECTION_ORDER_INCOMPLETE","Symbol Collection order requires an explicit complete order profile")
            elif node.order_kind=="lex-symbol":
                if not isinstance(node.element_domain,CollectionDomain) or not isinstance(node.element_domain.element_domain,SymbolDomain):
                    _fail("IR_COLLECTION_ORDER_PROFILE","lexicographic Symbol order requires Collection<Symbol> element domain")
                expected=node.element_domain.element_domain.identity
                if node.symbol_domain_id!=expected:
                    _fail("IR_COLLECTION_ORDER_PROFILE","lexicographic Symbol order profile/domain mismatch")
                if expected not in complete_order_domains:
                    _fail("IR_COLLECTION_ORDER_INCOMPLETE","lexicographic Symbol order requires an explicit complete order profile")
            else:
                _fail("IR_COLLECTION_ORDER_PROFILE","unknown Collection order profile")
        return domain

    def proposition(node: i.IRProposition, *, visible_places: set[int], current_act: int | None, recent_act: int | None) -> None:
        if isinstance(node,i.IREqualProposition):
            if value(node.left,visible_places=visible_places,current_act=current_act,recent_act=recent_act,context="execution")!=NATURAL or value(node.right,visible_places=visible_places,current_act=current_act,recent_act=recent_act,context="execution")!=NATURAL:
                _fail("IR_PROPOSITION_DOMAIN","Core numeric equality requires Natural operands")
            return
        if isinstance(node,i.IRNaturalGTProposition):
            if value(node.left,visible_places=visible_places,current_act=current_act,recent_act=recent_act,context="execution")!=NATURAL or value(node.right,visible_places=visible_places,current_act=current_act,recent_act=recent_act,context="execution")!=NATURAL:
                _fail("IR_NATURAL_GT_DOMAIN","Natural strict ordering requires Natural operands")
            return
        if isinstance(node,i.IRSymbolEqualProposition):
            expected=SymbolDomain(node.domain_id)
            ensure_declared_domain(expected,"IR_SYMBOL_EQUALITY_DOMAIN")
            left=value(node.left,visible_places=visible_places,current_act=current_act,recent_act=recent_act,context="execution")
            right=value(node.right,visible_places=visible_places,current_act=current_act,recent_act=recent_act,context="execution")
            if left!=expected or right!=expected:
                _fail("IR_SYMBOL_EQUALITY_DOMAIN","Symbol equality operands must belong to one exact declared domain")
            return
        if isinstance(node,i.IRCollectionMembershipProposition):
            ensure_declared_domain(node.element_domain,"IR_COLLECTION_ELEMENT_DOMAIN")
            item=value(node.item,visible_places=visible_places,current_act=current_act,recent_act=recent_act,context="execution")
            collection=value(node.collection,visible_places=visible_places,current_act=current_act,recent_act=recent_act,context="execution")
            if item!=node.element_domain or collection!=CollectionDomain(node.element_domain):
                _fail("IR_COLLECTION_MEMBERSHIP_DOMAIN","membership item/book domains disagree")
            return
        _fail("IR_PROPOSITION_KIND",f"unsupported proposition {type(node).__name__}")


    def output_path_max(node: i.IRAction) -> int:
        if isinstance(node, i.IRProduceResult):
            return 1
        if isinstance(node, i.IRThen):
            return sum(output_path_max(x) for x in node.actions)
        if isinstance(node, i.IRConditional):
            return max(output_path_max(node.if_holds), output_path_max(node.if_not))
        if isinstance(node, i.IRFixedRecurrence):
            inner = output_path_max(node.action)
            if inner and node.count > 1:
                _fail("IR_OUTPUT_IN_RECURRENCE", "result production inside fixed recurrence can occur more than once in one occurrence")
            return inner * node.count
        if isinstance(node, i.IRRepeatExactly):
            # A second direct Produce in the same occurrence is the existing
            # runtime output-cardinality error; RepeatExactly creates no result collection.
            return output_path_max(node.action)
        if isinstance(node, i.IRPostActionRecurrence):
            if output_path_max(node.action):
                _fail("IR_OUTPUT_IN_RECURRENCE", "result production inside post-action recurrence can occur repeatedly in one occurrence")
            return 0
        return 0

    def action(node: i.IRAction, *, current_act: int | None, recent_act: int | None, allow_output: bool) -> int | None:
        visible = set(places)
        if isinstance(node, i.IRReplaceCurrentFact):
            if node.place not in places:
                _fail("IR_UNRESOLVED_PLACE", "replacement references unknown place")
            actual = value(node.value, visible_places=visible, current_act=current_act, recent_act=recent_act, context="execution")
            if actual != place_domains[node.place]:
                _fail("IR_DOMAIN_PLACE_REPLACEMENT", "replacement value domain differs from fixed place domain")
            return None
        if isinstance(node, i.IRPerformAct):
            if node.act not in acts or node.act not in act_defs:
                _fail("IR_UNRESOLVED_ACT", "performance references unknown act")
            seen: set[int] = set()
            for assoc in node.associations:
                if assoc.role not in roles or role_owner[assoc.role] != node.act:
                    _fail("IR_ROLE_ASSOCIATION_TARGET", "invalid role association target: role does not belong to performed act")
                if assoc.role in seen:
                    _fail("IR_DUPLICATE_ROLE_ASSOCIATION", "role is associated more than once")
                seen.add(assoc.role)
                actual = value(assoc.value, visible_places=visible, current_act=current_act, recent_act=recent_act, context="execution")
                if actual != role_domains[assoc.role]:
                    _fail("IR_DOMAIN_ROLE_ASSOCIATION", "role association value has the wrong static domain")
            required = set(act_defs[node.act].roles)
            if seen != required:
                _fail("IR_ROLE_PROFILE", "role associations do not exactly match the performed act profile")
            return node.act
        if isinstance(node, i.IRProduceResult):
            if not allow_output or current_act is None:
                _fail("IR_OUTPUT_CONTEXT", "result production exists outside an act performance body")
            actual = value(node.value, visible_places=visible, current_act=current_act, recent_act=recent_act, context="execution")
            expected = output_domains[current_act]
            if expected is None or actual != expected:
                _fail("IR_DOMAIN_OUTPUT", "result production domain disagrees with the act output contract")
            return None
        if isinstance(node, i.IRThen):
            if not node.actions:
                _fail("IR_EMPTY_SEQUENCE", "explicit sequence is empty")
            recent = recent_act
            for child in node.actions:
                recent = action(child, current_act=current_act, recent_act=recent, allow_output=allow_output)
            return recent
        if isinstance(node, i.IRConditional):
            proposition(node.proposition, visible_places=visible, current_act=current_act, recent_act=recent_act)
            action(node.if_holds, current_act=current_act, recent_act=recent_act, allow_output=allow_output)
            action(node.if_not, current_act=current_act, recent_act=recent_act, allow_output=allow_output)
            return None
        if isinstance(node, i.IRFixedRecurrence):
            if type(node.count) is not int or node.count <= 0:
                _fail("IR_FIXED_RECURRENCE", "fixed recurrence count is not a positive Natural")
            output_path_max(node)
            action(node.action, current_act=current_act, recent_act=None, allow_output=allow_output)
            return None
        if isinstance(node, i.IRRepeatExactly):
            count_domain = value(
                node.count, visible_places=visible, current_act=current_act,
                recent_act=recent_act, context="execution",
            )
            if count_domain != NATURAL:
                _fail("IR_RECURRENCE_COUNT_DOMAIN", "RepeatExactly count must independently resolve to Natural")
            if not isinstance(node.action, (i.IRReplaceCurrentFact, i.IRPerformAct, i.IRProduceResult)):
                _fail("IR_RECURRENCE_BODY", "RepeatExactly must preserve exactly one atomic action boundary")
            action(node.action, current_act=current_act, recent_act=None, allow_output=allow_output)
            return None
        if isinstance(node, i.IRPostActionRecurrence):
            output_path_max(node)
            produced_by = action(node.action, current_act=current_act, recent_act=None, allow_output=allow_output)
            proposition(node.proposition, visible_places=visible, current_act=current_act, recent_act=produced_by)
            return None
        _fail("IR_ACTION_KIND", f"unsupported canonical action {type(node).__name__}")

    established: set[int] = set()
    seen_initial: set[int] = set()
    for initial in program.initial_facts:
        if initial.place not in places or initial.place in seen_initial:
            _fail("IR_INITIAL_FACT_STRUCTURE", "invalid or duplicate place initial establishment")
        actual = value(initial.value, visible_places=set(established), current_act=None, recent_act=None, context="initializer")
        if actual != place_domains[initial.place]:
            _fail("IR_DOMAIN_PLACE_INITIALIZER", "initial value domain differs from fixed place domain")
        seen_initial.add(initial.place)
        established.add(initial.place)
    if seen_initial != places:
        _fail("IR_INITIAL_FACT_STRUCTURE", "every place must have exactly one initial establishment")

    for definition in program.acts:
        if definition.act not in acts:
            _fail("IR_ACT_DEFINITION", "act definition references unknown act")
        if len(definition.roles) != len(set(definition.roles)):
            _fail("IR_ROLE_PROFILE", "duplicate role in act profile")
        for role in definition.roles:
            if role not in roles or role_owner[role] != definition.act:
                _fail("IR_ROLE_PROFILE", "act profile contains role owned by a different act")
        if output_path_max(definition.body) > 1:
            _fail("IR_OUTPUT_CARDINALITY", "an act occurrence can produce more than one result on one path")
        action(definition.body, current_act=definition.act, recent_act=None, allow_output=True)

    action(program.principal, current_act=None, recent_act=None, allow_output=False)


__all__ = ["CanonicalIRIssue", "CanonicalIRValidationError", "validate_canonical_ir"]
