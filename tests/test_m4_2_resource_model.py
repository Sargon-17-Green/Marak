from __future__ import annotations

import inspect
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from compiler.api import compile_source
from compiler.backend.portable import (
    DEFAULT_MAX_ACTIVE_PERFORMANCES as BACKEND_DEFAULT,
    PortableVM,
    VMNormal,
    VMResourceExhaustion,
    execute_ir,
)
from compiler.runtime.ir_reference import (
    DEFAULT_MAX_ACTIVE_PERFORMANCES as IRREF_DEFAULT,
    IRReferenceEvaluator,
    IRReferenceNormal,
    IRReferenceResourceExhaustion,
    execute_reference_ir,
)
from compiler.runtime.observables import backend_observable, ir_reference_observable, reference_observable
from compiler.runtime.reference import (
    DEFAULT_MAX_ACTIVE_PERFORMANCES as HAST_DEFAULT,
    NormalOutcome,
    ReferenceEvaluator,
    ResourceExhaustionOutcome,
    execute_reference,
)
from tests.test_m4_1_remediation import ZERO, act, body, current, deep_countdown, eq, num, perform, place_intro, replace, sub

ROOT = Path(__file__).resolve().parents[1]


def _three(source: str):
    c = compile_source(source)
    assert c.valid, [d.to_dict() for d in c.diagnostics]
    h = execute_reference(c.hast)
    i = execute_reference_ir(c.ir)
    b = execute_ir(c.ir)
    assert isinstance(h, NormalOutcome)
    assert isinstance(i, IRReferenceNormal)
    assert isinstance(b, VMNormal)
    assert reference_observable(h) == ir_reference_observable(i) == backend_observable(b)
    return c, h, i, b


def _sequential_many(n: int) -> str:
    # Each occurrence completes before the next recurrence iteration: high total
    # performance count, maximum nested active-performance depth == 1.
    return " ".join([
        place_intro("גד", n),
        act("ראובן"),
        body("ראובן", replace("גד", sub(num(1), current("גד")))),
        "ועתה " + perform("ראובן") + " וכן תעשה עד אשר " + eq(current("גד"), ZERO),
    ])


def test_default_has_no_artificial_active_performance_ceiling():
    assert HAST_DEFAULT is None
    assert IRREF_DEFAULT is None
    assert BACKEND_DEFAULT is None
    assert inspect.signature(execute_reference).parameters["max_active_performances"].default is None
    assert inspect.signature(execute_reference_ir).parameters["max_active_performances"].default is None
    assert inspect.signature(execute_ir).parameters["max_active_performances"].default is None


@pytest.mark.parametrize("depth", [5000, 10001, 20000])
def test_deep_finite_recursion_crosses_old_ceiling_all_layers(depth):
    c, h, i, b = _three(deep_countdown(depth))
    assert dict(backend_observable(b)["facts"])["גד"] == 0


def test_many_sequential_performances_have_no_cumulative_quota():
    _, h, i, b = _three(_sequential_many(20001))
    assert dict(backend_observable(b)["facts"])["גד"] == 0


def test_explicit_caller_budget_is_optional_tooling_control_only():
    c = compile_source(deep_countdown(300))
    assert c.valid
    h = execute_reference(c.hast, max_active_performances=100)
    i = execute_reference_ir(c.ir, max_active_performances=100)
    b = execute_ir(c.ir, max_active_performances=100)
    assert isinstance(h, ResourceExhaustionOutcome)
    assert isinstance(i, IRReferenceResourceExhaustion)
    assert isinstance(b, VMResourceExhaustion)
    for outcome in (h, i, b):
        assert "caller-imposed active performance budget 100 exhausted" in outcome.detail
    # The same finite program is normal under the default execution contract.
    assert isinstance(execute_reference(c.hast), NormalOutcome)
    assert isinstance(execute_reference_ir(c.ir), IRReferenceNormal)
    assert isinstance(execute_ir(c.ir), VMNormal)


def test_deep_execution_still_independent_of_python_recursion_limit():
    code = r'''import sys
from compiler.api import compile_source
from compiler.runtime.reference import execute_reference
from compiler.runtime.ir_reference import execute_reference_ir
from compiler.backend.portable import execute_ir
from tests.test_m4_1_remediation import deep_countdown
c=compile_source(deep_countdown(1000)); assert c.valid
sys.setrecursionlimit(80)
print(type(execute_reference(c.hast)).__name__, type(execute_reference_ir(c.ir)).__name__, type(execute_ir(c.ir)).__name__)'''
    p = subprocess.run(
        [sys.executable, "-c", code], cwd=ROOT,
        env={**os.environ, "PYTHONPATH": str(ROOT)}, text=True, capture_output=True, timeout=20,
    )
    assert p.returncode == 0, (p.stdout, p.stderr)
    assert p.stdout.strip() == "NormalOutcome IRReferenceNormal VMNormal"
    assert "RecursionError" not in p.stderr


def test_no_fuel_infinite_all_layers_have_no_default_quota_termination():
    data = json.loads((ROOT / "tests/fixtures/a13/a13_program_conformance.json").read_text(encoding="utf-8"))
    source = next(x["source"] for x in data["positive"] if x["id"] == "P-SELFREC-001")
    src = ROOT / "tests/fixtures/m4_2_infinite_subprocess.tmp"
    src.write_text(source, encoding="utf-8")
    invocations = (
        "from compiler.runtime.reference import execute_reference as ex; out=ex(c.hast)",
        "from compiler.runtime.ir_reference import execute_reference_ir as ex; out=ex(c.ir)",
        "from compiler.backend.portable import execute_ir as ex; out=ex(c.ir)",
    )
    try:
        for invocation in invocations:
            code = f'''from pathlib import Path
from compiler.api import compile_source
s=Path({str(src)!r}).read_text(encoding="utf-8")
c=compile_source(s); assert c.valid
{invocation}
print(type(out).__name__, getattr(out,"category",None))'''
            with pytest.raises(subprocess.TimeoutExpired):
                subprocess.run(
                    [sys.executable, "-c", code], cwd=ROOT,
                    env={**os.environ, "PYTHONPATH": str(ROOT)},
                    text=True, capture_output=True, timeout=0.75,
                )
    finally:
        src.unlink(missing_ok=True)


def test_activation_counters_return_to_zero_after_deep_completion_and_repeated_runs():
    c = compile_source(deep_countdown(5000))
    assert c.valid
    for cls, arg, normal in (
        (ReferenceEvaluator, c.hast, NormalOutcome),
        (IRReferenceEvaluator, c.ir, IRReferenceNormal),
        (PortableVM, c.ir, VMNormal),
    ):
        for _ in range(3):
            engine = cls(arg)
            outcome = engine.run()
            assert isinstance(outcome, normal)
            assert engine.active_performances == 0
