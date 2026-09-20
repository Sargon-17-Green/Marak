# D4 Compiler Frontier

## Starting frontier

D3 accepted frontier:
- candidate SHA-256: `afc6eda11a8d7f4b6499cf643d2ef5b36581bcad61b5fce761a7709274d2d643`;
- normalized tokens: 9,039;
- furthest normalized token: **105**;
- candidate line: **11**;
- mapped original line: **35**;
- diagnostic: `PARSE0002`, phase `parse`;
- text begins: `ותבחר מפלצת הספגטי המעופפת יום אחד...`.

## Post-C5.5 measurement

The production 0.5.5 compiler was run against the unchanged candidate in GitHub CI. The measured result is still:
- normalized tokens: **9,039**;
- furthest normalized token: **105**;
- candidate line 11 / original line 35;
- `PARSE0002`;
- `PROG0001` also remains because no unique legal Principal has yet been constructed;
- HAST: not reached;
- IR: not reached;
- artifact: not reached.

This is not evidence that C5.2–C5.5 failed. Their new constructions are available and independently executable, but the historical frontier wording is not one of them.

## Frontier classification

`D4-LANG-001`.

The source requires an unbounded day coordinate with a distinguished foundation origin and chronological before/after relation. A Natural day number is separately defined but explicitly does not determine before/after. Existing BidirectionalIndex semantics fit the relation, yet current production source exposes that domain only through a year-typed `מספר שנה` profile.

D4 therefore does not alter the candidate at this frontier.

## History

- D3 original candidate: token 105.
- D4 on C5.5: token 105.
- No token-count “advance” is claimed by inserting unrelated Preparation before the blocker.
