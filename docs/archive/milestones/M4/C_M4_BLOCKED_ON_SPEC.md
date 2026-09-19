# C M4 — Blocked on Spec

**No known A13/B12 semantic or surface blocker remains for the implemented Core v0.1 path.**

The M3 blockers for whitespace, whole-program root, `ועתה`, visibility/lifetime, source introduction-before-use, cessation/HALT and signed-subtraction ambiguity are closed by A13/B12 and implemented in M4.

Deferred, explicitly out-of-Core questions remain for future work only: strings, comments/headings semantics, signed integers, exceptions, modules/imports, collections/records/maps, floating point, concurrency/async, FFI and reflection. C M4 does not invent rules for them.

If later Master review finds a contradiction, it should receive a new `C-BLOCK-...` reproducer rather than retroactively reopening the resolved M3 entries.
