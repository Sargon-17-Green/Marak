# A17 — HANDOFF TO MASTER

baseline:
e8f766889676b219f0abf5c9e4f08fad3034fa5b

branch:
workstream-a/a17-general-bidirectional-index-surface

PR:
#17 — Draft, open, unmerged
https://github.com/Sargon-17-Green/Marak/pull/17

proposal evidence HEAD:
27f2121a974a1e07b9fc592a704542da347aa628

final handoff commit:
This file is itself added by the final handoff commit. Therefore it intentionally does not claim a self-referential SHA; use the PR branch HEAD reported by GitHub at review time as the final review HEAD.

## scope

A17 addresses only D4-LANG-001: a truthful general/non-year Controlled Biblical Hebrew surface for the already-existing B13 BidirectionalIndex domain.

A17 does not reopen prior A/B/C/D workstreams, does not create a new semantic domain, does not modify the Megillah, does not modify production grammar/parser/resolver/compiler/runtime/HAST/IR/artifacts, does not edit spec/CURRENT_CONSTRUCTION_REGISTRY.json, does not begin B16, and does not merge the PR.

## existing lexical privilege inventory

The current language is not a C/Python-style reserved-keyword system.

- compiler/lex/words.py: an orthographic word is not assumed to be a semantic token.
- NameTerminal is an open one-word name slot; reserved-word filtering is intentionally absent.
- WordTerminal has force only at an exact position in an admitted construction.
- ambiguity is preserved/rejected rather than guessed.
- baseline registry c5.5-a15-b13.1 contains 155 productions and 115 distinct exact WordTerminal spellings.
- current privileged non-word classes include explicit NameTerminal roles, two numeral lexicons, and the counted Symbol-label terminal.
- no active baseline production uses MorphTerminal.

## new privileged lexemes/phrases

Eight new normalized orthographic forms are proposed:

- מעלה
- מעלות
- מעלת
- המעלה
- היתד
- תעמד
- עומדת
- יצאה

All eight are construction-local. None is globally reserved. A spelling that matches one of them remains usable as an entity name in an explicit NameTerminal slot.

## D4-LANG-001 disposition

SURFACE_PROPOSAL_READY_FOR_B16/MASTER_REVIEW

A17 does not claim semantic closure or production closure.

## selected surface

Generic/non-year origin:

    מעלת היתד

Before origin:

    מעלה אחת לפני מעלת היתד
    שתי מעלות לפני מעלת היתד
    COUNT מעלות לפני מעלת היתד

After origin:

    מעלה אחת אחרי מעלת היתד
    שתי מעלות אחרי מעלת היתד
    COUNT מעלות אחרי מעלת היתד

COUNT reuses the existing A15 feminine-count morphology.

Exact mapping:
- מעלת היתד -> B13 ZeroIndex
- N מעלות לפני מעלת היתד -> BeforeZero(N)
- N מעלות אחרי מעלת היתד -> AfterZero(N)

## semantic domain

BidirectionalIndex

## new semantic domains

NONE

No Day, Date, Time, Timestamp, generic Integer, signed Natural, or Megillah-only primitive is proposed.

## year profile compatibility

A15/A16 year forms remain unchanged: שנת אין; the before/after years family; מספר שנה / מספר השנה; and the A16 successor/predecessor forms.

The year profile and the generic מעלה profile denote the same B13 semantic domain and may denote the same semantic values. A17 proposes no semantic subtype and no runtime profile tag.

Canonicality proposal: each spelling family is canonical inside its own linguistic profile. Source-preserving formatting preserves the resolved profile. Value-only source synthesis must receive an explicit target profile because a bare semantic Index Value does not encode year versus general provenance.

## generic/non-year literal

See selected surface above.

## typed reference

Generic declaration noun: מעלה
Generic definite reference head: המעלה

## Program Input head

Declaration:

    יהי למלאכה הזאת דבר ושמו ROLE
    ובטרם תחל המלאכה הזאת
    תעמד מעלה
    תחת הדבר אשר למלאכה הזאת שמו ROLE

Reference:

    המעלה אשר עומדת תחת הדבר אשר למלאכה הזאת שמו ROLE

No positional or transport semantics are introduced.

## place/state use

Current value:

    המעלה אשר במקום אשר שמו PLACE

Initialization reuses the A16 typed carrier frame.

Replacement:

    שים במקום אשר שמו PLACE את INDEX_VALUE תחת המעלה אשר במקום אשר שמו PLACE

## role use

Declaration uses feminine agreement תעמד מעלה in the existing named-role frame.

Current occurrence:

    המעלה אשר במעשה הזה עומדת תחת הדבר אשר במעשה אשר שמו ACT שמו ROLE

Performance association remains the existing profile-neutral named-role construction.

## result use

Output production remains:

    הוצא מן המעשה הזה את INDEX_VALUE

Immediate result:

    המעלה אשר יצאה עתה מן המעשה אשר שמו ACT

## Index equality surface

NOT SURFACED

B13 semantic identity exists, but A17 found no independent source need sufficient to add a generic equality production.

## Index order surface

Canonical strict order:

    INDEX_A לפני INDEX_B

It maps to B13 strict total Index order A < B.

A אחרי B is not a second canonical production; express the opposite relation by operand reversal: B לפני A.

## Index distance surface

NOT SURFACED

B13 has exact Natural distance semantically. The Megillah itself instructs the program to count how many days pass, so A17 leaves exact distance as source algorithm rather than a built-in primitive.

## pred/succ surface

    המעלה אשר אחר INDEX_VALUE
    המעלה אשר לפני INDEX_VALUE

These map to B13 succ and pred. Both remain total and cross the origin without special syntax.

## operations deliberately NOT surfaced

- Index equality
- direct Index distance primitive
- Natural to Index conversion
- Index to Natural conversion
- generic signed arithmetic
- unary minus
- generic Index Collection kinds such as ספר מעלות
- arbitrary user-supplied profile/type nouns
- Day/Date/Time/Timestamp operations

## rejected alternatives

- reusable arbitrary noun/profile family: rejected as an open type-like unit system with morphology and expected-context pressure.
- מעמד: Biblical, but primarily station/post/standing-place, with weaker evidence for a countable reversible discrete scale.
- צעד: Biblical and countable, but naturally denotes traversal/distance rather than stationary coordinate identity.
- מנין: rejected as a Controlled Biblical Hebrew basis; the biblical occurrence is Aramaic (Ezra 6:17) and semantically pulls toward enumeration.
- מקום: rejected because Marak already gives it frozen state-holder ontology.
- מעלת היסוד: rejected because foundation can imply beginning/lower bound, whereas the required line extends on both sides.
- מעלת אין: rejected because it would broaden A15's tightly constrained אין profile without independent evidence.

## period evidence

Primary attestations:
- 2 Kings 20:9–11: counted עשר מעלות and backward movement on the same scale.
- Isaiah 38:8: parallel counted מעלות scale and reversal.
- Isaiah 22:23–25 and Ezra 9:8: יתד as a fixed/supporting peg metaphor.
- Psalm 33:11: feminine תעמד.
- Psalm 111:3,10: feminine עומדת.
- Ezekiel 7:10: feminine יצאה.
- Isaiah 22:19: comparative evidence for מעמד.
- Job 31:4: comparative evidence for counted steps.

Controlled deviations:
- מעלת היתד is a controlled new composition, not claimed as a direct Biblical quotation.
- the complete counted before/after family is a controlled composition.
- the programming carrier clauses are controlled compositions.

Modernisms rejected:
- אינדקס / int-like terminology
- generic signed Integer terminology
- unary-minus source design
- Date/Time/Timestamp terminology
- generic-angle-bracket or modern type-annotation patterns

## normalization audit

PASS

The selected forms remain recoverable after punctuation erasure, Markdown transparency, niqqud removal, normative whitespace collapse, and line-break removal.

## ambiguity audit

PASS FOR MASTER/B16 REVIEW

- bare מעלה / מעלות / מעלת / היתד are not Index Values.
- year and generic literal profiles may not be mixed.
- expected type cannot rescue malformed source.
- homography is controlled by complete constructions, not parser guessing.
- strict order has one canonical orientation.

## collision audit

PASS

- current exact WordTerminal inventory: 115
- new exact construction-local forms: 8
- current/new intersection: empty in the A17 inventory
- no global reservation introduced
- selected generic literals remain normalized-disjoint from current year and Natural literals
- explicit NameTerminal slots retain lexical freedom

## backward-compatibility audit

PASS AT PROPOSAL LEVEL

- existing A13/A15/A16 source is not changed.
- year profile is not rewritten.
- Natural spelling/semantics are not changed.
- current registry is not edited.
- no production compatibility break is introduced by A17 itself.

## Megillah needs covered

- general non-year ordered coordinate input
- distinguished origin
- before/after literal positions
- typed Program Input flow
- typed place/state flow
- named-act role flow
- output/immediate-result flow
- strict chronological order
- one-step predecessor/successor traversal

## Megillah algorithmic operations deliberately left as acts

Exact distance/count remains source computation using strict order/direction, succ/pred, a Natural retained count, and existing control/recurrence mechanisms.

## proposal tests

- A17 reference checks: 4,415 / 4,415 PASS
- positive: 4,388
- negative: 27
- A17 pytest wrapper: 3 passed

Coverage includes normalization, punctuation/Markdown/niqqud transparency, exact literal mapping, succ/pred reference grid and inverse laws, strict order, lexical collision inventory, year/Natural disjointness, name-slot freedom witnesses, feminine carrier agreement, and forbidden-domain/primitive guards.

## production files changed

NONE

All A17 proposal files are under spec/proposals/a17/.

## Megillah changed

NO

## user decision required

NO

A17 found one materially stronger period-language solution; the rejected alternatives were not evidence-equivalent.

## open questions for B16

1. Is coexistence of year and generic profiles over one BidirectionalIndex domain acceptable without runtime profile provenance?
2. Is source-preserving/profile-selected formatter behavior sufficient canonicality discipline?
3. Does the fixed מעלה head remain a truthful language surface rather than a disguised generic Integer/type keyword?
4. Is strict A לפני B the correct minimal source exposure of B13 Index order?
5. Is exposing one-step succ/pred while leaving exact distance algorithmic the correct anti-imitation boundary?
6. Because both profiles share one semantic domain, should a value produced under one surface profile be admissible in a carrier written with the other, or should source-profile coherence be a static surface restriction? A17 does not invent a semantic unit subtype to answer this.

## CI/status

Proposal evidence HEAD:
27f2121a974a1e07b9fc592a704542da347aa628

GitHub Actions push run 35575613261: SUCCESS.
GitHub Actions pull_request run 35575626615: SUCCESS.

Each run completed all 15 jobs successfully: core; tooling portability Ubuntu/Windows; C5.1–C5.5 Ubuntu/Windows; and D4 Megillah conformance Ubuntu/Windows.

## final

A17 PERIOD-LANGUAGE SURFACE READY FOR MASTER REVIEW

This is not Master acceptance, not B16 acceptance, not a production implementation, and not a merge.