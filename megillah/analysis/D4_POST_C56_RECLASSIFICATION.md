# D4 — Post-C5.6 Reclassification

This document succeeds the historical `D4_POST_C55_RECLASSIFICATION.md` without deleting it.

## Baseline

- main: `5a5f8dae0dd8c3526de5f21f84a3a7b2aba984e3`
- compiler: `0.5.6-alpha.1`
- registry: `c5.6-a17-b16.1`
- C5.6: A17/B16 general/non-year BidirectionalIndex production integration.

## D4-LANG-001

Status: **CLOSED_BY_A17_B16_C56**.

The semantic domain remains exactly `BidirectionalIndex`. No Day/Date/profile subtype was added. D4 may now represent the Foundation coordinate and later day Program Inputs with the general `מעלה` source profile.

## Foundation/day-coordinate tranche

Historical original lines 35–37 are split by role:

- computational identity/origin requirement -> repaired to a named Index referent:
  `יהי מקום ושמו יסוד ובמקום אשר שמו יסוד יהי מעלת היתד לבדו`;
- explanatory denial that Foundation begins all days or Natural numbering -> documentary externalization with provenance.

Classification: `STRUCTURAL_EXPLICITNESS` + `DOCUMENTARY_EXTERNALIZATION`.

Preservation: semantic equivalent; no algorithm change.

Measured frontier:
- before: token 105 / candidate line 11 / original line 35;
- after: token 117 / candidate line 15 / original line 39;
- diagnostic remains `PARSE0002`.

## D4-SRC-001 — Luach Three fast path

Status: **CLOSED_BY_D4_PATCH_011**.

At the Luach Seven frontier, downstream values proved that the earlier linear `RepeatExactly` realization of Luach Three was not executable for the Megillah's own inputs. Production `RepeatExactly` executes one occurrence per count, while the original source explicitly supplies powers-of-two doubling/decomposition for large counts.

D4-PATCH-011 restores that source algorithm inside `לקחתפעמים`; it does not modify Marak, C5.4, the compiler, or runtime semantics. GitHub Actions run `35612611456` passed the dedicated D4 jobs on Ubuntu and Windows with 60 targeted tests, including a finite-fuel multiplication whose count is `2^127-1`.

Accordingly, historical `D4-DOC-012` is superseded as an externalization: the doubling/decomposition material is again executable production source.

## Luach Seven lifecycle note

Original lines 317–319 state that the five-stone table may be computed once and does not vary by day. D4-PATCH-012 retains this as a deterministic nested Natural table with one explicit builder; no day-dependent input participates in its construction.

## D4-CONF-001

The C5.6 negative-scope suite contains a frozen receipt asserting the pre-repair D4 candidate SHA/frontier. That receipt becomes false by design when this authorized D4 continuation changes the candidate. D4 does not edit C5.6 tests; the issue is routed as conformance maintenance and does not alter C5.6 semantic validity.
