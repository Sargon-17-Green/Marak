# C M4.1 — Root Diagnostic Fix

M4 counted normalized tokens equal to `ועתה`, so a legal name-slot spelling could be miscounted as a principal transition.

M4.1 derives candidate root transitions from whole-program grammar positions. A `ועתה` occurrence counts only when its prefix is empty/preparatory and the relevant program slice has the required grammatical category.

Thus an Act named `ועתה` with no principal transition is rejected as zero principal markers (`PROG0001`), not multiple markers.
