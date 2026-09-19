# C M4 — Decision Log Delta

| ID | Class | Status | Decision |
|---|---|---|---|
| C-M4-NORM-001 | SPEC-DERIVED | ACCEPTED | A13 exact 25-code-point whitespace set is normative; host Unicode whitespace predicates are not authoritative. |
| C-M4-PROG-001 | SPEC-DERIVED | ACCEPTED | canonical program separates Preparation from Principal selected by one top-level `ועתה`. |
| C-M4-RESOLVE-001 | SPEC-DERIVED / IMPLEMENTATION | ACCEPTED | source visibility is introduced-before-use; resolved references become typed stable IDs; no hoisting/runtime name lookup. |
| C-M4-HAST-001 | SEMANTICS-DERIVED | ACCEPTED | expand canonical HAST only for A13/B12 distinctions; retain anti-imitation naming firewall. |
| C-M4-IR-001 | IMPLEMENTATION | ACCEPTED | assign `core-ir-0.1-candidate-1`; structured deterministic IR preserves B12 observable distinctions. |
| C-M4-ARITH-001 | SEMANTICS-DERIVED | ACCEPTED | Natural subtraction is checked; provable underflow is static `SEM0201`, dynamic underflow is `ARITHMETIC_DOMAIN_ERROR`. |
| C-M4-RUNTIME-001 | SEMANTICS-DERIVED | ACCEPTED | outcomes are Normal/Error/Divergence; no language exit value and no catchable Core exception. |
| C-M4-REF-001 | IMPLEMENTATION | ACCEPTED | add an independent canonical-IR reference evaluator rather than using the backend as its own oracle. |
| C-M4-ART-001 | IMPLEMENTATION | ACCEPTED | assign explicit tagged canonical JSON artifact `core-artifact-0.1-candidate-1` with verifier and payload digest. |
| C-M4-BACKEND-001 | IMPLEMENTATION | ACCEPTED | portable VM may use conventional host control machinery internally but consumes IR only and does not define language ontology. |
| C-M4-OPT-001 | IMPLEMENTATION | ACCEPTED | M4 optimizer remains identity-preserving to avoid changing errors/effects/divergence timing. |
| C-M4-PKG-001 | TOOLING | ACCEPTED | all fixtures are repository-relative; relocation and byte-identical wheel builds are release gates. |
