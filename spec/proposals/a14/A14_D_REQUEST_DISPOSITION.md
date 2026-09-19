# A14 — D2 Request Disposition

## D-LANGUAGE-REQUEST-001 — runtime symbolic/text labels

- Need: **accepted**.
- Initial classification: `VALID_SURFACE_NEED`, `NEEDS_NEW_SURFACE`, `SEMANTICS_REQUIRED_FROM_B`.
- Existing A13 sufficient: **no**. Source names are identities, not runtime data.
- Preferred direction: a closed runtime `שם`/symbolic-name datum, distinct from source entity names.
- Not proposed now: general arbitrary strings.
- Alternatives considered: numeric codes; source identities as data; closed symbolic atoms; text
  sequences/general strings.
- Ambiguity: multiword month names and transparent punctuation make literal payload boundaries a real
  grammar issue.
- B dependency: atomic symbol vs textual sequence, equality/observability, output representation.
- Readiness: **AWAITING_B**.

## D-LANGUAGE-REQUEST-002 — year numbering before zero

- Need: **accepted**.
- Initial classification: `VALID_SURFACE_NEED`, `NEEDS_NEW_SURFACE`, `SEMANTICS_REQUIRED_FROM_B`.
- Existing A13 sufficient: **no** for direct source-level year designation.
- Preferred direction: year-relative expressions around a distinguished `שנת אין`, e.g. the family
  conceptually represented by `שנה אחת לפני שנת אין`, rather than generic unary minus.
- `אין` is not thereby the numeric literal zero and is not a general null/absence Value.
- Alternatives: generic signed integers; sign+magnitude naturals; year-relative domain.
- B dependency: whether YearNumber is a special domain or projects to signed arithmetic; ordering and
  arithmetic on such designations.
- Readiness: **AWAITING_B**.

## D-LANGUAGE-REQUEST-003 — ordered finite runtime data

- Need: **accepted**.
- Initial classification: `VALID_SURFACE_NEED`, `NEEDS_NEW_SURFACE`, `SEMANTICS_REQUIRED_FROM_B`.
- Existing A13 sufficient: **no** except by disproportionate numeric encoding.
- Preferred direction: explicit `ספר` value/referent with ordered relations already natural in the
  Megillah: `כתוב בספר`, `בראש הספר`, `אשר אחריו`, `האחרון`.
- Not assumed: array indices, zero/one based indexing, random access, homogenous machine storage.
- Alternatives: numeric encoding; plural nouns as collections; `ספר`; general sequence/list object.
- B dependency: identity, mutability/persistence, duplicates, element domain, order relation, empty
  book behavior and selection semantics.
- Readiness: **AWAITING_B**.

## D-LANGUAGE-REQUEST-004 — numeric ordering

- Need: **accepted**.
- Initial classification: `VALID_SURFACE_NEED`, `NEEDS_NEW_SURFACE`.
- Existing A13 sufficient: **no** locally; equality plus subtraction/recursion is computationally
  sufficient but not a reasonable surface repair.
- Preferred surface:
      A רב מן B
  where A is the number asserted greater and B is the comparator.
- Less-than is operand reversal, not a second primitive.
- `מעט/ימעט` is not admitted as a canonical alias in A14.
- No ≤/≥ surface is added.
- Readiness: **SURFACE_READY**.

## D-LANGUAGE-REQUEST-005 — productive numerals >9999

- Need: **accepted**.
- Initial classification: `VALID_SURFACE_NEED`, `NEEDS_NEW_SURFACE`.
- Existing A13 sufficient: semantically yes, surface-directly no.
- Preferred surface: the productive canonical grammar in `A14_PRODUCTIVE_NUMERALS.md`.
- Coverage: direct positive naturals 1..99,999,999.
- The A13 1..9999 forms are preserved byte-for-byte as the low-magnitude grammar.
- Readiness: **SURFACE_READY**.

## D-LANGUAGE-REQUEST-006 — exact N-times recurrence

- Need: **accepted**.
- Initial classification: `VALID_SURFACE_NEED`, `NEEDS_NEW_SURFACE`; dynamic-count subprofile is
  `SEMANTICS_REQUIRED_FROM_B`.
- Existing A13 sufficient: only for previously audited small counts and via non-local recursive repair.
- Literal preferred surface:
      REPEAT_COUNT פעמים ATOMIC_ACTION
- Runtime-count wording: **not frozen**; historical `פעמים כמספר VALUE` remains evidence pending B.
- Scope: exactly one atomic action; repeat a composite only by naming it as a `מעשה`.
- B dependency for runtime count: observe count once vs repeatedly, zero count, error/divergence in
  count evaluation.
- Readiness: **AWAITING_B** overall; the written-literal subprofile is **SURFACE_READY**.

## D-LANGUAGE-REQUEST-007 — external input binding

- Need: **accepted**.
- Initial classification: `VALID_SURFACE_NEED`, `NEEDS_NEW_SURFACE`, `SEMANTICS_REQUIRED_FROM_B`.
- Existing A13 sufficient only for hard-coded initial places, not reusable external binding.
- Preferred direction: top-level preparation declares explicitly named input-bearing places/things;
  the environment binds by that source identity, never by position.
- Not assumed: stdin, argv, file handles, network input, argument #1/#2.
- B dependency: binding lifecycle, type/domain, missing/extra bindings, mutability after establishment,
  failure timing.
- Readiness: **AWAITING_B**.

## Master clarification

No immediate Master clarification is required to continue A/B integration. The semantic alternatives
for 001/002/003/006/007 can be resolved by B first and returned to A for final wording.


## Post-B13 reconciliation note

B13 semantic proposals were available before A14 finalization and were reviewed at head
`3c47a57debd381c2b4e41d00d12c792ae43debe8`.

Where this document says `AWAITING_B`, the remaining gate is now **acceptance of the B13 model during
A/B integration review plus final A wording**, not an unanswered semantic research question.

The only material A14 correction caused by B13 is request 007: the preferred program-boundary object is
a Program Input Role rather than an externally initialized mutable `מקום`.
