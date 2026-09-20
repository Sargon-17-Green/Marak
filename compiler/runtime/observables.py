from __future__ import annotations

from typing import Any

from compiler.backend.portable import VMErrorOutcome, VMDivergence, VMNormal
from compiler.runtime.reference import DivergenceOutcome, ErrorOutcome, NormalOutcome
from compiler.runtime.ir_reference import IRReferenceDivergence, IRReferenceErrorOutcome, IRReferenceNormal
from compiler.models.values import observable_value
from compiler.runtime.invocation import InvalidInvocation


def _language_value(value):
    return value if type(value) is int else observable_value(value)


def _name_map(pairs) -> dict[int, str]:
    return dict(pairs)


def _invalid_invocation(outcome: InvalidInvocation) -> dict[str, Any]:
    return {
        "outcome": "InvalidInvocation",
        "issues": [
            {"code": x.code, "input": x.input_id.spelling, "program_contract": x.input_id.program_contract}
            for x in outcome.issues
        ],
    }


def reference_observable(outcome: object) -> dict[str, Any]:
    """B12 language-observation quotient for HAST reference execution.

    Implementation allocation serials and occurrence counters are deliberately
    erased.  Source-semantic identity is retained by typed source spelling.
    """
    if isinstance(outcome, InvalidInvocation):
        return _invalid_invocation(outcome)
    if isinstance(outcome, NormalOutcome):
        return {
            "outcome": "Normal",
            "facts": [[place.spelling, _language_value(value)] for place, value in outcome.state.facts],
            "products": [[p.act.spelling, _language_value(p.value)] for p in outcome.products],
        }
    if isinstance(outcome, ErrorOutcome):
        return {
            "outcome": "Error",
            "facts": [[place.spelling, _language_value(value)] for place, value in outcome.state.facts],
            "error": {"code": outcome.error.code, "phase": outcome.error.phase, "detail": outcome.error.detail},
            "products": [[p.act.spelling, _language_value(p.value)] for p in outcome.products],
        }
    if isinstance(outcome, DivergenceOutcome):
        return {
            "outcome": "Divergence",
            "products": [[p.act.spelling, _language_value(p.value)] for p in outcome.products],
            "harness_reason": outcome.harness_reason,
        }
    # Resource-exhaustion outcomes are implementation/tooling status, not a
    # Marak language observation.  They intentionally have their own shape.
    if type(outcome).__name__ == "ResourceExhaustionOutcome":
        return {"tooling_status": "ResourceExhausted", "category": getattr(outcome, "category", "IMPLEMENTATION_RESOURCE_EXHAUSTION")}
    raise TypeError(f"unsupported reference outcome: {type(outcome).__name__}")


def backend_observable(outcome: object) -> dict[str, Any]:
    """B12 language-observation quotient for portable backend execution."""
    if isinstance(outcome, InvalidInvocation):
        return _invalid_invocation(outcome)
    place = _name_map(getattr(outcome, "place_names", ()))
    act = _name_map(getattr(outcome, "act_names", ()))
    if isinstance(outcome, VMNormal):
        return {
            "outcome": "Normal",
            "facts": [[place[k], _language_value(value)] for k, value in outcome.facts],
            "products": [[act[p.act], _language_value(p.value)] for p in outcome.products],
        }
    if isinstance(outcome, VMErrorOutcome):
        return {
            "outcome": "Error",
            "facts": [[place[k], _language_value(value)] for k, value in outcome.facts],
            "error": {"code": outcome.error.code, "phase": outcome.error.phase, "detail": outcome.error.detail},
            "products": [[act[p.act], _language_value(p.value)] for p in outcome.products],
        }
    if isinstance(outcome, VMDivergence):
        return {
            "outcome": "Divergence",
            "products": [[act[p.act], _language_value(p.value)] for p in outcome.products],
            "harness_reason": "fuel-exhausted",
        }
    if type(outcome).__name__ == "VMResourceExhaustion":
        return {"tooling_status": "ResourceExhausted", "category": getattr(outcome, "category", "IMPLEMENTATION_RESOURCE_EXHAUSTION")}
    if type(outcome).__name__ == "ToolRuntimeFailure":
        return {"tooling_status": "InternalFailure", "category": getattr(outcome, "category", "IMPLEMENTATION_INTERNAL_FAILURE"), "host_exception_type": getattr(outcome, "host_exception_type", "Exception")}
    raise TypeError(f"unsupported backend outcome: {type(outcome).__name__}")


def ir_reference_observable(outcome: object) -> dict[str, Any]:
    """B12 language-observation quotient for canonical-IR reference execution."""
    if isinstance(outcome, InvalidInvocation):
        return _invalid_invocation(outcome)
    place = _name_map(getattr(outcome, "place_names", ()))
    act = _name_map(getattr(outcome, "act_names", ()))
    if isinstance(outcome, IRReferenceNormal):
        return {
            "outcome": "Normal",
            "facts": [[place[k], _language_value(value)] for k, value in outcome.facts],
            "products": [[act[p.act], _language_value(p.value)] for p in outcome.products],
        }
    if isinstance(outcome, IRReferenceErrorOutcome):
        return {
            "outcome": "Error",
            "facts": [[place[k], _language_value(value)] for k, value in outcome.facts],
            "error": {"code": outcome.error.code, "phase": outcome.error.phase, "detail": outcome.error.detail},
            "products": [[act[p.act], _language_value(p.value)] for p in outcome.products],
        }
    if isinstance(outcome, IRReferenceDivergence):
        return {
            "outcome": "Divergence",
            "products": [[act[p.act], _language_value(p.value)] for p in outcome.products],
            "harness_reason": outcome.harness_reason,
        }
    if type(outcome).__name__ == "IRReferenceResourceExhaustion":
        return {"tooling_status": "ResourceExhausted", "category": getattr(outcome, "category", "IMPLEMENTATION_RESOURCE_EXHAUSTION")}
    raise TypeError(f"unsupported IR reference outcome: {type(outcome).__name__}")


# White-box/debug projections.  These expose implementation serials explicitly
# and must never be described as B12 language-observable state.
def reference_debug_internal_state(outcome: object) -> dict[str, Any]:
    if isinstance(outcome, (NormalOutcome, ErrorOutcome)):
        return {
            "facts": [[p.serial, v] for p, v in outcome.state.facts],
            "products": [[x.occurrence.serial, x.act.serial, x.value] for x in outcome.products],
        }
    if isinstance(outcome, DivergenceOutcome):
        return {"products": [[x.occurrence.serial, x.act.serial, x.value] for x in outcome.products]}
    return {"kind": type(outcome).__name__}


def ir_reference_debug_internal_state(outcome: object) -> dict[str, Any]:
    d={"products": [[x.occurrence, x.act, x.value] for x in getattr(outcome, "products", ())]}
    if hasattr(outcome, "facts"): d["facts"]=[list(x) for x in outcome.facts]
    return d


def backend_debug_internal_state(outcome: object) -> dict[str, Any]:
    d={"products": [[x.occurrence, x.act, x.value] for x in getattr(outcome, "products", ())]}
    if hasattr(outcome, "facts"): d["facts"]=[list(x) for x in outcome.facts]
    return d


__all__ = [
    "reference_observable", "ir_reference_observable", "backend_observable",
    "reference_debug_internal_state", "ir_reference_debug_internal_state", "backend_debug_internal_state",
]
