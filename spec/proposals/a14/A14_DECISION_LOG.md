# A14 — Decision Log

A14 decisions are proposal decisions only; A13 remains frozen until a later integration milestone.

| ID | Status | Decision |
|---|---|---|
| A-SYM-001 | PREFERRED_SURFACE_CANDIDATE / AWAITING_B | Treat runtime calendar labels as explicit symbolic `שם` data, not implicit source names and not automatically general strings. |
| A-SYM-002 | NORMATIVE_CONSTRAINT_FOR_PROPOSAL | No implicit conversion from source identifier spelling to runtime symbolic datum. |
| A-YEAR-001 | PREFERRED_SURFACE_CANDIDATE / AWAITING_B | Prefer explicit year-relative `לפני שנת אין` designation over generic unary-minus syntax. |
| A-YEAR-002 | NORMATIVE_CONSTRAINT_FOR_PROPOSAL | `אין` is not introduced as general numeric zero or null. |
| A-COLL-001 | PREFERRED_SURFACE_CANDIDATE / AWAITING_B | Use explicit `ספר` as the leading ordered-data surface family; plural nouns alone do not create collections. |
| A-COLL-002 | NORMATIVE_CONSTRAINT_FOR_PROPOSAL | No indexing base or random-access semantics by convention. |
| A-CMP-001 | SURFACE_READY | `A רב מן B` is the canonical strict numeric-order proposition A>B. |
| A-CMP-002 | SURFACE_READY | Less-than is expressed by reversing A-CMP-001 operands; no canonical `מעט` alias or ≤/≥ form is added. |
| A-NUM-007 | SURFACE_READY | Extend direct numeral grammar productively to 99,999,999 while preserving A13 1..9999 spellings. |
| A-NUM-008 | SURFACE_READY | Controlled large-number scales use descending `אלף` components and `אלף אלפים`; `רבבה` is not a canonical alias. |
| A-REP-014 | SURFACE_READY | `REPEAT_COUNT פעמים ATOMIC_ACTION` (with `פעם אחת` and `שתי פעמים`) extends A3 exact written-count recurrence; REPEAT_COUNT has its own feminine morphology. |
| A-REP-015 | PREFERRED_SURFACE_CANDIDATE / AWAITING_B | Runtime-count family evidenced by `פעמים כמספר VALUE`; final dynamic surface word order remains unfrozen; semantic count-observation policy belongs to B. |
| A-REP-016 | NORMATIVE_CONSTRAINT_FOR_PROPOSAL | Count attaches to one atomic action; composite recurrence requires a named act performance. |
| A-INPUT-001 | PREFERRED_SURFACE_CANDIDATE / AWAITING_B | External inputs should be explicit identity-addressed preparatory establishments, not positional arguments or transport channels. |
| A-INPUT-002 | NORMATIVE_CONSTRAINT_FOR_PROPOSAL | No stdin/argv or declaration-order binding is inferred. |


## B13 reconciliation delta

B13 semantic head reviewed: `3c47a57debd381c2b4e41d00d12c792ae43debe8`.

- A-SYM-001: B13 finite atomic Symbol semantics MATCH; final multiword declaration surface remains preferred/unfrozen.
- A-YEAR-001: B13 BidirectionalIndex semantics MATCH; no generic Integer syntax needed.
- A-COLL-001: B13 immutable Collection semantics MATCH; A must avoid in-place book mutation wording.
- A-CMP-001/002: B13 strict-order proposition semantics MATCH; surface remains SURFACE_READY.
- A-NUM-007/008: B13 confirms no semantic extension is required; surface remains SURFACE_READY.
- A-REP-015: B13 closes semantics: observe one Natural count once at entry; 0 means zero performances.
  Final runtime-count word order remains an A surface question.
- A-INPUT-001: **REVISED**. Supersede any external-place interpretation. Preferred semantic object is a
  named immutable Program Input Role; A14 candidate wording is documented in
  `A14_EXTERNAL_INPUT_SURFACE.md`.
