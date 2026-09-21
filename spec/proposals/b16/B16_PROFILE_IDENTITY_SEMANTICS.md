# B16 Profile Identity Semantics

## One semantic domain

The only semantic domain involved is B13 `BidirectionalIndex`:

- `ZeroIndex`;
- `BeforeZero(n)`;
- `AfterZero(n)`.

No `YearIndex`, `GenericIndex`, profile-tagged Index, unit-tagged Index, Integer, or SignedNatural
is introduced.

## Source profiles

A resolved source construction may carry a non-semantic profile marker for source tooling:

`SourceProfile ∈ {YEAR, GENERAL}`.

Lowering erases that marker:

`lower(profile, index) = index : BidirectionalIndex`.

Therefore:
- `שנת אין` and `מעלת היתד` lower to the same `ZeroIndex`;
- corresponding ±N year/general literals lower to the same B13 Value;
- order, succ, pred, state, roles, outputs and inputs observe only the lowered Value.

## Tooling preservation

A source-preserving formatter may retain the resolved construction/profile in HAST or source-map
metadata so it can reproduce the user's linguistic family. That metadata is not semantic.

A value-only source generator cannot infer a profile from a bare Index Value. It must receive an
explicit target profile. Failure to provide such a tooling choice is a source-generation API issue,
not a language runtime ambiguity.

Semantic artifact validation does not require a profile tag. If artifacts carry optional source maps,
profile information may appear there only as non-semantic provenance.
