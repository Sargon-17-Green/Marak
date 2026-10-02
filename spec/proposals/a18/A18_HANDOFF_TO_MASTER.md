# A18 — HANDOFF TO MASTER

baseline:
`5a5f8dae0dd8c3526de5f21f84a3a7b2aba984e3`

branch:
`workstream-a/a18-multi-word-declared-source-names`

status:
`A18 SURFACE PROPOSAL READY FOR MASTER REVIEW`

finding:
`D4-LANG-002 — MULTI_WORD_DECLARED_NAMES_NOT_REPRESENTABLE`

## Scope receipt

A18 is proposal/design only.

Changed area:
`spec/proposals/a18/` only.

A18 did not:
- modify production grammar/parser/resolver/compiler/runtime;
- modify HAST/IR/artifacts;
- modify `spec/CURRENT_CONSTRUCTION_REGISTRY.json`;
- modify Megillah original/candidate/analysis;
- open B17;
- open C5.7;
- merge or promote itself.

## Current evidence receipt

Canonical `main` was verified at the requested SHA before branch creation.

Current registry receipt:
- 172 productions total;
- 61 name-bearing productions;
- 115 NameTerminal occurrences;
- 11 syntactic name roles;
- six underlying static source-identity families.

D4 repository evidence:
- `D4-LANG-002` is present in `D4_FINDINGS.json`;
- real welded example: `מספרטיפהגלויה`;
- T16 ledger: token 20,196, 76 targeted tests PASS;
- T17 is still `PENDING_MEASUREMENT` in the PR #20 ledger at its current repository head, so the
  later Master-reported T17 failure is newer than that ledger.

Stale-document note:
`D4_HANDOFF_TO_MASTER.md` and the opening portion of `D4_TEST_EVIDENCE.md` retain older C5.5-era
headers. They were not used as authority for current D4 status.

## Selected normative direction

Keep the current one-word SourceName unchanged.

Add a counted multi-word SourceName:

    שם אשר מספר המלים אשר בו הוא COUNT והמלים הן WORD_1 ... WORD_N

Constraints:
- `COUNT = N >= 2`;
- exactly N normalized orthographic words form the payload;
- count/frame are boundary syntax, not identity;
- canonical identity is the normalized payload word sequence;
- the same construction is used at declaration and every reference;
- no construction word is globally reserved from payload;
- no punctuation/layout/quote/maqaf/niqqud/cantillation boundary;
- no longest match, declaration-known match, expected-type rescue, fuzzy match, or nearest-name rule.

## Sites covered

YES:
- acts;
- places;
- act-owned roles;
- Program Input roles;
- Symbol domains;
- Symbol member source identities;
- all corresponding references, including body owner, result source, performed act, typed roles/places,
  Collection Symbol domain heads, and Program Input reads.

NO:
- Symbol visible labels;
- `המעשה הזה` occurrence deixis;
- numerals;
- typed value/domain heads;
- compiler-generated serial/program-contract identities.

## Identity / normalization

Simple name `X` -> canonical sequence `(X)`.

Counted name payload `X Y Z` -> canonical sequence `(X,Y,Z)`.

Canonical spelling metadata proposal: single-space join, subject to B17 review.

All normative whitespace variants within the payload are equal after current normalization.

`א־ב` is not a two-word name because maqaf is transparent and normalizes to `אב`.

No alias:
`מספר טיפה גלויה != מספרטיפהגלויה`.

## Prefix/overlap rule

Counted references distinguish `א ב` from `א ב ג` by the explicit count.

A18 therefore does not need a prefix-name ban. If a complete source nevertheless has two
computational parses, reject it. Never rank parses.

## Candidate disposition

Selected:
explicit word count at every multi-word declaration/reference.

Rejected:
- fixed terminator;
- outer-construction/next-marker boundary;
- declaration-known matching;
- quotation/punctuation/layout/escaping;
- welded/spaced aliasing.

The explicit-count family is selected because it alone preserves open-class payload words while
putting the endpoint in source before the payload is consumed. Implementation convenience is not the
selection criterion.

## Symbol label distinction

A15 counted labels are metadata, not source identity.

A18 independently selects the same boundary **principle** after comparison, but source-name identity is
separate. No label becomes a reference alias and no Text value is introduced.

## Period-language result

PASS FOR MASTER REVIEW AS CONTROLLED COMPOSITION.

Primary evidence:
- Genesis 2:19: naming relation ending `הוא שמו`;
- Jeremiah 23:6: `וזה שמו אשר יקראו יהוה צדקנו`, demonstrating a multi-word designation after a
  naming frame without importing quote syntax;
- Job 8:10: Biblical `מלים`.

The exact A18 count frame is a controlled Marak composition, not claimed as a direct Biblical
quotation.

## Open B17 questions

B17 must review:
1. identity continuity from one-word spelling to canonical word sequence;
2. whether count/frame remain surface-only and absent from semantic identity;
3. existing owner-qualified duplicate/equality scopes;
4. Program Input identity binding with multi-word spelling metadata;
5. HAST/IR/artifact canonical spelling representation;
6. Symbol member source-name versus visible-label independence;
7. any artifact/version implication of allowing spaces in spelling metadata.

A18 makes no semantic decision beyond the source-language requirements necessary to state the
proposal.

## Expected C5.7 work if later authorized

C5.7 would need a counted source-name grammar branch, exact N-word consumption, canonical source-name
leaf/span handling, all 11 name roles migrated consistently, resolver key generalization, and targeted
diagnostics.

C5.7 must not use declaration-dependent tokenization, longest-match, keyword filtering, expected-type
rescue, or label aliases.

## Routing request

Master decision requested:

`A18 → ACCEPT / RETURN / REJECT`.

If accepted:
`A18 → B17`.

Only after B17 acceptance:
`B17 → C5.7`.

Only after C5.7 production integration:
`C5.7 → D4/T17`.

This handoff is not Master acceptance, not B17 acceptance, not production integration, and not a merge.
