# D4-T21-RUNTIME-001 — Name-only constructive intrinsic dispatch

Status: **REMEDIATION CANDIDATE / MASTER REVIEW REQUIRED**

## Finding

Before this remediation, each opt-in runtime accelerated a user Act based on
its spelling, compatible role names, and the existence of scratch places/Acts.
No verification of the Act body or its helpers was performed.

Concrete counterexample is retained in
`tests/test_d4_t21_intrinsic_dispatch_safety.py`:

- A user-defined Act named `נותר` accepts Natural roles `מספר` and
  `מחלק`, has the expected scratch places, but deliberately returns 7.
- Calling it with 9 and 4 executes the user body and produces **7** normally.
- Reproducing the old unguarded dispatch by bypassing only the newly added
  certificate check produces **1**, the unrelated canonical modulo result.
- The test checks this distinction in HAST, IR reference and portable backends.

## Narrow implementation correction

`compiler/runtime/constructive_fingerprint_guard.py` implements a
fail-closed **full compiled program structural SHA-256 allowlist**, not an
Act-name allowlist. The hash streams every dataclass node's fully-qualified
type, field names and values, ordered containers, symbols, roles, bodies,
source spans, initial values, helper acts and principal.

Only exact T21 `after` / `before` production programs from the immutable
candidate SHA `6fda03c4ca953898b471da666c048d81020f9bea4fcd240b94aab7bb3f091881`
are authorized. Each has its own HAST and IR fingerprint.

Fingerprints (Evidence #15, job 119020287720):
- after / HAST: `56bbf6c05e6fa7682b9677294904222f65042fbea9bc39a975e57fdbc8f02f17`
- before / HAST: `42c40d1432d731e3cc8db1169d7c39f3fb29e3beb17e0d975cbd5d0da3287e89`
- after / IR: `690f24c5ae8f9fc69ff95f5106ed54af9498c4b56ade7bb0737dd75e46601a3e`
- before / IR: `92592062530a6aac7b64a141f6cfdfed76258bf6bc6fa91b0f71326bda3abd49`

On any missing/unrecognized/unsupported/mismatched program fingerprint,
the evaluator takes the normal source execution path even if
`constructive_intrinsics=True`. Fuel-driven execution remains on the
unaccelerated path as before.

The full-program restriction intentionally refuses optimizations for every
other Marak program, even structurally similar ones. This is a conservative,
auditable implementation policy, not a change to Marak language semantics.

The production E2E test now positively asserts both trusted program
fingerprints and that altered act tables are rejected *before* execution.
It still runs the real T21 gate pipeline in HAST / IR / portable, for both
directions, and compares retained exact observables.

## Scope and acceptance

- candidate bytes: unchanged
- candidate SHA: `6fda03c4ca953898b471da666c048d81020f9bea4fcd240b94aab7bb3f091881`
- frontier: `71,871`, original line `1251`
- T22: **NOT STARTED**
- PR #20: **Draft / open / unmerged**
- Exact-head CI and E2E results: **PENDING at documentation creation**

Only Master may close the finding or accept T21.
