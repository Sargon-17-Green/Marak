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

## Next source span

Original line 39:
`יום הינתן הלוחות אחרי יום היסוד.`

This occurrence is being audited separately from the following 14,777,149 arithmetic proof. No built-in Tablets primitive will be introduced.

## D4-CONF-001

The C5.6 negative-scope suite contains a frozen receipt asserting the pre-repair D4 candidate SHA/frontier. That receipt becomes false by design when this authorized D4 continuation changes the candidate. D4 does not edit C5.6 tests; the issue is routed as conformance maintenance and does not alter C5.6 semantic validity.
