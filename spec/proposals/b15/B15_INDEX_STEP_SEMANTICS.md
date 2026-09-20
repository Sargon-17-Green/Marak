# B15 BidirectionalIndex Step Semantics

A16:
- `מספר השנה אשר אחר I` -> B13 `succ(I)`;
- `מספר השנה אשר לפני I` -> B13 `pred(I)`.

The operand must independently resolve to BidirectionalIndex.

Exact crossings:
- pred(AfterZero(1)) = Zero;
- pred(Zero) = BeforeZero(1);
- succ(BeforeZero(1)) = Zero;
- succ(Zero) = AfterZero(1).

Farther magnitudes move exactly one step. Both operations are total over BidirectionalIndex.

The year-oriented source is an **acceptable surface narrowing** of B13's general BidirectionalIndex;
Year does not become a semantic built-in.

No generic Integer, unary minus, signed addition/subtraction, `++`, `--`, Natural underflow
promotion, or implicit Natural->Index conversion follows.

## Megillah adequacy

The year algorithm can begin from the admitted A15 literal `AfterZero(5000)` and walk by pred/succ
through Zero into BeforeZero values. Therefore current repair does not require a Natural->Index surface.
