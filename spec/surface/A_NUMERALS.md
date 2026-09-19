# A_NUMERALS.md

Status: A12 FROZEN CORE

## 1. Canonical direct forms

The existing A1 canonical written-number grammar for 1..9999 is frozen as the tested direct-literal
subset of Core v0.1.

Examples:
- 1 `אחד`
- 2 `שנים`
- 10 `עשרה`
- 11 `אחד עשר`
- 20 `עשרים`
- hundreds/thousands as frozen in A1.

The generated A1 table established 9999 unique canonical strings with zero collisions.

## 2. Meaning of the 9999 frontier

9999 is NOT:
- a semantic numeric maximum;
- a claim about the full Biblical numeral language;
- a bound on computed values.

It is merely the direct-literal subset frozen for this Core candidate.

Semantic naturals remain unbounded.

## 3. No cardinal `אפס`

`אפס` is not admitted as a Core cardinal zero.

Derived zero is the exact subtraction of one from one.

## 4. Literal embedding

    המספר אשר הוא NUMERAL

is the frozen numeric-literal noun phrase.

## 5. Future work

A productive direct magnitude grammar beyond 9999 remains a full-language extension and a Megillah
compatibility requirement, not an M1 blocker.

# A13 natural-domain clarification

Frozen Core numeric Values are natural numbers. `גרע A מן B` denotes B−A only when A≤B. If A>B,
Core v0.1 does not obtain a negative Value. The exact defined failure behavior is a B12 dependency.

No negative integer literal spelling is admitted. Negative integer surface syntax remains
OPEN_AFTER_M2.
