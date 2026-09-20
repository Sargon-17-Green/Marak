# B13 Symbolic Value Model

## B-SYM-001 — finite declared Symbols (PROPOSED)
A runtime symbol is an atomic value `Symbol(DomainId,MemberId)`. A resolved program declares a finite member set for each symbol domain. Execution cannot dynamically mint new member identities.

This is the preferred answer to D-LANGUAGE-REQUEST-001: the 17 cutlet labels and 47 month labels are closed named sets, while D2 provides no need for concatenation, arbitrary text input, substring operations, or text editing.

## Equality and identity
Two Symbols are equal iff both DomainId and MemberId are equal. Canonical visible spelling is member metadata, not the equality key. Thus separately declared same-spelling members are distinct unless A makes them one declaration/reference.

Compile-time Marak entity names are not runtime Symbols. No implicit source-name→Symbol conversion exists.

## Observation/artifacts
An observable Symbol exposes the declared member identity through its canonical external label. Memory address, intern-table index, and compiler SymbolId are not observable. A canonical artifact must preserve domain/member identity and label metadata conceptually; binary layout is C's concern.

## Ordering
Symbols have no intrinsic order from spelling or declaration order. If an algorithm needs order, the source must establish an explicit strict total order/rank for that symbol domain. The Megillah's explicit listed/ranked calendar names can supply such a relation.

## Integration
State-bearing referents, act roles, collections, and zero/one act outputs may declare a Symbol domain. No implicit Natural↔Symbol conversion exists.

General Text remains **OPEN_AFTER_M2** and is not secretly the representation of Symbol.
