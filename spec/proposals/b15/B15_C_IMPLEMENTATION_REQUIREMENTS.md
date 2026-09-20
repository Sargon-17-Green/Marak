# B15 C Implementation Requirements — Conceptual Only

This file is produced because all B15 semantic gates are green. It is not an implementation plan and
does not prescribe compiler architecture.

A future compiler implementation must preserve conceptually:

## Semantic contracts
- exact static domain for every resolved executable value expression;
- `PlaceId -> Domain`;
- `(ActId,RoleId) -> Domain`;
- `ActId -> None | OutputDomain`;
- `ProgramInputId -> Domain`.

## Validation
Reject source-resolved mismatches before execution:
- place initializer/replacement;
- role association;
- mixed output domains;
- wrong immediate-result head/staleness;
- Index step wrong operand;
- cross-domain Symbol equality;
- any expected-type rescue of unresolved source.

## Runtime operations
- immutable exact B13 Values;
- explicit state replacement only after successful RHS;
- occurrence-local role associations;
- nonterminal zero/one output;
- B12 immediate provenance;
- total Index succ/pred;
- same-domain Symbol identity proposition;
- pure immutable Collection operations.

## Runtime semantic errors
Preserve B12/B13 categories, especially `RESULT_PROVENANCE_ERROR`,
output cardinality, arithmetic/collection/index errors, and `RESOURCE_EXHAUSTION`.

## Observability
Do not expose addresses, object identity, host type tags, intern IDs, backing collection layout,
stack frames, result registers, or serialization details.

This document deliberately does not prescribe AST classes, IR layout, dispatch representation,
memory management strategy, ABI, code generation, parser implementation, or optimization design.
