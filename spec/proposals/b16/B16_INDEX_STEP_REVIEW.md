# B16 Index Step Review

A17 generic:
- `המעלה אשר אחר I` → B13 `succ(I)`;
- `המעלה אשר לפני I` → B13 `pred(I)`.

Both are accepted.

This is a faithful general-profile exposure of a capability already accepted in B13 and in the
A16/B15 year profile. It does not widen semantics.

Required laws:
- pred(AfterZero(1)) = ZeroIndex;
- pred(ZeroIndex) = BeforeZero(1);
- succ(BeforeZero(1)) = ZeroIndex;
- succ(ZeroIndex) = AfterZero(1);
- farther magnitudes move exactly one step;
- pred(succ(i)) = i and succ(pred(i)) = i.

One-step traversal is the minimum mechanics needed to let source itself perform exact counting.
It does not collapse that counting into a compiler primitive and exposes no host encoding.

No implication follows to:
- `++`/`--`;
- unary minus;
- generic signed addition/subtraction;
- Natural underflow promotion;
- implicit Natural conversion.
