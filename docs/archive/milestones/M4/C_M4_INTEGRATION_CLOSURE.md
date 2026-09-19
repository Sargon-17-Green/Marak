# C M4 — A13/B12 Integration Closure

Status: **C M4 COMPLETE — ready for Master review**.

C M4 continues directly from C M3 and integrates the Master-reviewed A13 surface and B12 semantic baselines into one executable Core v0.1 compiler path:

`source → normalize → parse → resolve → validate → canonical HAST → canonical validated IR → artifact → verify → reference/backend execution`.

## Closed M3 blockers

M4 closes the prior Core blockers for normative whitespace, whole-program root, `ועתה`, introduced-before-use, visibility/lifetime, ordinary completion instead of cessation/HALT, and Natural subtraction failure. These are no longer `BLOCKED_ON_SPEC` for Core v0.1.

## Implemented versions

- compiler: `0.4.0-alpha.2`
- language edition: `core-0.1-integration-candidate-a13-b12`
- registry: `a13-b12.1`
- HAST: `core-hast-0.1-candidate-1`
- IR: `core-ir-0.1-candidate-1`
- IR reference evaluator: `core-ir-reference-0.1-candidate-1`
- artifact: `core-artifact-0.1-candidate-1`
- portable backend: `portable-ir-vm-0.1-candidate-1`

## Central result

The A13 tiny Register-Machine witness now passes the complete compiler path and executes normally without a language HALT node. Reference HAST execution, independent IR-reference execution, and the portable IR VM agree on the B12-observable result.

This milestone does **not** declare M2 and does not extend Core with strings, comments, signed integers, modules, collections, exceptions, FFI, concurrency or other out-of-Core features.
