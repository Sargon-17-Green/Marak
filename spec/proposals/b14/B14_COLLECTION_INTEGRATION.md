# B14 Collection Integration

Every admitted A15 book kind maps to immutable homogeneous B13 `Collection<D>`. The explicit book-kind
head fixes D; no contextual guessing or heterogeneous append is allowed. Append returns a new value.

Exact operations: empty, append, count, membership, first, last, positive ordinal select, Natural order,
Symbol-domain order, and Lex(R) nested order.

Positions are Naturals 1..count. Zero or above-count yields `COLLECTION_POSITION_ERROR`. A position is
not an occurrence object. Duplicate equal values are legal; ordinal position disambiguates occurrences
without object identity. Stable implementation order among equal values is unobservable.

A realistic accumulation fails compositionally:
1. create empty book — supported;
2. retain it — no Collection state carrier;
3. compute append — supported;
4. replace retained book — no typed replacement;
5. read later — no typed place content reference;
6. pass to act — no Collection act role;
7. output — no Collection output.

Therefore D-LANGUAGE-REQUEST-003 remains blocked even though the pure collection operations themselves
are semantically exact.
