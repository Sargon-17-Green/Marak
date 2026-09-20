# C5.2 Handoff to Master

Baseline: `974ea3c2ec9474e9d6c5c4897970e69ed66de692`. Branch: `workstream-c/c5-2-symbol-index-ordering`. Draft PR: `#12`. Do not merge from this workstream; Master review is required.

Compiler candidate: `0.5.2-alpha.1`. HAST `core-hast-0.3-candidate-1`; IR `core-ir-0.3-candidate-1`; artifact `core-artifact-0.3-candidate-1`; registry `c5.2-a15-a16.1`. Language edition remains the pre-existing integration-candidate identifier by design.

Implemented end-to-end: finite Symbol domain/member declarations and counted labels; exact Symbol references; typed Symbol places/roles/outputs/immediate results; identity equality; explicit complete-chain order metadata; BidirectionalIndex literals and typed carriers; total Index successor/predecessor; Natural strict GT; and productive direct Naturals through 99,999,999.

Security/trust hardening includes canonical member-label verification, domain/member ownership checks, malformed Index rejection, typed proposition checks, Symbol-order integrity, duplicate identity rejection, and clean 0.2 artifact rejection.

## C5.2 remediation

Master finding `C5.2-MR-001` is remediated on implementation HEAD `51f302af95d0092e7a367b27af1d431090733f52` (previous blocked HEAD `dc6e8f8b8c3e78eb18607694ef51bd3765f06967`). The 30 corrupted Hebrew `message_he` literals in `compiler/resolve/a13_program.py` were restored without changing diagnostic codes, English meanings, trigger conditions, metadata, spans, or phase. `compiler/api.py` now reports `entry_is_surface_transition` as `ועתה`.

Regression coverage now locks the exact resolve explanation, statically inspects the C5.2 resolution diagnostics for stable codes and intact Hebrew, and rejects replacement-text corruption in compiler Python sources. The dedicated C5.2 Ubuntu/Windows matrix includes `tests/test_c5_2_scope_guard.py` and all required A13/B12/A15/B13/B14/A16/B15 regression gates.

Verification on PR CI run `35507259159`: full pytest **331 passed + 126 subtests passed**; C5.2 targeted suite **40 passed** on Ubuntu (job `106069069269`) and Windows (job `106069069325`); C5.1/artifact-IR regression, tooling portability, and proposal regressions all PASS. Registry regeneration is byte-identical with SHA-256 `2e1d5a8d685ca0f52c9a657cfd20a0594465c4cc5fa344bf55693a169c9a0483`.

Encoding audit of the full PR delta found no C5.2-added runs of three or more ASCII question marks, U+FFFD, mojibake markers, or UTF-8 decode failures after remediation. Pre-existing question-mark fixture strings in `tests/test_c5_1_domain_infrastructure.py` are byte-identical to the canonical baseline and were not modified as part of this finding.

Scope exclusions are preserved: no Collection operations, no Program Input source grammar, no general dynamic counted recurrence, and no Megillah candidate edits or compiler special cases.

Performance note: Natural-only compile smoke is slower than the C5.1 baseline on the measured Windows host; no arbitrary threshold was imposed. Treat this as a performance follow-up signal, not a semantic blocker.

C5.2 remains Draft and unmerged. Master must independently re-review the remediation HEAD before any merge decision.
