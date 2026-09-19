# C M4.2 Execution Resource Model

Execution distinguishes four unrelated concepts:

1. **Marak semantics:** no fixed recursion/performance-depth limit in Core v0.1.
2. **Fuel:** explicit test/harness bound used to classify unfinished execution as Divergence.
3. **Caller-imposed active-performance budget:** optional implementation control (`max_active_performances=N`); absent by default and not language semantics.
4. **Actual host resource failure:** e.g. allocation/`MemoryError`; mapped to `IMPLEMENTATION_RESOURCE_EXHAUSTION`, outside Marak Error values.

The internal activation/continuation list and active-performance count are implementation/debug state only. They are not language-observable and do not establish stack-frame semantics.
