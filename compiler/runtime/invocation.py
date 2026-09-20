"""Program Input invocation contract.

Bindings carry Marak semantic Values, never transport/host values. Validation
is contextual to the target program contract and precedes every Preparation.
"""
from __future__ import annotations

from dataclasses import dataclass

from compiler.models.domains import ProgramInputId
from compiler.models.values import NaturalValue, SemanticValue, value_domain

MISSING_INPUT_BINDING = "MISSING_INPUT_BINDING"
EXTRA_INPUT_BINDING = "EXTRA_INPUT_BINDING"
DUPLICATE_INPUT_BINDING = "DUPLICATE_INPUT_BINDING"
INPUT_DOMAIN_MISMATCH = "INPUT_DOMAIN_MISMATCH"


@dataclass(frozen=True, slots=True)
class InputBinding:
    input_id: ProgramInputId
    value: SemanticValue

    def __post_init__(self) -> None:
        if not isinstance(self.input_id, ProgramInputId):
            raise TypeError("InputBinding requires a resolved ProgramInputId; raw source spelling is not a binding identity")


@dataclass(frozen=True, slots=True)
class InvocationIssue:
    code: str
    input_id: ProgramInputId
    detail: str


@dataclass(frozen=True, slots=True)
class ValidatedInvocation:
    bindings: tuple[InputBinding, ...]
    program_contract: str | None = None


@dataclass(frozen=True, slots=True)
class InvalidInvocation:
    issues: tuple[InvocationIssue, ...]


def _contract_owner(program) -> str | None:
    owners = {x.input_id.program_contract for x in program.program_input_domains}
    return next(iter(owners), None) if len(owners) <= 1 else None


def validate_invocation(program, bindings: tuple[InputBinding, ...]) -> ValidatedInvocation | tuple[InvocationIssue, ...]:
    contracts = {x.input_id: x.domain for x in program.program_input_domains}
    seen: dict[ProgramInputId, SemanticValue] = {}
    issues: list[InvocationIssue] = []

    for binding in bindings:
        if binding.input_id in seen:
            issues.append(InvocationIssue(DUPLICATE_INPUT_BINDING, binding.input_id, "Program Input is bound more than once"))
            continue
        seen[binding.input_id] = binding.value
        expected = contracts.get(binding.input_id)
        if expected is None:
            issues.append(InvocationIssue(EXTRA_INPUT_BINDING, binding.input_id, "Program Input is not declared by this program contract"))
            continue
        try:
            actual = value_domain(binding.value)
        except TypeError:
            issues.append(InvocationIssue(INPUT_DOMAIN_MISMATCH, binding.input_id, "Program Input binding is not a Marak semantic Value"))
            continue
        if actual != expected:
            issues.append(InvocationIssue(INPUT_DOMAIN_MISMATCH, binding.input_id, "Program Input Value domain does not equal its declared domain"))

    for input_id in contracts:
        if input_id not in seen:
            issues.append(InvocationIssue(MISSING_INPUT_BINDING, input_id, "Required Program Input is missing"))

    if issues:
        return tuple(issues)
    return ValidatedInvocation(
        tuple(sorted(bindings, key=lambda x: (x.input_id.serial, x.input_id.spelling, x.input_id.program_contract))),
        _contract_owner(program),
    )


def prepare_invocation(program, supplied: tuple[InputBinding, ...] | ValidatedInvocation = ()) -> ValidatedInvocation | InvalidInvocation:
    # ValidatedInvocation is not a context-free bearer token. Revalidate its
    # immutable semantic bindings against the target program every time.
    raw = supplied.bindings if isinstance(supplied, ValidatedInvocation) else supplied
    result = validate_invocation(program, tuple(raw))
    return result if isinstance(result, ValidatedInvocation) else InvalidInvocation(result)


def runtime_input_values(validated: ValidatedInvocation) -> dict[ProgramInputId, object]:
    return {
        b.input_id: (b.value.value if isinstance(b.value, NaturalValue) else b.value)
        for b in validated.bindings
    }


__all__ = [
    "MISSING_INPUT_BINDING", "EXTRA_INPUT_BINDING", "DUPLICATE_INPUT_BINDING",
    "INPUT_DOMAIN_MISMATCH", "InputBinding", "InvocationIssue", "ValidatedInvocation",
    "InvalidInvocation", "validate_invocation", "prepare_invocation", "runtime_input_values",
]
