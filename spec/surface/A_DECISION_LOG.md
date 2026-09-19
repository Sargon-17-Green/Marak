# A_DECISION_LOG.md

Status: A12 FROZEN CANDIDATE LOG

## Frozen normative families

- A-CORE-001..003 — Controlled Biblical Hebrew, ambiguity rejection, lexical transparency.
- A-NAME-001..003 — explicit one-word Core names; no bare identifier magic; no parser-only reserved ban.
- A-NUM — canonical tested direct literals 1..9999 as Core admission subset; semantically unbounded numbers.
- A-STATE — named `מקום`, explicit current numeric content, initialized establishment, explicit replacement.
- A-CALC — calculated addition/subtraction; exact numeric identity; derived zero.
- A-SEQ — `ואחרי כן`.
- A-COND — `אם P A ואם לא B`, one atomic action per branch in Core.
- A-REP — audited counted repetition; `A וכן תעשה עד אשר P`.
- A-ACT — named reusable `מעשה`, explicit performance.
- A-BODY — A12 `זה דבר המעשה... / עד הנה דבר המעשה...`.
- A-ROLE — named numeric roles; explicit Value→Role association; no positional arguments.
- A-CURRENT — `המעשה הזה` as current performance occurrence inside body only.
- A-OUT — explicit nonterminating output, at most one numeric result in Core, immediate provenance reference.

## A12 supersessions

### A12-FIX-001 — body frame
SUPERSEDES:
    אלה דברי המעשה ...
    עד הנה דברי המעשה ...

WITH:
    זה דבר המעשה ...
    עד הנה דבר המעשה ...

Reason:
better semantic fit: matter/content of an act, not "words owned by an act".

### A12-FIX-002 — multi-result
SUPERSEDES A11 Core claims:
- zero/one/many numeric outputs;
- `first/second` positional result access.

Frozen Core:
- zero or one numeric output per performance.

Reason:
A11's ordinal result access reintroduced positional result semantics without a need derived from the
minimal Core or a sufficiently general Hebrew result-role system.

Future multi-result design remains OPEN.

### A12-FIX-003 — local mutable state
A11's performance-owned local `מקום` is REMOVED FROM FROZEN CORE v0.1.

Reason:
M1 does not require mutable local state, and the exact ownership/reference wording deserves further
full-language review.

`המעשה הזה` remains frozen only for performance-relative input-role fulfillment and output production.

This is scope reduction, not rejection of future local state.

## Proof-only

The Register-Machine organization remains proof-only.

## Open/full-language

- numeral literal grammar beyond 9999;
- multi-word names;
- nonnumeric role kinds;
- multiple named results;
- performance-owned mutable local state;
- collections/indexing;
- order comparisons beyond numeric equality;
- comments/documentation/semantic headings;
- failure/recovery surface;
- modules/imports/I/O.

# A13 Integration Closure decisions

| ID | Status | Normative decision | Rationale / anti-imitation | B consequence | C consequence | E tests |
|---|---|---|---|---|---|---|
| A-CORE-004 | NORMATIVE | Exact closed whitespace set; runs → U+0020; U+200B transparent. | Host-independent charter closure. | lexical only | freeze exact table | all code points + U+200B |
| A-CORE-005 | NORMATIVE | Program = preparatory discourse + exactly one `ועתה` principal execution. | Hebrew discourse transition, not `main`. | program wrapper | CoreProgram root | no-main/source-order attacks |
| A-CORE-006 | NORMATIVE | Place/act/role introductions and act definitions are preparatory, not executable by occurrence. | Saying what exists/is defined ≠ commanding performance. | initial establishment distinct from action | reclassify whole-program intro | inert-preparation tests |
| A-CORE-007 | NORMATIVE | Unique `ועתה`; no preparatory unit after it. | Explicit source boundary. | execution begins there | program grammar | 0/2 marker negatives |
| A-CORE-008 | NORMATIVE | Multiple top-level actions require `ואחרי כן`. | No statement-order convention. | explicit order only | adjacency not sequence | line/punctuation attacks |
| A-CORE-009 | NORMATIVE | Program completion is ordinary exhaustion; no HALT primitive. | HALT is proof-model vocabulary, not language need. | normal completion | no HALT production | RM normal-completion fixture |
| A-NAME-004 | NORMATIVE | Introduced-before-use visibility; no hoisting. | Ordinary discourse availability. | source-resolved | resolver rule | forward-ref negatives |
| A-NAME-005 | NORMATIVE | Duplicate same-kind names invalid; explicitly typed cross-kind spelling may coexist. | Unique referent without universal identifier namespace. | identity checks | duplicate diagnostics | collisions |
| A-ACT-002 | NORMATIVE | Prior act introduction; one body; roles before body. | Complete discourse contract. | action resolution | preamble validation | body-order negatives |
| A-ACT-003 | NORMATIVE | Direct self-reference legal after prior act intro. | No hidden forward ref. | recursive occurrence | resolver prior identity | self-recursion |
| A-ACT-004 | NORMATIVE | Reference before introduction illegal. | No hoisting. | no future identity | resolver error | forward-ref |
| A-ACT-005 | NORMATIVE | Mutual recursion only after all identities are introduced. | Prior discourse, not declaration magic. | recursion applies | resolve prior IDs | positive/negative mutual |
| A-ROLE-004 | NORMATIVE | Role identity persists; associated number exists only during one performance. | Source lifetime, not stack frame. | occurrence lifetime | context checks | outside-lifetime |
| A-BODY-003 | NORMATIVE | Named body delimiters only; definitions/intros not body units. | Word-delimited scope. | executable content only | grammar restriction | swallowing attacks |
| A-CALC-003 | NORMATIVE | Natural subtraction only: A≤B; A>B makes no negative Core Value. | No automatic Z extension. | B12 failure rule | no negative lowering | underflow cases |
