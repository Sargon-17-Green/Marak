# A14 — Year Number Surface

Status: **PREFERRED_SURFACE_CANDIDATE / AWAITING_B** — B13 BidirectionalIndex semantics reviewed; A/B integration acceptance and final typed wording remain.

## Need

The calendar year sequence contains:
- positive-numbered years;
- a distinguished year described by the source as `שנת אין`;
- years before it, such as `אחת לפני אין` and `שתים לפני אין`.

The need does not itself imply a general Integer type.

## Distinctions

A14 keeps three notions separate:

1. numeric natural zero — already expressible computationally in Core, but not by a direct `אפס`
   literal;
2. the calendar designation `שנת אין`;
3. absence/nothing — not inferred from either of the above.

`אין` is therefore not proposed as a general numeric zero token.

## Alternatives

### Generic signed number syntax
Deferred. It solves more than the Megillah asks for and would reopen the A13 natural-only Value domain.

### Sign+magnitude encoded in naturals
Computationally possible but produces a large, non-local source rewrite and hides the source's explicit
chronological language.

### Year-relative designation
Preferred.

The surface family should state the chronological relation directly:

    שנת אין
    שנה אחת לפני שנת אין
    שתי שנים לפני שנת אין
    ...
    NUMERAL שנים לפני שנת אין

Exact agreement/canonical morphology for the productive plural family remains to be finalized after B
chooses the semantic domain.

## Output notation versus semantic year identity

The Megillah separately says that when year numbers are *written in numeral signs*, years before
`שנת אין` receive `אות החסר`.

A14 treats that as representation/output formatting evidence, not proof that the runtime Value must be
a generic negative integer.

## B dependencies

B must answer:

- Is a calendar year designation a dedicated ordered domain or a signed numeric Value?
- Is distance from `שנת אין` a Natural plus a before/after relation?
- Which operations are required: successor/predecessor only, ordering, arithmetic, conversion to
  written notation?
- Is `שנת אין` semantically equivalent to numeric zero for any operation, or merely the origin of a
  year-numbering relation?

Until those questions close, A does not freeze a generic signed-number grammar.


## B13 reconciliation

B13 selects a separate `BidirectionalIndex` domain: ZeroIndex, AfterZero(n), BeforeZero(n), rather than
widening A13 Naturals to generic Integers. This directly supports A14's year-relative direction.

A14 therefore withdraws any need for generic signed-number syntax in this milestone. The remaining
surface task is to choose a typed year-number/index construction that makes `אין`, `לפני`, and `אחרי`
relations unambiguous without making `אין` a general numeric literal.
