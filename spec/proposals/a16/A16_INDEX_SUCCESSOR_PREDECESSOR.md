# A16 — BidirectionalIndex Successor / Predecessor
Status: proposal delta for B15 review.

## Exact surface
Successor: `מספר השנה אשר אחר INDEX_VALUE`.
Predecessor: `מספר השנה אשר לפני INDEX_VALUE`.
`INDEX_VALUE` must independently be an admitted year-profile BidirectionalIndex Value.

## Semantic target
`מספר השנה אשר אחר I` maps exactly to B13 `succ(I)`.
`מספר השנה אשר לפני I` maps exactly to B13 `pred(I)`.
The result remains BidirectionalIndex and both operations are total.

Required crossings: pred(AfterZero(1))=Zero; pred(Zero)=BeforeZero(1); succ(BeforeZero(1))=Zero; succ(Zero)=AfterZero(1).
No special crossing syntax exists.

## Evidence and boundary
The Megillah says `לשנה אשר אחר שנה...`, `לשנה אשר לפני שנה...`, `אחר שנה אחת תבוא שנת אין`, and `שנה אחר שנה` in the year-numbering section.
A16 keeps the A15 year-specific narrowing because the source need is years; no generic signed `index` noun is invented.
Natural subtraction is unchanged and cannot cross year zero. No Natural→Index conversion is added.
`++`, `--`, generic signed addition/subtraction, or treating `אין` as standalone zero are rejected.
