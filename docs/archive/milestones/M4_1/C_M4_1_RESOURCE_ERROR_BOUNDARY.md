# C M4.1 — Resource / Host Failure Boundary

`IMPLEMENTATION_RESOURCE_EXHAUSTION` is tooling/runtime infrastructure status. It is not a Core value, product or language runtime Error.

The three execution layers convert host `MemoryError`/`RecursionError` resource failures at their execution boundary to resource-exhaustion outcomes. The public `run_source` API also maps unexpected execution-host exceptions to `IMPLEMENTATION_INTERNAL_FAILURE` rather than a Marak Error.

The CLI renders infrastructure status separately and exits nonzero as a tooling convention. It emits no Python traceback by default. The Marak language has no process exit-code value.
