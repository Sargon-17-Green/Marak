# B13 Numeric Ordering Propositions

## B-ORD-001 (PROPOSED)
For Naturals a,b admit semantic propositions:
- `LT(a,b)` iff a<b;
- `GT(a,b)` iff a>b.

They are satisfaction judgments used by control, not Boolean values.

The Megillah also repeatedly states non-strict relations such as "not greater" and "not fewer". B13 therefore defines derived propositions without adding first-class logical operators:
- `LE(a,b)` iff LT(a,b) or numeric equality;
- `GE(a,b)` iff GT(a,b) or numeric equality.

A may give these direct linguistic forms; the program need not possess a general `or` or proposition-negation value.

## Laws
For all Naturals a,b exactly one of LT(a,b), a=b, GT(a,b) holds. LT/GT are irreflexive and transitive; `GT(a,b) ⇔ LT(b,a)`. LE/GE are reflexive and transitive. Magnitude is unbounded and exact.

## Conditional integration
A B12 conditional consumes the proposition through satisfaction `S ⊨ P`. No `true` or `false` value is produced.

Natural ordering on a non-Natural operand is `VALUE_DOMAIN_MISMATCH` if it survives static validation. BidirectionalIndex has its own ordering and is not implicitly comparable with Natural.
