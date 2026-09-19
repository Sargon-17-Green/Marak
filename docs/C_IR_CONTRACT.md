# Canonical Validated IR Contract

Version: `core-ir-0.1-candidate-1`.

The IR is Hebrew-independent, deterministic, source-mapped, serializable, backend-independent and accepted only after parse, resolution, ambiguity rejection and static semantic validation.

## State and numbers

- `IRInitialFact` is distinct from `IRReplaceCurrentFact`.
- `IRReadCurrentFact` reads a resolved Place identity.
- Naturals are exact and nonnegative.
- subtraction is `IRCheckedSubtractNatural` with semantic failure code `ARITHMETIC_DOMAIN_ERROR`.

## Control

- `IRThen` records explicit source-defined sequencing;
- `IRConditional` consumes a proposition, not a Boolean Value;
- `IRFixedRecurrence` and `IRPostActionRecurrence` preserve their distinct checkpoint semantics;
- normal completion is structured exhaustion; there is no `IRHalt`/`IRReturn`/`IRWhile`.

## Acts and results

- `IRPerformAct` addresses an `ActId` and carries identity-addressed `IRRoleAssociation` entries;
- role order may be canonicalized by stable identity but correspondence is not positional semantics;
- `IRProduceResult` records an occurrence product and does not terminate the act;
- `IRRecentResult` preserves immediate provenance semantics.

The optimizer in M4 is intentionally an identity-preserving pass. No transformation changes error timing, effects, divergence or source-defined action order.
