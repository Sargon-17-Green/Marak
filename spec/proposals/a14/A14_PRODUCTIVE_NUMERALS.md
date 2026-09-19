# A14 — Productive Biblical Numerals

Status: **SURFACE_READY proposal**

## Goal

Extend the controlled direct numeral language beyond A13's 1..9999 table without:
- Arabic digits;
- decimal-place notation in source;
- a lookup table ending at the Megillah maximum;
- accepting every Biblical variant.

The proposal is deliberately canonical: one spelling per admitted value.

## Domain

A14 direct numeral phrases cover:

    1 .. 99,999,999

Zero still has no direct cardinal numeral literal in this proposal.

The limit is a proposal-edition admission frontier, not a semantic bound on Naturals. It covers every
fixed large numeral required by the current Megillah, including 14,777,149.

## Base grammar

For 1..9999, the A13/A1 canonical spelling is unchanged.

## Thousand composition

A14 adds a controlled descending-scale grammar.

Examples:

    10,000  עשרת אלפים
    14,000  ארבעה עשר אלף
    70,000  שבעים אלף
    100,000 מאה אלף
    300,000 שלש מאות אלף
    307,000 שלש מאות אלף ושבעת אלפים
    777,149 שבע מאות אלף ושבעים אלף ושבעת אלפים ומאה וארבעים ותשעה

The grammar decomposes the thousand coefficient into at most:
- a hundred-thousands component;
- a ten-thousands component;
- a unit-thousands component;
then a sub-thousand remainder.

This distributed form follows attested Biblical large-number composition rather than disguising modern place-value notation.

## Million composition

Biblical Hebrew attests:

    אלף אלפים

for one million.

A14 uses that as the million scale.

Canonical examples:

    1,000,000  אלף אלפים
    2,000,000  שני אלפי אלפים
    3,000,000  שלשת אלפי אלפים
    10,000,000 עשרת אלפי אלפים
    14,000,000 ארבעה עשר אלף אלפים

For coefficients 2..10, the controlled construct form precedes `אלפי אלפים`.
For 11..99, the existing canonical cardinal phrase precedes `אלף אלפים`.

The 14-million form is directly present in the Megillah.

## Joining components

Nonzero magnitude components appear from greatest to least.

Every later component is joined by prefixed waw to its first word.

No omitted internal component implies a zero word.

## Megillah canonicalization

Historical source line 41 contains components whose intended sum is:

    14,000,000 + 777,000 + 149 = 14,777,149

A14 canonical direct form:

    ארבעה עשר אלף אלפים
    ושבע מאות אלף
    ושבעים אלף
    ושבעת אלפים
    ומאה וארבעים ותשעה

Historical line 43 expresses the same number using `רבבה` decompositions. A14 does not admit `רבבה` as
a second canonical scale alias; D may rewrite it to the one canonical form.

## Exactness

The grammar is structurally descending. A magnitude slot can occur at most once:
million, hundred-thousand, ten-thousand, unit-thousand, sub-thousand.

Therefore an accepted canonical phrase has one numeric decomposition.

The accompanying reference formatter and tests check:
- all A13 values 1..9999;
- every value 1..250,000 for collision-free generation;
- boundary/magnitude examples through 99,999,999;
- randomized larger values;
- Megillah target 14,777,149.

## Linguistic evidence

A14 is based on attested patterns including:
- `ארבעה עשר אלף ושבע מאות` (14,700);
- `אלף אלפים ומאה אלף` (1,100,000).

It is a controlled extension, not a claim that every generated phrase is independently attested as a verse.
