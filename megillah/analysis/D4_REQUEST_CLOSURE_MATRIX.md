# D4 Request Closure Matrix

Baseline: `main = 183410bc0300e496fd6fd7ba9ba73b4c6cb7b831`

Production compiler: `0.5.5-alpha.1`; registry: `c5.5-a15-b13.1`.

D4 distinguishes **production capability verified** from **historical Megillah wording already admitted**. A feature existing in C5.5 does not by itself close a source blocker.

| Request | Original source need / representative original spans | Post-M2 production construct | Production proof | Historical wording admitted? | Source repair | D4 status |
|---|---|---|---|---|---|---|
| D-LANGUAGE-REQUEST-001 | runtime cutlet/month names: lines 1443ff, 1663ff; ordered name books at 1781ff | finite Symbol domains/members, counted visible labels, explicit Symbol order, Symbol Collections | `test_request_001_symbol_labels_and_declared_order_are_production_executable`; HAST/IR/portable agreement | No. Raw name lists and `לשם ... תן מספר` are not Symbol declarations | STRUCTURAL_EXPLICITNESS: declare finite domains/members/labels/order and typed books | PARTIALLY_CLOSED |
| D-LANGUAGE-REQUEST-002 | year numbering across zero: lines 1343, 1351–1357, 1810ff | BidirectionalIndex year surface, total pred/succ, typed state/roles/output | `test_request_002_bidirectional_index_crosses_zero_exactly` | Partly. `שנת אין` is admitted; `אחת לפני אין`, `שתים לפני אין`, and `שנת חמשת אלפים` are not canonical A15 Index values | TEXTUAL_CANONICALIZATION + STRUCTURAL_EXPLICITNESS using exact year-typed Index forms | PARTIALLY_CLOSED |
| D-LANGUAGE-REQUEST-003 | ordered books/candidate sets/weavings: lines 1403ff, 1553ff, 1781ff | immutable typed Collection, append/count/membership/ordinal access/order/lex order | `test_request_003_ordered_collection_is_immutable_ordered_and_duplicate_preserving` | No. Historical `יהי שם ספר...` and imperative book prose are not typed Collection constructors | STRUCTURAL_EXPLICITNESS into exact Collection domains and pure operations | PARTIALLY_CLOSED |
| D-LANGUAGE-REQUEST-004 | comparisons `רב`/`ימעט`: lines 231ff, 1427ff, 1571ff, 1641ff | strict Natural proposition `A רב מן B` | `test_request_004_natural_ordering_is_proposition_not_boolean_value` | Frequently no. Forms such as `אם רב המספר מאחיו` and `ימעט` are not the canonical strict-GT surface | TEXTUAL_CANONICALIZATION / DISAMBIGUATION by explicit operands and orientation | PARTIALLY_CLOSED |
| D-LANGUAGE-REQUEST-005 | large written constants, e.g. line 41 and 125/127 wording at 177–189 | productive direct Natural surface through 99,999,999 | `test_request_005_large_megillah_numeral_is_direct_and_exact`; 14,777,149 exact | Not generally. Historical magnitude/order spellings must be audited occurrence-by-occurrence | TEXTUAL_CANONICALIZATION where value is independently established | PARTIALLY_CLOSED |
| D-LANGUAGE-REQUEST-006 | exact `N פעמים`, including dynamic `פעמים כמספר...`: lines 151,159,495ff, 177 | C5.4 `RepeatExactly`: prefix literal or `פעמים כמספר ... ATOMIC_ACTION`, count observed once | literal 127 + dynamic C5.5-input proofs in D4; existing C5.4 observe-once regression | No for many spans. Historical postposed `ACTION פעמים כמספר VALUE` is explicitly not canonical A15; `עשה כן עוד N פעמים` also needs explicit body identity | TEXTUAL_CANONICALIZATION plus named-act wrapping when repeated work is composite | PARTIALLY_CLOSED |
| D-LANGUAGE-REQUEST-007 | two immutable program inputs: original line 17; later `יום המעשה` / query-day references | C5.5 named Program Input Roles, immutable/non-positional, exact domain, validated before Preparation | two-role identity proof and invalid-invocation-before-Preparation proof in D4; C5.5 typed controls | **No faithful day-domain form yet.** Binding machinery exists, but source-day semantics are not Natural-only and production Index surface is year-specific | Blocked pending D4-LANG-001; do not hard-code Naturals or use `מספר שנה` for days | PARTIALLY_CLOSED / STILL BLOCKED AT SOURCE FRONTIER |

## Request closure count

- production capability families independently executable for the intended general class: **7/7**;
- historical source blockers fully closed in the current candidate by D4: **0/7**;
- repairable with existing production constructs but not yet source-repaired: **001–006**;
- still requiring a language-surface decision before faithful source repair: **007**, via `D4-LANG-001`.

## D-LANGUAGE-REQUEST-007 / day audit

The original itself establishes both:
- a unique Natural **day number** for each day (original lines 47–71), and
- that chronological before/after **cannot be derived from those numbers alone** (line 73: `ומן המספרים לבדם לא תדע אי זה יום לפני ואי זה יום אחרי ... מן הימים תדע ולא ממספריהם`).

Therefore a Natural Program Input preserves only the computational number, not the full source-described day relation.

B13 BidirectionalIndex semantics fit the required unbounded ordered line around a distinguished origin, but A15/A16/C5.5 intentionally expose that semantic domain only through year-typed source heads such as `מספר שנה`. D4 does not relabel a day as a year and does not invent a `Day` semantic domain.

The production negative/positive control is `test_day_domain_audit_current_surface_has_year_index_but_no_day_index_head`.


## Post-C5.6 continuation update

### D4-LANG-001

**CLOSED_BY_A17_B16_C56.**

The previously missing non-year/general source profile for the existing `BidirectionalIndex` domain is now production-integrated. D4-PATCH-001 uses the admitted origin `מעלת היתד` in a named Foundation referent and advances the candidate frontier from token 105 to 117.

### D-LANGUAGE-REQUEST-007

Language capability blocker: **CLOSED**.

C5.6 now permits the two eventual Program Input roles to be typed directly through the general `מעלה` profile. Source integration remains pending until the candidate reaches the historical input-contract section; it is no longer a language-design blocker.

### Conformance note

`D4-CONF-001` records that one C5.6 frozen receipt hard-codes the pre-repair candidate SHA/frontier. D4 does not edit that C5.6 test. It is a downstream conformance-maintenance issue, not a semantic/compiler defect.
