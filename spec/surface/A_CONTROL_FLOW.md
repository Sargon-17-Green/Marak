# A_CONTROL_FLOW.md

Status: A12 FROZEN CORE

## 1. Sequence

    A ואחרי כן B

means A completes before B begins.

No source-order-only execution rule.

## 2. Binary alternative

    אם P A ואם לא B

P is one complete admitted proposition.
A and B are one complete atomic action each in Core v0.1.

No dangling-else convention.

## 3. Exact zero predicate

A numeric zero test is equality with the canonical derived zero Value.

## 4. Finite counted recurrence

Only individually audited exact `N פעמים` constructions are admitted.

## 5. Post-action unbounded recurrence

    A וכן תעשה עד אשר P

Frozen meaning:
- A once;
- observe P after A;
- if false, repeat the same A;
- observe P after each completed repetition.

The initial A is never skipped.

The antecedent of `כן` is exactly one atomic action.

For a multi-action recurring procedure, make that procedure one named `מעשה` and repeat the one act
performance action.

## 6. Bare `עד אשר`

Bare:

    A עד אשר P

does not receive Core recurrence semantics.

## 7. Named recursive acts

Recursion remains expressible by an act performing an already introduced named act, including itself.

This is an additional unbounded-computation route, not a surface `while` substitute and not a required
normal program style.

# A13 whole-program execution and completion

Only the unique top-level `ועתה` begins principal execution. Preparatory units do not execute merely
because they appear earlier in the source.

After `ועתה`, more than one action executes in order only when the language explicitly says so with
`ואחרי כן`. Newline, punctuation and adjacency never substitute for that relation.

A performed act completes normally at body exhaustion. The program completes normally when the final
principal executable unit and all acts it performs have completed and no explicit continuation
remains. No HALT/exit primitive is part of Core v0.1.

A proposition observed by `אם` or `עד אשר` is not thereby a Boolean Value and cannot be stored/passed
as one by any frozen Core rule.
