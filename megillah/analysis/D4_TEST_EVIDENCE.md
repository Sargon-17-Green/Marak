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

## Post-C5.6 continuation — T13 / Luach Nine visible drops

GitHub Actions run `35615872737` verified Luach Nine on both dedicated D4 jobs.

- D3+D4 targeted suite: **68 passed**.
- candidate SHA-256: `955654dc6a57dfb9a358c57e76013afcc1c38bd09f64bacb450920e08b75dead`
- normalized tokens: **21,267**
- frontier token: **14,819**
- candidate line: **323**
- mapped original line: **595**
- next blocker: `# לוח עשרה: שש הקערות`.

## Post-C5.6 continuation — T14 / Luach Ten bowl initialization

GitHub Actions run `35616748974`: dedicated D4 Ubuntu+Windows PASS, **70 targeted tests**. Candidate SHA `cb69ee3c354344a75e3f641e6e8272cd04428af272084d6a7b175481522ebdbd`; normalized tokens 22,277; frontier token 16,012; candidate line 335; mapped original line 641.

## Post-C5.6 continuation — T15 / Luach Eleven arrangements

GitHub Actions run `35619093303`: dedicated D4 Ubuntu+Windows PASS, **74 targeted tests**. Candidate SHA `d3a3e99e6d4e8f40fc288e7b495ec7457d64f3cf0626210c2060bf9ee64c8985`; normalized tokens 24,666; frontier token 18,889; candidate line 392.

## Post-C5.6 continuation — T16 / Luach Twelve pours

GitHub Actions run `35620151386`: dedicated D4 Ubuntu+Windows PASS, **76 targeted tests**. Candidate SHA `6c6eb53613f9fc21c4428bb5f7883aabb1c968de88c7b170e4731359ed21a7c3`; normalized tokens 25,826; frontier token 20,196; candidate line 414.

## Post-C5.7 reconciliation — T17 / Luach Thirteen

Canonical main: `800a75914c2e3510fb51dacf2d193a283c11d467`.
The existing D history was preserved by merging canonical main into the existing D branch; no D commit was rebased, squashed, dropped, or rewritten. The reconciliation merge commit has parents historical T17 HEAD `3edae43158a8e15d03d293fcb38cc3e225b80fa0` and canonical main.

C5.7 production/compatibility verification:
- `tests/test_c5_7_multiword_source_names.py` + frozen D3/D4 compatibility tests: **47 passed in 1.22s**.
- compiler baseline: `0.5.7-alpha.1`; registry: `c5.7-a18-b17.1`.
- `D4-LANG-002` is closed by A18 -> B17 -> C5.7.

Historical T17 synthetic `PARSE0002` classification: **TEST_FIXTURE_DEFECT**.
The synthetic arrangement literal supplied six Natural values but contained only five append wrappers. A minimal isolation reproduced `PARSE0002` with expected `word:תחת`; the equivalent six-wrapper Collection parses through the Collection expression. The fixture was corrected by adding the missing append wrapper. No compiler, specification, or language finding is opened.

T17 targeted verification after the fixture correction:
- Luach 13 three-runtime snapshot-mix test + structural snapshot/commit/exact-46-driver test: **2 passed, 47 deselected in 73.52s**.
- no T17 multi-word source identity required conversion; no global unwelding was performed.

Real canonical-candidate measurement:
- candidate SHA-256: `4c003673d46f25547465062d1e6c538981a913d28d37f98a27d9cd2f28b80383`
- original SHA-256: `7b834f4a444e021bb65164282b851af960a6dbc0be3d458c2412181773b9db7b`
- normalized tokens: **29,824**
- frontier token: **24,481**
- candidate line: **447**
- mapped original line: **831**
- next blocker: Luach Fourteen.
- `23,221` remains synthetic-fixture history only and is not a candidate frontier.

Full local acceptance gates and Ubuntu/Windows D4 CI are recorded separately before Master handoff.

Full local pytest after the T17 fixture repair:
- `python -m pytest -q`: **609 passed, 126 subtests passed, 1 failed** in 539.84s.
- sole failure: `tests/test_c5_6_negative_scope.py::test_c56_preserves_frozen_d4_candidate_hash_and_frontier`.
- classification: existing `D4-CONF-001` stale C5.6 conformance receipt. It hard-codes pre-D4 candidate SHA `afc6eda11a8d7f4b6499cf643d2ef5b36581bcad61b5fce761a7709274d2d643` and therefore rejects current authorized D candidate SHA `4c003673d46f25547465062d1e6c538981a913d28d37f98a27d9cd2f28b80383`.
- D4 did not edit the frozen C5.6 test. No second full-suite failure occurred.

## Post-C5.7 T17 CI receipt

GitHub Actions run `37107450941` on branch head `fd851745090839e1ea68f71edd5a29a809c94cf0`:
- D4 Megillah conformance Windows: **78 passed in 195.14s**.
- D4 Megillah conformance Ubuntu: **78 passed in 222.25s**.
- both jobs verified original SHA-256 `7b834f4a444e021bb65164282b851af960a6dbc0be3d458c2412181773b9db7b`.
- both jobs measured candidate SHA-256 `4c003673d46f25547465062d1e6c538981a913d28d37f98a27d9cd2f28b80383`, normalized tokens **29,824**, and real candidate frontier **24,481**.
- T17 therefore reaches the Luach Fourteen boundary consistently on Ubuntu and Windows.


## Post-C5.7 continuation - T18 / Luach Fourteen

Starting checkpoint: T17 head `339d0daa62951c3a934f2a21f5046da4d06c04b0`; reconstructed T17 D3+D4 targeted suite: 78 passed and frontier 24,481 before T18 edits.

Before final T18 acceptance, canonical main advanced to `35e954d8c08da68a205cfea654b2597a4a77a714` by merging C5.6 conformance-receipt maintenance. T18 was reconciled by merge commit `29db3eecb784e78f962fe9376dc8c4d2f0248dcf` (parents T18 `9b3a8ab189454b02053c9c7503e01e043b7ec818` and canonical main). The maintenance freezes the historical C5.6 D4 candidate in its own fixture and removes dependence on live downstream D candidate bytes; this closes the previously known nonsemantic `D4-CONF-001` stale-receipt failure without changing D4 candidate semantics.

Authorized source span: original lines 831–891, with line 831 classified documentary and executable semantics drawn from lines 833–891 only. Luach Fifteen begins at original line 895 and is outside T18.

T18 local acceptance on the final candidate:
- Luach Fourteen focused suite: **6 passed, 49 deselected in 115.50s**.
- one complete post-drop blend: HAST reference = IR reference = portable backend, with fixed receipt `[3565, 3740, 5518, 1695, 8365, 7674]` from initial fills `[1,2,3,4,5,6]`;
- first arrangement receipt: `[2,4,1,3,6,5]`;
- the complete 12-blend driver passes on all three runtimes and returned the same fixed final receipt as the independent oracle;
- exact source-declared multi-word identity `מספר שש הקערות` resolves through C5.7 counted SourceName; no welded alias is introduced;
- snapshot-before-compute and simultaneous identity-keyed commit are structurally enforced;
- `גמר` resets the round counter and contains exact feminine-count `שתים עשרה פעמים` recurrence;
- large arrangement selectors are reduced with the source-authorized Luach Six short route `נותרמהר` modulo 720 before direct `מצאמערכה`; a structural regression forbids T18 from returning to the linear `בחרמערכה` path;
- an independent oracle over the source formula fixes the round-12 final bowl receipt as `[36108001607085984155684996137766958104, 148814309144118602128584347831122254145, 146577346212655508303902655220312506515, 113571227321377053045622633394311758065, 156703568566579726750728213438464676042, 87934172320087745809620382672045550969]`;
- T18 does not write `מערכתטיפהאחרונה`; the visible-drop-46 arrangement remains retained for Luach Fifteen.

The source basis for the fast modulo is original Luach Six lines 243–263: for a very large number, use the doubling/decomposition short route instead of repeated subtraction; the source explicitly states that the short route yields the same number as the long route. This resolves the earlier >20-minute exploratory runtime without changing the T18 algorithm or any result.

Real candidate measurement after the final fast-720 source repair:
- candidate SHA-256: `b8df350336aafb21c15b749349b60d97276b8dc6e4b8c940b30451220c445124`
- original SHA-256: `7b834f4a444e021bb65164282b851af960a6dbc0be3d458c2412181773b9db7b`
- normalized tokens: **33,492**
- frontier token: **28,438**
- candidate line: **466**
- mapped original line: **895**
- next blocker: Luach Fifteen.

Final local regression on the cleaned final tree: **84 D3+D4 targeted tests passed in 404.03s**. C5.7 multi-word source-name suite: **18 passed in 0.85s**. Dedicated Ubuntu/Windows D4 CI remains pending.

Full local pytest after reconciliation onto canonical main `35e954d8c08da68a205cfea654b2597a4a77a714`: **618 passed, 126 subtests passed in 504.89s**. The prior frozen-receipt failure no longer occurs; C5.6 now verifies its own historical fixture independently of the live D candidate.
