from __future__ import annotations

import dataclasses

import pytest

from compiler.api import compile_source
from compiler.models import hast as H
from compiler.models import ir as I
from compiler.models.domains import BIDIRECTIONAL_INDEX
from compiler.parse.current_registry import CURRENT_REGISTRY
from compiler.validate.ir_canonical import CanonicalIRValidationError, validate_canonical_ir
from compiler.validate.domains import DomainValidationError, validate_hast_domains
from tests.test_c5_2_surface_pipeline import (
    act, body, num, output, perform_one, place_nat, place_typed, replace_nat,
)
from tests.test_c5_6_general_index_surface import (
    general_index, general_place, index_lt, input_general, input_general_ref,
    replace_general,
)


def _codes(source: str) -> list[str]:
    c = compile_source(source)
    assert not c.valid, "negative C5.6 source unexpectedly compiled"
    return [d.code for d in c.diagnostics]


@pytest.mark.parametrize("bad", [
    "מעלה",
    "מעלות",
    "מעלת",
    "היתד",
    "מעלת יתד",
    "מעלה היתד",
    "מעלה אחת",
    "אחת לפני מעלת היתד",
    "מעלה אחת לפני היתד",
    "שתי מעלה לפני מעלת היתד",
    "אפס מעלות לפני מעלת היתד",
    "אפס מעלות אחרי מעלת היתד",
    "מעלת אין",
    "מעלה אין",
    "מינוס מעלה אחת",
    "שנה אחת לפני מעלת היתד",
    "מעלה אחת לפני שנת אין",
    "מספר מעלה",
    "מספר יום",
    "מספר היום",
    "המעלה המעלה אשר במקום אשר שמו יעד",
])
def test_negative_general_index_forms_are_not_rescued_by_typed_place_context(bad):
    src = " ".join([
        place_typed("יעד", bad),
        "ועתה " + replace_nat("דגל", num(1)),
    ])
    # A second ordinary place makes this a whole-program grammar test.
    src = place_nat("דגל", 1) + " " + src
    _codes(src)


def test_expected_type_does_not_rescue_malformed_general_surface_across_contexts():
    malformed = "מעלה אחת לפני היתד"
    sources = [
        " ".join([
            place_nat("דגל", 1),
            place_typed("יעד", general_index(0)),
            "ועתה " + replace_general("יעד", malformed),
        ]),
        " ".join([
            place_nat("דגל", 1),
            act("א"),
            # Existing Index role declaration; malformed association still cannot be rescued.
            "יהי במעשה אשר שמו א דבר ושמו ת ובעשות את המעשה אשר שמו א יעמד מספר שנה תחת הדבר אשר במעשה אשר שמו א שמו ת",
            body("א", output(general_index(0))),
            "ועתה " + perform_one("א", "ת", malformed),
        ]),
        " ".join([
            place_nat("דגל", 1),
            act("א"), body("א", output(malformed)),
            "ועתה עשה את המעשה אשר שמו א",
        ]),
        " ".join([
            input_general("קלט"),
            place_nat("דגל", 1),
            "ועתה אם " + index_lt(malformed, input_general_ref("קלט")) +
            " " + replace_nat("דגל", num(1)) +
            " ואם לא " + replace_nat("דגל", num(2)),
        ]),
    ]
    for src in sources:
        _codes(src)


@pytest.mark.parametrize("source", [
    # Invented primitive A אחרי B.
    "יהי מקום ושמו דגל ובמקום אשר שמו דגל יהי המספר אשר הוא אחת לבדו ועתה אם מעלת היתד אחרי מעלה אחת אחרי מעלת היתד שים במקום אשר שמו דגל את המספר אשר הוא אחת תחת המספר אשר במקום אשר שמו דגל ואם לא שים במקום אשר שמו דגל את המספר אשר הוא אחת תחת המספר אשר במקום אשר שמו דגל",
    # Direct Index equality.
    "יהי מקום ושמו דגל ובמקום אשר שמו דגל יהי המספר אשר הוא אחת לבדו ועתה אם מעלת היתד הוא מעלת היתד שים במקום אשר שמו דגל את המספר אשר הוא אחת תחת המספר אשר במקום אשר שמו דגל ואם לא שים במקום אשר שמו דגל את המספר אשר הוא אחת תחת המספר אשר במקום אשר שמו דגל",
    # Direct distance noun surface.
    "יהי מקום ושמו יעד ובמקום אשר שמו יעד יהי המספר אשר הוא אחת לבדו ועתה שים במקום אשר שמו יעד את מספר המעלות שבין מעלת היתד ובין מעלה אחת אחרי מעלת היתד תחת המספר אשר במקום אשר שמו יעד",
    # Forbidden generic Index collection kind.
    "יהי מקום ושמו ספר ובמקום אשר שמו ספר יהי ספר מעלות אשר אין בו מעלה לבדו ועתה שים במקום אשר שמו ספר את ספר מעלות אשר אין בו מעלה תחת הספר אשר במקום אשר שמו ספר",
])
def test_forbidden_surface_expansions_remain_absent(source):
    _codes(source)


def test_a17_words_remain_available_in_explicit_name_slots():
    src = " ".join([
        place_nat("מעלה", 1),
        act("היתד"),
        body("היתד", replace_nat("מעלה", num(2))),
        "ועתה עשה את המעשה אשר שמו היתד",
    ])
    c = compile_source(src)
    assert c.valid, [d.to_dict() for d in c.diagnostics]


def test_canonical_ir_rejects_non_index_strict_order_operand():
    src = " ".join([
        place_nat("דגל", 1),
        "ועתה אם " + index_lt(general_index(-1), general_index(1)) +
        " " + replace_nat("דגל", num(1)) +
        " ואם לא " + replace_nat("דגל", num(2)),
    ])
    c = compile_source(src)
    assert c.valid, [d.to_dict() for d in c.diagnostics]
    assert isinstance(c.ir.principal, I.IRConditional)
    prop = c.ir.principal.proposition
    assert isinstance(prop, I.IRIndexLTProposition)
    forged = dataclasses.replace(
        c.ir,
        principal=dataclasses.replace(
            c.ir.principal,
            proposition=dataclasses.replace(
                prop,
                left=I.IRNatural(prop.source_span, 1),
            ),
        ),
    )
    with pytest.raises(CanonicalIRValidationError, match="IR_INDEX_LT_DOMAIN"):
        validate_canonical_ir(forged)


def test_scope_has_no_profile_semantic_field_or_generic_index_collection_kind():
    assert "c5.6-" in CURRENT_REGISTRY.registry_version
    forbidden_ids = (
        "DISTANCE", "INDEX_EQUAL", "GENERIC_INDEX_COLLECTION",
        "DAY", "DATE", "TIME", "TIMESTAMP",
    )
    for prod in CURRENT_REGISTRY.productions:
        assert not any(x in prod.production_id for x in forbidden_ids)
    assert [f.name for f in dataclasses.fields(H.HastIndexValue)] == [
        "source_span", "side", "magnitude"
    ]
    assert [f.name for f in dataclasses.fields(I.IRIndexValue)] == [
        "source_span", "side", "magnitude"
    ]


def test_malformed_generic_program_input_reference_is_not_rescued_by_declared_index_domain():
    src = " ".join([
        input_general("קלט"),
        place_nat("דגל", 1),
        # Missing ROLE after שמו: expected Index context must not complete it.
        "יהי מקום ושמו יעד ובמקום אשר שמו יעד יהי "
        "המעלה אשר עומדת תחת הדבר אשר למלאכה הזאת שמו לבדו",
        "ועתה " + replace_nat("דגל", num(1)),
    ])
    _codes(src)


def test_hast_domain_validation_rejects_wrong_index_lt_operand_even_if_forged_directly():
    src = " ".join([
        place_nat("דגל", 2),
        "ועתה אם " + index_lt(general_index(-1), general_index(1)) +
        " " + replace_nat("דגל", num(1)) +
        " ואם לא " + replace_nat("דגל", num(2)),
    ])
    c = compile_source(src)
    assert c.valid, [d.to_dict() for d in c.diagnostics]
    assert isinstance(c.hast.principal, H.HastConditional)
    prop = c.hast.principal.proposition
    assert isinstance(prop, H.HastIndexLTProposition)
    forged = dataclasses.replace(
        c.hast,
        principal=dataclasses.replace(
            c.hast.principal,
            proposition=dataclasses.replace(
                prop,
                left=H.HastExactNatural(prop.source_span, 1),
            ),
        ),
    )
    with pytest.raises(DomainValidationError, match="DOMAIN_INDEX_LT"):
        validate_hast_domains(forged)
