# A15 — Post-M2 Integrated Surface Closure

Status: **A15 READY FOR B14 SEMANTIC INTEGRATION REVIEW**

Workstream: A — Surface Language / Controlled Biblical Hebrew

## 1. Authority and scope

A15 is proposal/integration material only. It does not reopen A13/B12, does not declare M3, does not modify the production compiler, and does not modify the Megillah candidate.

Canonical repository baseline inspected for A15:

    main = 621a656c25b7667640cc61a1d1a6ddef95db474d

Reviewed proposal inputs:

    A14 = 04292cbc1f53ea25bb2dd5534f86617c2a72a6fd
    B13 = 3c47a57debd381c2b4e41d00d12c792ae43debe8

A14 and B13 remain proposal evidence; A15 does not treat their Draft PR state as a language freeze. The Master decisions supplied for this work authorize the B13 semantic models as the semantic basis for this integrated surface closure.

## 2. Charter invariance

A15 adds no exception to `spec/LANGUAGE_CHARTER.md`.

Outside any future separately approved literal mechanism:

- only normalized Hebrew letters and the frozen whitespace set carry lexical structure;
- punctuation, maqaf, Markdown, niqqud, cantillation, Latin letters, Arabic digits, indentation, and line breaks do not establish syntax;
- every construction remains recoverable after punctuation erasure and whitespace collapse;
- if two plausible admitted readings change computation, the source is invalid rather than parser-ranked.

No A15 construction uses a quote delimiter or punctuation-sensitive payload.

## 3. Integrated request disposition

| Request | A15 disposition | Surface family |
|---|---|---|
| D-LANGUAGE-REQUEST-001 | `INTEGRATED_SURFACE_READY` | finite `משפחת שמות`, member declaration, counted visible-label metadata, typed runtime reference |
| D-LANGUAGE-REQUEST-002 | `INTEGRATED_SURFACE_READY` | year-typed `שנת אין` / exact `N שנים לפני/אחרי שנת אין` family mapping to BidirectionalIndex |
| D-LANGUAGE-REQUEST-003 | `INTEGRATED_SURFACE_READY` | typed immutable ordered `ספר`, pure append, count, membership, ordinal access, first/last, lexicographic ordering |
| D-LANGUAGE-REQUEST-004 | `INTEGRATED_SURFACE_READY` | strict Natural proposition `A רב מן B` |
| D-LANGUAGE-REQUEST-005 | `INTEGRATED_SURFACE_READY` | productive direct Natural family through the current 99,999,999 edition frontier |
| D-LANGUAGE-REQUEST-006 | `INTEGRATED_SURFACE_READY` | literal exact count plus canonical dynamic `פעמים כמספר VALUE ACTION` |
| D-LANGUAGE-REQUEST-007 | `INTEGRATED_SURFACE_READY` | immutable named Program Input Roles owned by `המלאכה הזאת` |

There is no remaining `AWAITING_B` in A15 and no `NEEDS_MASTER_CLARIFICATION` was found.

## 4. Exact construction registry — A15 proposal

### 4.1 Runtime Symbols

Domain:

    תהי משפחת שמות ושמה DOMAIN

Member plus canonical visible label metadata:

    יהי במשפחת השמות אשר שמה DOMAIN שם ושמו MEMBER
    ולשם אשר במשפחת השמות אשר שמה DOMAIN שמו MEMBER
    מספר המלים אשר בשמו הנראה יהיה LABEL_WORD_COUNT
    והמלים הן LABEL_WORDS

Runtime reference:

    השם אשר במשפחת השמות אשר שמה DOMAIN שמו MEMBER

`LABEL_WORD_COUNT` determines the intrinsic label boundary after normalization. The label words are metadata of the atomic member, not a Text Value.

If Symbol order is needed, it is declared by semantic member identity, never spelling:

    במשפט משפחת השמות אשר שמה DOMAIN
    יהיה SYMBOL_A מיד לפני SYMBOL_B

A complete adjacency chain is required before that relation may order collections.

### 4.2 BidirectionalIndex — year surface profile

    שנת אין
    שנה אחת לפני שנת אין
    שתי שנים לפני שנת אין
    YEAR_COUNT שנים לפני שנת אין
    שנה אחת אחרי שנת אין
    שתי שנים אחרי שנת אין
    YEAR_COUNT שנים אחרי שנת אין

The first maps to ZeroIndex; the before/after families map to B13 BeforeZero/AfterZero. `אין` is not a general zero token.

### 4.3 Finite ordered collections

Current kind heads:

    ספר מספרים
    ספר מספרי שנים
    ספר שמות ממשפחת השמות אשר שמה DOMAIN
    ספר ספרי מספרים
    ספר ספרי מספרי שנים
    ספר ספרי שמות ממשפחת השמות אשר שמה DOMAIN

Empty examples:

    ספר מספרים אשר אין בו מספר
    ספר שמות ממשפחת השמות אשר שמה DOMAIN אשר אין בו שם

Pure append:

    BOOK_KIND אשר בו כל אשר ב BOOK_VALUE כסדרו ואחר כלם ITEM_VALUE

Count:

    מספר הדברים אשר בתוך BOOK_VALUE

Membership proposition:

    ITEM_VALUE כתוב בתוך BOOK_VALUE

First / last:

    ELEMENT_HEAD אשר בראש BOOK_VALUE
    ELEMENT_HEAD האחרון אשר בתוך BOOK_VALUE

Positive ordinal selection:

    ELEMENT_HEAD אשר מספרו בסדר BOOK_VALUE הוא POSITION_VALUE

Natural ordering:

    הספר הערוך מן BOOK_VALUE מן המעט אל הרב

Symbol ordering:

    הספר הערוך מן BOOK_VALUE כמשפט משפחת השמות אשר שמה DOMAIN

Nested lexicographic ordering:

    הספר הערוך מן BOOKS_VALUE מראש כל ספר ועד אחריתו ORDER_PROFILE

A bare successor-by-value is deliberately absent because duplicates are legal. Successor of an occurrence is ordinal `k+1`; traversal uses explicit ordinal state and existing action/control constructs.

### 4.4 Strict Natural ordering

    NUMBER_VALUE_A רב מן NUMBER_VALUE_B

Meaning: `A > B`. `A < B` is written by reversing operands. No direct LE/GE surface is admitted in A15.

### 4.5 Productive direct Naturals

A13 1..9999 remains unchanged. A15 admits the A14 descending thousand/million family whose present direct-literal edition frontier is 99,999,999. The frontier is not a semantic Natural bound and is not permanent language law.

The Megillah magnitude 14,777,149 is admitted directly as:

    ארבעה עשר אלף אלפים ושבע מאות אלף ושבעים אלף ושבעת אלפים ומאה וארבעים ותשעה

### 4.6 Exact counted recurrence

Literal:

    פעם אחת ATOMIC_ACTION
    שתי פעמים ATOMIC_ACTION
    REPEAT_COUNT פעמים ATOMIC_ACTION

Dynamic:

    פעמים כמספר NATURAL_VALUE ATOMIC_ACTION

Both map to `RepeatExactly(N,A)`. Dynamic N is observed once before iteration. Zero means zero performances. Scope is exactly one atomic action.

### 4.7 Program Input Roles

Declaration:

    יהי למלאכה הזאת דבר ושמו ROLE
    ובטרם תחל המלאכה הזאת
    יעמד DOMAIN_HEAD
    תחת הדבר אשר למלאכה הזאת שמו ROLE

Natural reference:

    המספר אשר עומד תחת הדבר אשר למלאכה הזאת שמו ROLE

Other domains use their typed heads. Binding is by semantic role identity before Preparation, exactly once per invocation, immutable, and non-positional.

A14's schematic `למלאכה הזאת ינתן ...` is not canonical A15 wording because it risks an executable giving-event reading.

## 5. Source evidence policy

A15 treats the Megillah as the primary corpus for computational need and Biblical Hebrew as evidence for linguistic constructions, not as automatic semantic authority.

Key Megillah evidence includes: named cutlet/month families and explicitly multiword names; `שנת אין` and before-origin years; `ספר ימי חודשים`, `ספר שמות חודשים`, head/successor/last traversal and book ordering; `רב`/`ימעט` comparisons; large written constants; literal and `פעמים כמספר` recurrence; and the two named day inputs to the whole work.

Key Biblical parallels retained from A14 or independently rechecked include `X רב מן Y`; `שלש פעמים תכה`; large `אלף` compositions including `אלף אלפים`; `כל הנמצא כתוב בספר`; `מלים`; and `המלאכה הזאת`. Where Marak needs a stronger machine-recoverable boundary than free discourse, the controlled deviation is stated in the family document.

## 6. Ordinal-position decision

A15 found a genuine need for source-visible ordinal selection because the Megillah traverses ordered books and B13 allows duplicate Values. A bare value-relative `אחריו` cannot uniquely select an occurrence in all valid collections.

The admitted construction therefore states a positive ordinal relation: `מספרו בסדר BOOK הוא POSITION`. It is not an array index. Position zero is invalid; no bracket syntax or random-access implementation ontology is exposed.

## 7. Collection mutability decision

All collection construction and ordering is pure. A15 intentionally avoids imperative `הוסף לספר` wording. If B14 integrates Collection Values into a state-bearing A13/B12 carrier, changing the carrier must remain an explicit replacement operation after the pure Collection Value is computed. Nothing in A15 makes a book mutable.

## 8. Program owner decision

`המלאכה הזאת` is accepted as the whole-program owner only in the top-level Program Input Role profile. It cannot be used to denote the current named-act performance, for which A13 already freezes `המעשה הזה`.

## 9. Numeral-frontier decision

The present 99,999,999 frontier is grammatically explainable within the current magnitude family, but the decision to stop the million coefficient at 99 is still an edition boundary. A15 therefore records the family rather than a permanent maximum. Semantic Naturals remain unbounded.

## 10. Test policy

`tools/run_a15_surface_tests.py` is a proposal reference suite, not production compiler code. It checks semantic reference models and exact surface invariants for all seven requests, including Charter normalization perturbations, collisions, identity distinctions, ordinal errors, immutable append/order behavior, dynamic recurrence observe-once semantics, and non-positional inputs.

A15 also runs the existing repository suite unchanged after adding only proposal files. Results are recorded in `A15_TEST_RESULTS.json`.

## 11. Freeze boundary

A15 does **not** add:

- general Text or string literals;
- generic signed Integer;
- arrays or zero-based indexes;
- mutable collection objects;
- Boolean Values;
- source-visible LE/GE;
- comparator callbacks;
- implicit loop index or block-scoped `for`;
- positional program parameters;
- stdin/argv/HTTP semantics;
- generic modern type syntax;
- production compiler support.

## 12. Next gate

A15's seven surfaces are ready for B14 to verify exact semantic integration against B13 and frozen B12. A15 itself does not declare those proposal constructions frozen language law and does not declare M3.
