# B17 — HANDOFF TO MASTER

baseline:
`9abd731ba7c80fd714900219e1af4c8d9c41797b`

branch:
`workstream-b/b17-multi-word-source-name-semantics`

PR:
`#22 — Draft / open / unmerged`

HEAD:
This handoff is part of the final documentation/test-metadata commit and cannot contain its own commit SHA.
Use Draft PR #22 live head at Master review.
The independently validated semantic/reference candidate before this handoff metadata commit is:
`3f3edf445b8e3f9d29436ae86005bc3becf5a25f`.

A18 reviewed baseline:
`37e7591dcc42eeeb757a4b79b0dc752162e77079`

finding:
`D4-LANG-002 — MULTI_WORD_DECLARED_NAMES_NOT_REPRESENTABLE`

canonical identity representation:
Abstractly: canonical normalized orthographic payload word sequence `(w1,...,wn)`.
Concrete existing metadata: the same sequence serialized injectively as `spelling: str` with exactly one U+0020 SPACE between words.
No new identity kind or Name value is introduced.

count semantic:
NO

frame semantic:
NO

runtime name object:
NONE

dynamic lookup:
NONE

owner scopes:
acts:
existing program-wide act namespace; unchanged

places:
existing program-wide place namespace; unchanged

roles:
existing owner ActId + canonical role spelling; unchanged

program inputs:
existing owning reusable-program contract + canonical ProgramInput spelling; unchanged

symbol domains:
existing program-wide Symbol-domain namespace; unchanged

symbol members:
existing owner SymbolDomainId + canonical member source spelling; unchanged

cross-kind same spelling:
status:
ADMITTED where the existing complete Hebrew referring descriptions distinguish the typed kinds; no global identifier namespace is introduced.

prefix names:
status:
ADMITTED. `א ב` and `א ב ג` are distinct identities; explicit A18 count determines each payload endpoint. No longest-match rule exists.

introduction-before-use:
status:
UNCHANGED / REQUIRED.

forward references:
status:
NOT ADDED. The D reconnaissance example `אות החסר` is a pre-repair source issue, not a B17 visibility exception.

repeated-name co-reference:
status:
PASS. Exact canonical sequence in the same typed owner scope resolves to the same previously declared identity.

ProgramInputId:
status:
UNCHANGED. Multi-word spelling is metadata in the existing `ProgramInputId`; host binding remains by resolved ID and raw source strings are not binding identities.

program contract fingerprint:
status:
UNCHANGED ALGORITHM. Canonical multi-word spelling participates where existing ProgramInputId spelling already participates. A18 count/frame do not participate because they are absent from IR semantic material. Welded and spaced spellings therefore remain distinct.

Symbol source identity / visible label:
SEPARATE

HAST representation:
existing ActId/PlaceId/RoleId/ProgramInputId/SymbolDomainId/SymbolMemberId `spelling: str`; no new semantic field

IR representation:
existing `IRSymbol.spelling` and existing ProgramInput/Symbol ID dataclasses; integer references remain unchanged

artifact representation:
existing tagged canonical JSON string fields; U+0020 is ordinary data inside the existing spelling field

artifact schema bump required:
NO
reason:
no field, tag, opcode, type, owner rule or encoded structural shape changes; only the admitted contents of an existing spelling string widen from one canonical word to one-or-more canonical words

HAST version bump required:
NO

IR version bump required:
NO

artifact version bump required:
NO

registry bump required:
YES — when C5.7 integrates the accepted SourceName grammar

compiler bump required:
YES — when C5.7 integrates production support

language-edition semantic bump required:
NO — B17 finds no semantic requirement; current post-M2 registry/compiler versioning precedent already carries additive construction integrations without changing the edition identifier

whitespace normalization:
PASS — B17 consumes existing A13 normalization; canonical spelling is single-space serialization of the normalized payload sequence

welded/spaced distinction:
PASS — `מספרטיפהגלויה != מספר טיפה גלויה`

construction-word names:
PASS — allowed. D evidence includes names containing `מספר`, `אשר`, `כל`, `ספר`, `שנת`, and a 10-word name.

expected-type rescue:
ABSENT

longest match:
ABSENT

declaration-known parsing:
ABSENT

runtime observable multiword flag:
ABSENT

semantic reference tests:
PASS — B17 25/25; production compatibility 15/15

B13:
PASS — 28/28

B15:
PASS — 29/29

B16:
PASS — 28/28 downstream semantic tests + 4/4 required regression gates

A17:
PASS — 4,415/4,415 checks

A18:
ACCEPTED / MERGED by Master before B17; B17 found no remediation requirement

Program Input regressions:
PASS — 26/26 targeted

Symbol regressions:
PASS — 35/35 targeted

D3/D4 frozen regressions:
PASS — 29/29

full pytest:
PASS — 543 tests + 126 subtests in 40.53s

CI:
Use live exact-head status on Draft PR #22. The final handoff commit itself must be green before Master acceptance.

new findings:
NONE

blocking findings:
NONE

A18 remediation required:
NO

C5.7 requirements:
Implement the accepted counted SourceName at every A18 name role; emit one canonical single-space payload spelling to the resolver; preserve every existing namespace, owner and visibility rule; do not store count/frame in HAST/IR identity; do not add dynamic lookup, longest match, declaration-known tokenization, expected-type rescue, visible-label alias or welded/spaced alias; add targeted name-boundary, Program Input, Symbol, artifact and regression tests; bump production compiler/package and construction-registry versions, but not HAST/IR/artifact versions.

D4-LANG-002:
A18 surface ACCEPTED
B17 semantic status:
COMPLETE

D reconnaissance disposition:
The read-only inventory strengthens B17 stress coverage (10-word and keyword-bearing names) but creates no additional semantic identity family and no B17 blocker. Its forward-reference example does not change introduction-before-use. T17's synthetic `PARSE0002` remains a separate unclassified D test-fixture failure.

user decision required:
NO

final:
B17 MULTI-WORD SOURCE-NAME SEMANTICS COMPLETE — READY FOR MASTER REVIEW
