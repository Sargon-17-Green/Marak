# C5.6 — D4 Historical Conformance Receipt Maintenance

Finding: `D4-CONF-001 — CONFORMANCE_RECEIPT_STALE_AFTER_AUTHORIZED_D4_SOURCE_REPAIR`

Canonical maintenance baseline:
`800a75914c2e3510fb51dacf2d193a283c11d467`

Branch:
`workstream-c/c5-6-conformance-receipt-maintenance`

## Reconstructed historical intent

C5.6's accepted evidence asserted that C5.6 itself made no changes under:

- `megillah/original/**`
- `megillah/candidates/**`
- `megillah/analysis/**`

At the C5.6 snapshot, the then-current D4 candidate had SHA-256
`afc6eda11a8d7f4b6499cf643d2ef5b36581bcad61b5fce761a7709274d2d643`
and C5.6 parsing reached `PARSE0002` at normalized token 105 / candidate line 11.

Those facts are valid historical C5.6 evidence. They are not a normative statement
that future authorized Workstream D candidates must retain those bytes or that frontier.

## Previous faulty invariant

`tests/test_c5_6_negative_scope.py` read the live repository path
`megillah/candidates/Megilat_HaItim_Marak_Candidate.md` and required its bytes
and compiler frontier to remain equal to the C5.6-era snapshot forever.

That made an authorized downstream D source repair look like a C5.6 regression.

## New invariant

The historical evidence is moved to an intentionally frozen test receipt:

- `tests/fixtures/c5_6_conformance/D4_HISTORICAL_RECEIPT.json`
- `tests/fixtures/c5_6_conformance/D4_CANDIDATE_AT_C5_6.md`

The receipt fixes the C5.6 baseline, validated implementation HEAD, accepted merge,
C5.6 registry version, historical candidate SHA/frontier and the historical
no-Megillah-mutation scope claim.

The test hashes the frozen fixture and compiles that fixture explicitly with
`C5_6_REGISTRY`. It therefore remains capable of detecting:

- accidental mutation of the historical candidate snapshot;
- accidental corruption of the receipt;
- parser behavior that stops reproducing the historical C5.6 frontier under the
  frozen C5.6 registry.

The test no longer reads the live `megillah/candidates/**` path and does not assert
any current D SHA or frontier. A dedicated regression uses different simulated
downstream candidate bytes and proves that they are not an input to the historical
receipt proof.

## Why future D advancement is safe

T18/T19/etc. may legitimately replace the live D candidate and advance D's own
frontier ledger. Neither value is referenced by the C5.6 historical receipt test.
D retains ownership of current candidate/frontier truth; C5.6 retains ownership
only of its own frozen integration evidence.

## Scope

This maintenance changes no compiler production file, no C5.6 grammar/registry
semantics, no HAST/IR/artifact contract, and no Megillah file.

Only conformance tests, a frozen test fixture/receipt, and maintenance evidence are
in scope.

## Verification

Maintenance branch on canonical main:
- repaired C5.6 negative-scope suite: **35/35 PASS**;
- complete C5.6 targeted group: **67/67 PASS**;
- D3/D4 frozen regressions: **29/29 PASS**;
- full pytest: **563 passed + 126 subtests passed**.

Downstream-evolution proof:
- temporary read-only audit clone HEAD: `339d0daa62951c3a934f2a21f5046da4d06c04b0`;
- live D candidate SHA there: `4c003673d46f25547465062d1e6c538981a913d28d37f98a27d9cd2f28b80383`;
- live D frontier ledger: **24,481**;
- repaired C5.6 negative-scope suite with the frozen receipt/fixture: **35/35 PASS**;
- no D change was committed or pushed.

This directly proves that the historical C5.6 receipt remains valid in both the
historical/main candidate context and an authorized downstream D context with different
candidate bytes/frontier.

## Finding status

`D4-CONF-001: CLOSED_CANDIDATE`

Final closure remains a Master decision.
