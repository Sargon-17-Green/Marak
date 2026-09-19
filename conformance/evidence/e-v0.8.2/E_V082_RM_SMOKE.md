# RM / Universality Regression Smoke

- A13 tiny RM compiled and executed as Normal in HAST reference, IR reference and portable backend; semantic observations matched and projected registers ended at zero.
- Independent E generated RM smoke: **23/23 PASS** (5 countdown, 5 addition, 5 branch, 5 random-forward, 3 divergence) against the independent E RM interpreter.
- B12 run_all independently rerun: 128 RM countdown cases PASS and 65 DECJZ underflow-guard cases PASS.

M4.2's resource-model change therefore did not break the existing M1 universality witness.
