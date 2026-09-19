# C M4 — Implementation Status

Target baseline: A13 surface + B12 semantics.

## Implemented

- exact normative whitespace and 27-letter normalization;
- whole-program Preparation/Principal grammar with exactly one `ועתה`;
- explicit sequencing only;
- introduced-before-use, typed IDs, duplicate/self/hoisting rules;
- canonical HAST covering the frozen Core;
- exact Natural arithmetic, checked subtraction and proposition judgment;
- occurrence-specific named roles, recursion, outputs and immediate provenance;
- Normal/Error/Divergence execution contract;
- versioned canonical IR;
- HAST reference evaluator and independent IR reference evaluator;
- deterministic artifact format and verifier;
- portable executable IR backend;
- working CLI check/compile/run/explain/version;
- differential execution and tiny RM end-to-end;
- relocation and reproducible package verification.

## Deliberately not implemented in Core v0.1

Strings, comments, heading semantics, signed integers, exceptions/catch, modules/imports, collections, records/maps, floating point, concurrency/async, FFI and reflection.

These are deferred language scope, not blockers for C M4.

## Final verification totals

- C full suite: **230 passed + 126 subtests**.
- A13 selftest: **289/289 PASS**.
- B12 run-all: **PASS** (including B12 semantics 33/33, RM countdown 128, RM underflow guard 65).
- Relocated full suite: **230 passed + 126 subtests** with the original source path absent.
- Final wheel reproducibility: byte-identical builds; SHA-256 `266189bb6e478baec313c320b3fefd32e98c78b3f686556effe89905833dd320`.

Status: **C M4 COMPLETE — ready for Master review**. This is not an M2 declaration.
