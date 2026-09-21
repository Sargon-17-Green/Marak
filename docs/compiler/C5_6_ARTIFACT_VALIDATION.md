# C5.6 — Artifact and Canonical IR Validation

## Version transition

C5.6 adds a new semantic proposition node to HAST/IR/artifact vocabulary and therefore advances the serialized identities coherently:

- package: `0.5.6a1`
- compiler: `0.5.6-alpha.1`
- registry: `c5.6-a17-b16.1`
- HAST: `core-hast-0.7-candidate-1`
- IR: `core-ir-0.7-candidate-1`
- artifact: `core-artifact-0.7-candidate-1`
- portable backend: `portable-ir-vm-0.7-candidate-1`
- IR reference: `core-ir-reference-0.7-candidate-1`
- language edition: unchanged, `core-0.1-integration-candidate-a13-b12`

No 0.6→0.7 migration reader is added.

## New artifact node

`IRIndexLTProposition` is included in the explicit artifact type vocabulary.

Its serialized fields are exactly the dataclass fields:

- source_span;
- left;
- right.

No profile field exists.

## Structural verification

Artifact verification requires both operands to deserialize as IR Values. Unknown tags, missing fields, extra fields, malformed spans, and semantic-node substitution are rejected.

The exact artifact tag whitelist is not weakened.

## Semantic verification

After decoding, `validate_canonical_ir()` independently proves that both strict-order operands have domain `BIDIRECTIONAL_INDEX`.

Forged Natural/other-domain operands are rejected with `IR_INDEX_LT_DOMAIN`.

This remains true even if an attacker recomputes a valid artifact payload digest.

## Stale contracts

The current verifier rejects:

- artifact `core-artifact-0.6-candidate-1`;
- IR `core-ir-0.6-candidate-1`;
- any unknown future/stale tag or field shape.

0.6 and 0.7 are not silently treated as identical.

## Canonical fixtures

The nine committed canonical artifacts are regenerated at the 0.7 envelope/IR contract.

Before deterministic conversion, each existing 0.6 artifact's stored payload digest was checked against canonical JSON bytes. The C5.6 CI job reruns the canonical compiler regeneration and requires:

`git diff --exit-code -- spec/CURRENT_CONSTRUCTION_REGISTRY.json artifacts`.

The same job publishes generated hashes on Ubuntu and Windows for cross-platform comparison.

## C5.5 invocation protection

C5.6 does not change Program Input artifact/invocation semantics.

The full C5.5 adversarial suite remains in full pytest, including owner validation, Symbol canonicality, recursive Collection validation, invocation revalidation, and the pre-Preparation invalid-invocation boundary.
