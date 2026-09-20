from __future__ import annotations

import hashlib
from pathlib import Path

from compiler.api import compile_source
from compiler.backend.portable import execute_ir
from compiler.models.domains import NATURAL
from compiler.models.values import BidirectionalIndexValue, NaturalValue
from compiler.parse.a15_numerals import format_natural
from compiler.runtime.invocation import InputBinding
from compiler.runtime.ir_reference import execute_reference_ir
from compiler.runtime.observables import backend_observable, ir_reference_observable, reference_observable
from compiler.runtime.reference import execute_reference
from tests.test_c5_2_surface_pipeline import (
    current, gt_source, idx_place, member, num, order, place_nat, place_typed,
    pred, replace_idx, replace_nat, sym, symbol_domain,
)
from tests.test_c5_3_collections import (
    book_place, nat_book, place_book, replace_book, sort_nat,
    sort_sym, symbol_book,
)
from tests.test_c5_4_recurrence import increment, repeat_dynamic, repeat_literal
from tests.test_c5_5_program_inputs import (
    input_id, input_nat, input_nat_ref, place_nat_value,
)
from tests.test_c5_5_typed_inputs import input_index

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT / "megillah" / "original" / "Megilat_HaItim_Yehuda_FINAL_2026-09-18.md"
CANDIDATE = ROOT / "megillah" / "candidates" / "Megilat_HaItim_Marak_Candidate.md"

ORIGINAL_SHA = "7b834f4a444e021bb65164282b851af960a6dbc0be3d458c2412181773b9db7b"
D3_STARTING_CANDIDATE_SHA = "afc6eda11a8d7f4b6499cf643d2ef5b36581bcad61b5fce761a7709274d2d643"


def run_three(source: str, bindings=()):
    compiled = compile_source(source)
    assert compiled.valid, [d.to_dict() for d in compiled.diagnostics]
    h = reference_observable(execute_reference(compiled.hast, bindings=bindings))
    i = ir_reference_observable(execute_reference_ir(compiled.ir, bindings=bindings))
    b = backend_observable(execute_ir(compiled.ir, bindings=bindings))
    assert h == i == b
    return compiled, b


def test_d4_integrity_and_d3_repairs_are_preserved():
    assert hashlib.sha256(ORIGINAL.read_bytes()).hexdigest() == ORIGINAL_SHA
    text = CANDIDATE.read_text(encoding="utf-8")
    assert "יהי מעשה ושמו חיבור" in text
    assert "ולא תקח שנה אם ירבו ימיה על חמשת אלפים ושבע מאות ושבעים ושמנה" in text
    assert "וכן תעשה עד אשר" in text
    assert "ואחרי כן" in text


def test_request_001_symbol_labels_and_declared_order_are_production_executable():
    domain = "חדשים"
    first = "ראשון"
    second = "שני"
    place = "ספר"
    source = " ".join([
        symbol_domain(domain),
        member(domain, first, 1, "טין"),
        member(domain, second, 2, "הדלת הסגורה"),
        order(domain, first, second),
        place_book(place, symbol_book(domain, second, first)),
        "ועתה " + replace_book(place, sort_sym(domain, book_place(place))),
    ])
    _, observed = run_three(source)
    assert dict(observed["facts"])[place] == ["טין", "הדלת הסגורה"]


def test_request_002_bidirectional_index_crosses_zero_exactly():
    place = "שנה"
    source = " ".join([
        place_typed(place, "שנה אחת אחרי שנת אין"),
        "ועתה " + replace_idx(place, pred(idx_place(place)))
        + " ואחרי כן " + replace_idx(place, pred(idx_place(place))),
    ])
    _, observed = run_three(source)
    assert dict(observed["facts"])[place] == {"index": "BeforeZero", "magnitude": 1}


def test_request_003_ordered_collection_is_immutable_ordered_and_duplicate_preserving():
    place = "ספר"
    source = " ".join([
        place_book(place, nat_book(7, 3, 7)),
        "ועתה " + replace_book(place, sort_nat(book_place(place))),
    ])
    _, observed = run_three(source)
    assert dict(observed["facts"])[place] == [3, 7, 7]


def test_request_004_natural_ordering_is_proposition_not_boolean_value():
    _, observed = run_three(gt_source())
    assert dict(observed["facts"])["דגל"] == 1


def test_request_005_large_megillah_numeral_is_direct_and_exact():
    phrase = "ארבעה עשר אלף אלפים ושבע מאות אלף ושבעים אלף ושבעת אלפים ומאה וארבעים ותשעה"
    assert format_natural(14_777_149) == phrase
    source = " ".join([
        place_nat("גדול", 14_777_149),
        "ועתה " + replace_nat("גדול", num(14_777_149)),
    ])
    _, observed = run_three(source)
    assert dict(observed["facts"])["גדול"] == 14_777_149


def test_request_006_repeat_exactly_literal_127_executes_exact_count():
    source = " ".join([
        place_nat("מונה", 1),
        "ועתה " + repeat_literal(127, increment("מונה")),
    ])
    _, observed = run_three(source)
    assert dict(observed["facts"])["מונה"] == 128


def test_request_006_dynamic_count_composes_with_c55_program_input_and_observes_once():
    role = "מנין"
    place = "מונה"
    source = " ".join([
        input_nat(role),
        place_nat(place, 1),
        "ועתה " + repeat_dynamic(input_nat_ref(role), increment(place)),
    ])
    compiled = compile_source(source)
    assert compiled.valid, [d.to_dict() for d in compiled.diagnostics]
    pid = input_id(compiled, role)
    _, observed = run_three(source, (InputBinding(pid, NaturalValue(5)),))
    assert dict(observed["facts"])[place] == 6


def test_request_007_binding_mechanism_supports_two_distinct_natural_roles_by_identity():
    left, right, target = "מעשה", "שאלה", "יעד"
    source = " ".join([
        input_nat(left),
        input_nat(right),
        place_nat_value(target, num(1)),
        "ועתה " + replace_nat(
            target,
            f"המספר הנחשב בהוסיף את {input_nat_ref(left)} על {input_nat_ref(right)}",
        ),
    ])
    compiled = compile_source(source)
    assert compiled.valid, [d.to_dict() for d in compiled.diagnostics]
    a, b = input_id(compiled, left), input_id(compiled, right)
    _, forward = run_three(
        source,
        (InputBinding(a, NaturalValue(7)), InputBinding(b, NaturalValue(13))),
    )
    _, reverse = run_three(
        source,
        (InputBinding(b, NaturalValue(13)), InputBinding(a, NaturalValue(7))),
    )
    assert forward == reverse
    assert dict(forward["facts"])[target] == 20


def test_day_domain_audit_current_surface_has_year_index_but_no_day_index_head():
    role = "יוםקלט"
    valid_index = " ".join([
        input_index(role),
        place_typed("שמור", "שנת אין"),
        "ועתה " + replace_idx("שמור", "מספר השנה אשר עומד תחת הדבר אשר למלאכה הזאת שמו יוםקלט"),
    ])
    assert compile_source(valid_index).valid

    day_input = (
        "יהי למלאכה הזאת דבר ושמו יוםקלט "
        "ובטרם תחל המלאכה הזאת יעמד מספר יום "
        "תחת הדבר אשר למלאכה הזאת שמו יוםקלט "
        "יהי מקום ושמו יעד ובמקום אשר שמו יעד יהי המספר אשר הוא אחד לבדו "
        "ועתה שים במקום אשר שמו יעד את המספר אשר הוא אחד תחת המספר אשר במקום אשר שמו יעד"
    )
    compiled = compile_source(day_input)
    assert not compiled.valid


def test_day_natural_number_alone_is_explicitly_insufficient_in_source_evidence():
    text = CANDIDATE.read_text(encoding="utf-8")
    assert "ומן המספרים לבדם לא תדע אי זה יום לפני ואי זה יום אחרי" in text
    assert "אם יום אחד לפני חברו או אחריו מן הימים תדע ולא ממספריהם" in text


def test_five_result_fields_need_no_generic_tuple_value():
    cut_domain, month_domain = "קציצות", "חדשים"
    source = " ".join([
        symbol_domain(cut_domain),
        member(cut_domain, "ארד", 1, "ארד"),
        symbol_domain(month_domain),
        member(month_domain, "טין", 1, "טין"),
        place_typed("שנה", "שנת אין"),
        place_typed("קציצה", sym(cut_domain, "ארד")),
        place_nat("יוםקציצה", 3),
        place_typed("חדש", sym(month_domain, "טין")),
        place_nat("יוםחדש", 5),
        "ועתה " + replace_nat("יוםחדש", num(5)),
    ])
    _, observed = run_three(source)
    facts = dict(observed["facts"])
    assert facts["שנה"] == {"index": "Zero"}
    assert facts["קציצה"] == "ארד"
    assert facts["יוםקציצה"] == 3
    assert facts["חדש"] == "טין"
    assert facts["יוםחדש"] == 5


def test_program_input_invalid_invocation_stops_before_preparation():
    role = "קלט"
    target = "יעד"
    # A valid input of 2 would make Preparation attempt 1-2 and fail.
    # With no binding, invocation validation must win before Preparation starts.
    initializer = f"המספר הנחשב בגרע {input_nat_ref(role)} מן {num(1)}"
    source = " ".join([
        input_nat(role),
        place_nat_value(target, initializer),
        "ועתה " + replace_nat(target, num(1)),
    ])
    compiled = compile_source(source)
    assert compiled.valid, [d.to_dict() for d in compiled.diagnostics]
    observed = backend_observable(execute_ir(compiled.ir, bindings=()))
    assert observed["outcome"] == "InvalidInvocation"
    assert [x["code"] for x in observed["issues"]] == ["MISSING_INPUT_BINDING"]
