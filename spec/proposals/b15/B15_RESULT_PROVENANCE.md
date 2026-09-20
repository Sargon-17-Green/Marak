# B15 Result Provenance

B15 preserves B12 provenance exactly while widening the payload domain.

A direct successfully completed performance establishes ephemeral:
`Recent(o, a, product)`,
where product is `None` or `Some(v:D)` and D is the act's static output domain.

## Immediate typed reference

Validation requires:
1. the referenced act has `ActOutputDomain(a)=D`;
2. the typed immediate-result head denotes the same exact D;
3. source structure places the reference in the inherited immediately following executable position.

A wrong typed head is InvalidProgram. A structurally intervening caller action makes a later reference
stale/invalid; validation should reject it rather than model a historical result register.

## Runtime zero-output path

An act may have static output domain D while a reached runtime path produces no value.
The direct performance still completes, but reading its immediate result encounters empty product and
raises the existing B12 `RESULT_PROVENANCE_ERROR`.

No null, optional, default, stale prior result, or implicit dereference is created.

If an invalid/stale artifact reaches the runtime evaluator despite validation, B12's
`RESULT_PROVENANCE_ERROR` remains the fallback category.
