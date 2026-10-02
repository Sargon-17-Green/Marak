# A18 — Multi-word Declared Source Names

Status: **A18 SURFACE PROPOSAL READY FOR MASTER REVIEW**

Baseline: `5a5f8dae0dd8c3526de5f21f84a3a7b2aba984e3`  
Branch: `workstream-a/a18-multi-word-declared-source-names`

A18 addresses only `D4-LANG-002 — MULTI_WORD_DECLARED_NAMES_NOT_REPRESENTABLE`.
It is a Workstream-A language-surface proposal. It changes no production registry, parser,
resolver, compiler, runtime, HAST, IR, artifact schema, Megillah source, B17 material, or C5.7 material.

The proposal generalizes the source-name surface while preserving the existing static identity model.
It does **not** create Text/String values, dynamic lookup, runtime names, aliases, or a Megillah-only
identifier facility.

## 1. Problem statement

Current normative Core says in A-NAME-001 that a source name is one normalized Hebrew orthographic
word in an explicit naming/reference construction. The production grammar implements that rule with
`NameTerminal`, which consumes exactly one normalized word. This is internally coherent but prevents
ordinary multi-word proper designations from serving as source-declared names.

The gap is not that the parser cannot technically consume more tokens. The gap is that Marak has no
normative, post-normalization rule that tells a reader and compiler exactly which words belong to a
multi-word source identity.

Any A18 mechanism must survive the Charter normalization in which punctuation, maqaf, Markdown,
indentation, line breaks, niqqud and cantillation cannot establish a boundary.

## 2. Evidence from D4

At current D4 head, `megillah/analysis/D4_FINDINGS.json` records `D4-LANG-002` as a real
`MULTI_WORD_DECLARED_NAMES_NOT_REPRESENTABLE` surface defect. D4 repairs currently use welded
scaffolding such as:

    יהי מקום ושמו מספרטיפהגלויה
    ובמקום אשר שמו מספרטיפהגלויה ...

The intended Judean-prose source designation is naturally multi-word, e.g. `מספר טיפה גלויה`.
A18 does not edit that candidate; it uses it only as evidence.

The D4 frontier ledger at PR #20 head independently records T16 at token 20,196 with 76 targeted tests
passing. Its T17 entry is still `PENDING_MEASUREMENT` at that repository head; the later Master report
of the T17 `PARSE0002` failure is therefore newer than that ledger, not contradicted by it.

Some older D4 documents retain stale C5.5-era headings/frontiers. A18 treats
`D4_FINDINGS.json` and `D4_FRONTIER_LEDGER.json` as the current repository evidence for this
finding rather than treating those stale headers as current state.

## 3. Complete naming-site inventory

The baseline current construction registry has 172 productions. Exactly 61 productions contain at
least one `NameTerminal`, with 115 name occurrences and 11 terminal roles. Those 11 syntactic roles
resolve to six source-identity families:

| Static identity family | NameTerminal roles | Multi-word applies? | Existing identity machinery |
|---|---|---:|---|
| named act | ActionName, RoleOwnerActionName, BodyActionName, ResultActionName, PerformedActionName | YES, at every declaration/reference occurrence | `ActId(serial, spelling)`; resolver act table |
| named place | PlaceName | YES | `PlaceId(serial, spelling)`; resolver place table |
| act-owned role | DeclaredRoleName, AssociatedRoleName | YES | `RoleId(serial, owner, spelling)`; key is owner + source spelling |
| Program Input role | ProgramInputRoleName | YES | `ProgramInputId(serial, spelling, program_contract)`; program-owned binding |
| Symbol domain | SymbolDomainName | YES | `SymbolDomainId(serial, spelling)` |
| Symbol member source identity | SymbolMemberName | YES | `SymbolMemberId(serial, spelling)`, resolved within a Symbol domain |

The complete per-production inventory is in `A18_NAME_SITE_INVENTORY.md`.

The following are deliberately **not** source names and are not generalized by A18:

- Symbol visible labels: declaration metadata, already multi-word through an explicit counted-label
  mechanism; never used for source resolution.
- `המעשה הזה`: a deictic current occurrence, not a declared name.
- numeral lexemes, Collection kind words, fixed typed heads, and construction words.
- program-contract fingerprints, serial IDs, runtime values, domains, and artifact-internal IDs.

The six identity families share the same lexical name-slot idea but not identical duplicate scopes or
ownership semantics. A18 therefore generalizes their **surface name representation**, not their
ownership rules.

## 4. Current grammar constraints

A18 is constrained by existing normative and implementation evidence:

1. Only the 27 admitted Hebrew letters and the closed A13 whitespace set carry code meaning outside
   future strings.
2. Every nonempty normative whitespace run normalizes to one U+0020 SPACE.
3. Other characters are transparent/deleted; punctuation cannot delimit a name.
4. `NameTerminal` is open-class and has no reserved-word filter.
5. a bare word is never a reference merely because it is a name elsewhere.
6. the parser preserves ambiguity and has no ranking, nearest match, recovery, expected-type rescue,
   or longest-match commitment.
7. same spelling may remain legal in different typed source kinds when the complete referring
   descriptions distinguish them.
8. Symbol visible labels are a separate metadata mechanism and do not define Symbol source identity.

A18 must preserve all eight properties.

## 5. Candidate designs

A18 evaluated four real boundary families.

### Candidate A — explicit word count at every occurrence

A multi-word source name carries an overt word count in both declarations and references. The count
then determines exactly how many normalized orthographic words form the identity payload.

Evaluated surface frame:

    שם אשר מספר המלים אשר בו הוא COUNT והמלים הן WORD_1 ... WORD_N

where `COUNT = N` and `N >= 2`.

Strengths:
- boundary is explicit before the payload;
- grammar words may safely occur inside the payload;
- declaration and reference are symmetric;
- declaration-table knowledge is unnecessary for parsing;
- prefix names such as `א ב` and `א ב ג` remain mechanically distinguishable;
- normalization gives a simple canonical identity sequence;
- diagnostics can point at the count or the first token after the promised payload.

Costs:
- deliberately verbose;
- every reference to a multi-word name repeats the count frame;
- future C implementation needs a source-name terminal/nonterminal capable of consuming an exact
  counted payload.

A18 selects this family.

### Candidate B — terminator / closing construction

Examples considered abstractly include a name followed by a fixed Hebrew closing phrase such as a
resumptive `הוא שמו`-type boundary.

Strengths:
- potentially shorter references;
- a Biblical naming/resumptive idiom exists.

Weaknesses:
- if the closing words are themselves legal inside a source name, the parser must decide whether an
  occurrence is payload or terminator;
- forbidding those words would create a de facto reserved-name vocabulary;
- choosing first/last terminator is a longest/nearest-match rule;
- escaping the terminator would be a modern identifier convention;
- a semantically empty universal END-like marker is specifically disfavored by Marak's
  anti-imitation audit.

Result: rejected as the normative general mechanism.

### Candidate C — structural framing without a numeric boundary

Examples considered include fuller naming clauses that announce a name and resume the containing
construction after it, without stating a word count.

Strengths:
- can sound more literary than explicit counting.

Weaknesses:
- structural framing still needs a machine-recoverable payload endpoint;
- if endpoint recognition depends on the next outer construction word, then construction words cannot
  freely occur in names;
- if all potential continuations are tried, a single source may acquire overlapping parses whose
  resolution depends on surrounding grammar rather than the name construction itself.

Result: rejected unless it reintroduces an explicit payload measure, in which case it reduces to
Candidate A.

### Candidate D — declaration-known matching

Declare a multi-word name once, then let references consume whichever previously declared word
sequence matches.

Strengths:
- short references after declaration;
- still static rather than runtime.

Weaknesses:
- parsing a reference now depends on the semantic declaration environment;
- `א ב` versus `א ב ג` requires longest-match or a rejection rule based on the current declaration
  set;
- adding an otherwise unrelated declaration can change how later tokens are segmented;
- diagnostics become phase-coupled and harder to localize;
- it pressures the parser toward nearest declaration / expected kind rescue.

Result: rejected.

Punctuation, quotation marks, maqaf, Markdown, line breaks, indentation, capitalization, niqqud,
cantillation, backticks, brackets, escape sequences, and welded-name equivalence are not candidates:
the Charter either erases them or A18 rejects them as imported identifier conventions.

## 6. Rejected alternatives and reasons

The following are explicitly non-normative:

- `מספרטיפהגלויה` as an automatic alias of `מספר טיפה גלויה`;
- quotation-marked or bracketed identifiers;
- “read until the next construction word”;
- “read the longest declared name”;
- “choose the name whose type makes the sentence valid”;
- declaration-order or nearest-declaration disambiguation;
- a global ban on construction words inside names;
- using Symbol visible-label text as a Symbol member reference;
- reusing `CountedLabelTerminal` semantically as source identity without a separate A18 rule.

## 7. Proposed normative surface

A18 proposes a two-form `SourceName`:

    SourceName ::= SimpleSourceName | CountedSourceName

    SimpleSourceName ::= NAME_WORD

    CountedSourceName ::=
        שם אשר מספר המלים אשר בו הוא NAME_WORD_COUNT
        והמלים הן NAME_WORD{NAME_WORD_COUNT}

Normative constraints:

- `NAME_WORD` is one normalized Hebrew orthographic word over the admitted 27 letters.
- `SimpleSourceName` is exactly the existing one-word surface.
- `NAME_WORD_COUNT` uses an admitted exact direct Natural spelling; the counted-name form requires
  a value of at least 2.
- exactly that many following normalized orthographic words are the source-name payload.
- the framing words and count are **not** part of the identity.
- the counted form is legal in every source-name slot covered by the six static identity families.
- a one-word name has no counted alias; this prevents two canonical source-name encodings for the
  same one-word identity.

Examples:

    יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן מספר טיפה גלויה

    המקום אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן מספר טיפה גלויה

    יהי מעשה ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן ספר חדש

This is intentionally not compact identifier syntax. It is an overt Hebrew description that makes the
boundary part of the human-readable source.

## 8. Precise grammar impact

A18 does not edit the production registry, but if Master accepts it the normative grammar delta is:

1. every existing source-name slot that currently admits `NameTerminal(role)` must admit the same
   role through `SourceName(role)`;
2. `SourceName(role)` has the legacy one-word branch and the counted branch above;
3. both branches yield one source-name leaf/value to later static resolution;
4. a counted branch consumes the count frame and exactly N payload words before returning control to
   the enclosing production;
5. no outer production may redefine the payload endpoint;
6. complete-parse ambiguity remains invalid; C5.7 must not rank the branches.

There are no new source identity kinds, no new runtime operations, and no changes to value domains.

## 9. Normalization and canonical identity

Let `Norm` be the existing Charter code normalization.

For a source name occurrence:

- normalize the whole source first under the existing A13 rule;
- for a simple name, the canonical name-word sequence is `(w)`;
- for a counted name with count N, it is `(w1, ..., wN)`;
- canonical spelling is the sequence joined with one U+0020 SPACE.

Identity equality of source spellings is exact equality of the canonical normalized word sequence.
The count is boundary syntax and is not an identity component.

Therefore all normative-whitespace variants of:

    א ב

inside a counted payload normalize to the same canonical spelling `א ב`, including spaces, tabs or
line separators from the fixed normative set.

By contrast:

    א־ב

does **not** become the two-word name `א ב`. Maqaf is transparent, so under current normalization it
becomes the one orthographic word `אב`.

Niqqud and cantillation are likewise transparent and cannot distinguish identities.

There is no stemming, prefix stripping, case folding, fuzzy equality, Unicode compatibility
normalization, or spelling correction beyond the already normative Marak normalization.

## 10. Duplicate, collision and ambiguity rules

Existing ownership scopes remain unchanged, applied to the canonical word sequence:

- duplicate place: reject within the program;
- duplicate act: reject within the program;
- duplicate role: reject within the same owning act;
- duplicate Program Input role: reject within the owning program contract/discourse;
- duplicate Symbol domain: reject within the program;
- duplicate Symbol member: reject within the same Symbol domain.

Cross-kind equal canonical source names remain potentially legal where their full Hebrew referring
descriptions distinguish them, preserving A-NAME-005.

Prefix overlap is not itself ambiguity under counted references:

    א ב
    א ב ג

can coexist because every multi-word occurrence states count 2 or count 3. No longest-match choice is
available or needed.

However, if the complete normalized source still admits two computationally distinct parses—for
example because a counted-name framing sequence also completes a different admitted outer
construction—the source is invalid. The parser must preserve and reject that ambiguity, not choose a
preferred parse.

A wrong count is never repaired. If count 2 is followed by `א ב ג`, only `א ב` belongs to the name;
`ג` must parse as outer syntax or the source fails. If count 4 reaches end of source after three
payload words, the source fails.

## 11. Backward compatibility

A18 is additive at the surface level.

Every currently legal one-word name remains:
- legal;
- represented by the same normalized one-word sequence;
- bound in the same typed namespace/owner;
- resolved to the same static identity;
- unaffected by construction-word spelling.

Existing source is not reinterpreted as a counted name merely because its one-word name happens to be
`שם`, `מעשה`, `מקום`, `אשר`, or another grammar word. The counted branch requires its entire
fixed frame and count payload.

No current one-word source is rewritten. No automatic welded/spaced alias is created.

## 12. Positive examples

### Place

    יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן מספר טיפה גלויה
    ובמקום אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן מספר טיפה גלויה
    יהי המספר אשר הוא אחד לבדו

### Act

    יהי מעשה ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן חשב מספר

### Role with multi-word owner and multi-word role

    יהי במעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן חשב מספר
    דבר ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מספר ראשון
    ובעשות את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן חשב מספר
    יעמד מספר תחת הדבר אשר במעשה אשר שמו
    שם אשר מספר המלים אשר בו הוא שנים והמלים הן חשב מספר
    שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מספר ראשון

### Construction words inside the payload

    יהי מעשה ושמו שם אשר מספר המלים אשר בו הוא ארבעה והמלים הן מעשה מקום אשר שמו

The final four words are one name because the count says four. None is globally reserved.

### Program Input

    יהי למלאכה הזאת דבר ושמו
    שם אשר מספר המלים אשר בו הוא שלשה והמלים הן היום אשר נשאל
    ובטרם תחל המלאכה הזאת יעמד מספר
    תחת הדבר אשר למלאכה הזאת שמו
    שם אשר מספר המלים אשר בו הוא שלשה והמלים הן היום אשר נשאל

### Symbol domain/member source names

    תהי משפחת שמות ושמה
    שם אשר מספר המלים אשר בו הוא שנים והמלים הן חדשי השנה

The visible label mechanism of each member remains separate.

## 13. Negative examples

Reject:

    יהי מקום ושמו מספר טיפה גלויה

because an unframed multi-word payload has no boundary.

Reject a counted form with count 1: one-word names use the legacy simple form only.

Reject:

    ... שם אשר מספר המלים אשר בו הוא שנים והמלים הן א ב ג ...

if `ג` cannot independently begin/continue the required outer grammar. Do not silently enlarge the
name to three words.

Reject declaration count 3 and reference count 2 even when the first two words match. They denote
different canonical word sequences; no prefix rescue exists.

Reject a declaration of `מספר טיפה גלויה` followed by a reference to `מספרטיפהגלויה`.
They are distinct normalized identities.

Reject a reference that relies on the declaration table to decide whether `א ב` or `א ב ג` was
intended.

Reject any use of punctuation, quotes, maqaf, Markdown or line breaks as the only name boundary.

## 14. Megillah examples

The D4 scaffolding:

    מספרטיפהגלויה

can be expressed, after later authorized D4 repair, as the source identity payload:

    מספר טיפה גלויה

through:

    שם אשר מספר המלים אשר בו הוא שלשה והמלים הן מספר טיפה גלויה

at both declaration and reference sites.

Other welded D4 scaffolding such as `טיפההבאה`, `אבניטיפות`, or `עשהטיפהגלויה` would become
eligible for ordinary multi-word names under the same general rule **only if D4 independently decides
that those are the faithful source names**. A18 does not prescribe those Megillah repairs.

## 15. Non-Megillah examples

A general inventory program may use:

    יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מספר כללי

A reusable act may use:

    יהי מעשה ושמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן חשב סכום חדש

A Symbol domain may use:

    תהי משפחת שמות ושמה
    שם אשר מספר המלים אשר בו הוא שלשה והמלים הן סוגי כלי נחשת

These examples require no calendar, day, bowl, drop, or Megillah ontology.

## 16. Open semantic questions for B17

A18 deliberately does not answer these semantic/artifact questions:

1. confirm that a multi-word source name is the same static identity concept as a one-word source
   name, with only canonical spelling generalized from one word to a word sequence;
2. confirm formally that `COUNT` and the framing words have no semantic identity role;
3. confirm duplicate/equality scopes for all six identity families remain exactly their current
   owner-qualified scopes;
4. confirm Program Input host association remains by resolved `ProgramInputId`, never by a raw
   source string, including when spelling metadata contains spaces;
5. define whether canonical HAST/IR/artifact spelling metadata should store the canonical
   single-space spelling or another representation, without turning spelling into runtime lookup;
6. confirm that Symbol member source identity remains independent of its visible label even when both
   happen to have the same multi-word normalized words;
7. determine whether any artifact/version contract needs an explicit schema statement for
   multi-word spelling metadata even if the underlying field remains a string.

If B17 finds that any of these requires a new runtime name object, dynamic lookup, or changed semantic
identity relation, it must return that finding to Master rather than treating A18 as authorization.

## 17. Expected C5.7 parser/resolver consequences — not implementation

If Master and B17 accept A18, C5.7 is expected to need:

- a grammar representation for the counted source-name branch while retaining the legacy one-word
  branch;
- exact count parsing followed by exact N-word payload consumption;
- one parse leaf/span covering the complete source-name construction while retaining the canonical
  payload spelling/sequence for resolution;
- migration of all 11 current name roles / 61 name-bearing productions to the accepted
  `SourceName` grammar abstraction;
- resolver keys generalized from one-token text to canonical normalized source-name identity;
- repeated-name co-reference checks over canonical sequences;
- duplicate diagnostics over canonical sequences;
- source-map coverage for the entire counted name;
- diagnostics for malformed count frame, count < 2, insufficient payload, unmatched repeated name,
  duplicate normalized identity, and whole-program parse ambiguity.

C5.7 must **not**:
- consult declarations to choose the name boundary;
- implement longest-match over declared names;
- filter construction words out of name payloads;
- use expected semantic type to rescue a parse;
- make Symbol visible labels source aliases;
- alter D4 as part of compiler integration.

## 18. Risks

Primary risks:

- verbosity: multi-word references are intentionally long;
- lexical-frame collision: because simple names are open-class, the first word `שם` can itself be a
  legal one-word name; complete-grammar ambiguity must remain a rejection condition;
- numeral admission: the count relies on an admitted exact Natural spelling and inherits its lexical
  frontier; that is a source-admission issue, not a semantic limit on static identity;
- implementation resource use: an explicitly enormous count can demand a very large payload; C may
  need ordinary resource safeguards without changing name semantics;
- artifact assumptions: downstream code may currently assume `spelling` has no spaces;
- formatter behavior: source-preserving formatting must preserve the accepted name construction;
  synthesis must emit the explicit counted form for multi-word identities;
- future grammar evolution: adding an outer construction that creates a complete parse collision with
  the counted frame must be treated as a grammar ambiguity, not solved by precedence.

These risks are materially smaller than terminator collision or declaration-dependent tokenization
because Candidate A makes payload length explicit before the payload.

## 19. Master handoff

A18 proposes one normative direction:

**Keep all existing one-word source names unchanged; add an explicit counted multi-word source-name
form, repeated symmetrically at every declaration/reference site, with static identity equal to the
canonical normalized sequence of payload words.**

Disposition requested from Master:

- accept/reject/return the A18 surface proposal;
- if accepted, route semantic review to B17;
- only after B17 acceptance route production integration to C5.7;
- only after C5.7 integration return D4 to T17/final surface conformance.

A18 itself does not open B17, C5.7, or D4 and does not promote any registry or canon.
