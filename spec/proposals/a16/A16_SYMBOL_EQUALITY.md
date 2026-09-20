# A16 — Symbol Equality Proposition
Status: proposal delta for B15 review.

## Exact surface
`SYMBOL_VALUE_A הוא SYMBOL_VALUE_B` is admitted as a distinct typed Symbol-equality production.
It reuses the already frozen copular equality family but does not generalize A13 numeric equality to arbitrary Values.

## Semantic target
Both operands must be Symbols from the same declared Symbol domain D.
The proposition holds iff B13 DomainId and MemberId are both equal; within one D this is exact member identity.
Same visible label with different MemberId is therefore not equal.
Visible-label words, source spelling, declaration order, and implementation identity are never compared.

Cross-domain Symbol equality is intentionally source-invalid in A16. B13 can mathematically return false across domains, but the Megillah only requires comparison inside one name family/book domain; admitting unrelated-domain comparison has no independent source need.

## Proposition boundary
The construction is a proposition usable by admitted condition/recurrence semantics. It creates no Boolean Value.
Source member identifiers are not operands unless used through an admitted Symbol Value reference.

## Evidence
The Megillah says `אם שם אחד יהיה בראש שני הספרים` and continues until `השמות ... לא יהיו אחד` in both cutlet-name and month-name ordering.
The capability is therefore required; the exact copular form inherits A13's audited Biblical identity-clause family rather than importing string equality.
