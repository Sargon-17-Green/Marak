# B14 A Surface Gaps — A16 Input

## B14-A-SURFACE-GAP-001 — TYPED_STATE_BEARING_REFERENTS
Need: retain/read/replace Symbol, BidirectionalIndex, Collection values.
A15 gap: A13 place forms are explicitly numeric; A15 adds no typed carrier family.
Evidence: incremental books, dynamic year numbering, retained selected names.
B13: B-VAL-POST-001.
Constraints: no implicit dereference; identity distinct from value; B12 commit/error boundary preserved;
domain linguistically recoverable. No syntax prescribed.

## B14-A-SURFACE-GAP-002 — TYPED_ACT_ROLES
Need: pass/read occurrence-specific Symbol/Index/Collection associations in named acts.
A15 gap: A13 named-act roles are numeric; only whole-program inputs are generalized.
Evidence: reusable collection/order/name calculations.
B13: B-VAL-POST-001.
Constraints: named non-positional role association; immutable per occurrence; no alias, parameter cell,
stack-frame visibility, or runtime name search.

## B14-A-SURFACE-GAP-003 — TYPED_ACT_OUTPUT_AND_IMMEDIATE_RESULT
Need: zero/one non-Natural act output plus typed immediate provenance reference.
A15 gap: A13 output and `המספר אשר יצא עתה` are numeric; A15 adds no typed forms.
Evidence: final year number, cutlet name, month name; reusable data-producing acts.
B13: B-VAL-POST-001, B-OBS-002.
Constraints: output is not return; no abrupt termination; at most one per occurrence; immediate
provenance is not a global last-result register; no stdout/exit semantics.

## B14-A-SURFACE-GAP-004 — BIDIRECTIONAL_INDEX_SUCCESSOR_PREDECESSOR
Need: source constructions denoting B13 succ(Index) and pred(Index).
A15 gap: explicitly not surfaced.
Evidence: Megillah `מספרי השנים`, around 1341–1361, requires runtime next/previous year across zero.
B13: B-IDX-001.
Constraints: result remains Index; no generic Integer or Natural underflow promotion; crossing zero exact.

## B14-A-SURFACE-GAP-005 — SYMBOL_EQUALITY_PROPOSITION
Need: exact equality proposition between two Symbol values.
A15 gap: frozen A13 equality is numeric; A15 only provides membership/equality internally.
Evidence: name-book traversal compares corresponding names before advancing.
B13: B-SYM-001.
Constraints: proposition not Boolean; equality by DomainId+MemberId, never label spelling; no coercion.
Do not generalize equality to other domains merely for symmetry without independent need.
