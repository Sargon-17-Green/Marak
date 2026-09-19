# C M4.1 — E v0.8 Unchanged Rerun

The original E v0.8 test files and expected-failure decorators were not edited.

Direct unchanged-test discovery against the M4.1 implementation produces **14 unexpected successes**: all expected-failure reproducers for E-FIND-021 through E-FIND-025 no longer reproduce their defect.

One ordinary E v0.8 test still fails: `test_occurrence_serial_renaming_not_language_datum`. Its title/comment and E-FIND-021 say occurrence serial is not language data, but its final assertion expects `backend_observable` to differ when only occurrence serial changes. That assertion conflicts with the finding and B12. C intentionally keeps the serial-invariant public quotient and exposes raw occurrence IDs only through the debug-internal API.

This document does not declare E green; E/Master owns gate interpretation.

A shadow runner was also made from the authoritative E v0.8 package by replacing **only** its tested `inputs/C_M4_HANDOFF.zip` slot with the M4.1 implementation. `run_v08.py`, all tests, and all E tool Python files remained byte-identical (18/18 files by SHA-256). Running the unchanged `run_v08.py` produced the same 14 unexpected successes plus the one contradictory ordinary assertion described above.
