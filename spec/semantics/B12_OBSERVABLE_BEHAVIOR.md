# B12 Observable Behavior

For B-Core v0.1, semantic observation includes only language-defined effects/outcomes:

1. normal completion vs defined runtime error vs divergence;
2. final current numeric facts of source state-bearing places for terminating/error outcomes;
3. explicitly produced act outputs and their defined provenance semantics;
4. the stable runtime error category when execution errors.

Not observable:
- backend register allocation;
- memory addresses;
- stack depth;
- stack frame identity;
- instruction count;
- optimizer steps;
- hidden counters;
- internal event trace;
- Python/JS/C exception classes;
- symbol table indices.

## Trace

Internal trace is:

**RUNTIME_INTERNAL**

and non-observable in Core v0.1.

A runtime may collect trace for debugging.

An optimizer need preserve:
- state;
- outputs;
- error/divergence;
- source-defined order where observable,

but need not preserve internal diagnostic event count/order when those do not alter observable behavior.

No Core program can read the trace.

`explain` or compiler diagnostics are tooling, not program-visible trace introspection.

## Outputs are not stdout

The act-output model is a language semantic product/provenance relation.

B12 does not equate it with terminal output or a file descriptor.
