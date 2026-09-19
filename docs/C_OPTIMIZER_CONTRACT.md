# C Optimizer Contract

M4 uses an intentionally minimal optimizer. The current pass is `identity-preserve-observables` and returns the same validated IR object.

This is deliberate: optimization may not reorder effects, change explicit source sequence, move or erase a potentially failing computation, alter `ARITHMETIC_DOMAIN_ERROR` timing, change result provenance, or alter termination/divergence without a proof justified by B12 observability.

Future constant folding is permitted only when exact arithmetic, purity, semantic kind and error behavior are all proven preserved.
