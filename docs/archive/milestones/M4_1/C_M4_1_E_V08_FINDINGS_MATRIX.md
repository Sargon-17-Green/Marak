# C M4.1 — E v0.8 Findings Matrix

| Finding | Reproduced before | Fix | New regression | E v0.8 unchanged behavior after fix | Status |
|---|---|---|---|---|---|
| E-FIND-021 | yes | semantic observation quotient + separate debug-internal projection | `test_e_find_021_public_quotient_erases_serials_but_debug_retains_them` | finding reproducer becomes unexpected success; one non-expected-failure E test contains the opposite stale raw-serial assertion | CLOSED in C; E internal inconsistency documented |
| E-FIND-022 | yes | grammar-position root diagnostic | `test_e_find_022_name_slot_is_not_principal_marker` | unexpected success | CLOSED |
| E-FIND-023 | yes | iterative explicit continuations in HAST reference, IR reference and VM; resource boundary + CLI firewall | depth 300/1000, recursionlimit=80, no-fuel resource outcome | two reproducers become unexpected success | CLOSED |
| E-FIND-024 | yes, eight cases | shared `validate_canonical_ir` semantic pass in compiler and artifact verifier | all eight malformed-IR cases | eight unexpected successes | CLOSED |
| E-FIND-025 | yes | target-role descriptor/value-expression separation | caller-role product=5 + recursive role isolation | two unexpected successes | CLOSED |
| E-FIND-026 | informational | no semantic pruning | E parser-stress tool, 128 actions | PASS; 7607 state keys, unique parse | WATCH |
