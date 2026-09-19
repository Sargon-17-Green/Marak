# C M4.2 — Implementation Status

Target baseline: unchanged A13 surface + B12 semantics.

## Implemented and retained

- exact normative whitespace and 27-letter normalization;
- whole-program Preparation/Principal grammar with exactly one `ועתה`;
- explicit sequencing only;
- introduced-before-use, typed IDs, duplicate/self/hoisting rules;
- canonical HAST and validated IR for frozen Core;
- exact Natural arithmetic, checked subtraction and non-Boolean proposition judgment;
- occurrence-specific named roles, recursion, outputs and immediate provenance;
- Normal/Error/Divergence execution contract;
- deterministic artifact format and semantic verifier;
- HAST reference evaluator, independent IR reference evaluator and portable backend;
- public semantic observation quotient independent of implementation serial allocation;
- iterative/trampolined act execution with no Python-stack dependence;
- **no fixed default active-performance/depth ceiling**;
- optional explicit caller performance budget as tooling/harness control only;
- CLI `marak` check/compile/run/explain/version;
- relocation and reproducible wheel verification.

## M4.2 remediation

E-FIND-023 is addressed by removing the former default `10_000` active-performance quota from all three execution layers. Finite recursion beyond that old boundary is tested directly; no-fuel self recursion remains running until an external harness terminates it. E-FIND-027 is addressed by cleaning stale generated handoff metadata from the canonical source root and using coherent Marak/MIT/package metadata.

## Deliberately outside Core v0.1

Strings, comments, heading semantics, signed integers, exceptions/catch, modules/imports, collections, records/maps, floating point, concurrency/async, FFI and reflection. These are deferred scope, not M4.2 blockers.
