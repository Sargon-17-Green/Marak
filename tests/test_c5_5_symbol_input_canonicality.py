from __future__ import annotations

from compiler.api import compile_source
from compiler.backend.portable import execute_ir
from compiler.models.domains import CollectionDomain, SymbolMemberId
from compiler.models.values import CollectionValue, SymbolValue
from compiler.runtime.invocation import (
    INPUT_DOMAIN_MISMATCH,
    InputBinding,
    ValidatedInvocation,
    validate_invocation,
)
from compiler.runtime.ir_reference import execute_reference_ir
from compiler.runtime.observables import (
    backend_observable,
    ir_reference_observable,
    reference_observable,
)
from compiler.runtime.reference import execute_reference
from tests.test_c5_2_surface_pipeline import (
    member,
    num,
    place_nat,
    replace_nat,
    symbol_domain,
)
from tests.test_c5_5_program_inputs import (
    input_nat,
    input_nat_ref,
    place_nat_value,
    subtract,
)


def input_symbol(role: str, domain: str) -> str:
    return (
        f"יהי למלאכה הזאת דבר ושמו {role} "
        f"ובטרם תחל המלאכה הזאת יעמד שם ממשפחת השמות אשר שמה {domain} "
        f"תחת הדבר אשר למלאכה הזאת שמו {role}"
    )


def input_collection(role: str, kind: str) -> str:
    return (
        f"יהי למלאכה הזאת דבר ושמו {role} "
        f"ובטרם תחל המלאכה הזאת יעמד {kind} "
        f"תחת הדבר אשר למלאכה הזאת שמו {role}"
    )


def input_id(compiled, spelling: str):
    return next(
        item.input_id
        for item in compiled.ir.program_input_domains
        if item.input_id.spelling == spelling
    )


def input_domain(compiled, spelling: str):
    return next(
        item.domain
        for item in compiled.ir.program_input_domains
        if item.input_id.spelling == spelling
    )


def three(compiled, bindings):
    h = reference_observable(execute_reference(compiled.hast, bindings=bindings))
    i = ir_reference_observable(execute_reference_ir(compiled.ir, bindings=bindings))
    b = backend_observable(execute_ir(compiled.ir, bindings=bindings))
    assert h == i == b
    return b


def symbol_program(*, external_label: str = "אדום", preparation_fault: bool = False):
    domain, declared, role = "צבעים", "אדוםפנימי", "צבעקלט"
    parts = [
        symbol_domain(domain),
        member(domain, declared, 1, external_label),
        input_symbol(role, domain),
    ]
    if preparation_fault:
        natural_role = "מספרקלט"
        parts.extend([
            input_nat(natural_role),
            place_nat_value(
                "שגיאה",
                subtract(input_nat_ref(natural_role), num(1)),
            ),
            "ועתה " + replace_nat("שגיאה", num(1)),
        ])
    else:
        parts.extend([
            place_nat("יעד", 1),
            "ועתה " + replace_nat("יעד", num(1)),
        ])
    src = " ".join(parts)
    compiled = compile_source(src)
    assert compiled.valid, [d.to_dict() for d in compiled.diagnostics]
    declaration = compiled.ir.symbol_members[0]
    return compiled, role, declaration


def assert_domain_mismatch(observed):
    assert observed["outcome"] == "InvalidInvocation"
    assert [issue["code"] for issue in observed["issues"]] == [INPUT_DOMAIN_MISMATCH]


def test_undeclared_symbol_member_is_rejected_before_preparation_in_all_engines():
    compiled, role, declaration = symbol_program(preparation_fault=True)
    pid = input_id(compiled, role)

    natural_pid = input_id(compiled, "מספרקלט")
    natural_binding = InputBinding(natural_pid, __import__(
        "compiler.models.values", fromlist=["NaturalValue"]
    ).NaturalValue(2))

    valid = three(
        compiled,
        (
            InputBinding(
                pid,
                SymbolValue(
                    declaration.domain_id,
                    declaration.member_id,
                    declaration.external_label,
                ),
            ),
            natural_binding,
        ),
    )
    assert valid["outcome"] == "Error"
    assert valid["error"]["phase"] == "PREPARATION"

    invented = SymbolMemberId(
        declaration.member_id.serial + 1000,
        "מומצא",
    )
    invalid = three(
        compiled,
        (
            InputBinding(
                pid,
                SymbolValue(declaration.domain_id, invented, "מומצא"),
            ),
            natural_binding,
        ),
    )
    assert_domain_mismatch(invalid)


def test_declared_symbol_with_forged_external_label_is_rejected_not_normalized():
    compiled, role, declaration = symbol_program()
    pid = input_id(compiled, role)
    observed = three(
        compiled,
        (InputBinding(
            pid,
            SymbolValue(
                declaration.domain_id,
                declaration.member_id,
                "תווית מזויפת",
            ),
        ),),
    )
    assert_domain_mismatch(observed)


def test_exact_declared_symbol_member_and_canonical_label_pass():
    compiled, role, declaration = symbol_program()
    pid = input_id(compiled, role)
    observed = three(
        compiled,
        (InputBinding(
            pid,
            SymbolValue(
                declaration.domain_id,
                declaration.member_id,
                declaration.external_label,
            ),
        ),),
    )
    assert observed["outcome"] == "Normal"


def test_collection_of_symbol_recursively_validates_members_and_labels():
    domain, declared, role = "צבעים", "אדוםפנימי", "ספרצבעים"
    src = " ".join([
        symbol_domain(domain),
        member(domain, declared, 1, "אדום"),
        input_collection(role, f"ספר שמות ממשפחת השמות אשר שמה {domain}"),
        place_nat("יעד", 1),
        "ועתה " + replace_nat("יעד", num(2)),
    ])
    compiled = compile_source(src)
    assert compiled.valid, [d.to_dict() for d in compiled.diagnostics]
    pid = input_id(compiled, role)
    declared_domain = input_domain(compiled, role)
    declaration = compiled.ir.symbol_members[0]
    element_domain = declared_domain.element_domain

    valid_symbol = SymbolValue(
        declaration.domain_id,
        declaration.member_id,
        declaration.external_label,
    )
    valid = CollectionValue(element_domain, (valid_symbol,))
    assert three(compiled, (InputBinding(pid, valid),))["outcome"] == "Normal"

    invented = SymbolValue(
        declaration.domain_id,
        SymbolMemberId(declaration.member_id.serial + 1000, "מומצא"),
        "מומצא",
    )
    assert_domain_mismatch(
        three(
            compiled,
            (InputBinding(pid, CollectionValue(element_domain, (invented,))),),
        )
    )

    forged = SymbolValue(
        declaration.domain_id,
        declaration.member_id,
        "תווית מזויפת",
    )
    assert_domain_mismatch(
        three(
            compiled,
            (InputBinding(pid, CollectionValue(element_domain, (forged,))),),
        )
    )


def test_nested_collection_of_symbol_rejects_deep_forged_label():
    domain, declared, role = "צבעים", "אדוםפנימי", "ספריספריצבעים"
    src = " ".join([
        symbol_domain(domain),
        member(domain, declared, 1, "אדום"),
        input_collection(role, f"ספר ספרי שמות ממשפחת השמות אשר שמה {domain}"),
        place_nat("יעד", 1),
        "ועתה " + replace_nat("יעד", num(2)),
    ])
    compiled = compile_source(src)
    assert compiled.valid, [d.to_dict() for d in compiled.diagnostics]
    pid = input_id(compiled, role)
    declared_domain = input_domain(compiled, role)
    assert isinstance(declared_domain, CollectionDomain)
    inner_domain = declared_domain.element_domain
    assert isinstance(inner_domain, CollectionDomain)
    declaration = compiled.ir.symbol_members[0]

    forged = SymbolValue(
        declaration.domain_id,
        declaration.member_id,
        "תווית מזויפת",
    )
    inner = CollectionValue(inner_domain.element_domain, (forged,))
    outer = CollectionValue(inner_domain, (inner,))
    assert_domain_mismatch(three(compiled, (InputBinding(pid, outer),)))


def test_manually_constructed_validated_invocation_is_revalidated_semantically():
    compiled, role, declaration = symbol_program()
    pid = input_id(compiled, role)
    forged = SymbolValue(
        declaration.domain_id,
        declaration.member_id,
        "תווית מזויפת",
    )
    stale_or_foreign_token = ValidatedInvocation(
        (InputBinding(pid, forged),),
        pid.program_contract,
    )
    assert_domain_mismatch(three(compiled, stale_or_foreign_token))


def test_cross_program_symbol_metadata_collision_does_not_bypass_membership_layer():
    a, role_a, member_a = symbol_program(external_label="אדום")
    b, role_b, member_b = symbol_program(external_label="כחול")
    aid = input_id(a, role_a)
    bid = input_id(b, role_b)

    assert aid.serial == bid.serial
    assert aid.spelling == bid.spelling
    assert aid.program_contract != bid.program_contract
    assert member_a.domain_id == member_b.domain_id
    assert member_a.member_id == member_b.member_id
    assert member_a.external_label != member_b.external_label

    value_valid_only_for_a = SymbolValue(
        member_a.domain_id,
        member_a.member_id,
        member_a.external_label,
    )

    validated_a = validate_invocation(
        a.ir,
        (InputBinding(aid, value_valid_only_for_a),),
    )
    assert isinstance(validated_a, ValidatedInvocation)

    # Use B's correct ProgramInputId so ownership passes. Rejection must come
    # from B's own canonical Symbol member metadata, independently.
    assert_domain_mismatch(
        three(
            b,
            (InputBinding(bid, value_valid_only_for_a),),
        )
    )
