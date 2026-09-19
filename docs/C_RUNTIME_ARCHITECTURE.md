# C Runtime Architecture

C separates three execution roles:

1. HAST reference semantics (`compiler.runtime.reference`);
2. canonical-IR reference semantics (`compiler.runtime.ir_reference`);
3. portable IR backend (`compiler.backend.portable`).

Core outcomes are Normal, Error and Divergence. Fuel is an explicit test/harness mechanism only and never a Core error.

Act recursion is implemented with explicit internal activations/continuations. These are `IMPLEMENTATION_ONLY`; they do not establish a user-visible Marak call-stack ontology. The default execution path has **no artificial active-performance or recursion-depth ceiling**. `max_active_performances=N` is an optional caller-imposed harness/resource control; its exhaustion is an implementation/tooling boundary, not a Marak semantic rule. Actual host allocation/resource failure is mapped to `IMPLEMENTATION_RESOURCE_EXHAUSTION` and is likewise not a language value or catchable Core error.

State is represented semantically as current facts attached to resolved Place identities. Initial establishment is distinct from later replacement. Role values are immutable associations local to one performance occurrence. Result products are occurrence-provenanced and are not stdout. Active-performance counters and allocation serials are debug/internal data only.

No language-level exception stack, exit code, Unit result, main return, HALT primitive or global last-result register exists.
