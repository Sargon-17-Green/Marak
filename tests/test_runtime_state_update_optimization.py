from __future__ import annotations

from compiler.api import compile_source
from compiler.backend.portable import execute_ir
from compiler.runtime.ir_reference import execute_reference_ir
from compiler.runtime.observables import (
    backend_observable,
    ir_reference_observable,
    reference_observable,
)
from compiler.runtime.reference import SemanticState, execute_reference
from compiler.models.symbols import PlaceId
from tests.test_c5_2_surface_pipeline import (
    act,
    body,
    current,
    num,
    perform,
    place_nat,
    replace_nat,
)


def test_semantic_state_cached_lookup_preserves_copy_out_and_replacement_contract():
    a = PlaceId(1, "א")
    b = PlaceId(2, "ב")
    s0 = SemanticState()
    s1 = s0.establish(a, 3).establish(b, 5)

    copy_out = s1.as_dict()
    copy_out[a] = 99

    assert s1.read(a) == 3
    assert s1.read(b) == 5

    s2 = s1.replace(a, 8)
    assert s1.read(a) == 3
    assert s2.read(a) == 8
    assert s2.read(b) == 5
    assert s2.facts == tuple(sorted(s2.facts, key=lambda kv: kv[0].serial))


def test_in_place_runtime_state_updates_preserve_three_runtime_language_observation():
    counter = "מונה"
    increment = "הגדל"
    source = " ".join([
        place_nat(counter, 1),
        act(increment),
        body(
            increment,
            replace_nat(
                counter,
                f"המספר הנחשב בהוסיף את {num(1)} על {current(counter)}",
            ),
        ),
        "ועתה מאה ועשרים ושבע פעמים " + perform(increment),
    ])

    compiled = compile_source(source)
    assert compiled.valid, [d.to_dict() for d in compiled.diagnostics]

    h = reference_observable(execute_reference(compiled.hast))
    i = ir_reference_observable(execute_reference_ir(compiled.ir))
    b = backend_observable(execute_ir(compiled.ir))

    assert h == i == b
    assert h["outcome"] == "Normal"
    assert dict(h["facts"])[counter] == 128
