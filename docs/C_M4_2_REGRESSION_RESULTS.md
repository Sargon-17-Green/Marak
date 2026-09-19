# C M4.2 Regression Results

## C suite

- C M4.1 baseline requirement: **242 pytest tests + 126 subtests**.
- C M4.2 final source: **256 pytest tests + 126 subtests PASS**.
- Added coverage: no-default-quota execution, depth 5,000/10,001/20,000, high sequential performance count, explicit caller budget, all-layer no-fuel timeout, activation cleanup, bootstrap metadata, MIT/Marak/CLI metadata and absolute-path cleanup.

## Upstream baselines

- A13 selftest: **289/289 PASS**.
- B12 `run_all.py`: **PASS**; B11 original 14/14, B11 intent 14/14, B12 semantics 33/33, RM countdown 128 cases, RM underflow guard 65 cases.

## E v0.8.1 unchanged tests

The original E v0.8.1 test files were not edited. Run against C M4.2 via environment-root injection:

- 29 ordinary tests: PASS;
- `test_no_hardcoded_recursion_depth_limit`: **unexpected success**;
- `test_no_fuel_infinite_recursion_keeps_running_until_external_timeout`: **unexpected success**.

The unittest process therefore exits nonzero solely because its two `@expectedFailure` defect reproducers now succeed. E-FIND-021/022/024/025 ordinary regression tests remain PASS.
