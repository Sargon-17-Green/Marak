# C M4.1 — Recursion Execution Model

Language recursion is no longer represented by recursive Python calls.

The HAST reference evaluator, canonical-IR reference evaluator and portable VM each execute acts with an explicit implementation work stack containing continuation records for sequence, conditional cleanup, finite recurrence, post-action recurrence and performance completion.

These records are **IMPLEMENTATION-ONLY**. They are not Marak-visible frames and do not define language stack semantics.

Verification:

- depths 10, 100, 250, 300 and 1000 complete normally in all layers;
- depth 300 still completes after compilation when Python `sys.setrecursionlimit(80)` is set;
- finite completion leaves `active_performances == 0`;
- fuel exhaustion remains `Divergence`, a harness observation;
- no-fuel infinite recursion reaches a separate implementation resource classification rather than `RecursionError` or a language Error.
