# C M4.1 — Regression Results

Current C suite after remediation: **242 tests + 126 subtests PASS** at the documentation checkpoint; final packaging verification records the final count.

Upstream baselines after remediation:

- A13 selftest: 289/289 PASS.
- B12 `run_all.py`: PASS; B12 semantics 33, RM countdown 128, RM underflow guard 65, plus B11 compatibility suites.
- E artifact fuzz: 2000 cases, no uncontrolled exceptions.
- E generated property corpus: 550/550 attempted with no failures.
- E RM generated corpus: 240 cases PASS.
- E parser stress 128 actions: unique parse, 2701 tokens, 7607 state keys, ~11.2 MB peak, ~13.4 s in this run.

The E mutation tool itself has source-text mutation anchors tied to the pre-refactor M4 backend formatting; after the required recursion rewrite several anchors no longer exist. C M4.1 supplies behavior/architecture mutation guards instead of altering E's tool.

Final C M4.1 source-tree suite: **242/242 tests PASS + 126 subtests PASS**.

Relocation final:
- original source path absent during run;
- 242/242 + 126 subtests PASS;
- wheel builds byte-identical;
- wheel SHA-256 `29f82d91ccdb19a15a354cce71f364b1c870f6fed6522647e6d497ed80de2623`;
- clean venv install PASS;
- installed CLI `version/check/compile/run/explain` PASS;
- tiny RM installed-CLI result: Normal, `גד=0`, `עזר=0`.
