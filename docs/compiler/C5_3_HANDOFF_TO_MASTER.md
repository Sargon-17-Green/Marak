# C5.3 Handoff to Master

C5.3 READY FOR MASTER REVIEW

Baseline: `main = 56ab7977e2023145a6777e6aff85abe196803246`.

Branch: `workstream-c/c5-3-finite-ordered-collections`.

Draft PR: `#13` — do not merge from this workstream. Independent Master review is required.

## Versions

- compiler: `0.5.3-alpha.1`
- HAST: `core-hast-0.4-candidate-1`
- IR: `core-ir-0.4-candidate-1`
- artifact: `core-artifact-0.4-candidate-1`
- construction registry: `c5.3-a15-a16.1`
- language edition: unchanged at `core-0.1-integration-candidate-a13-b12`

The HAST/IR/artifact versions were bumped coherently because C5.3 adds serialized Collection operation nodes. The language edition was not changed.

## Implemented production surface and semantics

C5.3 integrates only the accepted finite ordered Collection tranche.

Implemented end-to-end:

- the six approved finite book kinds: Natural, BidirectionalIndex, one exact Symbol domain, and one nesting level for each of those three;
- typed empty Collections;
- pure immutable append;
- exact Collection count;
- semantic membership;
- first, last, and 1-based ordinal selection through explicit Natural positions;
- deterministic Natural order;
- Symbol order only from the explicit complete C5.2 adjacency-chain profile;
- nested lexicographic order derived from the leaf relation, including strict-prefix behavior;
- typed Collection places, replacements, roles, associations, outputs, and immediate results;
- recursive observation of Collection values;
- exact static domain checks across source, HAST, IR, artifact verification, and execution.

No iterator/cursor abstraction, mutable list/array semantics, generic comparator act, generic Integer, Boolean value, generic Text value, Program Input source grammar, new counted recurrence, C5.4 work, or Megillah edit was added.

## Important implementation hardening

Collection immediate-result resolution no longer depends on the textual order in which already-introduced act bodies are defined. Deferred bodies retain a source-visibility snapshot and may learn only independently derived whole-program output contracts. This does not use expected consumer type as inference.

Pure append execution now collapses a left-associated append chain iteratively before one final tuple construction. This preserves immutability and evaluation/error order while avoiding repeated prefix copies.

Artifact verification recursively validates Collection element domains, nested Symbol-domain ownership, selection position domains, exact order tags/profiles, membership domains, and all new serialized operation metadata.

## Tests and CI

Implementation verification run: GitHub Actions `35521163064` (#170).

- C5.3 Ubuntu: 45 targeted PASS; 376 full-suite PASS + 126 subtests.
- C5.3 Windows: 45 targeted PASS; 376 full-suite PASS + 126 subtests.
- C5.1, C5.2, core, and tooling-portability jobs: PASS.
- A13: 289 checks PASS.
- B12: PASS.
- A15: 335,280 case checks PASS.
- B13: 28 PASS.
- B14: 22 PASS.
- A16: 2,548 checks PASS.
- B15: 29 PASS.

See `docs/compiler/C5_3_TEST_EVIDENCE.md` for the detailed matrix and adversarial coverage.

## Registry / artifact portability

Current registry SHA-256:

`924bf2e4047bea13fadc42e4161018c5b15171773fc93ff7f8b6224f77f2f665`

Ubuntu and Windows independently produced the same current-schema hashes for the retained Symbol/Index/large-Natural portability corpus. The current registry and nine committed canonical artifacts regenerate byte-identically in CI.

## Performance / resource sanity

No Collection semantic size ceiling was introduced.

C5.3 includes a source-first 128-element end-to-end test and a CI resource-sanity probe for 16/32/64/128 elements. The probe reports compile time, backend execution time, and traced peak memory on Ubuntu and Windows without imposing a threshold.

The runtime append-chain path was specifically changed to eliminate repeated tuple-prefix copying; this is an implementation optimization only and does not alter language semantics.

## Known issues / findings

No known C5.3 semantic blocker remains at this handoff point.

The resource-sanity probe is evidence collection, not a performance contract; no arbitrary timing/RSS threshold has been introduced.

C5.1 and C5.2 remain closed and were not reopened semantically. Their tests/artifact expectations were changed only where required by the C5.3 schema/current-registry transition.

C5.3 remains Draft and unmerged. Do not claim Master acceptance until independent Master review is complete. Do not start C5.4 from this handoff.
