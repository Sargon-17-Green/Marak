from __future__ import annotations

import dataclasses
import hashlib
import json
from pathlib import Path

import pytest

from compiler.api import compile_source
from compiler.models import hast as H
from compiler.models import ir as I
from compiler.models.domains import BIDIRECTIONAL_INDEX, ProgramInputId, BidirectionalIndexDomain
from compiler.parse.c5_6_registry import C5_6_REGISTRY
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


ROOT = Path(__file__).resolve().parents[1]
C56_D4_RECEIPT = (
    ROOT / "tests" / "fixtures" / "c5_6_conformance" / "D4_HISTORICAL_RECEIPT.json"
)


def _load_c56_d4_historical_receipt() -> dict[str, object]:
    receipt = json.loads(C56_D4_RECEIPT.read_text(encoding="utf-8"))

    assert receipt["schema"] == "marak-c5-6-d4-historical-receipt-v1"
    assert receipt["c5_6"] == {
        "baseline_sha": "f7c1be2e913d73c4722f92d8c27c8c7e6dd26a91",
        "validated_implementation_head": "0dd3e270bf769a9028df3fbf7d64cafd6a09f677",
        "accepted_merge_sha": "5a5f8dae0dd8c3526de5f21f84a3a7b2aba984e3",
        "registry_version": "c5.6-a17-b16.1",
    }
    assert receipt["historical_d4_candidate"] == {
        "fixture": "tests/fixtures/c5_6_conformance/D4_CANDIDATE_AT_C5_6.md",
        "sha256": "afc6eda11a8d7f4b6499cf643d2ef5b36581bcad61b5fce761a7709274d2d643",
        "frontier": {
            "diagnostic": "PARSE0002",
            "furthest_token": 105,
            "candidate_line": 11,
            "original_line": 35,
        },
    }
    assert receipt["scope_claim"] == {
        "megillah_paths_changed_by_c5_6": [],
        "historically_unchanged_prefixes": [
            "megillah/original/",
            "megillah/candidates/",
            "megillah/analysis/",
        ],
    }
    assert receipt["live_d_state_is_out_of_scope"] is True
    return receipt


def _verify_c56_historical_d4_fixture(
    receipt: dict[str, object],
    *,
    fixture_override: Path | None = None,
) -> None:
    historical = receipt["historical_d4_candidate"]
    assert isinstance(historical, dict)
    fixture = fixture_override or ROOT / str(historical["fixture"])
    expected_sha = str(historical["sha256"])

    assert hashlib.sha256(fixture.read_bytes()).hexdigest() == expected_sha
    assert C5_6_REGISTRY.registry_version == receipt["c5_6"]["registry_version"]

    compiled = compile_source(
        fixture.read_text(encoding="utf-8"),
        file=fixture.as_posix(),
        registry=C5_6_REGISTRY,
    )
    assert not compiled.valid
    frontier = max(
        (
            d for d in compiled.diagnostics
            if isinstance((d.metadata or {}).get("furthest_token"), int)
        ),
        key=lambda d: d.metadata["furthest_token"],
    )
    expected_frontier = historical["frontier"]
    assert isinstance(expected_frontier, dict)
    assert frontier.code == expected_frontier["diagnostic"]
    assert frontier.metadata["furthest_token"] == expected_frontier["furthest_token"]
    assert frontier.source_span is not None
    assert frontier.source_span.start.line == expected_frontier["candidate_line"]


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
    assert "c5.7-" in CURRENT_REGISTRY.registry_version
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


def test_profile_is_absent_from_program_input_and_domain_semantic_identity():
    assert [f.name for f in dataclasses.fields(ProgramInputId)] == [
        "serial", "spelling", "program_contract"
    ]
    assert [f.name for f in dataclasses.fields(BidirectionalIndexDomain)] == []


def test_c56_historical_d4_receipt_reproduces_frozen_snapshot():
    receipt = _load_c56_d4_historical_receipt()
    _verify_c56_historical_d4_fixture(receipt)


def test_c56_historical_d4_receipt_rejects_fixture_tampering(tmp_path):
    receipt = _load_c56_d4_historical_receipt()
    historical = receipt["historical_d4_candidate"]
    assert isinstance(historical, dict)

    frozen = ROOT / str(historical["fixture"])
    tampered = tmp_path / frozen.name
    tampered.write_bytes(frozen.read_bytes() + b"\n# tampered\n")

    with pytest.raises(AssertionError):
        _verify_c56_historical_d4_fixture(receipt, fixture_override=tampered)


def test_c56_receipt_is_independent_of_authorized_downstream_d_candidate_bytes(tmp_path):
    receipt = _load_c56_d4_historical_receipt()
    historical = receipt["historical_d4_candidate"]
    assert isinstance(historical, dict)

    simulated_live_candidate = tmp_path / "Megilat_HaItim_Marak_Candidate.md"
    simulated_live_candidate.write_text(
        "authorized downstream D candidate evolution\n",
        encoding="utf-8",
    )
    assert (
        hashlib.sha256(simulated_live_candidate.read_bytes()).hexdigest()
        != historical["sha256"]
    )

    # The C5.6 receipt verifies its own frozen snapshot only. The simulated
    # downstream candidate is intentionally not an input to the historical proof.
    _verify_c56_historical_d4_fixture(receipt)
