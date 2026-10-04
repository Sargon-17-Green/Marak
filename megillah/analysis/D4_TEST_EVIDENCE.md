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

Before final T18 acceptance, canonical main advanced to `35e954d8c08da68a205cfea654b2597a4a77a714` by merging C5.6 conformance-receipt maintenance. T18 was reconciled by merge commit `145fdbd8d584ddeef9424e65d480986ae39af593` (parents T18 `109f85f3418b6a49776eb32a253f070602318fd3` and canonical main). The maintenance freezes the historical C5.6 D4 candidate in its own fixture and removes dependence on live downstream D candidate bytes; this closes the previously known nonsemantic `D4-CONF-001` stale-receipt failure without changing D4 candidate semantics.

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
- candidate SHA-256: `f55785a16a659c2c4423a255da051bb1f16481280519596011c1537b7d6e46ec`
- original SHA-256: `7b834f4a444e021bb65164282b851af960a6dbc0be3d458c2412181773b9db7b`
- normalized tokens: **33,492**
- frontier token: **28,438**
- candidate line: **466**
- mapped original line: **895**
- next blocker: Luach Fifteen.

Final local regression on the cleaned final tree: **84 D3+D4 targeted tests passed in 404.03s**. C5.7 multi-word source-name suite: **18 passed in 0.85s**. GitHub Actions run `37133055384` then verified the final branch head on both dedicated D4 jobs: Ubuntu **84 passed in 230.35s** and Windows **84 passed in 281.47s**. Both jobs measured canonical Git candidate SHA `f55785a16a659c2c4423a255da051bb1f16481280519596011c1537b7d6e46ec`, original SHA `7b834f4a444e021bb65164282b851af960a6dbc0be3d458c2412181773b9db7b`, normalized tokens **33,492**, and frontier **28,438** at candidate line **466** / mapped original line **895**. The earlier local Windows worktree SHA `b8df350336aafb21c15b749349b60d97276b8dc6e4b8c940b30451220c445124` was the same candidate after CRLF checkout conversion; converting CRLF back to LF yields the canonical Git/CI SHA.

Full local pytest after reconciliation onto canonical main `35e954d8c08da68a205cfea654b2597a4a77a714`: **618 passed, 126 subtests passed in 504.89s**. The prior frozen-receipt failure no longer occurs; C5.6 now verifies its own historical fixture independently of the live D candidate.

## Canonical source-name cleanup after accepted T18

Starting accepted checkpoint: T18 HEAD 5f35e8cb9b8d4c16db1797c4832c6300791dc2c1, candidate SHA f55785a16a659c2c4423a255da051bb1f16481280519596011c1537b7d6e46ec, frontier 28,438 at candidate line 466 / original line 895.

Inventory and migration:
- total source-declared identity instances: 261;
- Acts 72, Places 87, Roles 100, Program Inputs 2, Symbol Domains 0, Symbol Members 0;
- artificially welded identity instances: 173, representing 158 distinct spellings;
- genuine single-word identities: 87;
- already-canonical multi-word identities: 1;
- uncertain identities: 0;
- welded aliases retained: NONE;
- semantic identity families added: NONE;
- compiler / grammar / algorithm changes: NONE.

Live anti-weld regression: 4 passed. It checks only the verified inventory of removed spellings and does not implement a Hebrew-word or compound detector.

Local verification on the cleanup candidate:
- tests/test_d4_post_c56_megillah.py: 55 passed in 665.54s;
- T17+T18 focused: 8 passed, 47 deselected in 242.58s;
- D3 + D4 conformance + canonical-name regression: 33 passed in 3.56s;
- C5.7 multi-word SourceName + Program Input/Symbol regressions: 34 passed in 1.07s.

Candidate measurement after source-name canonicalization only:
- candidate SHA-256: 9a048d98a03b5df02359bfcb21a0c28677621c7b67be16d72159c19b17dba755;
- original SHA-256 remains 7b834f4a444e021bb65164282b851af960a6dbc0be3d458c2412181773b9db7b;
- normalized tokens: 62,821;
- syntactic frontier: 57,767;
- candidate line: 466;
- mapped original line: 895;
- semantic/source boundary remains Luach Fifteen;
- source advancement beyond T18: NO.

Full local pytest after cleanup: **622 passed, 126 subtests passed in 727.84s**. Across the non-overlapping D3/D4 targeted file groups, **88 tests pass**. Ubuntu/Windows/full-workflow receipts are recorded after the cleanup push.


## Post-C5.7 continuation — T19 / Luach Fifteen

Starting accepted checkpoint: canonical main `35e954d8c08da68a205cfea654b2597a4a77a714`; D branch cleanup head `b53602e672bdf574fa38b6d7dfd0b8f9c100294d`; cleanup candidate SHA `9a048d98a03b5df02359bfcb21a0c28677621c7b67be16d72159c19b17dba755`; semantic boundary original line 895.

Authorized span: original lines **895–995**. Luach Sixteen begins at original line **999** and is outside T19.

T19 source repair:
- seals are ordinary Natural constants **1, 10, 11, 12, 20, 21, 22, 30, 31, 32, 33**; seal 40 is not declared;
- successor-bowl lookup uses the separately retained visible-drop-46 arrangement `מערכת הטיפה האחרונה`, not the twelfth post-drop blend arrangement;
- the first-answer and direction formulas are implemented exactly from the source with already admitted arithmetic acts;
- parity uses the source-authorized short remainder route with divisor 2;
- later answer numbers advance or retreat by one in the fixed direction, wrapping `M→1` or `1→M`, so the sequence traverses all 1..`M` values before returning;
- asking does not mutate `מלא הקערות`, `מערכת הטיפה האחרונה`, or `המערכה הנוכחית`;
- all newly declared multi-word source names use the accepted C5.7 counted SourceName surface;
- compiler / grammar / registry / HAST / IR / artifact / semantic types / identity families: **UNCHANGED**.

During acceptance, the first T19 source head already measured through to Luach Sixteen, but two multi-call tests failed because the test helper emitted `בהיות` for every role association instead of `בהיות` followed by `ובהיות`. Commit `c6adce2bcc4c59dc7b35e0406935962b5dd10e84` fixes that **test fixture only**; the live candidate source and candidate SHA are unchanged.

GitHub Actions run `37150104605` (#562), accepted executable/evidence head `c6adce2bcc4c59dc7b35e0406935962b5dd10e84`:
- Ubuntu focused T19: **4 passed** in 156.53s;
- Windows focused T19: **4 passed** in 109.31s;
- Ubuntu combined D3+D4: **92 passed** in 471.42s;
- Windows combined D3+D4: **92 passed** in 319.81s;
- post-M2 proposal regressions: **PASS** on both D4 jobs;
- core full pytest: **626 passed, 126 subtests passed**;
- A13 selftest: **289 checks PASS**;
- semantics integrated suite: **PASS**;
- immutable original SHA-256 remains `7b834f4a444e021bb65164282b851af960a6dbc0be3d458c2412181773b9db7b`.

Final T19 candidate measurement:
- candidate SHA-256: `8e57e223d7cdcd4cba299a828e1d409f0ed2061b0e7b25362bfedaec2d645f90`;
- normalized tokens: **66,769**;
- frontier token: **62,110**;
- candidate line: **507**;
- mapped original line: **999**;
- diagnostic: `PARSE0002`;
- next blocker: **Luach Sixteen — לבחור אחת מדרכים רבות**.

T19 status: **COMPLETE / VERIFIED_BY_DEDICATED_D4_CI**.

T20 / Luach Sixteen was **not started** in this tranche.

## Post-C5.7 continuation — T20 / Luach Sixteen

Starting accepted documentation HEAD: 67fef199c4e7ee4f97962e41187ac4d0f792e52b. T19 was Master-accepted and was not reopened. T20 is limited to original Luach Sixteen; Luach Seventeen at original line 1165 is the hard stop.

Executable/evidence head: 86ebc611a56cd96d85a27ff0078bde27bddaed5e.

T20 implements both source-mandated cardinality regimes of the unbiased general selector:
- Branch A (N <= M): greatest acceptable multiple, rejection of the unequal tail, fixed-direction T19 stepping, one-based mapping;
- Branch B (N > M): minimal exact k, exact M^k capacity, base-M wide-number construction from successive T19 answers, cyclic wide direction, wide rejection, one-based mapping.

Focused T20 evidence:
- Ubuntu: 4 passed in 237.10s;
- Windows: 4 passed in 196.50s;
- finite-model independent oracles cover Branch A fairness/boundaries and Branch B k=2 and k=3 cases, forward/backward wide traversal, rejection tails, and wrap;
- a real-M case with N=M+1 verifies exact Natural arithmetic beyond M on all three runtimes;
- state-preservation checks cover bowl fills and retained arrangements;
- structural checks enforce counted multi-word source names, the source-authorized fast remainder route, and six-bowl-arrangement exclusion.

Regression/CI evidence on push run 37171652776 (#568):
- focused T19: 4 passed on Ubuntu, 4 passed on Windows;
- combined D3+D4: 96 passed on Ubuntu, 96 passed on Windows;
- core: 630 passed, 126 subtests passed;
- A13 selftest: 289 checks PASS;
- C5.7 multi-word SourceName jobs: PASS on Ubuntu and Windows;
- post-M2 proposal/semantics regressions: PASS;
- overall push workflow: SUCCESS.
PR run 37171656172 (#569) is also SUCCESS.

Final executable candidate measurement:
- candidate SHA-256: 4aebd9cdac116fa1c1c931d51bf4fe56ae15ac5a998e09a752dcbb06049e340a;
- original SHA-256: 7b834f4a444e021bb65164282b851af960a6dbc0be3d458c2412181773b9db7b;
- normalized tokens: 68,973;
- frontier token: 65,148;
- candidate line: 559;
- mapped original line: 1165;
- diagnostic: PARSE0002;
- next blocker: # לוח שבעה עשר: שערי הקציצה.

T20 status: COMPLETE / VERIFIED_BY_DEDICATED_D4_CI — READY FOR MASTER REVIEW.

T21 / Luach Seventeen was not started.
