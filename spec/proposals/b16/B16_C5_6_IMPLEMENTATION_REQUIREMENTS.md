# B16 C5.6 Implementation Requirements — Conceptual Only

This document exists because all B16 semantic gates are green. It is not implementation code and does
not prescribe parser/IR architecture beyond observable semantic requirements.

C5.6 may add **only** the A17 constructions accepted by B16:

## Generic BidirectionalIndex literals
- `מעלת היתד` -> ZeroIndex;
- one/two/productive-count `מעלות לפני מעלת היתד` -> BeforeZero(N);
- corresponding `אחרי` forms -> AfterZero(N).

## Generic BidirectionalIndex carrier forms
- Program Input declaration/reference with `מעלה/המעלה` and A17 feminine agreement;
- current place head and replacement displaced-value head;
- named-act role declaration/current-role head;
- immediate result head;
- existing output production accepting a resolved generic Index expression.

All map to the existing static semantic domain `BidirectionalIndex`.

## Operations
- strict order `INDEX_A לפני INDEX_B` -> existing B13 Index strict-order proposition;
- `המעלה אשר אחר INDEX` -> existing B13 succ;
- `המעלה אשר לפני INDEX` -> existing B13 pred.

## Required profile behavior
- year/general source families are independently parsed and internally coherent;
- after independent resolution to BidirectionalIndex, cross-profile flow is permitted;
- no profile/unit field is added to semantic Value/domain contracts;
- source/HAST tooling may preserve profile as non-semantic construction provenance;
- semantic artifact identity and invocation validation remain profile-neutral;
- value-only source generation must receive an explicit target profile rather than infer one.

## Explicitly forbidden C5.6 additions
- Index equality surface;
- direct Index distance surface;
- Natural→Index or Index→Natural source conversion;
- generic signed arithmetic;
- unary minus/++/--;
- generic Index Collection kind;
- arbitrary user-defined unit/profile noun;
- Day/Date/Time/Timestamp domains;
- runtime profile tag or profile mismatch error.

All B12/B13/B15 errors, effects, observables and resource-exhaustion rules remain unchanged.
