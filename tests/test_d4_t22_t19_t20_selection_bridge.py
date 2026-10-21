"""Isolated real T19 bowl1/seal10 -> T20 choice bridge for T22.

The bowls here are deliberately synthetic and bounded: this is a three-engine
component regression, NOT a T22 full production E2E or c=t drop receipt.
No accepted T21 whitelist extension is permitted.
"""
from __future__ import annotations

import pytest

from compiler.api import compile_source
from compiler.backend.portable import execute_ir
from compiler.runtime.ir_reference import execute_reference_ir
from compiler.runtime.observables import backend_observable, ir_reference_observable, reference_observable
from compiler.runtime.reference import execute_reference
from compiler.runtime.constructive_fingerprint_guard import approved_canonical_program
from tests.test_c5_3_collections import (
    append_books_nat, book_place, count, empty_books_nat, nat_book, nth_book,
    place_book, replace_book, sort_lex_nat,
)
from tests.test_c5_2_surface_pipeline import place_nat
from tests.test_d4_t19_luach15 import _perform
from tests.test_d4_t20_luach16 import (
    _call_choice_expr, _counted, _nat, _oracle as _choice_oracle,
    _place, _preparation, _setup,
)


YEAR_RECORDS = (
    (400, 3, 10),
    (252, 5, 11),
    (5781, 1, 12),
    (400, 1, 8),
    (400, 2, 9),
)
SORTED_RECORDS = sorted(YEAR_RECORDS, key=lambda row: (row[0], row[1]))
SEAL = "חותם תחילת שנת חמשת אלפים ולסופה"


def _oracle(m: int):
    # Synthetic bowl fills [10,20,30,40,50,60] and preserved visible-drop
    # order [2,4,1,3,6,5] => bowl 1's successor is bowl 3.
    fill_1, fill_successor, fill_6 = 10, 30, 60
    seal = 10

    def keep(n: int) -> int:
        return n % m or m

    first = keep((fill_1 + seal + 181) ** 2 + 179 * fill_successor + seal)
    direction = keep((first + seal + 1 + 193) ** 2 + 193 * first + 197 * fill_6) % 2
    selection = _choice_oracle(m, len(YEAR_RECORDS), first, direction)["way"]
    return first, direction, selection


def _set_number(payload: str, expr: str) -> str:
    name = _counted(payload)
    return f"שים במקום אשר שמו {name} את {expr} תחת {_place(payload)}"


def _source(m: int) -> str:
    book = empty_books_nat()
    for row in YEAR_RECORDS:
        book = append_books_nat(book, nat_book(*row))

    declarations = " ".join([
        place_nat(_counted("מענה השנה"), 1),
        place_nat(_counted("כיוון השנה"), 1),
        place_book("מועמדים", book),
        place_book("נבחרת", nat_book(1)),
    ])

    actions = [
        _setup(m),
        replace_book("מועמדים", sort_lex_nat(book_place("מועמדים"))),
        _perform("חשב מענה ראשון", [
            ("קערה", _nat(1)),
            ("חותם", _place(SEAL)),
        ]),
        _set_number("מענה השנה", "המספר אשר יצא עתה מן המעשה אשר שמו " + _counted("חשב מענה ראשון")),
        _perform("חשב כיוון המענה", [
            ("מענה", _place("מענה השנה")),
            ("חותם", _place(SEAL)),
        ]),
        _set_number("כיוון השנה", "המספר אשר יצא עתה מן המעשה אשר שמו " + _counted("חשב כיוון המענה")),
        _call_choice_expr(
            count(book_place("מועמדים")),
            _place("מענה השנה"),
            _place("כיוון השנה"),
        ),
        replace_book(
            "נבחרת",
            nth_book(
                book_place("מועמדים"),
                "המספר אשר יצא עתה מן המעשה אשר שמו בחירה",
            ),
        ),
    ]
    return _preparation(declarations) + " ועתה " + " ואחרי כן ".join(actions)


@pytest.mark.parametrize("m", [13, 17])
def test_bowl1_seal10_real_t19_t20_selection_from_ordered_year_records(m: int):
    c = compile_source(_source(m))
    assert c.valid, [d.to_dict() for d in c.diagnostics]
    assert not approved_canonical_program(c.hast, "hast")
    assert not approved_canonical_program(c.ir, "ir")

    h = reference_observable(execute_reference(c.hast, constructive_intrinsics=True))
    i = ir_reference_observable(execute_reference_ir(c.ir, constructive_intrinsics=True))
    b = backend_observable(execute_ir(c.ir, constructive_intrinsics=True))
    assert h == i == b

    first, direction, selected = _oracle(m)
    assert [v for a, v in b["products"] if a == "חשב מענה ראשון"][-1] == first
    assert [v for a, v in b["products"] if a == "חשב כיוון המענה"][-1] == direction
    assert [v for a, v in b["products"] if a == "בחירה"][-1] == selected
    facts = dict(b["facts"])
    assert facts["מועמדים"] == [list(r) for r in SORTED_RECORDS]
    assert facts["נבחרת"] == list(SORTED_RECORDS[selected - 1])
