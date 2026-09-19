# D2 Safe Patch Verification

Compiler baseline: 0.4.2-alpha.1 / A13+B12 current registry.

## D-PATCH-0002 — named act introduction
- Historical form יהי שם מעשה חיבור: 0 NamedActIdentity parses.
- Replacement יהי מעשה ושמו חיבור: exactly 1 NamedActIdentity parse.
- Status: SEMANTICALLY_CONFIRMED for the introduction itself.
- Caveat: the following historical body is not thereby repaired.

## D-PATCH-0003 — recurrence marker
- A complete minimal A13 program using וכן תעשה עד אשר compiled and ran normally.
- Test state changed from 2 to 0 by repeated natural decrement.
- Replacing the marker with וכן עשה caused PARSE0002.
- Status: SEMANTICALLY_CONFIRMED for the recurrence wording.
- Caveat: the Megillah's surrounding addition/update action still needs independent legalization.

## D-PATCH-0004 — explicit sequence
- A complete minimal A13 program using ואחרי כן compiled and ran normally.
- Two increments changed test state from 1 to 3.
- Replacing it with ואחר כן caused PROG0004 + PARSE0002.
- Status: SEMANTICALLY_CONFIRMED.

## D-PATCH-0001 — 5778
- Both canonical 5778 and canonical 5781 numeral spellings compile as direct literals, so this is not a grammar issue.
- A 5778 probe executes with value 5778; a 5781 probe executes with value 5781.
- The reason for changing the source remains algorithmic evidence: six maximum 963-day gate intervals equal 5778 and the same source repeats 5778 in the relevant bounds.
- Status remains MASTER_APPROVAL_REQUIRED because the value itself changes.
