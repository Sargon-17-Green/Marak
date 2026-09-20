# C5.3 Test Evidence

Baseline: `56ab7977e2023145a6777e6aff85abe196803246` (merged C5.2 production baseline).

Branch: `workstream-c/c5-3-finite-ordered-collections`.

Draft PR: #13. C5.3 remains unmerged and requires independent Master review.

## Candidate identities

- compiler: `0.5.3-alpha.1`
- package (PEP 440): `0.5.3a1`
- HAST: `core-hast-0.4-candidate-1`
- IR: `core-ir-0.4-candidate-1`
- artifact: `core-artifact-0.4-candidate-1`
- portable backend: `portable-ir-vm-0.4-candidate-1`
- IR reference: `core-ir-reference-0.4-candidate-1`
- construction registry: `c5.3-a15-a16.1`
- language edition remains `core-0.1-integration-candidate-a13-b12`

The serialized-contract versions were bumped because C5.3 adds new HAST/IR/artifact node kinds. The language edition was intentionally not changed.

## Verified CI evidence

GitHub Actions PR run `35521163064` (run #170) is green for the implementation state through commit `76dc003cefe9e9fec82cca6d51123c2e518ef496`.

Dedicated C5.3 jobs:

- Ubuntu job `106105375522`: **45 targeted tests passed**; **376 full-suite tests + 126 subtests passed**.
- Windows job `106105375417`: **45 targeted tests passed**; **376 full-suite tests + 126 subtests passed**.

The same run also passed the C5.1 regression matrix, C5.2 regression matrix, tooling portability, and core job.

Required proposal regressions passed in the C5.3 matrix on both operating systems:

- A13: **289 checks PASS**.
- B12 integrated semantic/regression/RM suite: **PASS**.
- A15: **335,280 case checks PASS**, including all 9,999 frozen A13 numerals.
- B13: **28 reference tests PASS**.
- B14: **22 integration tests PASS**.
- A16: **2,548 checks PASS** (2,518 positive / 30 negative).
- B15: **29 independent tests PASS**.

## Canonical bytes / portability

The current construction registry regenerates byte-identically on Ubuntu and Windows.

Current registry SHA-256:

`924bf2e4047bea13fadc42e4161018c5b15171773fc93ff7f8b6224f77f2f665`

The current 0.4 artifact hashes for the retained C5.2 portability corpus were independently produced with identical values on Ubuntu and Windows and are locked in `tests/test_c5_2_portability.py`:

- Symbol corpus: `7862d3b43bcff13bf7f7fbd4c9390b38c8b8a3806a8bc785f0bbbd0c62d5249b`
- BidirectionalIndex corpus: `1f301398973e84ed327a48b31557d9eaaf62ed5ceb9dc4465abc44d412580e65`
- large-Natural corpus: `b4ddf822987986a044c0bb997c8b5e93af9d844d5ded21e230cfca617c781f19`

The nine committed canonical M4 artifacts were regenerated for artifact schema 0.4 and the C5.3 CI verifies that regeneration leaves both `spec/CURRENT_CONSTRUCTION_REGISTRY.json` and `artifacts/` clean.

## C5.3 semantic coverage

Source-first coverage exercises the complete production path `source -> normalize -> lex -> parse -> resolve -> validate -> HAST -> IR -> artifact -> verify -> execute -> observable result`, with differential agreement among HAST reference, IR reference, and portable backend.

Covered behavior includes:

- all six approved book kinds and all six typed empty forms;
- pure immutable append, exact count, semantic membership, first/last/1-based ordinal selection;
- Natural, BidirectionalIndex, Symbol, and nested-Collection selection;
- Natural numeric ordering, explicit-complete-profile Symbol ordering, and nested lexicographic ordering with strict-prefix behavior and stable ties;
- duplicate preservation and same-visible-label/different-Symbol-identity behavior;
- Collection places, roles, outputs, immediate results, nested occurrences, recursive roles, and recursive Collection outputs;
- failed RHS atomicity, earlier-effect retention, destination preservation, and later-work suppression;
- dynamic `COLLECTION_POSITION_ERROR` for zero/out-of-range positions;
- source renaming/internal serial-shift invariance for nested Symbol Collections;
- Charter transparency for whitespace, punctuation, nonsemantic Arabic digits/Latin text, niqqud, Markdown punctuation, and Hebrew quote punctuation;
- negative surface guards against generic/untyped Collection syntax, bracket indexing, generic equality/comparator acts, hidden iterator/cursor constructs, deeper unsupported nesting, and generic Boolean/Integer additions.

The resolver also removes an implementation-only body-definition-order dependency for Collection immediate-result contracts by deferring unresolved output-contract resolution while preserving the source visibility snapshot. Cyclic unanchored Collection result contracts are rejected statically rather than inferred from a consumer.

## Artifact trust-boundary coverage

Adversarial valid-digest artifact tests reject:

- forged Collection literal element-domain metadata;
- forged append element-domain metadata;
- non-Natural ordinal-position operands;
- unknown Collection order tags;
- Symbol ordering without a complete explicit profile;
- forged Symbol order-profile/domain ownership;
- recursive nested element-domain mismatches.

Canonical IR validation recursively verifies nested Collection domains and declared Symbol-domain ownership. Older artifact schema 0.3 is explicitly rejected by the 0.4 verifier.

## Resource sanity

No Collection-specific semantic size cap was added. A guard rejects introduction of names such as `MAX_COLLECTION`, `collection_limit`, `collection_cap`, or `max_book_size` in the C5.3 execution path.

Pure append-chain evaluation was changed from repeated immutable tuple-prefix copying to iterative chain collapse plus one final tuple materialization, removing the accidental runtime O(n^2) prefix-copy pattern while preserving inner-to-outer evaluation/error order.

A source-first 128-element Collection test passes end-to-end. The final C5.3 CI additionally runs `tools/c5_3_resource_sanity.py` for 16/32/64/128 elements on Ubuntu and Windows and reports compile time, backend time, and traced peak memory without imposing an arbitrary performance threshold.

