# B13 Reference / Property Test Results

The reference model is evidence only; normative semantics are the prose/laws in B13 documents.

## Result
- B13 reference/property tests: **28/28 PASS** locally and again on the authorized Windows checkout.
- Frozen B12 `spec/semantics/run_all.py`: **PASS unchanged** on the same Windows checkout.
  - B11 original integration suite: 14/14, plus 324 RM grid cases.
  - B11 intent regression under B12: 14/14.
  - B12 semantic suite: 33/33.
  - B12 RM witness: 128 countdown cases + 65 underflow-guard cases.
- Index successor/predecessor inverse grid: -300..300.
- Index order/distance cross-product: 101×101 pairs.
- Natural ordering includes magnitudes beyond 2000 decimal digits.
- Collection ordering checks every permutation of three distinct Naturals.
- Counted recurrence checks N=0, N=1, N=10,000, count evaluation once, error boundary, output event order, and wrong-domain count.
- Program input binding checks order independence, missing/extra/duplicate bindings, domain mismatch, and immutable association.
- Large-Natural test uses an exact value above 10^5000 without relying on host string conversion.

## Host leakage finding
An earlier draft test attempted Python integer→string conversion for a 5001-digit Natural and encountered Python's configurable digit-conversion safety limit. B13 explicitly rejected that host limit as semantic evidence and changed the test to compare the mathematical integer exactly instead. No Marak magnitude ceiling was introduced.

## Logs
- `test_logs/B13_REFERENCE_TESTS.log` — original reference run.
- `test_logs/B13_WINDOWS_REFERENCE.log` — independent run from the repository checkout.
- `test_logs/B12_FROZEN_REGRESSION_WINDOWS.log` — frozen B12 compatibility regression.
