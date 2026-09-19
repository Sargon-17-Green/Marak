# A15 — Productive Direct Naturals

Status: **INTEGRATED_SURFACE_READY** for D-LANGUAGE-REQUEST-005.

## 1. Semantic rule

Every admitted direct phrase denotes exactly one B13/B12 Natural magnitude. Naturals have no semantic maximum.

A15 preserves the A13 canonical 1..9999 family byte-for-word at the normalized word level and extends it with the A14 descending `אלף` / `אלף אלפים` magnitude family.

## 2. Edition family

This A15 proposal edition directly admits the productive family 1..99,999,999. Examples include:

    עשרת אלפים
    ארבעה עשר אלף
    שבע מאות אלף ושבעים אלף ושבעת אלפים
    אלף אלפים
    ארבעה עשר אלף אלפים

The Megillah constant 14,777,149 is:

    ארבעה עשר אלף אלפים
    ושבע מאות אלף
    ושבעים אלף
    ושבעת אלפים
    ומאה וארבעים ותשעה

Line breaks carry no meaning.

## 3. Frontier audit

`99,999,999` is **not** a semantic ceiling and is **not** asserted to be a permanent limit of Biblical numeral grammar.

It is the structural frontier of the present admitted magnitude family: the highest admitted million coefficient in this edition is 99, followed by the complete sub-million family through 999,999. Once those edition choices are fixed, 99,999,999 follows mechanically.

The choice to stop the million coefficient family at 99 is an edition boundary, not evidence that higher magnitudes are impossible or invalid forever. A future surface edition may add a higher magnitude family without changing the Natural domain.

## 4. Canonicalization

Magnitude components descend. A magnitude slot occurs at most once. Later nonzero components receive the prefixed waw. A15 does not add `רבבה` as a second alias and does not accept Arabic digits as source numerals.

Zero remains without a direct cardinal literal. Computed zero remains available through frozen Core semantics.

## 5. Evidence

A14 documented Biblical large-number composition including Numbers 17:14, Numbers 1:46, Numbers 31:32, 2 Chronicles 17:15, and 1 Chronicles 21:5 (`אלף אלפים`). A15 retains the controlled descending subset rather than claiming that every Biblical variant is an alias.

## 6. Verification

The A15 reference suite checks all 9,999 A13 direct forms for uniqueness, the Megillah constant, magnitude boundaries, a collision-free generated prefix through 250,000, and 75,000 deterministic large random samples. The exact test record is in `A15_TEST_RESULTS.json`.
