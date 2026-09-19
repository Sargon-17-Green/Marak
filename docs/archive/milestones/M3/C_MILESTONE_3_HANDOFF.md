# C-MILESTONE-03 Handoff — A12 frozen surface candidate / B11 semantic Core closure

Status: **COMPLETE AT THE CURRENT IMPLEMENTABLE SPEC FRONTIER, WITH TWO A12 SURFACE-FREEZE BLOCKERS RECORDED.**

This does **not** declare C-Core v0.1 complete or A-Core v0.1 FINAL. M3 closes because C implements the A12 frozen constructions available to the compiler, integrates the post-anti-imitation B7–B11 semantic Core distinctions, and refuses to invent the two missing surface rules needed to parse A12's whole tiny Register-Machine witness.

## Current registry

The current registry is `a12.2-c-b11-mapped`, language edition `core-0.1-frozen-candidate-a12-b11-review`.

Implemented surface includes exact direct numerals 1..9999, `מקום` state-bearing referents, exact arithmetic/propositions, explicit sequence, finite counted repetition, paired conditional shell, post-action recurrence, named `מעשה` identity/performance, singular A12 body delimiters, named non-positional roles, current-performance deictic, zero-or-one output and immediate single-result reference.

A11 plural body syntax, ordinal/multiple-result access and performance-owned mutable local places are deliberately absent from the current grammar. Historical A11 remains immutable evidence.

## B11 semantic readiness

B11 maps every frozen A12 semantic family exactly, subject only to its explicit subtraction-domain clarification. C therefore marks the reusable-act gates `READY` for:

- named act performance;
- named input roles and explicit role association;
- `המעשה הזה` current performance occurrence;
- A12 body execution/completion at exhaustion;
- zero-or-one numeric output that does not terminate;
- immediate result tied to the explicitly resolved just-completed performance.

This does **not** introduce canonical `Function`, `Parameter`, `Return`, `Frame`, Boolean Value, or positional call semantics. `compiler.semantic_core.performance` uses semantic occurrence/provenance objects; historical B1–B5 machinery remains isolated under `compiler.reference_models`.

## Anti-imitation boundary

Canonical compiler layers cannot import the historical reference calculus. The post-audit semantic substrate represents state referents, proposition satisfaction, recurrence checkpoints, described-act occurrences and named role relations directly. Backend implementations may later use conventional machinery internally only if they preserve these distinctions.

## A12 corrections enforced

- body: singular `זה דבר... / עד הנה דבר...` only;
- output: zero or one numeric output only;
- result reference: immediate single result only; no ordinal access;
- performance-local mutable state: not in frozen Core.

Two result-production actions parse but fail semantic validation with `SEM0012`. Body-name mismatch fails explicit co-reference with `REF0021`; there is no nearest-open-body repair.

## Numeral implementation

The A12 direct-literal frontier is loaded from the re-frozen canonical fixture:

- 9,999 distinct values;
- source fixture SHA-256 `aafcbb51affc3facb1ed001809d09f82b8bd76929098eac54b790052c36a04d8`;
- maximum canonical numeral length: six words.

`NumeralTerminal` emits every licensed boundary, not a longest-match guess.

## Verification

- C suite: **157 PASS + 20 subtests**.
- A12 upstream adversarial runner: **517 checks PASS**.
- E-Core v0.6 against current C after B11 readiness update: **141/141 PASS, no skips**.
- Historical reference-model import firewall remains active.

## Remaining A12 surface blockers

A12 asks C to prove that `examples/a12_tiny_machine.he.txt` parses, but the same frozen package does not normatively specify two surface relations used by that source:

1. `חדל מעשות את המעשה אשר שמו NAME` is used by the witness but absent from `A12_FROZEN_CONSTRUCTIONS.json`;
2. multiple top-level introductions, definitions and the entry performance are juxtaposed, while A12 explicitly denies bare-source-order execution semantics and does not freeze a whole-program discourse aggregation grammar.

C records these as specification blockers rather than adding witness-specific productions.

## Next C frontier

Once A/Master resolves those surface blockers and source visibility/lifetime relations, C can complete whole-source A12 resolution and freeze canonical validated IR, reference execution, backend and artifact versions. B11 semantics no longer blocks reusable-act lowering in principle. Until the IR contract is frozen, `IR_VERSION` and `ARTIFACT_FORMAT_VERSION` remain `unassigned`.
