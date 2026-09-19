# A15 — Numeric Ordering

Status: **INTEGRATED_SURFACE_READY** for D-LANGUAGE-REQUEST-004.

## Exact strict proposition

    NUMBER_VALUE_A רב מן NUMBER_VALUE_B

This maps exactly to B13 `GT(A,B)` over Naturals. It is a proposition consumed by control; it is not a Boolean Value.

Less-than has no second predicate spelling. Express `A < B` by reversing operands:

    NUMBER_VALUE_B רב מן NUMBER_VALUE_A

Equality remains the frozen A13 `A הוא B` construction.

## No LE / GE surface

B13 defines LE and GE as derived semantic relations. A15 found no independent source need that justifies direct `<=`/`>=` wording in this integration edition. Therefore no source-visible LE/GE construction is added. A source condition requiring a non-strict relation must use already admitted control structure around strict order/equality rather than gaining a new hidden Boolean algebra.

## Evidence

The comparative frame `X רב מן Y` is directly Biblical (`עם רב ממך`, Deuteronomy 20:1; `כי רב ממך הדרך`, 1 Kings 19:7). The Megillah repeatedly requires greater/fewer comparisons. A15 intentionally chooses one strict orientation to avoid rival aliases.

## Rejection

Reject `רב A מן B`, `A רב B`, automatic `מעט`/`ימעט` inverse syntax, symbolic `<`/`>`, a storable truth value, or mixed Natural/BidirectionalIndex comparison.
