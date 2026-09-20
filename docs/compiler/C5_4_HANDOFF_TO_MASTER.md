C5.4-MR-001 REMEDIATION READY FOR MASTER RE-REVIEW

baseline:
`a63acfb52b73357bbbf42d1df4d49d068f8f7f51`

branch:
`workstream-c/c5-4-exact-counted-recurrence`

PR:
#14 — Draft, open, unmerged

previous blocked HEAD:
`fda669946081dc2d0919ce189c0ffdc5ded55d21`

remediation code commit:
`cd34efdf0bf2d05c0e135addc6d1af8c5b1d2d12`

remediation review HEAD:
Use the branch HEAD containing this document. The final delivery records the exact SHA after documentation-only CI verification.

finding:
`C5.4-MR-001`

root cause:
The resolver passed enclosing-sequence `recent_act` into recurrence bodies, while B12, canonical IR validation, and all runtimes define recurrence entry as a fresh immediate-result-provenance boundary for the body.

production changes:
Only `compiler/resolve/a13_program.py` changed in production. RepeatExactly, historical fixed counted recurrence, and post-action recurrence now lower their repeated action with `recent_act=None`. Dynamic RepeatExactly count lowering still receives incoming `recent_act`. Post-action proposition lowering still receives only provenance freshly produced by its repeated Perform.

count incoming-provenance behavior:
Preserved. A dynamic count may use the structurally immediate result of the preceding Perform and is evaluated once at recurrence entry.

body provenance behavior:
Corrected. Iteration 1 and all later iterations do not inherit provenance from before the recurrence.

post-action recurrence behavior:
Corrected/aligned. The repeated action starts without incoming provenance; after it completes, the proposition may observe only provenance created by that repeated action itself.

negative source reproducer:
PASS — a prior producing Perform followed by RepeatExactly whose body reads that prior immediate result is rejected statically with `REF0112`.

positive count-provenance test:
PASS — a prior Perform produces Natural 3, the dynamic count reads that immediate result, and a provenance-independent body executes exactly three times.

first-iteration provenance test:
PASS — the same prior immediate result can be valid for dynamic count selection but is rejected with `REF0112` when reused inside iteration 1.

canonical-validation agreement test:
PASS — invalid recurrence-body provenance is rejected by `check()`/resolver; the valid dynamic-count counterpart compiles and passes `validate_canonical_ir()`.

targeted C5.4:
PASS — 41/41 on Ubuntu and Windows in run #211.

full pytest:
PASS — 417 passed + 126 subtests on Ubuntu and Windows in run #211.

C5.1:
PASS — Ubuntu and Windows in run #211.

C5.2:
PASS — Ubuntu and Windows in run #211.

C5.3:
PASS — Ubuntu and Windows in run #211.

A13/B12/A15/B13/B14/A16/B15:
PASS — A13 289; B12 33 + RM witness; A15 335,280 with 9,999 frozen A13 numerals; B13 28; B14 22; A16 2,548; B15 29.

Ubuntu CI:
PASS — C5.4 targeted 41, full 417 + 126 subtests, proposal regressions, 4096 resource sanity, regeneration, and committed-byte verification.

Windows CI:
PASS — C5.4 targeted 41, full 417 + 126 subtests, proposal regressions, 4096 resource sanity, regeneration, and committed-byte verification.

registry regeneration:
PASS cross-host; SHA-256 `cef84d06ff6f3f1a9212e812ceb3a8326c3687f75d0c7da093ed782febdb28af`.

canonical artifact regeneration:
PASS cross-host; all nine hashes are unchanged and identical on Ubuntu/Windows; committed-byte diff is clean.

scope confirmation:
No Program Input, C5.5, Megillah change, iterator/cursor, loop index, generic while/for, implicit output collection, recurrence semantic cap, language-edition change, or reopening of C5.1–C5.3. No runtime/artifact semantic workaround was added.

known issues:
No known blocker remains from C5.4-MR-001 on the workstream side. Independent Master re-review is still required. PR #14 remains Draft/open/unmerged; this document does not claim MASTER ACCEPTED.
