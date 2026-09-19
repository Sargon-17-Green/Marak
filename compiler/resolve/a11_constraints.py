from __future__ import annotations

from dataclasses import dataclass

from compiler.parse.forest import ParseElement, ParseLeaf, ParseNode
from compiler.source.source_map import OriginalSpan


@dataclass(frozen=True, slots=True)
class A11ConstraintIssue:
    code: str
    message_en: str
    message_he: str
    source_span: OriginalSpan | None
    metadata: dict[str, object]


def _direct_leaves(node: ParseNode, role: str) -> tuple[ParseLeaf, ...]:
    return tuple(
        child for child in node.children
        if isinstance(child, ParseLeaf) and child.terminal_role == role
    )


def _all_leaves(element: ParseElement, role: str) -> tuple[ParseLeaf, ...]:
    if isinstance(element, ParseLeaf):
        return (element,) if element.terminal_role == role else ()
    out: list[ParseLeaf] = []
    for child in element.children:
        out.extend(_all_leaves(child, role))
    return tuple(out)


def _all_nodes(element: ParseElement, production_id: str) -> tuple[ParseNode, ...]:
    if isinstance(element, ParseLeaf):
        return ()
    out = [element] if element.production_id == production_id else []
    for child in element.children:
        out.extend(_all_nodes(child, production_id))
    return tuple(out)


def _require_same(
    leaves: tuple[ParseLeaf, ...],
    *,
    code: str,
    rule: str,
    message_en: str,
    message_he: str,
) -> A11ConstraintIssue | None:
    if len(leaves) < 2:
        return None
    expected = leaves[0].text
    for leaf in leaves[1:]:
        if leaf.text != expected:
            return A11ConstraintIssue(
                code, message_en, message_he, leaf.original,
                {
                    "rule": rule,
                    "expected_name": expected,
                    "actual_name": leaf.text,
                },
            )
    return None


def find_a11_constraint_issues(root: ParseNode) -> tuple[A11ConstraintIssue, ...]:
    out: list[A11ConstraintIssue] = []
    _visit(root, out)
    return tuple(out)


def _visit(node: ParseNode, out: list[A11ConstraintIssue]) -> None:
    if node.production_id == "A11.BODY.DEFINITION":
        issue = _require_same(
            _direct_leaves(node, "BodyActionName"),
            code="REF0011",
            rule="a11-body-opener-closer-explicit-co-reference",
            message_en="The A11 body opener and closer must explicitly name the same act; no nearest-open-body rule repairs a mismatch.",
            message_he="פותח הגוף וסוגר הגוף ב-A11 חייבים לנקוב במפורש באותו מעשה; אין כלל של 'הגוף הפתוח הקרוב ביותר' המתקן אי-התאמה.",
        )
        if issue:
            out.append(issue)

        body_names = _direct_leaves(node, "BodyActionName")
        if body_names:
            body_name = body_names[0].text
            # Only current-role-value phrases assert that their explicitly named
            # role owner is the act whose current performance is this body.
            for role_value in _all_nodes(node, "A11.NUMBER.CURRENT.ROLE"):
                owners = _direct_leaves(role_value, "RoleOwnerActionName")
                if owners and owners[0].text != body_name:
                    out.append(A11ConstraintIssue(
                        "REF0015",
                        "A current-performance role-value phrase inside this body names a different owning act.",
                        "תיאור ערך-תפקיד של 'המעשה הזה' בתוך גוף זה נוקב במעשה בעלים אחר.",
                        owners[0].original,
                        {
                            "rule": "a11-current-performance-role-owner",
                            "body_action": body_name,
                            "role_owner_action": owners[0].text,
                        },
                    ))

    elif node.production_id == "A11.ROLE.DECLARATION":
        issue = _require_same(
            _direct_leaves(node, "RoleOwnerActionName"),
            code="REF0012",
            rule="a11-role-declaration-owner-co-reference",
            message_en="Every explicit act name in one A11 role declaration must name the same act.",
            message_he="כל שמות המעשה המפורשים בהצהרת תפקיד אחת של A11 חייבים לנקוב באותו מעשה.",
        )
        if issue:
            out.append(issue)
        issue = _require_same(
            _direct_leaves(node, "DeclaredRoleName"),
            code="REF0013",
            rule="a11-role-declaration-role-co-reference",
            message_en="The repeated role name in one A11 role declaration must be identical.",
            message_he="שם התפקיד החוזר בהצהרת תפקיד אחת של A11 חייב להיות זהה.",
        )
        if issue:
            out.append(issue)

    elif node.production_id == "A11.ACT.PERFORM.WITH.ROLES":
        performed = _direct_leaves(node, "PerformedActionName")
        # A role association has two semantically distinct subtrees:
        #   * its direct target descriptor (owner/name of the callee role), and
        #   * its NumberValue, evaluated in the caller occurrence.
        # Only direct leaves of RoleAssociations nodes belong to the target.
        # Recursively scanning RoleOwnerActionName/AssociatedRoleName would
        # incorrectly reinterpret caller-role reads inside NumberValue as target
        # ownership declarations (E-FIND-025).
        association_nodes = (
            _all_nodes(node, "A11.ROLE.ASSOCIATIONS.ONE")
            + _all_nodes(node, "A11.ROLE.ASSOCIATIONS.MORE")
        )
        if performed:
            expected = performed[0].text
            seen: set[str] = set()
            for association in association_nodes:
                owners = _direct_leaves(association, "RoleOwnerActionName")
                roles = _direct_leaves(association, "AssociatedRoleName")
                if len(owners) != 1 or len(roles) != 1:
                    continue
                owner = owners[0]
                role = roles[0]
                if owner.text != expected:
                    out.append(A11ConstraintIssue(
                        "REF0014",
                        "Each target role association must explicitly belong to the act being performed; names inside its value expression do not redefine that target.",
                        "כל שיוך של תפקיד יעד חייב להשתייך במפורש למעשה המבוצע; שמות שבתוך ביטוי הערך אינם מגדירים מחדש את היעד.",
                        owner.original,
                        {
                            "rule": "a11-performance-target-role-owner-co-reference",
                            "performed_action": expected,
                            "role_owner_action": owner.text,
                        },
                    ))
                if role.text in seen:
                    out.append(A11ConstraintIssue(
                        "REF0016",
                        "The same target role is associated more than once in one performance.",
                        "אותו תפקיד יעד שויך יותר מפעם אחת באותו ביצוע.",
                        role.original,
                        {"rule": "a11-no-duplicate-target-role-association", "role_name": role.text},
                    ))
                seen.add(role.text)

    elif node.production_id in {"A11.LOCAL.INTRODUCE", "A11.LOCAL.REPLACE"}:
        issue = _require_same(
            _direct_leaves(node, "LocalPlaceName"),
            code="REF0017",
            rule="a11-local-place-explicit-co-reference",
            message_en="The repeated local-place descriptions in this A11 construction must explicitly name the same performance-owned place.",
            message_he="תיאורי המקום המקומי החוזרים במבנה A11 זה חייבים לנקוב במפורש באותו מקום השייך לביצוע.",
        )
        if issue:
            out.append(issue)

    for child in node.children:
        if isinstance(child, ParseNode):
            _visit(child, out)


__all__ = ["A11ConstraintIssue", "find_a11_constraint_issues"]
