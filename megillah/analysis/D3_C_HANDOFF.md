# D3 Handoff to Workstream C

## Existing finding carried from D2
D-C-FIND-001 — TOOLING_PORTABILITY

Observed on Windows:
1. tools/dump_current_registry.py / its test compares path text using a forward-slash suffix while Windows reports backslashes.
2. Path.write_text newline translation can write CURRENT_CONSTRUCTION_REGISTRY.json with CRLF, breaking byte-equality against the LF A13 snapshot.

## D3 reproduction
Full local pytest after adding the D3 tests:
- 261 passed;
- 2 failed;
- 126 subtests passed.

The two failures are exactly:
- tests/test_current_registry_tool.py::CurrentRegistryToolTests::test_dump_current_registry_targets_current_file_and_preserves_a3_snapshot
- tests/test_m4_static_audit.py::M4StaticAuditTests::test_historical_registry_snapshots_are_distinct_from_new_current_snapshot

A13 selftest: 289 checks PASS.
B12 semantic run_all: PASS.
D3 targeted tests: 7/7 PASS.

The registry file modified by the reproducer was restored from Git before D3 commit.

## D3 compiler status
No new semantic C bug was found.

The current candidate frontier, PARSE0002 at token 105, is consistent with current A13 grammar: the failing historical day-valued construction is not claimed to be valid Core.

D does not modify compiler/tooling code. C may fix D-C-FIND-001 independently.
