# D2 — M2 Rebase Report

Status: **D2 REBASE COMPLETE — READY FOR MASTER REVIEW**

- Canonical repository baseline: Sargon-17-Green/Marak main at 8a3a25e2fb5e438b01fef9694570f20d16a34ff3
- Work branch: workstream-d/m2-rebase
- Original: megillah/original/Megilat_HaItim_Yehuda_FINAL_2026-09-18.md
- Original SHA-256: 7b834f4a444e021bb65164282b851af960a6dbc0be3d458c2412181773b9db7b (verified)
- Compiler: 0.4.2-alpha.1
- Language edition: core-0.1-integration-candidate-a13-b12

## Baseline verification
- editable install: PASS
- A13 selftest: PASS, 289 checks
- B12 semantic run_all: PASS (33 B12 tests plus B11 regressions and RM witness)
- Windows pytest: 254 PASS / 2 FAIL / 126 subtests PASS
- the two pytest failures are D-C-FIND-001 tooling portability; E v0.8.2 records 256/256 + 126 PASS in its verified environment
- E v0.8.2: 13 READY / 0 BLOCKED / 0 NEEDS_MASTER_CLARIFICATION

## Reclassification result
- Active D2 classes: {'DOCUMENTATION_OR_PROSE_INSIDE_SOURCE': 2, 'SOURCE_NOT_LANGUAGE': 16, 'SOURCE_PROGRAMMING_BUG': 1, 'SOURCE_AMBIGUITY': 3}
- Finding status counts: {'RECLASSIFIED': 11, 'STILL_VALID': 5, 'CLOSED_BY_A13': 1, 'NEW_D2': 6}
- Genuine SPEC_HOLE count: 0.
- A13/B12 materially shrink D1's former SPEC_HOLE set; most become concrete SOURCE_NOT_LANGUAGE or source ambiguity findings.

## Current source frontier
- Normalization succeeds.
- Original parse fails at normalized token 0 / source line 1 with PROG0001 + PARSE0002.
- A scratch probe removing the documentary prefix and fixing only the first act introduction reaches token 4, then fails at the historical body prose beginning וזה דבר החיבור.
- Resolve, validate and execution are not reached for the Megillah.

## Source inventory
- Current A13 normalizer: 9,227 normalized tokens; 984 unique words; 83 Markdown heading lines.
- Normalized SHA-256: e4f51e69498f166e92ac8b738ac9e9166dda891ce2a2e22859ffc53b07287765.
- The original has one lexical ועתה at physical line 169; it is not a recognized top-level transition in the current parse.

## Patch posture
- Proposed local patch IDs: 4; applied/accepted patches: 0.
- D-PATCH-0001 remains Master-gated because it changes the erroneous algorithmic bound despite strong 5778 evidence.
- No corrected candidate source is created in D2.

## Post-M2 language requests
- Language requests recorded: 5; D implements none.
- Requests cover runtime symbolic labels, signed years, ordered finite collections, numeric ordering/pre-gated recurrence, and productive >9999 numeral spelling.
