# C M4.2 Handoff to E

C-side remediation is complete locally; E/Master determines gate status.

Recommended E v0.8.2 verification:

1. rerun the unchanged E v0.8.1 E-FIND-023 tests against this source;
2. expect the two former `@expectedFailure` reproducers to become unexpected successes;
3. verify defaults for all three execution APIs have no finite active-performance quota;
4. verify finite depth 5,000 and 10,001+ completes when actual resources permit;
5. verify no-fuel self recursion survives until external timeout, without `RecursionError` or fixed-quota result;
6. verify an explicitly supplied finite budget remains caller/tooling-only;
7. inspect canonical source root for E-FIND-027 cleanup;
8. smoke E-FIND-021/022/024/025 and tiny RM.

C evidence additionally tests depth 20,000 and 20,001 sequential performances. No Marak maximum depth is inferred from those finite test points.
