# D4 Test Evidence

Workstream: **D4 — Post-C5.5 Megillah Conformance**

Canonical baseline:
`main = 183410bc0300e496fd6fd7ba9ba73b4c6cb7b831`

Verified executable/evidence head:
`6a2bffcce5d390c47c524c7d06ce5429500a4a4c`

GitHub Actions run:
`35570493493`

Run URL:
`https://github.com/Sargon-17-Green/Marak/actions/runs/35570493493`

## Production identity observed

- package: `marak`
- version: `0.5.5a1` / compiler milestone C5.5
- current registry line: `c5.5-a15-b13.1`
- Python CI: 3.11
- no production compiler/runtime/spec file changed by D4

## Integrity

PASS:
- historical original SHA-256:
  `7b834f4a444e021bb65164282b851af960a6dbc0be3d458c2412181773b9db7b`
- D3 starting/final D4 candidate SHA-256:
  `afc6eda11a8d7f4b6499cf643d2ef5b36581bcad61b5fce761a7709274d2d643`
- D3 approved repairs retained
- D3 provenance inherited for every non-empty candidate line
- no invented `מספר יום` input surface in the candidate
- no stdin/argv transport convention inserted

## D3 + D4 targeted suite

Ubuntu:
`29 passed in 0.69s`

Windows:
PASS in the paired D4 job.

The 29 tests include the retained D3 regression suite plus D4 request-closure, domain, provenance, output-strategy and negative-source controls.

## D-LANGUAGE-REQUEST closure probes

### 001 — Symbol labels/order

Positive PASS:
- finite Symbol family;
- counted visible labels;
- declared total order;
- Symbol Collection sorting;
- HAST / IR reference / portable backend agree.

Negative PASS:
- a raw visible label such as `טין` is not itself a `SymbolValue`.

Disposition:
production capability verified; historical Megillah wording still requires structural repair.

### 002 — BidirectionalIndex

Positive PASS:
- predecessor crosses `AfterZero(1) -> Zero -> BeforeZero(1)`.

Negative PASS:
- historical alias `שנת חמשת אלפים` is not an admitted Index literal;
- canonical relative Index form is admitted.

Disposition:
production capability verified; historical year wording still requires canonicalization.

### 003 — finite ordered Collections

Positive PASS:
- immutable ordered Natural Collection;
- duplicate preservation;
- canonical ordering.

Negative PASS:
- bare untyped `ספר` is not a Collection value.

Disposition:
production capability verified; historical book prose still requires typed structural repair.

### 004 — Natural ordering

Positive PASS:
- canonical strict Natural proposition `A רב מן B` executes.

Negative PASS:
- historical `ימעט מן` form is not silently admitted as the canonical comparator.

Disposition:
production capability verified; occurrence-specific comparison repairs remain.

### 005 — productive large numerals

Positive PASS:
- direct Natural `14,777,149` is recognized exactly.

Negative PASS:
- historical `חמש ועשרים ומאה` for 125 is rejected;
- canonical direct Natural is `מאה ועשרים וחמשה`.

Disposition:
productive numeral capability verified; historical spellings remain occurrence-specific repairs.

### 006 — RepeatExactly

Positive PASS:
- literal count 127 executes exactly 127 repetitions;
- runtime count from a C5.5 Natural Program Input composes with C5.4;
- count is the accepted exact-count model.

Negative PASS:
- postposed historical `ACTION פעמים כמספר ...` is not silently accepted as canonical C5.4 syntax.

Disposition:
production capability verified; historical recurrence wording/body structure remains source repair.

### 007 — Program Input Roles

Positive PASS:
- two same-domain inputs bind by named identity, not position;
- reversing binding order is observationally identical;
- input reads are available to Preparation;
- invalid invocation is returned before Preparation.

Negative/domain PASS:
- production accepts BidirectionalIndex Program Input only through the year-typed surface;
- a fabricated `מספר יום` input head is rejected;
- candidate source explicitly states that chronological before/after cannot be recovered from Natural day numbers alone.

Disposition:
binding mechanism verified; faithful Megillah day-input source profile remains blocked by `D4-LANG-001`.

## Day/domain audit

The original source establishes:
1. one unique Natural number per day; and
2. a separate chronological before/after relation that is explicitly not inferable from those numbers alone.

Therefore:
- Natural-only Program Inputs are insufficient;
- Symbol is finite and unsuitable;
- Collection/pair encodings would be opaque source distortion;
- a year-typed Index spelling for a day is linguistically false;
- host date/datetime/timestamp is outside Marak semantics.

A15 explicitly says the semantic domain `BidirectionalIndex` is general but its source surface is intentionally year-typed, and that a generic source noun was deferred only because no independent source need then justified one. D4 supplies that independent need.

## Five-result strategy

PASS as a focused production proof without a tuple:
- year number: BidirectionalIndex;
- cutlet name: Symbol;
- day in cutlet: Natural;
- month name: Symbol;
- day in month: Natural.

All five heterogeneous retained facts coexist and are observed consistently by the three runtime paths in the standalone proof.

This is not whole-program algorithm equivalence.

## Current whole-candidate frontier

Measured by `tools/d4_frontier_probe.py`:

- candidate normalized tokens: **9,039**
- valid: **false**
- furthest normalized token: **105**
- candidate line: **11**
- mapped original line: **35**
- diagnostic: `PARSE0002`
- phase: `parse`
- additional whole-program diagnostic: `PROG0001`
- HAST reached: **no**
- IR reached: **no**
- artifact reached: **no**

First failing historical source begins:
`ותבחר מפלצת הספגטי המעופפת יום אחד ותקרא את שמו יום היסוד.`

No fake Preparation or unrelated downstream rewrite was inserted merely to advance this number.

## Full repository and regression evidence

Run `35570493493`:

- core/full pytest: **478 passed, 126 subtests passed**
- A13 selftest: **PASS**
- B12 semantics / run_all: **PASS**
- A15 surface reference suite: **PASS**
- B13 reference suite: **PASS**
- B14 integration suite: **PASS**
- A16 surface reference suite: **PASS**
- B15 reference/adequacy suite: **PASS**
- C5.1 Ubuntu: **PASS**
- C5.1 Windows: **PASS**
- C5.2 Ubuntu: **PASS**
- C5.2 Windows: **PASS**
- C5.3 Ubuntu: **PASS**
- C5.3 Windows: **PASS**
- C5.4 Ubuntu: **PASS**
- C5.4 Windows: **PASS**
- C5.5 Ubuntu: **PASS**
- C5.5 Windows: **PASS**
- D4 Ubuntu: **PASS**
- D4 Windows: **PASS**
- tooling portability Ubuntu: **PASS**
- tooling portability Windows: **PASS**

All 15 workflow jobs completed successfully.

## Scope conclusion

No `D4-C-*` compiler defect was established.

No new algorithm-changing source patch was made.

One new language-surface need is established:
`D4-LANG-001`.

D can continue independent analysis, but it cannot honestly move the production candidate through the current first frontier until Master routes that finding.

## Post-C5.6 continuation — T07 / Luach Five

GitHub Actions run `35607304124` verified the Luach Five repair on both dedicated D4 jobs.

- D3+D4 targeted suite: **47 passed** on Ubuntu; Windows dedicated D4 job also PASS.
- candidate SHA-256: `c150be620c995b517429805e9871c8d0418755932a90224a204b1e03e7e6fbc6`
- normalized tokens: **10,476**
- frontier token: **2,313**
- candidate line: **173**
- mapped original line: **197**
- next source blocker: `# לוח שש: הנותר ודבר שמור`
- original immutable SHA remains `7b834f4a444e021bb65164282b851af960a6dbc0be3d458c2412181773b9db7b`.

The full workflow is not a D4 gate: core/C5.6 still hit the frozen `D4-CONF-001` candidate receipt, and one Windows proposal-regression job also failed outside the dedicated D4 signal. Neither is repaired from Workstream D.

## Post-C5.6 continuation — T08 / Luach Six remainder

GitHub Actions run `35608830982` verified ordinary remainder and `שמור` on both dedicated D4 jobs.

- D3+D4 targeted suite: **51 passed** on Ubuntu; Windows dedicated D4 job also PASS.
- candidate SHA-256: `33f6956df02374db4a88465063d9e29ffb11c1f1a42130ec932638de3e6cf0ff`
- normalized tokens: **10,808**
- frontier token: **2,820**
- candidate line: **191**
- mapped original line: **229**
- next blocker: `## לקחת מספר מאחיו`
- original immutable SHA remains `7b834f4a444e021bb65164282b851af960a6dbc0be3d458c2412181773b9db7b`.

## Post-C5.6 continuation — T09 / Luach Six wrapped subtraction

GitHub Actions run `35609691265` verified wrapped sibling subtraction on both dedicated D4 jobs.

- D3+D4 targeted suite: **55 passed**.
- candidate SHA-256: `afe50064bf02d22969283fa0587264f87e0104d430c2f396239740512f232233`
- normalized tokens: **11,088**
- frontier token: **3,197**
- candidate line: **205**
- mapped original line: **243**
- next blocker: `## אם רב המספר מאד`
- original immutable SHA remains `7b834f4a444e021bb65164282b851af960a6dbc0be3d458c2412181773b9db7b`.

## Post-C5.6 continuation — T10A / Luach Three fast multiplication remediation

GitHub Actions run `35612611456` verified D4-PATCH-011 on both dedicated D4 jobs.

- D3+D4 targeted suite: **60 passed**.
- candidate SHA-256: `51b620c645c256fca805c16367e472bc0f5d5406bf6a7012bbaf7e2658013c09`
- normalized tokens: **12,087**
- frontier token: **4,311**
- candidate line: **216**
- mapped original line: **269**
- next blocker remained Luach Seven.
- the finite-fuel `2^127-1` multiplication regression completed normally on all three runtimes.

This closes `D4-SRC-001` without a compiler, runtime, language-surface, A17/B16, or C5.6 change.

## Post-C5.6 continuation — T11 / Luach Seven five stones

GitHub Actions run `35613420964` verified the complete five-stone table on both dedicated D4 jobs.

- D3+D4 targeted suite: **63 passed**.
- candidate SHA-256: `5cfc545b2203815b82054b745e5bdbeacd928a2e8f0d025ca892ad2eecba10be`
- normalized tokens: **13,209**
- frontier token: **5,723**
- candidate line: **243**
- mapped original line: **323**
- next blocker: `# לוח שמונה: שבע הטיפות הנסתרות`
- full 46-row × 5-stone table regression: PASS on HAST reference, IR reference and portable backend.
- exact last visible drop stones:
  `[73799454308499791987382386781055001470, 147925408106533232424672641008220632365, 94499522601819303005579577099149028685, 108473647672201258090947028490673028834, 137131922036975206684616468948804344042]`.

## Post-C5.6 continuation — T12 / Luach Eight hidden drops

GitHub Actions run `35615232527` verified Luach Eight on both dedicated D4 jobs.

- D3+D4 targeted suite: **66 passed**.
- candidate SHA-256: `e9550217dbd0dc6fbe949d51a9333eee6d7322cc373620f6190b82f3088888e8`
- normalized tokens: **16,458**
- frontier token: **9,473**
- candidate line: **282**
- mapped original line: **465**
- next blocker: `# לוח תשעה: עשיית שש וארבעים הטיפות`.
