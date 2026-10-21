"""D4-T21-RUNTIME-001: a user-defined act body must never be shadowed by a name."""
from __future__ import annotations

from dataclasses import dataclass, replace
from unittest.mock import patch

from compiler.api import compile_source
from compiler.backend.portable import execute_ir
from compiler.runtime.constructive_fingerprint_guard import approved_canonical_program, structural_program_sha256
from compiler.runtime.ir_reference import execute_reference_ir
from compiler.runtime.observables import backend_observable, ir_reference_observable, reference_observable
from compiler.runtime.reference import execute_reference
from tests.test_c5_2_surface_pipeline import act, body, num, output, place_nat
from tests.test_d4_t21_luach17 import _call, _counted


def _adversarial_source(result: int = 7) -> str:
    name = "נותר"  # canonical intrinsic spelling, noncanonical body
    roles = [
        f"יהי במעשה אשר שמו {name} דבר ושמו {role} ובעשות את המעשה אשר שמו {name} יעמד מספר תחת הדבר אשר במעשה אשר שמו {name} שמו {role}"
        for role in ("מספר", "מחלק")
    ]
    return " ".join([
        place_nat(_counted("עבודת הנותר"), 0),
        place_nat(_counted("מחלק הנותר"), 1),
        act(name), *roles,
        body(name, output(num(result))),
        "ועתה " + _call(name, (("מספר", num(9)), ("מחלק", num(4)))),
    ])


def _observable(c, runtime: str, accelerated: bool) -> dict:
    if runtime == "hast":
        return reference_observable(execute_reference(c.hast, constructive_intrinsics=accelerated))
    if runtime == "ir":
        return ir_reference_observable(execute_reference_ir(c.ir, constructive_intrinsics=accelerated))
    if runtime == "portable":
        return backend_observable(execute_ir(c.ir, constructive_intrinsics=accelerated))
    raise AssertionError(runtime)


def test_legacy_name_only_dispatch_is_an_actual_counterexample_in_all_three_engines():
    """Simulate old missing body guard and prove the unsafe 1 != declared 7."""
    c = compile_source(_adversarial_source())
    assert c.valid, [d.to_dict() for d in c.diagnostics]
    assert [v for act, v in _observable(c, "hast", False)["products"] if act == "נותר"] == [7]
    for runtime, module in (
        ("hast", "compiler.runtime.reference"),
        ("ir", "compiler.runtime.ir_reference"),
        ("portable", "compiler.backend.portable"),
    ):
        slow = _observable(c, runtime, False)
        with patch(module + ".approved_canonical_program", return_value=True):
            unguarded_fast = _observable(c, runtime, True)
        assert slow != unguarded_fast, runtime
        assert [v for act, v in unguarded_fast["products"] if act == "נותר"] == [1]
        assert [v for act, v in slow["products"] if act == "נותר"] == [7]


def test_noncanonical_compatible_name_falls_back_in_all_three_engines():
    c = compile_source(_adversarial_source())
    assert c.valid
    assert not approved_canonical_program(c.hast, "hast")
    assert not approved_canonical_program(c.ir, "ir")
    for runtime in ("hast", "ir", "portable"):
        assert _observable(c, runtime, True) == _observable(c, runtime, False)
        assert [v for act, v in _observable(c, runtime, True)["products"] if act == "נותר"] == [7]


def test_program_fingerprint_binds_bodies_principal_and_dependencies():
    a = compile_source(_adversarial_source(7))
    b = compile_source(_adversarial_source(8))
    assert a.valid and b.valid
    assert structural_program_sha256(a.hast) != structural_program_sha256(b.hast)
    assert structural_program_sha256(a.ir) != structural_program_sha256(b.ir)
    assert structural_program_sha256(a.hast) != structural_program_sha256(a.ir)
    # A change in the compiled act table / helper definitions changes the
    # trusted whole-program fingerprint, regardless of identical spellings.
    assert structural_program_sha256(replace(a.hast, acts=())) != structural_program_sha256(a.hast)
    assert structural_program_sha256(replace(a.ir, acts=())) != structural_program_sha256(a.ir)
