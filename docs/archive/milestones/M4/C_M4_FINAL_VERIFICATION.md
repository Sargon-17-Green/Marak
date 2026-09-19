# C M4 Final Verification — A13/B12 Core Compiler Integration

Status: **C M4 COMPLETE — ready for Master review**.

This does **not** declare M2.

## Version dimensions

- compiler: `0.4.0-alpha.2`
- language edition: `core-0.1-integration-candidate-a13-b12`
- construction registry: `a13-b12.1`
- HAST: `core-hast-0.1-candidate-1`
- IR: `core-ir-0.1-candidate-1`
- IR reference evaluator: `core-ir-reference-0.1-candidate-1`
- artifact: `core-artifact-0.1-candidate-1`
- portable backend: `portable-ir-vm-0.1-candidate-1`

## Final test evidence

- C full suite: **230 passed + 126 subtests**.
- Legacy C M3 test-method baseline retained: **157 test methods**.
- New M4 test methods: **73**.
- A13 upstream selftest: **289/289 PASS**.
- A12 regression represented by A13: **517/517 PASS** when the upstream runner is staged with its fixture at the path its own script expects; the unmodified A13 package contains a runner-relative fixture-layout defect, recorded separately.
- B12 `run_all.py`: **PASS**.
  - B11 original: **14/14 PASS**.
  - B11 RM grid: **324 PASS**.
  - B11 intent under B12: **14/14 PASS**.
  - B12 semantics: **33/33 PASS**.
  - RM countdown: **128 PASS**.
  - RM underflow guard: **65 PASS**.
- Relocated repository with the original source path absent: **230 passed + 126 subtests**.
- Relocated source CLI and installed CLI: `version`, `check`, `compile`, `run`, `explain` all PASS on the A13 tiny RM.

## Tiny Register-Machine gate

`A13_TINY_MACHINE.he.txt`:

- normalize: PASS
- whole-program parse: PASS
- resolve: PASS
- validate: PASS
- canonical HAST: PASS
- canonical validated IR: PASS
- artifact serialization: PASS
- artifact verification: PASS
- HAST reference execution: PASS
- independent IR reference execution: PASS
- portable backend execution: PASS
- installed-wheel `check`: PASS
- installed-wheel `compile`: PASS
- installed-wheel `run`: PASS
- installed-wheel `explain`: PASS

Parser evidence: 238 tokens, 823 state keys, 823 derivations, 69 completed nodes, one unique full-program alternative. Execution completes `Normal`; both places in the witness end at Natural zero and no language HALT node exists.

## Reproducibility and packaging

Two independent fixed-epoch wheel builds are byte-identical.

Final wheel SHA-256:

`266189bb6e478baec313c320b3fefd32e98c78b3f686556effe89905833dd320`

The same wheel hash was reproduced from the relocated tree. Clean virtual-environment installation and installed CLI verification pass.

## Artifact/runtime guarantees verified

The canonical artifact is explicit tagged JSON, deterministic, versioned and integrity-checked. No `pickle`, `eval`, arbitrary Python-object deserialization, timestamps or random IDs are used in canonical content.

The verifier rejects incompatible versions/edition, unknown or malformed semantic nodes, duplicate or unresolved identities, invalid role references, negative Naturals, malformed checked subtraction/control/result operations and malformed program structure.

Runtime outcomes are `Normal`, `Error`, or `Divergence`. Dynamic Natural-underflow maps to `ARITHMETIC_DOMAIN_ERROR`; no negative Core Natural is produced. A failing replacement evaluates its RHS before commit; earlier completed effects remain and later sequence work does not execute.

## Differential execution

The compiler has three separately implemented execution layers:

1. HAST reference semantics;
2. independent canonical-IR reference evaluator;
3. portable IR backend.

They agree on the observable result for the A13 tiny RM and the M4 general-purpose examples, including state updates, checked arithmetic, recurrence, named-role association, recursion, product production and immediate product consumption. Fuel is test-harness machinery only and fuel exhaustion is never a language Error.

## Anti-imitation verification

Canonical compiler models do not introduce `Function`, `Parameter`, `Return`, `Frame`, `While`, `BooleanValue`, `Statement`, magic `main`, positional-call semantics or a language HALT primitive. Historical candidate calculi remain isolated under `compiler.reference_models` and are not imported into canonical compiler paths.

Conventional backend implementation machinery is classified as implementation-only and does not define language ontology.

## Blockers and divergences

No known A13/B12 surface or semantic blocker remains for the implemented Core v0.1 path.

Strings, comments/headings semantics, signed integers, catchable exceptions, modules/imports, collections, records/maps, floating point, concurrency/async, FFI and reflection remain intentionally outside Core and are not M4 blockers.

No semantic divergence from A13/B12 is known. One upstream A13-package regression-runner layout defect is documented as a packaging issue only; C did not modify the authoritative A13 artifact to hide it.
