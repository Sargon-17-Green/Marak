# B-Core v0.1 Runtime / Static Failure Model — A13

## InvalidProgram
Static semantic invalidity.

Includes:
- reference before introduction;
- duplicate same-kind identity;
- duplicate role within owner;
- duplicate body;
- role/body ordering violations;
- statically proved Natural subtraction underflow;
- other frozen A13 validity failures.

## RuntimeError(E)
Defined fatal execution failure.

Core stable category added in B12:
- `ARITHMETIC_DOMAIN_ERROR`.

Other existing semantic categories may remain where relevant, but backend exception names are not
language semantics.

Runtime error:
- is not a value;
- is not output;
- is not catchable in Core;
- prevents continuation;
- carries state after all earlier completed effects, before the failing uncommitted transition.

## Resource exhaustion
Separate implementation-resource outcome/classification.

## Divergence
Legal nontermination, not error.

## No UB
No admitted Core execution may fall into undefined behavior.
