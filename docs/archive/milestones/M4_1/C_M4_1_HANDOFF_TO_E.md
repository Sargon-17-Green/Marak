# C M4.1 — Handoff to E

Please retest the unchanged A13/B12 conformance surface against this C M4.1 package. In particular rerun the original E-FIND-021..025 reproducers and independent artifact fuzzing.

Expected remediation behavior:

- finite recursion depth 300 and 1000 completes without host-stack semantics;
- public CLI has no default Python traceback leakage;
- all eight E-FIND-024 malformed artifacts are rejected;
- caller-role to callee-role source returns product 5;
- recursive role values remain occurrence-local;
- `backend_observable` is allocation/occurrence-serial invariant;
- raw serials are available only from debug-internal projections;
- Act name `ועתה` does not count as a root marker.

E v0.8 itself was not weakened or rewritten by C.
