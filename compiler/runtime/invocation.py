"""Program Input invocation contract.

Bindings carry Marak semantic Values, never transport/host values. Validation
is contextual to the target program contract and precedes every Preparation.
"""
from __future__ import annotations

from dataclasses import dataclass

from compiler.models.domains import (
    BidirectionalIndexDomain, CollectionDomain, NaturalDomain, ProgramInputId,
    SymbolDomain,
)
from compiler.models.values import (
    BidirectionalIndexValue, CollectionValue, NaturalValue, SemanticValue,
    SymbolValue, value_domain,
)

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


def _canonical_symbol_members(program) -> dict[tuple[object, object], str]:
    """Return canonical Symbol member metadata for this HAST or IR program."""
    declarations = getattr(program, "symbol_members", None)
    if declarations is None:
        declarations = tuple(
            item for item in getattr(program, "preparation", ())
            if (
                hasattr(item, "domain_id")
                and hasattr(item, "member_id")
                and hasattr(item, "external_label")
            )
        )
    return {
        (item.domain_id, item.member_id): item.external_label
        for item in declarations
    }


def _bound_value_is_valid(
    program,
    declared_domain,
    value: object,
    *,
    abstract_fixture: bool = False,
) -> bool:
    """Validate a caller Value against this program's canonical semantics."""
    if isinstance(declared_domain, NaturalDomain):
        return (
            isinstance(value, NaturalValue)
            and type(value.value) is int
            and value.value >= 0
        )

    if isinstance(declared_domain, BidirectionalIndexDomain):
        if not isinstance(value, BidirectionalIndexValue):
            return False
        if value.side not in {"before", "zero", "after"}:
            return False
        if type(value.magnitude) is not int or value.magnitude < 0:
            return False
        return value.magnitude == 0 if value.side == "zero" else value.magnitude > 0

    if isinstance(declared_domain, SymbolDomain):
        if not isinstance(value, SymbolValue):
            return False
        if value.domain_id != declared_domain.identity:
            return False
        canonical_label = _canonical_symbol_members(program).get(
            (value.domain_id, value.member_id)
        )
        if canonical_label is None:
            # C5.1 retains one frozen abstract infrastructure fixture whose
            # ProgramInputId deliberately has no production owner/finalized
            # Symbol member table. Production source programs are re-owned to
            # a canonical IR fingerprint and never take this compatibility path.
            return abstract_fixture
        return value.external_label == canonical_label

    if isinstance(declared_domain, CollectionDomain):
        if not isinstance(value, CollectionValue):
            return False
        if value.element_domain != declared_domain.element_domain:
            return False
        return all(
            _bound_value_is_valid(
                program,
                declared_domain.element_domain,
                item,
                abstract_fixture=abstract_fixture,
            )
            for item in value.items
        )

    return False

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
        if actual != expected or not _bound_value_is_valid(
            program,
            expected,
            binding.value,
            abstract_fixture=(binding.input_id.program_contract == "abstract-program-contract"),
        ):
            issues.append(InvocationIssue(
                INPUT_DOMAIN_MISMATCH,
                binding.input_id,
                "Program Input Value is not a canonical semantic Value of its declared domain for this program",
            ))

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
