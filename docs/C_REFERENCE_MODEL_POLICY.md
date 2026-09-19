# C reference-model policy

## Purpose

C needs executable semantic oracles while A/B are still changing. An oracle may embody a model that is useful for differential testing without being the ontology of the language.

## Boundary

`compiler.reference_models` is the only namespace for such executable candidate calculi.

A reference model may contain conventional implementation/metanotation concepts such as:
- frames;
- cells/locations;
- Boolean values;
- Expr/Cmd;
- call-by-value;
- Return/Unit;
- pre-test loops.

Their presence there proves only that the candidate calculus is executable and testable.

It does **not** license corresponding canonical HAST/IR nodes or surface rules.

## Import firewall

The following canonical layers MUST NOT import `compiler.reference_models`:
- `compiler.api`;
- `compiler.models`;
- parse/current registry machinery;
- resolve;
- validate;
- optimize;
- backend;
- artifact;
- runtime.

Tests enforce this by AST-level import inspection.

## Current model

`b4_candidate.py` preserves the historical B4 action calculus after B6 demoted it to reference-only status. It supports recursion, mutual recursion, fresh parameter cells, lexical-not-dynamic lookup, strict argument order, Return/Unit, and non-rollback errors solely as an oracle.

## Promotion rule

No concept moves from a reference model into canonical HAST/IR because its tests are green. Promotion requires a current A+B decision derived independently from computational need, Biblical-Hebrew structure, and observable semantics.
