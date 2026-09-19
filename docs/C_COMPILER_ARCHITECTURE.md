# C Compiler Architecture

Status: A13/B12 Core implementation with C M4.2 adversarial remediation.

Pipeline:

`SourceText → normalization/source map → orthographic lexing → candidate morphology → ambiguity-preserving chart parse → typed resolution → validation → canonical HAST → canonical validated IR → identity optimizer → deterministic artifact → verifier → IR reference / portable backend`.

Compiler architecture may be conventional; language ontology is not inferred from it. Parser, resolver, HAST, IR, artifact and backend have explicit boundaries. Historical reference calculi are isolated under `compiler.reference_models` and canonical modules are statically forbidden from importing them.

Execution uses explicit implementation continuations/activations, with no default semantic depth quota. This implementation strategy does not introduce a Marak call stack, maximum recursion depth, exception model or performance-count observable.
