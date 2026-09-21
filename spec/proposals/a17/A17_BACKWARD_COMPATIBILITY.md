# A17 — Backward Compatibility

Baseline: `e8f766889676b219f0abf5c9e4f08fad3034fa5b`.

## Frozen forms

A17 does not alter any A13/A15/A16 surface or B12/B13/B14/B15 semantic rule.

The A15/A16 year profile remains exactly:

- `שנת אין`
- `שנה אחת לפני שנת אין`
- `שתי שנים לפני שנת אין`
- `COUNT שנים לפני שנת אין`
- corresponding `אחרי` forms
- typed head `מספר שנה` / reference `מספר השנה`
- `מספר השנה אשר אחר I`
- `מספר השנה אשר לפני I`

Natural constructions remain unchanged, including `המספר אשר הוא ...`, Natural subtraction domain behavior, and Natural strict `רב מן`.

## No global reservation

The current grammar explicitly lacks reserved-word filtering for `NameTerminal`. A17 preserves that model. Existing programs may continue to use words such as `מעלה` or `היתד` as names in explicit name slots.

## Parse-collision design

New generic literals begin with one of `מעלת`, `מעלה`, or a feminine count followed by `מעלות`; current year literals use `שנת`, `שנה`, `שתי שנים`, or a feminine count followed by `שנים`.

For N>=3, the potentially shared numeral prefix is resolved by the immediately following distinct noun:
- generic: `COUNT מעלות ...`
- year: `COUNT שנים ...`

Natural literals retain the head `המספר אשר הוא`.

Carrier references distinguish:
- generic: `המעלה ...`
- year: `מספר השנה ...`
- Natural: `המספר ...`

No selected normalized canonical form is equal to an existing canonical year/Natural form.

## Canonical source policy

A semantic Index Value can have more than one surface representation because year and general profiles are distinct linguistic families. This does not change semantic identity. It is analogous to different well-typed source expressions denoting the same value, not to hidden runtime variants.

A source-preserving formatter keeps the parsed profile. A value-only formatter must be told which profile to emit.

## Scope guard

A17 must change only `spec/proposals/a17/`. In particular it does not touch:
- `spec/CURRENT_CONSTRUCTION_REGISTRY.json`;
- compiler/parser/resolver/runtime;
- HAST/IR/artifact schemas;
- compiler version;
- Megillah original/candidate/analysis.
