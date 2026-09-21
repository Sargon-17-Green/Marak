# B16 CI / Regression Evidence

Semantic/reference candidate HEAD:
`aab6d5d2d10fe72d24faa42c29f540da29c70d30`

GitHub Actions:
- workflow: CI
- run: `35579729051`
- run number: `326`
- result: **15/15 jobs SUCCESS**

The matrix includes core; tooling portability on Ubuntu/Windows; C5.1, C5.2, C5.3, C5.4 and C5.5 on
Ubuntu/Windows; and D4 Megillah conformance on Ubuntu/Windows.

## Core evidence

`python -m pytest -q`:
**478 passed, 126 subtests passed in 14.83s**

This includes:
- B16 semantic reference tests: **30/30 PASS**;
- B16 required regression-gate tests: **4/4 PASS**.

The regression gates themselves execute and assert:
- B13 reference suite: **28/28 PASS**;
- B15 reference suite: **29/29 PASS**;
- A16 reference checks: **2,548/2,548 PASS** (2,518 positive; 30 negative);
- A17 proposal checks: **4,415/4,415 PASS** (4,388 positive; 27 negative).

Additional core gates:
- A13 selftest: **289 checks PASS**;
- B12 `run_all`: PASS;
- B11 original integrated suite: 14 tests, RM grid 324;
- B11 intent under B12: 14 tests;
- B12 semantic tests: 33;
- RM countdown cases: 128;
- RM underflow-guard cases: 65.

No production, registry or Megillah mutation is part of B16.
