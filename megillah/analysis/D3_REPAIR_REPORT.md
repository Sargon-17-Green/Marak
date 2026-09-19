# D3 — Core-Compatible Megillah Repair Tranche

Status: D3 CORE-COMPATIBLE REPAIR COMPLETE — READY FOR MASTER REVIEW

## Baseline
- D2 merge SHA: 4471b8e50d850bd3548af091134c16895c781ac9
- D3 baseline main: 4471b8e50d850bd3548af091134c16895c781ac9
- branch: workstream-d/d3-core-repair
- compiler: 0.4.2-alpha.1
- edition: core-0.1-integration-candidate-a13-b12

## Candidate
megillah/candidates/Megilat_HaItim_Marak_Candidate.md

Candidate SHA-256: afc6eda11a8d7f4b6499cf643d2ef5b36581bcad61b5fce761a7709274d2d643

Original SHA-256: 7b834f4a444e021bb65164282b851af960a6dbc0be3d458c2412181773b9db7b

The candidate is explicitly non-canonical and partial.

## Applied D2 patches
- D-PATCH-0001 — Master-approved 5781 → 5778;
- D-PATCH-0002 — both approved named-act introduction spans;
- D-PATCH-0003 — one approved וכן עשה → וכן תעשה span;
- D-PATCH-0004 — two approved ואחר כן → ואחרי כן spans.

No mass replacements were performed.

## Structural repair
D3-STRUCT-0001 converts historical דבר החיבור to an explicit named act חיבור with roles ראשון and שני, explicit body boundaries, and one numeric result.

A standalone C M4.2 proof compiles/runs and yields 11 for 5+6.
The worked example is retained as test/documentation evidence, not production execution.

## Traceability
- D3_DOCUMENTARY_SPAN_MAP.json records every span externalized in this tranche.
- D3_SOURCE_PROVENANCE.json maps every candidate line to its original line(s) or structural source span.
- the input-contract paragraph is retained as a blocker, not mislabeled as documentation.
- no Markdown stripping/preprocessor exists.

## Compiler progress
Original frontier: token 0.
Local-patch-only tranche frontier: token 0.
D3 structural candidate frontier: token 105, candidate line 11 / original line 35.

The repaired addition act is therefore accepted as Preparation before the next blocker.

## Tests
- A13 selftest: 289 checks PASS.
- B12 semantic run_all: PASS.
- D3 targeted tests: 7/7 PASS.
- Full Windows pytest: 261 passed, 2 failed, 126 subtests passed.

The only two full-suite failures are the already documented D-C-FIND-001 portability issues. No new semantic regression was observed.

## Blockers
All remaining known language blockers are the already routed D-LANGUAGE-REQUEST-001..007.
No D-LANGUAGE-REQUEST-008+ was opened.

## Compiler findings
No new semantic C bug.
D-C-FIND-001 Windows tooling portability remains nonblocking and is handed off separately.

## Non-goals
No full algorithm-equivalence claim.
No post-M2 language implementation.
No release/tag.
No modification of the historical original.
