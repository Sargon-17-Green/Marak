# D4 — T21 Evidence Remediation Closure Candidate

Status: **CLOSED_CANDIDATE**  
Scope: D4 / T21 / Luach Seventeen evidence remediation only.  
T22: **NOT STARTED**.  
PR #20 remains Draft / open / unmerged.

## Immutable subject

- Evidence/runtime HEAD: `5a6896c70a74e35504e6db8492223a139344ceee`
- Candidate SHA-256: `6fda03c4ca953898b471da666c048d81020f9bea4fcd240b94aab7bb3f091881`
- Candidate changed by remediation: **NO**
- Language / T21 algorithm changed: **NO**
- Runtime implementation changed: **YES**, under the user-authorized semantics-preserving implementation exception of 2026-10-20.

## Findings

- `D4-T21-EVID-001 — END_TO_END_THREE_RUNTIME_GATE_PIPELINE_NOT_RETAINED`
  - Closure state: **CLOSED_CANDIDATE**
- `D4-T21-EVID-002 — FULL_PRODUCTION_THREE_RUNTIME_EVIDENCE_NOT_COMPUTATIONALLY_TRACTABLE_UNDER_CURRENT_RUNTIME_IMPLEMENTATION`
  - Closure state: **CLOSED_CANDIDATE**
  - Resolution: opt-in semantics-preserving constructive intrinsics plus state-implementation optimization. No host-oracle substitution, pasted constants, hard-coded result table, or T21 projection was used.

## Semantics-preserving runtime remediation

The retained production evidence continues to execute the real production source and chain. The runtime implementation was optimized in two layers:

1. avoid redundant state reconstruction/copying during constructive execution;
2. opt-in constructive intrinsics for the canonical acts:
   - `לקחת מספר פעמים`;
   - `הנותר בדרך הקצרה`;
   - `נותר`;
   - `חלק`.

The intrinsics reproduce the language-observable product/provenance sequence and final scratch facts required by their canonical implementations. They are disabled when a fuel budget is supplied so the baseline step-by-step evaluator remains available for equivalence/diagnostic checks.

Focused slow-vs-fast regressions require exact observable agreement across HAST, IR reference, and portable backends.

## Retained full-production evidence

GitHub Actions workflow: **D4 T21 Evidence #12**  
Run ID: `39432731750`

All six production executions completed successfully:

| side | runtime | job ID | compile seconds | execute seconds | artifact ID |
| --- | --- | ---: | ---: | ---: | ---: |
| after | HAST | 118661762341 | 96.045 | 3.049 | 12269265904 |
| after | IR reference | 118661761949 | 105.701 | 1.460 | 12268858173 |
| after | portable | 118661761291 | 86.679 | 1.381 | 12268916733 |
| before | HAST | 118661762024 | 83.393 | 2.394 | 12268223487 |
| before | IR reference | 118661761810 | 76.156 | 1.319 | 12268587735 |
| before | portable | 118661761976 | 88.350 | 1.439 | 12269740377 |

### Exact retained observables

For the positive side, all three decompressed canonical JSON observable files are byte-identical (SHA-256 of the decompressed file bytes):

- SHA-256: `ceae6a783f4cd00c01fbf9d63ea8899cf0250f015de5837be312549d3bccb1ea`
- products: `456191`
- `חשב רווח שער`: `377`
- `בחירה`: `336`
- query snapshot: `AfterZero / 1`
- resulting gate snapshot: `AfterZero / 377`

For the negative side, all three decompressed canonical JSON observable files are byte-identical (SHA-256 of the decompressed file bytes):

- SHA-256: `6761637960ced70cbd884eedc4b877a6d860852c88b4cb55363ed98898b6db6d`
- products: `455969`
- `חשב רווח שער`: `762`
- `בחירה`: `721`
- query snapshot: `BeforeZero / 1`
- resulting gate snapshot: `BeforeZero / 762`

The full facts also agree exactly by side, including `השער התיכון`, `יום שאלת השער`, `השער הנוכחי`, `מונה השערים`, `מלא הקערות`, and `מערכת הטיפה האחרונה`.

The repository comparator `tests/d4_t21_end_to_end_compare.py` requires exactly the same conditions independently checked above:
- HAST == IR reference == portable observable for each side;
- positive gap == 377;
- negative gap == 762.

## Required production pipeline result

Positive:
`חשב רווח שער -> drops/bowls -> T19 bowl query -> T20 selector -> +41 -> actual gate position`
=> **PASS**, resulting gate **+377**.

Negative:
same full production chain
=> **PASS**, resulting gate **-762**.

## Independent recheck and exact-head comparator

- The six Evidence #12 artifact ZIPs were inspected independently.
- All three decompressed `after` JSON files had byte-identical SHA-256 `ceae6a783f4cd00c01fbf9d63ea8899cf0250f015de5837be312549d3bccb1ea`.
- All three decompressed `before` JSON files had byte-identical SHA-256 `6761637960ced70cbd884eedc4b877a6d860852c88b4cb55363ed98898b6db6d`.
- The Evidence #12 comparator job was cancelled when the receipt documentation commit superseded that run. It must NOT be cited as a successful comparator.
- The comparator was subsequently verified **PASS** in exact-head **D4 T21 Evidence #13**, run `39434003695`, on documentation HEAD `80e4f2d3f109074feb87d372f3e9d694775d8ec3`. In that run, six execution jobs and the comparator succeeded; the optional profiler job was intentionally skipped.
- The same documentation HEAD also passed **19/19** jobs in CI #614 (push; run `39434003730`) and **19/19** in CI #615 (PR; run `39434012823`).
- This documentation-only hash correction produces a new HEAD and therefore requires the normal exact-HEAD CI and E2E checks again before final Master handoff.

## Acceptance boundary

This document does **not** claim Master acceptance.

Before handoff, verify:
- exact-head CI push and PR workflows are green;
- the comparator job for the latest exact HEAD is green;
- PR #20 remains Draft/open/unmerged;
- T22 remains unstarted.
