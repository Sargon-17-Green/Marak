# A14 Verification Log

- A14 direct surface checks: 302/302 PASS.
- Negative fixtures: 24.
- Ambiguity-focus fixtures: 4.
- Numeral collision-generation checks: 300,000.
- Repeat-count collision-generation checks: 300,000.
- Megillah numeral-bearing lines: 453.
- Megillah `פעמים` tokens: 96 on 92 lines.
- Repository regression on Windows: 262 passed, 126 subtests passed, 2 known baseline portability tests deselected.

Deselected baseline-only tests:
1. `tests/test_current_registry_tool.py::CurrentRegistryToolTests::test_dump_current_registry_targets_current_file_and_preserves_a3_snapshot`
2. `tests/test_m4_static_audit.py::M4StaticAuditTests::test_historical_registry_snapshots_are_distinct_from_new_current_snapshot`

A14 does not modify the affected tooling/registry files.
