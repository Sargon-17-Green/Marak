# Conformance

The repository contains several layers of executable evidence:

- `tests/` — compiler and runtime regression/conformance tests;
- `spec/surface/tools/a13_selftest.py` — frozen surface-contract checks;
- `spec/semantics/run_all.py` — semantic and Register-Machine checks;
- `conformance/evidence/e-v0.8.2/` — the independent adversarial M2 gate-review evidence.

E v0.8.2 concluded with **13 READY / 0 BLOCKED / 0 NEEDS_MASTER_CLARIFICATION**.

Historical E test files are retained as evidence. A later cleanup may normalize the independent suite into a repository-native runner without changing its expected semantics.
