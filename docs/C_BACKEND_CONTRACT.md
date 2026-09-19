# C Backend Contract

The portable backend consumes canonical validated IR only. It never parses Hebrew and never resolves names.

Backend version: `portable-ir-vm-0.1-candidate-3`.

The backend uses an iterative execution loop with explicit continuation records and occurrence records. These are implementation-only. They do not imply user-visible variables, stack frames, positional arguments, `while`, `return`, `main` or HALT.

By default the backend has no artificial active-performance/depth quota. An optional `max_active_performances=N` argument is a caller-imposed harness control only. Actual `MemoryError`/host resource exhaustion is translated to an implementation-resource outcome rather than a Marak language Error. Fuel remains a separate nontermination harness mechanism and yields Divergence when exhausted.

The backend implements exact Natural arithmetic with checked subtraction, B12 effect boundaries, explicit sequence, conditional selection, recurrence checkpoints, occurrence-specific role association, nonterminal output production, immediate provenance and Normal/Error/Divergence outcomes.

Differential tests compare it against both HAST and canonical-IR reference evaluators through an implementation-erased semantic observation quotient.
