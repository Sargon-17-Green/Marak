# C M4.1 — Implementation Status

**Status: COMPLETE for the requested C remediation scope; ready for Master/E review.**

Closed in C: E-FIND-021, 022, 023, 024 and 025. E-FIND-026 remains informational/watch only.

Final evidence:
- C: 242/242 tests + 126 subtests PASS;
- A13: 289/289 PASS;
- B12 `run_all.py`: PASS;
- E expected-failure reproducers 021–025: all 14 become unexpected successes without changing E tests/decorators;
- artifact fuzz: 2000 cases, no uncontrolled exceptions;
- generated property: 550 cases, no failures;
- generated RM corpus: 240 cases PASS;
- recursion: finite 10/100/250/300/1000 Normal in all three layers; depth 300 remains Normal with host recursion limit 80;
- relocation: PASS with original path absent;
- clean wheel install and CLI matrix: PASS;
- reproducible wheel SHA-256: `29f82d91ccdb19a15a354cce71f364b1c870f6fed6522647e6d497ed80de2623`.

The one ordinary failing E v0.8 assertion is an E-internal contradiction with E-FIND-021/B12 and is not resolved by reintroducing the prohibited serial leak.
