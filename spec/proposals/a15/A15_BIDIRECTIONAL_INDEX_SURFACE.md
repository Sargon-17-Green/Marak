# A15 — BidirectionalIndex Surface

Status: **INTEGRATED_SURFACE_READY** for D-LANGUAGE-REQUEST-002.

## 1. Chosen scope

B13 deliberately chose the general semantic domain `BidirectionalIndex`, not a built-in `Year` and not a generic signed Integer. The present source evidence, however, is specifically year numbering. A15 therefore exposes a **year-typed surface family** and maps it to the general B13 domain. A generic source noun for arbitrary BidirectionalIndex values is deferred because no independent source need justifies one.

This is a surface restriction, not a semantic claim that B13 indices can only represent years.

## 2. Exact value family

Origin:

    שנת אין

One before / one after:

    שנה אחת לפני שנת אין
    שנה אחת אחרי שנת אין

Two before / two after:

    שתי שנים לפני שנת אין
    שתי שנים אחרי שנת אין

Productive distance, for positive distance `N >= 3`:

    YEAR_COUNT שנים לפני שנת אין
    YEAR_COUNT שנים אחרי שנת אין

`YEAR_COUNT` uses the same controlled feminine-count morphology used before the feminine nouns `פעמים`/`שנים`, without the following noun. It denotes an exact positive Natural distance.

Mapping:

- `שנת אין` -> `ZeroIndex`;
- `N שנים לפני שנת אין` -> `BeforeZero(N)`;
- `N שנים אחרי שנת אין` -> `AfterZero(N)`.

The special one/two forms map to the same definitions with N=1/2.

## 3. Typed references

Where the value is obtained through another referent, A15 uses the typed head `מספר השנה`, for example a Program Input Role reference:

    מספר השנה אשר עומד תחת הדבר אשר למלאכה הזאת שמו ROLE

`מספר השנה` is a surface category for the year-number relation. It is not a `NumberValue` and does not enter A13 Natural arithmetic implicitly.

## 4. `אין` is not zero, null, or absence

`אין` is admitted only inside the exact typed phrase `שנת אין`, including the larger before/after constructions that contain that phrase. A15 does not admit:

    אין
    אפס
    מינוס N

as BidirectionalIndex literals.

No rule converts `שנת אין` to Natural zero merely because B13's mathematical model calls the origin `ZeroIndex`. No null/absence Value is introduced.

## 5. Positive historical year notation

The historical Megillah uses phrases such as `שנת חמשת אלפים`. A15 does not make that phrase a second constructor alias for `AfterZero(5000)`, because doing so would create two canonical surfaces for the same new domain before a separate linguistic audit. D may locally rewrite such runtime year designations to the relative A15 family when it adopts this surface.

The B13 explicit Natural-to-Index conversion remains a semantic operation available for later surface work; A15 does not smuggle it in through same-looking numerals.

## 6. Ordering and arithmetic

B13 defines successor, predecessor, distance, and strict order for BidirectionalIndex. A15 does not add new source spellings for those operations in this request because the Megillah's immediate blocker is representation across the origin. In particular, the Natural comparison surface `A רב מן B` is not implicitly extended to mixed Natural/Index operands.

B12 Natural subtraction remains unchanged and never produces a before-origin index.

## 7. Evidence and controlled deviation

Megillah evidence is explicit: `שנת אין`, `אחת לפני אין`, `שתים לפני אין`, and continuing year after year. A15 adds the repeated typed head `שנת אין` to the before/after forms so that `אין` cannot escape into a general literal category. The symmetric `אחרי` family is a controlled generalization required to expose both halves of B13's accepted index domain.

## 8. Rejection

Reject:

- standalone `אין` as a Value;
- direct `אפס` origin spelling;
- `מינוס N`;
- Natural arithmetic applied to an index without an explicit admitted conversion;
- mixed Natural/BidirectionalIndex ordering by expected type;
- an untyped `N לפני אין` / `N אחרי אין` shortcut.
