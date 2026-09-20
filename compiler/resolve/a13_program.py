from __future__ import annotations

from dataclasses import dataclass

from compiler.models.hast import (
    HastActBody, HastActIntroduction, HastAddNatural, HastConditional,
    HastCoreProgram, HastCurrentFact, HastCurrentRoleNumber, HastEqualProposition,
    HastExactNatural, HastExecutable, HastFixedRecurrence, HastNumber,
    HastPerformAct, HastPlaceIntroduction, HastPostActionRecurrence,
    HastProduceResult, HastProposition, HastRecentResult, HastReplaceCurrentFact,
    HastRoleAssociation, HastRoleDeclaration, HastSubtractNatural, HastThen,
    HastPlaceDomain, HastRoleDomain, HastActOutputDomain,
)
from compiler.models.domains import NATURAL
from compiler.models.symbols import ActId, PlaceId, RoleId
from compiler.parse.forest import ParseElement, ParseLeaf, ParseNode
from compiler.source.source_map import OriginalSpan


@dataclass(frozen=True, slots=True)
class A13ResolutionIssue:
    code: str
    message_en: str
    message_he: str
    source_span: OriginalSpan | None
    metadata: dict[str, object]


class A13ResolutionError(Exception):
    def __init__(self, issue: A13ResolutionIssue):
        super().__init__(f"{issue.code}: {issue.message_en}")
        self.issue = issue


class _Env:
    def __init__(self) -> None:
        self.next_serial = 1
        self.places: dict[str, PlaceId] = {}
        self.acts: dict[str, ActId] = {}
        self.roles: dict[tuple[int, str], RoleId] = {}
        self.bodies: set[int] = set()

    def serial(self) -> int:
        value = self.next_serial
        self.next_serial += 1
        return value


def _span(node: ParseNode | ParseLeaf) -> OriginalSpan | None:
    return node.original


def _issue(code: str, en: str, he: str, where: ParseNode | ParseLeaf | None, **metadata) -> A13ResolutionError:
    return A13ResolutionError(A13ResolutionIssue(code, en, he, None if where is None else _span(where), dict(metadata)))


def _direct_leaves(node: ParseNode, role: str) -> tuple[ParseLeaf, ...]:
    return tuple(c for c in node.children if isinstance(c, ParseLeaf) and c.terminal_role == role)


def _all_leaves(element: ParseElement, role: str) -> tuple[ParseLeaf, ...]:
    if isinstance(element, ParseLeaf):
        return (element,) if element.terminal_role == role else ()
    out: list[ParseLeaf] = []
    for child in element.children:
        out.extend(_all_leaves(child, role))
    return tuple(out)


def _child_nodes(node: ParseNode, symbol: str) -> tuple[ParseNode, ...]:
    return tuple(c for c in node.children if isinstance(c, ParseNode) and c.symbol == symbol)


def _one_child(node: ParseNode, symbol: str) -> ParseNode:
    children = _child_nodes(node, symbol)
    if len(children) != 1:
        raise RuntimeError(f"internal parse contract: {node.production_id} expected one {symbol}, got {len(children)}")
    return children[0]


def _single_parse_child(node: ParseNode) -> ParseNode:
    children = tuple(c for c in node.children if isinstance(c, ParseNode))
    if len(children) != 1:
        raise RuntimeError(f"internal parse wrapper contract: {node.production_id}")
    return children[0]


def _flatten_preparation(node: ParseNode) -> list[ParseNode]:
    if node.production_id == "A13.PREPARATION.ONE":
        return [_one_child(node, "PreparatoryUnit")]
    if node.production_id == "A13.PREPARATION.MORE":
        return _flatten_preparation(_one_child(node, "Preparation")) + [_one_child(node, "PreparatoryUnit")]
    raise RuntimeError(f"not an A13 Preparation node: {node.production_id}")


def _flatten_sequence(node: ParseNode, *, body: bool) -> list[ParseNode]:
    one = "A12.BODY.SEQUENCE.ONE" if body else "A13.EXEC.SEQUENCE.ONE"
    more = "A12.BODY.SEQUENCE.MORE" if body else "A13.EXEC.SEQUENCE.MORE"
    unit_symbol = "BodyUnit" if body else "ExecutableUnit"
    seq_symbol = "BodySequence" if body else "ExecutableSequence"
    if node.production_id == one:
        return [_one_child(node, unit_symbol)]
    if node.production_id == more:
        return _flatten_sequence(_one_child(node, seq_symbol), body=body) + [_one_child(node, unit_symbol)]
    raise RuntimeError(f"not a sequence node: {node.production_id}")


def _resolve_place(name: str, env: _Env, where: ParseLeaf | ParseNode, *, self_name: str | None = None) -> PlaceId:
    if name not in env.places:
        if self_name is not None and name == self_name:
            raise _issue(
                "REF0106",
                "A place is not visible inside its own initializer.",
                "מקום אינו זמין בתוך הביטוי הקובע את תוכנו הראשוני שלו עצמו.",
                where,
                name=name,
            )
        raise _issue(
            "REF0101", "Place reference occurs before its complete introduction.",
            "הפניה למקום מופיעה לפני השלמת הצגתו.", where, kind="place", name=name,
        )
    return env.places[name]


def _resolve_act(name: str, env: _Env, where: ParseLeaf | ParseNode) -> ActId:
    if name not in env.acts:
        raise _issue(
            "REF0101", "Act reference occurs before its introduction.",
            "הפניה למעשה מופיעה לפני הצגתו.", where, kind="act", name=name,
        )
    return env.acts[name]


def _resolve_role(owner: ActId, name: str, env: _Env, where: ParseLeaf | ParseNode) -> RoleId:
    key = (owner.serial, name)
    if key not in env.roles:
        raise _issue(
            "REF0101", "Role reference occurs before its declaration.",
            "הפניה לתפקיד מופיעה לפני הצהרתו.", where,
            kind="role", owner=owner.spelling, name=name,
        )
    return env.roles[key]


def _lower_number(
    node: ParseNode,
    env: _Env,
    *,
    current_act: ActId | None,
    recent_act: ActId | None,
    pending_self_place: str | None = None,
) -> HastNumber:
    span = node.original
    if span is None:
        raise RuntimeError("number node lacks source span")
    pid = node.production_id
    if pid == "A12.NUMBER.LITERAL":
        leaves = tuple(l for l in _all_leaves(node, "Numeral:a12-direct-1-9999") if l.numeric_value is not None)
        if len(leaves) != 1:
            raise RuntimeError("literal numeral leaf contract")
        return HastExactNatural(span, leaves[0].numeric_value)  # type: ignore[arg-type]
    if pid == "A10.PLACE.CURRENT_NUMBER":
        leaf = _direct_leaves(node, "PlaceName")[0]
        return HastCurrentFact(span, _resolve_place(leaf.text, env, leaf, self_name=pending_self_place))
    if pid == "A11.NUMBER.CURRENT.ROLE":
        owner_leaf = _direct_leaves(node, "RoleOwnerActionName")[0]
        role_leaf = _direct_leaves(node, "AssociatedRoleName")[0]
        owner = _resolve_act(owner_leaf.text, env, owner_leaf)
        role = _resolve_role(owner, role_leaf.text, env, role_leaf)
        if current_act != owner:
            raise _issue(
                "REF0110", "A current role number is available only in an occurrence of its owning act.",
                "המספר הנוכחי של תפקיד זמין רק בעת ביצוע המעשה שהוא בעל התפקיד.",
                role_leaf, owner=owner.spelling, role=role.spelling,
            )
        return HastCurrentRoleNumber(span, role)
    if pid == "A12.RESULT.IMMEDIATE.SINGLE":
        leaf = _direct_leaves(node, "ResultActionName")[0]
        act = _resolve_act(leaf.text, env, leaf)
        if recent_act is None:
            raise _issue(
                "REF0112", "Immediate result reference has no structurally immediate preceding performance.",
                "להפניית התוצאה המיידית אין ביצוע קודם הצמוד לה מבחינה מבנית.",
                leaf, act=act.spelling,
            )
        if recent_act != act:
            raise _issue(
                "REF0113", "Immediate result reference names a different act from the directly preceding performance.",
                "הפניית התוצאה המיידית נוקבת במעשה שונה מן הביצוע הקודם הישיר.",
                leaf, expected=recent_act.spelling, actual=act.spelling,
            )
        return HastRecentResult(span, act)
    if pid == "A9.NUMBER.ADD":
        nums = _child_nodes(node, "NumberValue")
        if len(nums) != 2:
            raise RuntimeError("addition arity contract")
        return HastAddNatural(
            span,
            _lower_number(nums[0], env, current_act=current_act, recent_act=recent_act, pending_self_place=pending_self_place),
            _lower_number(nums[1], env, current_act=current_act, recent_act=recent_act, pending_self_place=pending_self_place),
        )
    if pid == "A9.NUMBER.SUBTRACT":
        nums = _child_nodes(node, "NumberValue")
        if len(nums) != 2:
            raise RuntimeError("subtraction arity contract")
        return HastSubtractNatural(
            span,
            _lower_number(nums[0], env, current_act=current_act, recent_act=recent_act, pending_self_place=pending_self_place),
            _lower_number(nums[1], env, current_act=current_act, recent_act=recent_act, pending_self_place=pending_self_place),
        )
    raise RuntimeError(f"unsupported admitted NumberValue production {pid}")


def _lower_proposition(node: ParseNode, env: _Env, *, current_act: ActId | None, recent_act: ActId | None) -> HastProposition:
    if node.production_id != "A9.PROPOSITION.NUMERIC_IDENTITY":
        raise RuntimeError(f"unsupported proposition {node.production_id}")
    nums = _child_nodes(node, "NumberValue")
    assert len(nums) == 2
    assert node.original is not None
    return HastEqualProposition(
        node.original,
        _lower_number(nums[0], env, current_act=current_act, recent_act=recent_act),
        _lower_number(nums[1], env, current_act=current_act, recent_act=recent_act),
    )


def _flatten_role_associations(node: ParseNode) -> list[ParseNode]:
    if node.production_id == "A11.ROLE.ASSOCIATIONS.ONE":
        return [node]
    if node.production_id == "A11.ROLE.ASSOCIATIONS.MORE":
        prev = _one_child(node, "RoleAssociations")
        return _flatten_role_associations(prev) + [node]
    raise RuntimeError(f"unexpected role association production {node.production_id}")


def _repeat_count(node: ParseNode) -> int:
    mapping = {
        "A9.REPEAT.COUNT.3": 3, "A9.REPEAT.COUNT.4": 4, "A9.REPEAT.COUNT.5": 5,
        "A9.REPEAT.COUNT.6": 6, "A9.REPEAT.COUNT.7": 7, "A9.REPEAT.COUNT.8": 8,
        "A9.REPEAT.COUNT.9": 9,
    }
    try:
        return mapping[node.production_id]
    except KeyError as exc:
        raise RuntimeError(f"unexpected repeat count production {node.production_id}") from exc


def _lower_action(
    node: ParseNode,
    env: _Env,
    *,
    current_act: ActId | None,
    recent_act: ActId | None,
) -> HastExecutable:
    # Semantic-category wrappers are transparent; the category itself remains
    # in HAST through the concrete admitted child.
    if node.symbol in {"BodyUnit", "ExecutableUnit"}:
        return _lower_action(_single_parse_child(node), env, current_act=current_act, recent_act=recent_act)
    pid = node.production_id
    span = node.original
    if span is None:
        raise RuntimeError("action node lacks source span")

    if pid == "A10.PLACE.REPLACE":
        names = _direct_leaves(node, "PlaceName")
        if len(names) != 2:
            raise RuntimeError("replace place-name contract")
        if names[0].text != names[1].text:
            raise _issue(
                "REF0001", "Replacement destination descriptions must co-refer explicitly.",
                "תיאורי יעד ההחלפה חייבים להתייחס במפורש לאותו מקום.", names[1],
                expected=names[0].text, actual=names[1].text,
            )
        place = _resolve_place(names[0].text, env, names[0])
        value = _lower_number(_one_child(node, "NumberValue"), env, current_act=current_act, recent_act=recent_act)
        return HastReplaceCurrentFact(span, place, value)

    if pid in {"A10.ACT.PERFORM", "A11.ACT.PERFORM.WITH.ROLES"}:
        role_name = "ActionName" if pid == "A10.ACT.PERFORM" else "PerformedActionName"
        act_leaf = _direct_leaves(node, role_name)[0]
        act = _resolve_act(act_leaf.text, env, act_leaf)
        required = {rid.spelling: rid for (owner, _), rid in env.roles.items() if owner == act.serial}
        associations: list[HastRoleAssociation] = []
        seen: set[str] = set()
        role_nodes = _child_nodes(node, "RoleAssociations")
        if pid == "A11.ACT.PERFORM.WITH.ROLES":
            if len(role_nodes) != 1:
                raise RuntimeError("role association wrapper contract")
            for assoc_node in _flatten_role_associations(role_nodes[0]):
                owners = _direct_leaves(assoc_node, "RoleOwnerActionName")
                roles = _direct_leaves(assoc_node, "AssociatedRoleName")
                nums = _child_nodes(assoc_node, "NumberValue")
                # In the recursive MORE node direct leaves/name and NumberValue
                # belong only to the newly appended association.
                if len(owners) != 1 or len(roles) != 1 or len(nums) != 1:
                    raise RuntimeError("role association direct-shape contract")
                if owners[0].text != act.spelling:
                    raise _issue(
                        "REF0111", "Role association explicitly names a different owning act.",
                        "שיוך התפקיד נוקב במפורש במעשה בעלים שונה.", owners[0],
                        performed=act.spelling, owner=owners[0].text,
                    )
                role = _resolve_role(act, roles[0].text, env, roles[0])
                if role.spelling in seen:
                    raise _issue(
                        "REF0111", "A role is associated more than once in one performance.",
                        "תפקיד משויך יותר מפעם אחת בביצוע יחיד.", roles[0], role=role.spelling,
                    )
                seen.add(role.spelling)
                associations.append(HastRoleAssociation(
                    assoc_node.original or span,
                    role,
                    _lower_number(nums[0], env, current_act=current_act, recent_act=recent_act),
                ))
        if set(seen) != set(required):
            missing = sorted(set(required) - seen)
            extra = sorted(seen - set(required))
            raise _issue(
                "REF0111", "Performance role associations must match the described act's required roles exactly.",
                "שיוכי התפקידים בביצוע חייבים להתאים בדיוק לתפקידי המעשה המתואר.",
                act_leaf, act=act.spelling, missing=missing, extra=extra,
            )
        return HastPerformAct(span, act, tuple(sorted(associations, key=lambda a: a.role.serial)))

    if pid == "A12.RESULT.PRODUCE":
        if current_act is None:
            raise _issue(
                "REF0114", "Result production is licensed only within the current act performance.",
                "הפקת תוצאה מותרת רק בתוך הביצוע הנוכחי של מעשה.", node,
            )
        value = _lower_number(_one_child(node, "NumberValue"), env, current_act=current_act, recent_act=recent_act)
        return HastProduceResult(span, value)

    if pid == "A10.CONDITIONAL.PAIRED":
        prop = _lower_proposition(_one_child(node, "Proposition"), env, current_act=current_act, recent_act=recent_act)
        branches = _child_nodes(node, "AtomicAction")
        assert len(branches) == 2
        return HastConditional(
            span, prop,
            _lower_action(branches[0], env, current_act=current_act, recent_act=recent_act),
            _lower_action(branches[1], env, current_act=current_act, recent_act=recent_act),
        )

    if pid == "A10.REPEAT.COUNTED":
        count = _repeat_count(_one_child(node, "RepeatCount"))
        action = _lower_action(_one_child(node, "AtomicAction"), env, current_act=current_act, recent_act=recent_act)
        return HastFixedRecurrence(span, count, action)

    if pid == "A10.RECURRENCE.AFTER_UNTIL":
        action = _lower_action(_one_child(node, "AtomicAction"), env, current_act=current_act, recent_act=recent_act)
        action_recent = action.act if isinstance(action, HastPerformAct) else None
        prop = _lower_proposition(_one_child(node, "Proposition"), env, current_act=current_act, recent_act=action_recent)
        return HastPostActionRecurrence(span, action, prop)

    if node.symbol in {"AtomicAction", "BodyAtomicAction", "ConditionalConsequence", "CountedConsequence", "AfterGatedRecurrence"}:
        return _lower_action(_single_parse_child(node), env, current_act=current_act, recent_act=recent_act)

    raise RuntimeError(f"unsupported admitted action production {pid}")


def _lower_sequence(node: ParseNode, env: _Env, *, current_act: ActId | None, body: bool) -> HastExecutable:
    units = _flatten_sequence(node, body=body)
    actions: list[HastExecutable] = []
    recent: ActId | None = None
    for unit in units:
        action = _lower_action(unit, env, current_act=current_act, recent_act=recent)
        actions.append(action)
        recent = action.act if isinstance(action, HastPerformAct) else None
    if len(actions) == 1:
        return actions[0]
    assert node.original is not None
    return HastThen(node.original, tuple(actions))


def resolve_a13_program(root: ParseNode) -> HastCoreProgram:
    if root.symbol != "CoreProgram":
        raise RuntimeError("A13 resolver requires a CoreProgram parse root")
    if root.original is None:
        raise RuntimeError("CoreProgram lacks source span")
    env = _Env()
    preparation_hast = []

    prep_nodes: list[ParseNode] = []
    prep_children = _child_nodes(root, "Preparation")
    if prep_children:
        prep_nodes = _flatten_preparation(prep_children[0])

    for wrapper in prep_nodes:
        inner = _single_parse_child(wrapper) if wrapper.production_id != "A13.PREP.PLACE.INTRODUCE" else wrapper
        pid = wrapper.production_id

        if pid == "A13.PREP.PLACE.INTRODUCE":
            names = _direct_leaves(wrapper, "PlaceName")
            assert len(names) == 2
            if names[0].text != names[1].text:
                raise _issue(
                    "REF0001", "Initialized place introduction must explicitly repeat the same place name.",
                    "הצגת מקום מאותחל חייבת לחזור במפורש על אותו שם מקום.", names[1],
                    expected=names[0].text, actual=names[1].text,
                )
            name = names[0].text
            if name in env.places:
                raise _issue("REF0102", "Duplicate place name.", "שם מקום כפול.", names[0], name=name)
            value_node = _one_child(wrapper, "NumberValue")
            initial = _lower_number(value_node, env, current_act=None, recent_act=None, pending_self_place=name)
            place = PlaceId(env.serial(), name)
            env.places[name] = place
            preparation_hast.append(HastPlaceIntroduction(wrapper.original or root.original, place, initial))
            continue

        if pid == "A13.PREP.ACT.INTRODUCE":
            leaf = _all_leaves(inner, "ActionName")[0]
            name = leaf.text
            if name in env.acts:
                raise _issue("REF0103", "Duplicate act name.", "שם מעשה כפול.", leaf, name=name)
            act = ActId(env.serial(), name)
            env.acts[name] = act
            preparation_hast.append(HastActIntroduction(wrapper.original or root.original, act))
            continue

        if pid == "A13.PREP.ROLE.DECLARE":
            owners = _direct_leaves(inner, "RoleOwnerActionName")
            roles = _direct_leaves(inner, "DeclaredRoleName")
            if not owners or not roles:
                raise RuntimeError("role declaration shape")
            if len({x.text for x in owners}) != 1 or len({x.text for x in roles}) != 1:
                raise _issue(
                    "REF0001", "Role declaration repeated descriptions must co-refer explicitly.",
                    "התיאורים החוזרים בהצהרת תפקיד חייבים להתייחס במפורש לאותם שמות.",
                    owners[-1] if len({x.text for x in owners}) != 1 else roles[-1],
                )
            owner_name, role_name = owners[0].text, roles[0].text
            if owner_name not in env.acts:
                raise _issue("REF0107", "Role owner act has not been introduced.", "המעשה בעל התפקיד טרם הוצג.", owners[0], owner=owner_name)
            owner = env.acts[owner_name]
            if owner.serial in env.bodies:
                raise _issue("REF0108", "Role declaration appears after its owner's body definition.", "הצהרת תפקיד מופיעה לאחר הגדרת גוף המעשה בעליו.", roles[0], owner=owner_name, role=role_name)
            key = (owner.serial, role_name)
            if key in env.roles:
                raise _issue("REF0104", "Duplicate role name within one act.", "שם תפקיד כפול בתוך מעשה אחד.", roles[0], owner=owner_name, role=role_name)
            role = RoleId(env.serial(), owner, role_name)
            env.roles[key] = role
            preparation_hast.append(HastRoleDeclaration(wrapper.original or root.original, role))
            continue

        if pid == "A13.PREP.BODY.DEFINE":
            body_node = inner
            names = _direct_leaves(body_node, "BodyActionName")
            assert len(names) == 2
            if names[0].text != names[1].text:
                raise _issue(
                    "REF0021", "Body opener and closer must explicitly name the same act.",
                    "פותח הגוף וסוגר הגוף חייבים לנקוב במפורש באותו מעשה.", names[1],
                    expected=names[0].text, actual=names[1].text,
                )
            name = names[0].text
            if name not in env.acts:
                raise _issue("REF0109", "Body owner act has not been introduced.", "המעשה בעל הגוף טרם הוצג.", names[0], owner=name)
            act = env.acts[name]
            if act.serial in env.bodies:
                raise _issue("REF0105", "Duplicate body definition for one act.", "הגדרת גוף כפולה לאותו מעשה.", names[0], act=name)
            body = _lower_sequence(_one_child(body_node, "BodySequence"), env, current_act=act, body=True)
            env.bodies.add(act.serial)
            preparation_hast.append(HastActBody(wrapper.original or root.original, act, body))
            continue

        raise RuntimeError(f"unsupported A13 preparatory production {pid}")

    missing_bodies = [act for act in env.acts.values() if act.serial not in env.bodies]
    if missing_bodies:
        act = sorted(missing_bodies)[0]
        raise _issue(
            "SEM0203", "Every introduced Core act requires exactly one body before principal execution.",
            "לכל מעשה שהוצג ב־Core נדרש גוף אחד בדיוק לפני הביצוע העיקרי.", root,
            missing=[a.spelling for a in sorted(missing_bodies)],
        )

    principal_node = _one_child(root, "PrincipalExecution")
    seq = _one_child(principal_node, "ExecutableSequence")
    principal = _lower_sequence(seq, env, current_act=None, body=False)

    def body_has_output(action: HastExecutable) -> bool:
        if isinstance(action, HastProduceResult):
            return True
        if isinstance(action, HastThen):
            return any(body_has_output(x) for x in action.actions)
        if isinstance(action, HastConditional):
            return body_has_output(action.if_holds) or body_has_output(action.if_not)
        if isinstance(action, (HastFixedRecurrence, HastPostActionRecurrence)):
            return body_has_output(action.action)
        return False

    places = tuple(sorted(env.places.values()))
    acts = tuple(sorted(env.acts.values()))
    roles = tuple(sorted(env.roles.values()))
    body_by_act = {x.act: x.body for x in preparation_hast if isinstance(x, HastActBody)}
    return HastCoreProgram(
        root.original,
        tuple(preparation_hast),
        principal,
        places,
        acts,
        roles,
        tuple(HastPlaceDomain(x, NATURAL) for x in places),
        tuple(HastRoleDomain(x, NATURAL) for x in roles),
        tuple(HastActOutputDomain(x, NATURAL if body_has_output(body_by_act[x]) else None) for x in acts),
        (),
    )


__all__ = ["A13ResolutionIssue", "A13ResolutionError", "resolve_a13_program"]
