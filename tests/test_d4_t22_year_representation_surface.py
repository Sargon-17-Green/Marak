"""Focused three-runtime checks for Luach 18 year representation primitives.

These are real compiled/executed Marak programs, but not yet the full T22
production year-selection path. Keep the distinctions explicit.
"""
from __future__ import annotations

from compiler.api import compile_source
from compiler.backend.portable import execute_ir
from compiler.runtime.constructive_fingerprint_guard import approved_canonical_program
from compiler.runtime.ir_reference import execute_reference_ir
from compiler.runtime.observables import backend_observable, ir_reference_observable, reference_observable
from compiler.runtime.reference import execute_reference
from tests.test_c5_3_collections import (
    append_books_nat, append_idx, book_place, empty_books_nat, empty_idx,
    nat_book, place_book, replace_book, sort_lex_nat, append_nat,
)
from tests.test_c5_6_general_index_surface import general_index
from tests.test_c5_7_multiword_source_names import counted


YEAR_NAME = (
    "שנת", "חמשת", "אלפים", "מיום", "ברוא",
    "מפלצת", "הספגטי", "המעופפת", "שמים", "וארץ",
)


def _three(source: str):
    compiled = compile_source(source)
    assert compiled.valid, [d.to_dict() for d in compiled.diagnostics]
    h = reference_observable(execute_reference(compiled.hast))
    i = ir_reference_observable(execute_reference_ir(compiled.ir))
    b = backend_observable(execute_ir(compiled.ir))
    assert h == i == b
    return compiled, h


def test_duration_opening_ordinal_lexicographic_sort_in_all_three_engines():
    # Each record is [duration, opening-gate ordinal, closing-gate ordinal].
    # Ascending ordinal corresponds to earlier opening, so lex sort equals
    # the source's (duration, earlier opening) required order.
    rows = ((400, 4, 10), (252, 6, 12), (400, 2, 8), (400, 3, 9))
    book = empty_books_nat()
    for row in rows:
        book = append_books_nat(book, nat_book(*row))
    src = " ".join([
        place_book("מועמדים", book),
        "ועתה " + replace_book("מועמדים", sort_lex_nat(book_place("מועמדים"))),
    ])
    _, obs = _three(src)
    assert dict(obs["facts"])["מועמדים"] == [
        [252, 6, 12], [400, 2, 8], [400, 3, 9], [400, 4, 10]
    ]


def test_pair_of_bidirectional_gate_indices_and_ten_word_year_name():
    name = counted(*YEAR_NAME)
    pair = append_idx(
        append_idx(empty_idx(), general_index(-1)),
        general_index(2),
    )
    src = " ".join([
        place_book(name, pair),
        "ועתה " + replace_book(name, book_place(name)),
    ])
    compiled, obs = _three(src)
    assert dict(obs["facts"])[" ".join(YEAR_NAME)] == [
        {"index": "BeforeZero", "magnitude": 1},
        {"index": "AfterZero", "magnitude": 2},
    ]
    assert any(p.spelling == " ".join(YEAR_NAME) for p in compiled.hast.places)


def test_non_t21_maraksurface_remains_outside_intrinsic_whitelist():
    name = counted(*YEAR_NAME)
    pair = append_idx(append_idx(empty_idx(), general_index(-1)), general_index(2))
    src = " ".join([place_book(name, pair), "ועתה " + replace_book(name, book_place(name))])
    compiled, original = _three(src)
    assert not approved_canonical_program(compiled.hast, "hast")
    assert not approved_canonical_program(compiled.ir, "ir")
    accelerated = (
        reference_observable(execute_reference(compiled.hast, constructive_intrinsics=True)),
        ir_reference_observable(execute_reference_ir(compiled.ir, constructive_intrinsics=True)),
        backend_observable(execute_ir(compiled.ir, constructive_intrinsics=True)),
    )
    assert all(observable == original for observable in accelerated)
