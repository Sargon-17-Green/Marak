# C M4 Exit Criteria Matrix

All 35 C M4 exit criteria are satisfied for Master review.

| # | Criterion | Status | Primary evidence |
|---:|---|---|---|
| 1 | A13 exact whitespace | PASS | `test_m4_a13_b12.py`, normalization contract |
| 2 | whole CoreProgram parses | PASS | A13 positive programs + tiny RM |
| 3 | exactly one `ועתה` | PASS | program-root negatives |
| 4 | preparation separated from execution | PASS | HAST/IR contracts |
| 5 | explicit principal sequencing | PASS | adjacency trap + `IRThen` |
| 6 | introduced-before-use | PASS | resolver tests |
| 7 | no hoisting | PASS | hoisting trap |
| 8 | self/mutual recursion rules | PASS | resolver + differential recursion tests |
| 9 | typed IDs | PASS | PlaceId/ActId/RoleId resolution |
| 10 | occurrence-specific roles | PASS | role lifetime/permutation tests |
| 11 | ℕ-only Core | PASS | HAST/IR/verifier/runtime tests |
| 12 | checked subtraction | PASS | `IRCheckedSubtractNatural` |
| 13 | static underflow | PASS | `SEM0201` tests |
| 14 | dynamic underflow defined | PASS | `ARITHMETIC_DOMAIN_ERROR` tests |
| 15 | failure effect boundary | PASS | replacement/preparation boundary tests |
| 16 | proposition non-value | PASS | type/category traps |
| 17 | output nonterminal | PASS | output-is-not-return test |
| 18 | stale provenance statically rejected | PASS | stale-result tests |
| 19 | dynamic no-output provenance | PASS | `RESULT_PROVENANCE_ERROR` test |
| 20 | no HALT primitive required | PASS | tiny RM + completion trap |
| 21 | canonical HAST expanded | PASS | `core-hast-0.1-candidate-1` |
| 22 | canonical IR versioned | PASS | `core-ir-0.1-candidate-1` |
| 23 | reference evaluator | PASS | HAST + independent IR reference evaluators |
| 24 | portable backend | PASS | `portable-ir-vm-0.1-candidate-1` |
| 25 | artifact/verifier | PASS | `core-artifact-0.1-candidate-1` adversarial tests |
| 26 | tiny RM end-to-end | PASS | `C_M4_RM_END_TO_END.md` |
| 27 | general non-RM examples | PASS | `examples/m4/`, `test_m4_examples.py` |
| 28 | differential execution | PASS | three-way evaluator tests |
| 29 | no Megillah special cases | PASS | static audit |
| 30 | no conventional-language leakage | PASS | anti-imitation/static audit |
| 31 | M3 regressions | PASS | legacy 157 methods retained |
| 32 | no absolute test dependencies | PASS | static + relocation audit |
| 33 | relocation verification | PASS | original path absent, 230/230 + 126 subtests |
| 34 | clean package install | PASS | final wheel install/CLI matrix |
| 35 | reproducibility | PASS | byte-identical wheel builds and relocated hash |
