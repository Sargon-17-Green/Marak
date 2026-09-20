# C5.2 Test Evidence

Remediation implementation HEAD: `51f302af95d0092e7a367b27af1d431090733f52`. Previous Master-blocked HEAD: `dc6e8f8b8c3e78eb18607694ef51bd3765f06967`.

GitHub Actions PR run `35507259159` reran the production compiler suite: **331 passed + 126 subtests passed**. The dedicated C5.2 suite, now including `tests/test_c5_2_scope_guard.py`, is **40 passed** on both Ubuntu (job `106069069269`) and Windows (job `106069069325`).

Independent/spec regression gates all pass in the C5.2 matrix on both operating systems: A13 289 checks; B12 integrated/intent/semantic/RM suites PASS; A15 335,280 case checks with all 9,999 A13 numerals and 75,000 random large samples; B13 28 tests; B14 22 tests; A16 2,548 checks (2,518 positive / 30 negative); B15 29 tests.

The C5.1 regression job also passes on Ubuntu and Windows, covering `tests/test_c5_1_domain_infrastructure.py`, `tests/test_m4_ir_artifact_backend.py`, and `tests/test_m4_occurrence_results.py`. The current construction-registry JSON regenerates byte-identically; both tooling jobs report SHA-256 `2e1d5a8d685ca0f52c9a657cfd20a0594465c4cc5fa344bf55693a169c9a0483`.

`C5.2-MR-001` is fixed: all 30 C5.2-added corrupted Hebrew diagnostic literals were restored, `entry_is_surface_transition` is exactly `ועתה`, and regression guards cover both. A full PR-delta encoding audit after remediation found no C5.2-added question-mark replacement runs, U+FFFD, mojibake markers, or UTF-8 decode failures. Question-mark fixture strings that remain in `tests/test_c5_1_domain_infrastructure.py` predate C5.2 and are byte-identical to baseline.

Performance smoke remains historical evidence and was not changed by this remediation: on the measured Windows/Python 3.11 host, C5.2 Natural-only compile median was 78.11 ms versus C5.1 54.92 ms (+42.2%); Natural-only run median 0.172 ms versus 0.160 ms (+7.1%). Representative compile medians: Symbol 146.54 ms; Index 101.20 ms; large-numeral 49.10 ms.

Machine-readable evidence is under `docs/compiler/evidence/`. PR #12 remains Draft and unmerged.
