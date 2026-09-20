# A16 Handoff to B15
Status: **A16 READY FOR B15 SEMANTIC REMEDIATION REVIEW**
Review base: B14 `3c2c1d1ea4afda7365e912b161735112d63e9ac3`.

B15 should independently verify, not trust A16's mapping assertions:
- typed initializer fixes one state domain without widening A13 `מקום`;
- typed replacements preserve B12 RHS-before-commit/error effects;
- role declarations/associations/current references preserve identity-based, occurrence-specific semantics;
- output-site domain resolution is compatible with B13 zero/one output and does not imply return;
- immediate-result heads preserve exact performance provenance and adjacency;
- Index `אחר`/`לפני` map exactly to total succ/pred and never to Natural arithmetic;
- Symbol `הוא` maps to DomainId+MemberId identity, with A16's same-domain source restriction assessed as surface narrowing;
- Collection carriers never mutate Collection Values and derive element domain from source declaration/provenance, not expected type.

Required evidence is in `fixtures/A16_SURFACE_FIXTURES.json`, `reference/a16_reference.py`, and `reference/run_a16_surface_tests.py`.
Programs A/B/C exercise Symbol, Index, and Collection end-to-end flow through place → role → output → immediate result; Program C also exercises pure append, replacement, count, and ordinal selection.
Negative fixtures cover all user-required rejection classes, including wrong domains, stale result, second output, Natural zero crossing, source/label equality, and implicit dereference.

Regression logs for A13, A15, B12, B13, B14, full pytest, and A16 are under `test_logs/`.
No production compiler or Megillah candidate change is part of this proposal.
B15 should return its own semantic verdict; A16 claims only `CLOSED_FOR_B15_REVIEW` for each B14 gap.
