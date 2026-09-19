# C M4 — Reference / Backend Equivalence

M4 has three independently useful execution layers:

1. HAST semantic reference evaluator;
2. canonical-IR reference evaluator (`core-ir-reference-0.1-candidate-1`), consuming IR only;
3. portable IR VM backend (`portable-ir-vm-0.1-candidate-1`).

All are projected onto the same B12-observable contract: state facts, defined occurrence products/provenance, and `Normal/Error/Divergence`. Internal stack depth, Python classes, trace events and registers are erased.

Differential tests cover A13 positive programs, the tiny RM, role-association permutation, exact arithmetic, checked underflow, conditional laziness, explicit sequence, recurrence, recursive acts, nonterminal output, immediate-result consumption and harness divergence.

The canonical IR reference evaluator is not implemented by invoking the portable VM, so agreement is meaningful rather than tautological.
