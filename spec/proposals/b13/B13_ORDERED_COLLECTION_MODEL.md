# B13 Ordered Finite Collection Model

## B-COLL-001 — immutable finite ordered collection (PROPOSED)
A collection is a finite ordered mathematical series from one declared element domain:

`Collection<D> = ⟨v1,...,vn⟩`, `n∈ℕ`.

It is an immutable value. Memory layout, capacity, allocation identity, and sharing are unobservable. Collections may contain collections with a declared compatible nested domain; B13 does not propose unrestricted heterogeneous containers.

## Minimal operations and evidence
- empty construction / constructive append — build books/candidates incrementally;
- count — source counts and traversal bounds;
- membership/equality search — uniqueness constraints;
- position selection — first/next/nth chosen entries;
- traversal in stored order — source explicitly visits head then successors;
- deterministic ordering by an admitted strict total relation — `ערוך את כל הספרים`.

No deletion, random mutation, slicing, hash map, iterator object, or object identity is added.

## B-COLL-002 — positions (PROPOSED)
Semantic positions are positive Naturals `1..count(C)`, matching source first/second/.../last semantics rather than a host-language zero-based convention.

`select(C,k)` outside that interval yields `COLLECTION_POSITION_ERROR`.

## Equality
Collections support structural equality when their element domain supports equality: same length and pairwise equal elements. Equal contents are equal values regardless of construction history.

`append(⟨v1,...,vn⟩,x)=⟨v1,...,vn,x⟩`; the original value is unchanged.

## B-COLL-003 — ordering (PROPOSED)
`order(C,R)` requires an admitted strict total order `R` on the element domain and yields a permutation in nondecreasing order.

For collections of ordered elements, `Lex(R)` compares the first unequal position; if one is a strict prefix, the shorter is smaller. Identical collection values are ties, so stable tie order has no observable consequence.

Arbitrary executable comparator acts are not part of B13. If a purported relation is not an admitted strict total order, validation should reject it; a surviving dynamic violation is `ORDER_RELATION_ERROR`.

## Effects
Collection construction/order are pure. Failure during a collection-valued RHS follows B12: no replacement commits; earlier completed actions stay committed.
