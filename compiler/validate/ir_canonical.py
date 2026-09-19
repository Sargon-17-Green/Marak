"""Source-independent semantic validation for decoded canonical A13/B12 IR.

This is the artifact trust-boundary validator.  It checks invariants that the
source compiler/resolver must already have established, without invoking the
parser or relying on source-language objects.  Both compiler emission and
artifact verification use this pass so the two boundaries cannot drift.
"""
from __future__ import annotations

from dataclasses import dataclass

from compiler.models import ir as i


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


def _constant_number(node: i.IRNumber) -> int | None:
    if isinstance(node, i.IRNatural):
        return node.value
    if isinstance(node, i.IRAddNatural):
        a = _constant_number(node.addend)
        b = _constant_number(node.augend)
        return None if a is None or b is None else a + b
    if isinstance(node, i.IRCheckedSubtractNatural):
        amount = _constant_number(node.amount)
        source = _constant_number(node.source)
        if amount is None or source is None:
            return None
        if amount > source:
            _fail("IR_STATIC_ARITHMETIC_DOMAIN", f"constant Natural subtraction {source}-{amount} is out of domain")
        return source - amount
    return None


def validate_canonical_ir(program: i.IRProgram) -> None:
    if not isinstance(program, i.IRProgram):
        _fail("IR_NOT_PROGRAM", "payload is not IRProgram")

    by = {s.serial: s for s in program.symbols}
    places = {s.serial for s in program.symbols if s.kind == "place"}
    acts = {s.serial for s in program.symbols if s.kind == "act"}
    roles = {s.serial for s in program.symbols if s.kind == "role"}
    role_owner = {s.serial: s.owner for s in program.symbols if s.kind == "role"}
    act_defs = {a.act: a for a in program.acts}

    def number(
        node: i.IRNumber,
        *,
        visible_places: set[int],
        current_act: int | None,
        recent_act: int | None,
        context: str,
    ) -> None:
        if isinstance(node, i.IRNatural):
            if type(node.value) is not int or node.value < 0:
                _fail("IR_NEGATIVE_NATURAL", "Natural constant is negative or non-integral")
            return
        if isinstance(node, i.IRReadCurrentFact):
            if node.place not in places:
                _fail("IR_UNRESOLVED_PLACE", "current-fact read references unknown place")
            if node.place not in visible_places:
                _fail("IR_INITIALIZER_VISIBILITY", "initializer reads self or a not-yet-established place")
            return
        if isinstance(node, i.IRReadRoleNumber):
            if node.role not in roles:
                _fail("IR_UNRESOLVED_ROLE", "role-number read references unknown role")
            if current_act is None or role_owner[node.role] != current_act:
                _fail("IR_ROLE_OWNER_CONTEXT", "role-number read is not owned by the current act occurrence")
            return
        if isinstance(node, i.IRRecentResult):
            if node.act not in acts:
                _fail("IR_UNRESOLVED_RESULT_ACT", "recent-result read references unknown act")
            if context == "initializer":
                _fail("IR_RECENT_RESULT_IN_INITIALIZER", "recent-result reference is not valid in preparation initializer")
            if recent_act != node.act:
                _fail("IR_RECENT_RESULT_PROVENANCE", "recent-result reference lacks the directly preceding matching performance")
            return
        if isinstance(node, i.IRAddNatural):
            number(node.addend, visible_places=visible_places, current_act=current_act, recent_act=recent_act, context=context)
            number(node.augend, visible_places=visible_places, current_act=current_act, recent_act=recent_act, context=context)
            _constant_number(node)
            return
        if isinstance(node, i.IRCheckedSubtractNatural):
            if node.error_code != "ARITHMETIC_DOMAIN_ERROR":
                _fail("IR_SUBTRACTION_ERROR_CODE", "checked Natural subtraction has non-canonical error code")
            number(node.amount, visible_places=visible_places, current_act=current_act, recent_act=recent_act, context=context)
            number(node.source, visible_places=visible_places, current_act=current_act, recent_act=recent_act, context=context)
            _constant_number(node)
            return
        _fail("IR_NUMBER_KIND", f"unsupported canonical number node {type(node).__name__}")

    def proposition(node: i.IRProposition, *, visible_places: set[int], current_act: int | None, recent_act: int | None) -> None:
        if not isinstance(node, i.IREqualProposition):
            _fail("IR_PROPOSITION_KIND", f"unsupported proposition {type(node).__name__}")
        number(node.left, visible_places=visible_places, current_act=current_act, recent_act=recent_act, context="execution")
        number(node.right, visible_places=visible_places, current_act=current_act, recent_act=recent_act, context="execution")

    def output_path_max(node: i.IRAction) -> int:
        """Maximum outputs of the *current occurrence* along one execution path.

        Outputs produced by nested IRPerformAct belong to the child occurrence
        and therefore do not contribute to the caller's output cardinality.
        """
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
        if isinstance(node, i.IRPostActionRecurrence):
            if output_path_max(node.action):
                _fail("IR_OUTPUT_IN_RECURRENCE", "result production inside post-action recurrence can occur repeatedly in one occurrence")
            return 0
        if isinstance(node, i.IRPerformAct):
            return 0
        return 0

    def action(
        node: i.IRAction,
        *,
        current_act: int | None,
        recent_act: int | None,
        allow_output: bool,
    ) -> int | None:
        visible = set(places)
        if isinstance(node, i.IRReplaceCurrentFact):
            if node.place not in places:
                _fail("IR_UNRESOLVED_PLACE", "replacement references unknown place")
            number(node.value, visible_places=visible, current_act=current_act, recent_act=recent_act, context="execution")
            return None
        if isinstance(node, i.IRPerformAct):
            if node.act not in acts or node.act not in act_defs:
                _fail("IR_UNRESOLVED_ACT", "performance references unknown act")
            seen: set[int] = set()
            for assoc in node.associations:
                if assoc.role not in roles or role_owner[assoc.role] != node.act:
                    _fail("IR_ROLE_ASSOCIATION_TARGET", "association target role does not belong to performed act")
                if assoc.role in seen:
                    _fail("IR_DUPLICATE_ROLE_ASSOCIATION", "role is associated more than once")
                seen.add(assoc.role)
                # Association values are evaluated in the caller occurrence.
                number(assoc.value, visible_places=visible, current_act=current_act, recent_act=recent_act, context="execution")
            required = set(act_defs[node.act].roles)
            if seen != required:
                _fail("IR_ROLE_PROFILE", "role associations do not exactly match the performed act profile")
            return node.act
        if isinstance(node, i.IRProduceResult):
            if not allow_output or current_act is None:
                _fail("IR_OUTPUT_CONTEXT", "result production exists outside an act performance body")
            number(node.value, visible_places=visible, current_act=current_act, recent_act=recent_act, context="execution")
            return None
        if isinstance(node, i.IRThen):
            if not node.actions:
                _fail("IR_EMPTY_SEQUENCE", "explicit sequence is empty")
            recent = recent_act
            for child in node.actions:
                produced_by = action(child, current_act=current_act, recent_act=recent, allow_output=allow_output)
                recent = produced_by
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
        if isinstance(node, i.IRPostActionRecurrence):
            output_path_max(node)
            produced_by = action(node.action, current_act=current_act, recent_act=None, allow_output=allow_output)
            proposition(node.proposition, visible_places=visible, current_act=current_act, recent_act=produced_by)
            return None
        _fail("IR_ACTION_KIND", f"unsupported canonical action {type(node).__name__}")
        return None

    # Preparation order is the canonical establishment order.  An initializer
    # may observe only places established by preceding entries.
    established: set[int] = set()
    seen_initial: set[int] = set()
    for initial in program.initial_facts:
        if initial.place not in places or initial.place in seen_initial:
            _fail("IR_INITIAL_FACT_STRUCTURE", "invalid or duplicate place initial establishment")
        number(initial.value, visible_places=set(established), current_act=None, recent_act=None, context="initializer")
        seen_initial.add(initial.place)
        established.add(initial.place)
    if seen_initial != places:
        _fail("IR_INITIAL_FACT_STRUCTURE", "every place must have exactly one initial establishment")

    # Act bodies execute in occurrence context owned by the declared ActId.
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

    # Principal execution has no current act occurrence and cannot produce output.
    action(program.principal, current_act=None, recent_act=None, allow_output=False)


__all__ = ["CanonicalIRIssue", "CanonicalIRValidationError", "validate_canonical_ir"]
