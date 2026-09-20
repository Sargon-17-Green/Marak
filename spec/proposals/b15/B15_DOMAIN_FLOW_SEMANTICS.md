# B15 Domain Flow Semantics

## Validated semantic contracts

After resolution/validation, the semantic source model conceptually carries:

- `ExprDomain(ExpressionId) -> D`;
- `PlaceDomain(PlaceId) -> D`;
- `RoleDomain(ActId, RoleId) -> D`;
- `ActOutputDomain(ActId) -> None | D`;
- `ProgramInputDomain(ProgramInputId) -> D`.

These contracts are conceptual language metadata. A canonical HAST/validated IR must preserve their
meaning, but B15 defines no serialization layout, runtime tag representation, or compiler architecture.

## Static-first rule

No consumer may supply a missing domain. A source expression must independently resolve to one exact
domain before its use in:
- initialization;
- replacement;
- role association;
- output;
- immediate result;
- equality;
- Index step;
- collection construction.

Expected type never rescues ambiguous or untyped source.

## End-to-end flow

For Symbol, BidirectionalIndex and Collection, A15+A16 now support:
value construction -> place establishment -> current-content reference -> replacement -> named act role
association -> current-role read -> output -> immediate provenance -> later retention.

Program Input Roles from A15 can feed the same typed state path because their declared domain is already
part of the validated invocation contract.

Therefore **DOMAIN_FLOW_COMPLETE**.
