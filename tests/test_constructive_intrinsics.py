from __future__ import annotations

from compiler.api import compile_source
from compiler.backend.portable import execute_ir
from compiler.runtime.constructive_intrinsics import constructive_intrinsic_trace
from compiler.runtime.ir_reference import execute_reference_ir
from compiler.runtime.observables import (
    backend_observable,
    ir_reference_observable,
    reference_observable,
)
from compiler.runtime.reference import execute_reference
from tests.test_d4_t21_luach17 import _call, _nat, _preparation


def _source() -> str:
    principal = " ואחרי כן ".join([
        _call("לקחת מספר פעמים", [("מספר", _nat(13)), ("מנין", _nat(11))]),
        _call("הנותר בדרך הקצרה", [("מספר", _nat(137)), ("מחלק", _nat(17))]),
        _call("נותר", [("מספר", _nat(137)), ("מחלק", _nat(17))]),
        _call("חלק", [("מספר", _nat(137)), ("מחלק", _nat(17))]),
        _call("לקחת מספר פעמים", [("מספר", _nat(0)), ("מנין", _nat(0))]),
        _call("הנותר בדרך הקצרה", [("מספר", _nat(7)), ("מחלק", _nat(11))]),
    ])
    return _preparation() + " ועתה " + principal


def test_constructive_intrinsic_pure_traces_cover_edges():
    mul = constructive_intrinsic_trace(
        "לקחת מספר פעמים",
        {"מספר": 13, "מנין": 11},
    )
    assert mul is not None
    assert mul.result == 143
    assert mul.fact_updates == (("מכפלה", 143), ("מנין הכפל הנותר", 0))
    assert mul.products == (
        ("חיבור", 104),
        ("חיבור", 130),
        ("חיבור", 143),
        ("לקחת מספר פעמים", 143),
    )

    rem = constructive_intrinsic_trace(
        "הנותר בדרך הקצרה",
        {"מספר": 137, "מחלק": 17},
    )
    assert rem is not None
    assert rem.result == 1
    assert rem.products[-1] == ("הנותר בדרך הקצרה", 1)

    simple = constructive_intrinsic_trace(
        "נותר",
        {"מספר": 137, "מחלק": 17},
    )
    assert simple is not None
    assert simple.result == 1
    assert simple.fact_updates == (
        ("עבודת הנותר", 1),
        ("מחלק הנותר", 17),
    )
    assert simple.products == (("נותר", 1),)

    divide = constructive_intrinsic_trace(
        "חלק",
        {"מספר": 137, "מחלק": 17},
    )
    assert divide is not None
    assert divide.result == 8
    assert divide.fact_updates == (
        ("עבודת החלוקה", 1),
        ("מחלק החלוקה", 17),
        ("מנת החלוקה", 8),
        ("שארית החלוקה", 1),
    )
    assert divide.products == (("חלק", 8),)

    for act in ("הנותר בדרך הקצרה", "נותר", "חלק"):
        assert constructive_intrinsic_trace(
            act,
            {"מספר": 9, "מחלק": 0},
        ) is None


def test_constructive_intrinsics_are_exactly_observable_equivalent_in_all_runtimes():
    compiled = compile_source(_source())
    assert compiled.valid, [d.to_dict() for d in compiled.diagnostics]

    slow_h = reference_observable(execute_reference(compiled.hast))
    fast_h = reference_observable(
        execute_reference(compiled.hast, constructive_intrinsics=True)
    )

    slow_i = ir_reference_observable(execute_reference_ir(compiled.ir))
    fast_i = ir_reference_observable(
        execute_reference_ir(compiled.ir, constructive_intrinsics=True)
    )

    slow_b = backend_observable(execute_ir(compiled.ir))
    fast_b = backend_observable(
        execute_ir(compiled.ir, constructive_intrinsics=True)
    )

    assert slow_h == slow_i == slow_b
    assert fast_h == fast_i == fast_b
    assert fast_h == slow_h

    products = fast_h["products"]
    assert [v for act, v in products if act == "לקחת מספר פעמים"] == [143, 0]
    assert [v for act, v in products if act == "הנותר בדרך הקצרה"][-1:] == [7]
    assert [v for act, v in products if act == "נותר"] == [1]
    assert [v for act, v in products if act == "חלק"] == [8]


def test_intrinsics_do_not_change_fuel_step_semantics():
    compiled = compile_source(_source())
    assert compiled.valid

    slow = reference_observable(execute_reference(compiled.hast, fuel=50))
    requested_fast = reference_observable(
        execute_reference(
            compiled.hast,
            fuel=50,
            constructive_intrinsics=True,
        )
    )
    assert requested_fast == slow
