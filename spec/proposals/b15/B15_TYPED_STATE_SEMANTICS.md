# B15 Typed State Semantics

## Contract establishment

A non-Natural place declaration contains a complete typed initializer expression E.
Resolution derives `domain(E)=D` without executing E and records `PlaceDomain(p)=D`.

The place identity `p` remains distinct from its current value. `המקום אשר שמו PLACE` never
implicitly dereferences.

For Collection places, `Collection<D>` is recovered by resolving the PlaceId and reading its static
place contract. The consumer does not infer D.

## Initial execution

If E normal-completes with a value in D, Preparation establishes `S[p -> v]`.
If E errors, no fact for p is established by that unit and B12 error propagation applies.
If E diverges, Preparation diverges; no completed partially initialized place exists.

## Lifetime

`PlaceDomain(p)=D` is fixed for the entire invocation. State replacement changes only the current
Value, never D.

## Replacement

For `Replace(p,RHS)`:
1. validation requires `domain(RHS)=PlaceDomain(p)`;
2. execution evaluates RHS;
3. only normal exact-domain completion commits `S[p -> v]`;
4. error/divergence commits no replacement;
5. earlier completed effects remain and later explicit continuation does not begin after fatal error or divergence.

Structurally known wrong-domain replacement is InvalidProgram. No conversion exists between Natural
and Index, between Symbol domains, or between distinct Collection domains.

## Collection immutability

`append(C,x)=C'` leaves C unchanged. A Collection-bearing place changes only by explicit replacement.
Backing representation, sharing and object identity are not observable.
