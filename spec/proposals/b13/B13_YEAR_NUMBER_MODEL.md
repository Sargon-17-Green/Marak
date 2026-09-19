# B13 Year / Bidirectional Index Model

## B-IDX-001 — BidirectionalIndex (PROPOSED)
Do not widen B12 Natural into a generic signed arithmetic domain. Admit a separate general-purpose domain for positions in a count extending on both sides of zero:
- `ZeroIndex`;
- `AfterZero(n)` for positive Natural n;
- `BeforeZero(n)` for positive Natural n.

It is isomorphic to ℤ for proofs, but does not inherit generic signed multiplication/division/underflow semantics.

## Successor/predecessor
`succ(Zero)=AfterZero(1)`; `pred(Zero)=BeforeZero(1)`; `pred(AfterZero(1))=Zero`; `succ(BeforeZero(1))=Zero`; farther values adjust magnitude by one. Both operations are total.

## Ordering/distance
All BeforeZero values precede Zero; Zero precedes every AfterZero. Among AfterZero, smaller magnitude is smaller. Among BeforeZero, larger magnitude is smaller. This is a strict total order.

`distance(i,j)` is the Natural number of successor/predecessor steps between i and j.

## B-IDX-002 — explicit Natural relation (PROPOSED)
Natural→Index is explicit: 0→Zero, positive n→AfterZero(n). Index→Natural succeeds only for Zero/AfterZero; BeforeZero yields `INDEX_TO_NATURAL_DOMAIN_ERROR`.

`Natural(5)` and `AfterZero(5)` are distinct-domain values. B12 Natural subtraction underflow remains `ARITHMETIC_DOMAIN_ERROR`; it never auto-promotes to BidirectionalIndex.

## Rejected models
A generic Integer type overgeneralizes D2 evidence. A built-in Year type would promote Megillah domain logic into the language. An exposed sign/magnitude pair would make an encoding observable and force source-level representation mechanics.
