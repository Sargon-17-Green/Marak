# C5.2 Test Evidence

Local production compiler suite: **329 passed + 126 subtests passed**. C5.2 targeted suite: **38 passed**.

Independent/spec regression gates all pass: A13 289 checks; B12 integrated/intent/semantic/RM suites PASS; A15 335,280 case checks with all 9,999 A13 numerals and 75,000 random large samples; B13 28 tests; B14 22 tests; A16 2,548 checks (2,518 positive / 30 negative); B15 29 tests.

The current construction-registry JSON regenerates byte-identically with SHA-256 `2e1d5a8d685ca0f52c9a657cfd20a0594465c4cc5fa344bf55693a169c9a0483`. Windows canonical artifact hashes are committed as portability assertions and the CI matrix reruns them on Ubuntu and Windows.

Performance smoke uses no pass/fail threshold. On the measured Windows/Python 3.11 host, C5.2 Natural-only compile median is 78.11 ms versus C5.1 54.92 ms (+42.2%). Natural-only run median is 0.172 ms versus 0.160 ms (+7.1%). Representative compile medians: Symbol 146.54 ms; Index 101.20 ms; large-numeral 49.10 ms. The compile delta is recorded as a follow-up optimization signal, not hidden behind an arbitrary threshold.

Machine-readable evidence is under `docs/compiler/evidence/`.
