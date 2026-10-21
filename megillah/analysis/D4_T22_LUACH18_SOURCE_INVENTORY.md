# D4 T22 — Luach Eighteen / שנת חמשת אלפים — source inventory and first checkpoint

**STATUS: IN PROGRESS — NOT T22 PASS / NOT MASTER ACCEPTED.**

Starting accepted Workstream D HEAD:
`20e462bb3d470c6aff7717d4d9f3096b9ed333b9`.
Canonical `main`: `35e954d8c08da68a205cfea654b2597a4a77a714`.
PR #20 must stay Draft/open/unmerged. T23 NOT STARTED.

## Exact original source provenance

Normative source: `megillah/original/Megilat_HaItim_Yehuda_FINAL_2026-09-18.md`,
SHA-256 `7b834f4a444e021bb65164282b851af960a6dbc0be3d458c2412181773b9db7b`.

| Original line(s) | Required meaning |
| --- | --- |
| 1251 | Luach Eighteen heading, documentary |
| 1253–1255 | Year is (opening gate, closing gate]; opening gate belongs to previous year |
| 1257–1261 | Enumerate pairs containing the action day c: S < c <= E |
| 1263 | At least six adjacent gate-to-gate transitions, not six gate objects |
| 1265 | Duration >= 252 inclusive |
| 1267 | Duration <= **5781** inclusive |
| 1269–1273 | Retain every eligible pair; sort by (duration ascending, S ascending) |
| 1275 | 46 drops and six bowls with action day and question day both c |
| 1277 | Bowl 1, seal **10** |
| 1279 | Use the actual T20 unbiased choice over every ordered eligible year |
| 1281 | Full selected-year canonical name: `שנת חמשת אלפים מיום ברוא מפלצת הספגטי המעופפת שמים וארץ` |
| 1283 | Existence-proof heading belongs to T22 |
| 1285–1287 | Each gate gap 42..963, six-gap witness 252..5778 |
| 1289 | If c is a gate, choose E=c and S six preceding gates |
| 1291–1293 | If c is not a gate, choose immediate preceding S, then six following gates to E |
| 1295–1299 | Witness is admitted on every action day; not sole eligible pair |
| 1301 | Separator, documentary |
| **1303** | **Luach Nineteen begins — HARD STOP** |

### Explicit source discrepancy requiring T22-only repair

The untouched T21 candidate's documentary Luach Eighteen text currently
says **5778** at candidate line 614. This is the *six-gap witness maximum*,
not the *admissibility maximum* of **5781** in original line 1267.
The subsequent T22 source-level repair must distinguish these numbers.
This checkpoint deliberately leaves candidate bytes unchanged pending
an executable, source-conformant repair.

## Finite relevant search theorem

Let c be the (integer) action day and (S,E) a candidate year.
The source requires S < c <= E and 252 <= E-S <= 5781.

Therefore S >= c-5781 (because E >= c) and S <= c-1.
Likewise E <= S+5781 <= c+5780 and E >= c.
Hence it suffices to enumerate all consecutive gate positions inside
the proved corridor:

- S in [c-5781, c-1]
- E in [c, c+5780].

For each pair, retain the exact *global ordinal* number of gate transitions,
test >= 6, duration 252..5781, and order by (E-S, S). Every admissible
pair is in that corridor; no arbitrary number of gates or days is imposed.
When enumerating from the real unbounded stream, retain ordinal gate
coordinates so the step-count requirement is not lost.

### Existence witness

If c equals a gate, E=c and S is the sixth preceding gate.
Otherwise S is the immediate preceding gate and E the sixth successor of S.
Each of the six gaps lies in [42,963], hence the duration is in [252,5778],
which is within the broader admission interval [252,5781].
Both constructions satisfy S<c<=E. The witness proves the set nonempty;
it never permits discarding other eligible years.

## Independent, bounded finite-model tests

`tests/test_d4_t22_finite_year_model.py` is an independently written
finite gate oracle. It checks 10 cases (including exhaustive-vs-proved-corridor
comparisons with patterned and randomized gap sequences, exact gate-day
boundaries, six vs seven+ transitions, exact 252/5781/5782 bounds,
ties, and both constructive witnesses).

Local authoring check: `10 passed` (pytest). This is **not** production
HAST/IR/portable evidence and does not authorize a new intrinsic whitelist.
The model deliberately contains no T22 selected year, no fixed gate table,
and no oracle-fed production answer.

## Remaining mandatory T22 work — not yet completed

1. Source-level Marak repair for all Luach 18 semantics, retaining T21 machinery.
2. Correct counted SourceName for the ten-word canonical year name.
3. Real 46-drop/six-bowl query with c=t; bowl one/seal ten;
   actual T19 first-answer/direction and T20 unbiased selection.
4. Full candidate enumeration/order, three-runtime executable tests and
   independent oracle comparison.
5. Regressions T19–T21, D3+D4 on both operating systems, C5.7, full pytest.
6. Actual measured frontier to original Luach 19 line 1303, plus exact-head
   CI and Master handoff. Stop before T23.

The current T21-only constructive intrinsic whitelist remains fail-closed
for every new T22 program; it must not be expanded merely for performance.
