# D2 Compiler Bugs / Tooling Findings

## D-C-FIND-001 — TOOLING_PORTABILITY
Environment: Windows 10/11, Python 3.11, compiler 0.4.2-alpha.1, main 8a3a25e2fb5e438b01fef9694570f20d16a34ff3

Observed:
- pytest: 254 passed, 2 failed, 126 subtests passed
- dump_current_registry.py prints a backslash path while test asserts a forward-slash suffix
- Path.write_text newline translation rewrites CURRENT_CONSTRUCTION_REGISTRY.json as CRLF, breaking byte-equality against LF A13 snapshot

Expected: Repository CI/tooling should be host-portable or explicitly normalize paths/newlines.
Minimal reproducer: `python tools/dump_current_registry.py; then run tests/test_current_registry_tool.py and tests/test_m4_static_audit.py on Windows`
Semantic impact: none observed; A13 selftest 289 checks PASS and B12 run_all PASS
Action: Report to C; do not modify compiler from Workstream D.

Counted as a Marak semantic compiler bug: **NO**. No valid-source semantic miscompile was found in D2.
