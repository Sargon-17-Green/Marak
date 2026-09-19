# C M4 Handoff — A13/B12 Core Compiler Integration

Status: **C M4 COMPLETE — ready for Master review**. No M2 declaration is made here.

## Authoritative inputs

- C M3 handoff: `C_WORKSTREAM_C_MILESTONE_03_HANDOFF_2026-09-19(1).zip`
- A13: `A13_A_Core_v0.1_Integration_Frozen_Candidate(1).zip`
- B12: `B_Workstream_Milestone_B12_A13_SEMANTIC_INTEGRATION_2026-09-19(1).zip`

## Result

C M4 implements the A13/B12 Core pipeline from normalized source through whole-program parse, typed resolution, static validation, canonical HAST, versioned canonical IR, deterministic verified artifact, independent IR reference evaluation and portable backend execution.

The A13 tiny RM passes the entire path and completes normally. General non-RM examples are included under `examples/m4/` and compiled artifacts under `artifacts/`.

## Evidence summary

- C: 230 passed + 126 subtests.
- A13: 289/289 PASS.
- A12 regression under A13: 517/517 PASS in runner-compatible staging; upstream path defect documented.
- B12: run-all PASS, including 33/33 semantics, 128 countdown and 65 underflow-guard cases.
- Relocation with original source path absent: 230 passed + 126 subtests; source and installed CLI matrix PASS.
- Reproducible final wheel SHA-256: `266189bb6e478baec313c320b3fefd32e98c78b3f686556effe89905833dd320`.

## Core versions

- compiler `0.4.0-alpha.2`
- language `core-0.1-integration-candidate-a13-b12`
- registry `a13-b12.1`
- HAST `core-hast-0.1-candidate-1`
- IR `core-ir-0.1-candidate-1`
- IR reference `core-ir-reference-0.1-candidate-1`
- artifact `core-artifact-0.1-candidate-1`
- backend `portable-ir-vm-0.1-candidate-1`

## Review entry points

Start with:

1. `C_M4_FINAL_VERIFICATION.md`
2. `docs/C_M4_INTEGRATION_CLOSURE.md`
3. `docs/C_M4_A13_B12_RECONCILIATION.md`
4. `C_M4_A13_B12_CONTRACT.json`
5. `docs/C_M4_HAST_CONTRACT.md`
6. `docs/C_M4_IR_CONTRACT.md`
7. `docs/C_M4_ARTIFACT_CONTRACT.md`
8. `docs/C_M4_REFERENCE_BACKEND_EQUIVALENCE.md`
9. `docs/C_M4_RM_END_TO_END.md`
10. `docs/C_M4_RELOCATION_VERIFICATION.md`
11. `docs/C_M4_ANTI_IMITATION_DELTA.md`
12. `docs/C_M4_BLOCKED_ON_SPEC.md`

`docs/C_M4_HANDOFF_TO_E_V08.md` is a handoff document only. E v0.8 was not started in Workstream C.
