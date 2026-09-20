from __future__ import annotations

from dataclasses import dataclass

from compiler.models.domains import ProgramInputId
from compiler.models.ir import IRProgram
from compiler.models.values import SemanticValue, value_domain

MISSING_INPUT_BINDING = "MISSING_INPUT_BINDING"
EXTRA_INPUT_BINDING = "EXTRA_INPUT_BINDING"
DUPLICATE_INPUT_BINDING = "DUPLICATE_INPUT_BINDING"
INPUT_DOMAIN_MISMATCH = "INPUT_DOMAIN_MISMATCH"


@dataclass(frozen=True, slots=True)
class InputBinding:
    input_id: ProgramInputId
    value: SemanticValue


@dataclass(frozen=True, slots=True)
class InvocationIssue:
    code: str
    input_id: ProgramInputId
    detail: str


@dataclass(frozen=True, slots=True)
class ValidatedInvocation:
    bindings: tuple[InputBinding, ...]


def validate_invocation(program: IRProgram, bindings: tuple[InputBinding, ...]) -> ValidatedInvocation | tuple[InvocationIssue, ...]:
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
            issues.append(InvocationIssue(EXTRA_INPUT_BINDING, binding.input_id, "Program Input is not declared by this program"))
            continue
        if value_domain(binding.value) != expected:
            issues.append(InvocationIssue(INPUT_DOMAIN_MISMATCH, binding.input_id, "Program Input Value domain does not equal its declared domain"))

    for input_id in contracts:
        if input_id not in seen:
            issues.append(InvocationIssue(MISSING_INPUT_BINDING, input_id, "Required Program Input is missing"))

    if issues:
        return tuple(issues)
    return ValidatedInvocation(tuple(sorted(bindings, key=lambda x: x.input_id.serial)))


__all__ = [
    "MISSING_INPUT_BINDING", "EXTRA_INPUT_BINDING", "DUPLICATE_INPUT_BINDING",
    "INPUT_DOMAIN_MISMATCH", "InputBinding", "InvocationIssue", "ValidatedInvocation",
    "validate_invocation",
]
