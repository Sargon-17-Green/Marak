# E v0.8.2 — Final C M4.2 Remediation Verification

## Verdict

**E v0.8.2 READY FOR MASTER M2 GATE REVIEW**.

E-FIND-023 and E-FIND-027 are CLOSED. E-FIND-021/022/024/025 remain CLOSED under regression smoke. E-FIND-026 remains INFORMATIONAL / WATCH.

All E-side M2 gates are READY. Final M2 declaration belongs to the Master.

## Key independent results

- C M4.2: 256 pytest tests + 126 subtests PASS.
- E v0.8.1 unchanged against C M4.2: 29 ordinary PASS; exactly the two historical E-FIND-023 `expectedFailure` reproducers became `unexpected success`.
- New E v0.8.2 resource verification: default active-performance budget is None in HAST reference, IR reference and portable backend.
- Finite recursion: 4,999 / 5,000 / 10,001 / 20,000 / **25,000** normal in all three layers with equal semantic observations.
- 20,001 sequential completed performances: normal.
- Python recursion limit 80: Marak depth 1,000 normal in all three layers.
- No-fuel infinite recursion: each layer remained running until E's external timeout.
- Explicit `max_active_performances=100`: caller-imposed tooling ResourceExhaustion; same source without budget is normal.
- Deep-completion activation counters returned to zero across repeated runs.
- A13 selftest: 289 PASS. B12 run_all: PASS.
- 021/022/024/025 + anti-imitation focused regression: 23 tests PASS.
- RM smoke: tiny RM differential PASS plus 23 generated machines against independent E RM interpreter.
- C M4.2 outer SHA ledger: 257/257 entries verified.
- canonical source-root metadata: Marak / marak / CLI marak / MIT / compiler 0.4.2-alpha.1; no stale inner handoff/checksum ledgers.
- wheel-only CLI version/check/compile/run/explain: PASS.
- source relocation with original source hidden: full 256 + 126 PASS.
- two fixed-epoch wheel builds: byte-identical.
