# B16 Strict Index Order Semantics

A17 `A לפני B` is accepted as the source exposure of B13 strict Index order.

## Why this is language-level rather than a Megillah shortcut

The relation is part of the accepted semantic structure of `BidirectionalIndex`, not a procedure
defined by the Megillah. The Megillah's D4 evidence requires distinguishing whether one day is before
or after another and explicitly says that this relation is known from the days rather than from their
day numbers.

The order relation:
- is pure;
- is strict and total;
- is useful for any two-sided ordered coordinate, not only calendar years/days;
- does not compute distance;
- does not expose sign/magnitude encoding;
- yields proposition satisfaction only, not a Boolean Value.

A second `A אחרי B` primitive is unnecessary because `A after B` is exactly `B לפני A`.

## Total-order laws relied upon

For all Index a,b exactly one semantic case holds:
- `a < b`;
- `b < a`;
- a and b are the same Index Value.

That third case is a theorem of strict total order and is sufficient for same-day discrimination
without an equality surface.
