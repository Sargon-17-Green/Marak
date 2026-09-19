# E v0.8.2 Test and Evidence Index

## Reused / upstream
- C M4.2 full suite: 256 pytest tests + 126 subtests.
- A13 selftest: 289 checks.
- B12 run_all: full semantic suite plus 128 RM countdown and 65 DECJZ underflow-guard cases.
- E v0.8.1 unchanged: 31 methods; 29 ordinary PASS and two E-FIND-023 historical expected failures became unexpected successes.
- Focused v0.8.1 regression smoke for 021/022/024/025 + anti-imitation: 23/23 PASS.

## New E v0.8.2
- 12 independent executable test methods.
- finite recursion checked through depth 25,000 in all three execution layers.
- 20,001 sequential performance occurrences.
- three external-timeout no-fuel infinite-recursion probes.
- explicit caller budget and activation-cleanup probes.
- full 257-entry M4.2 outer checksum verification.
- source metadata/bootstrap-readiness checks.
- tiny RM three-layer differential.

## Generated / watch
- 23 small generated RM cases against E's independent RM interpreter.
- two completed 128-action parser-watch runs.
- two independent fixed-epoch wheel builds compared byte-for-byte.
