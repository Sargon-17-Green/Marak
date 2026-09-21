# A17 — Mapping to Existing B13 Semantics

A17 introduces no semantic object. All accepted forms map to B13 `BidirectionalIndex`.

| A17 surface | B13 target |
|---|---|
| `מעלת היתד` | `ZeroIndex` |
| `N מעלות לפני מעלת היתד` | `BeforeZero(N)` |
| `N מעלות אחרי מעלת היתד` | `AfterZero(N)` |
| `A לפני B` | strict Index order `A < B` |
| `המעלה אשר אחר I` | `succ(I)` |
| `המעלה אשר לפני I` | `pred(I)` |
| generic place/input/role/result head | same `BidirectionalIndex` domain contract already used by A16/B15/C5.5 |

One/two morphology is merely source spelling for N=1/2.

## Carrier semantics

A17 reuses B15's static-first domain rule:
- each Index expression independently resolves to `BidirectionalIndex`;
- a place/role/output/program-input domain contract is established statically;
- expected type never rescues an incomplete or ambiguous source phrase.

The generic head changes only how source truthfully describes the existing domain outside years.

## Profile identity

`שנת אין` and `מעלת היתד` both denote B13 `ZeroIndex`; corresponding before/after magnitudes likewise denote the same semantic values. No `YearIndex`, `DayIndex`, or `GenericIndex` semantic subtype exists.

Surface profile provenance is not runtime-observable. B16 must verify that this profile coexistence is an acceptable surface distinction and not an unintended semantic unit system.

## Operations surfaced

A17 proposes surface only for:
- general literal construction;
- typed carriers needed for actual value flow;
- strict Index order;
- total predecessor/successor.

## Operations left semantic-only

A17 deliberately does not expose:
- B13 exact `distance(i,j)` as a primitive;
- Index equality;
- Natural↔Index conversion.

The distance algorithm is source work: determine direction, step toward the anchor/target, and update a Natural count. This avoids turning a Megillah algorithm into a language keyword.

No generic arithmetic closure follows from the fact that BidirectionalIndex is mathematically isomorphic to the integers.
