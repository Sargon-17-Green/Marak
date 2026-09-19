# D2 — M2 Rebase Report

Status: **D2 REBASE COMPLETE — READY FOR MASTER REVIEW**

- Canonical repository baseline: Sargon-17-Green/Marak main at 8a3a25e2fb5e438b01fef9694570f20d16a34ff3
- Work branch: workstream-d/m2-rebase
- Compiler: 0.4.2-alpha.1
- Language edition: core-0.1-integration-candidate-a13-b12
- Original SHA-256: 7b834f4a444e021bb65164282b851af960a6dbc0be3d458c2412181773b9db7b (verified)

## Baseline verification
- A13 selftest: PASS, 289 checks
- B12 semantic run_all: PASS
- GitHub PR CI: PASS
- Windows local pytest portability note remains D-C-FIND-001; no semantic C bug was found.

## Reclassification result
- Total finding families: 24
- Active findings: 23
- Active classes: {'DOCUMENTATION_OR_PROSE_INSIDE_SOURCE': 2, 'SOURCE_NOT_LANGUAGE': 17, 'SOURCE_PROGRAMMING_BUG': 1, 'SOURCE_AMBIGUITY': 3}
- Status counts: {'RECLASSIFIED': 11, 'STILL_VALID': 5, 'CLOSED_BY_A13': 1, 'NEW_D2': 7}
- Genuine current SPEC_HOLE count: 0.

## Local patch evidence
- Four local patches remain unapplied to the historical original.
- D-PATCH-0002, 0003, and 0004 are now SEMANTICALLY_CONFIRMED against C M4.2 minimal/full-program probes.
- D-PATCH-0001 remains MASTER_APPROVAL_REQUIRED because it changes the numeric algorithmic bound from 5781 to 5778.

## Structural conclusion
- A truthful whole-file candidate is not yet warranted.
- The first reusable algorithmic description, דבר החיבור, can be expressed as a legal A13 named act with two named roles and one result; a proof program returns 11 for 5+6.
- Whole-program repair is nevertheless blocked by current post-M2 capability questions recorded in D2_LANGUAGE_REQUESTS.md/json.
- The single lexical ועתה at historical line 169 is not the A13 program entry.

## Current compiler frontier
- Original normalization succeeds.
- Parse/program composition fails at normalized token 0/source line 1 with PROG0001 + PARSE0002.
- A controlled scratch probe after documentary-prefix removal and first act-introduction repair reaches normalized token 4 and then fails at the historical body prose.
- Resolve/validate/execute are not reached for the whole Megillah.

## Inventory
- 9,227 normalized tokens; 984 unique normalized words; 83 Markdown heading lines.
- D2_SECTION_INVENTORY.json now records all 83 heading-delimited spans objectively; headings are not treated as semantic boundaries.

## Master-routing requests
- Language/interface requests: 7.
- No language feature is implemented by D.
- Separate while/pre-check syntax, multiplication primitives, and positional multi-result tuples are deliberately not requested at this stage.
