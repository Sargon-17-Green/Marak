# C5.1 Artifact Compatibility

C5.1 changes the serialized validated-IR schema by adding explicit domain/value tags and domain-contract tables. Therefore schema versions are bumped rather than silently reinterpreted.

- HAST: `core-hast-0.2-candidate-1`
- IR: `core-ir-0.2-candidate-1`
- Artifact: `core-artifact-0.2-candidate-1`
- Portable backend: `portable-ir-vm-0.2-candidate-1`
- IR reference evaluator: `core-ir-reference-0.2-candidate-1`

The language edition string remains `core-0.1-integration-candidate-a13-b12`; C does not invent a new language edition.

The artifact serializer explicitly tags Domain IDs, Domain descriptors, Program Input identities, and typed IR Values. The verifier rejects unknown tags, incomplete or duplicate contracts, cross-domain flows, and old `core-artifact-0.1-candidate-1` payloads. Existing committed M4 example artifacts were regenerated under 0.2 and remain byte-deterministic for a fixed source/IR.

Old/new artifacts are never silently cross-read. Version rejection precedes execution.
