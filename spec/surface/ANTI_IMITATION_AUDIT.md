# ANTI_IMITATION_AUDIT.md

Status: A8 — explicit anti-imitation audit of Workstream A0–A7
Scope: Surface Language only
Date: 2026-09-19

## 1. Audit rule

This audit does NOT ask whether a construct resembles a familiar programming language.

It asks:

1. What computational/semantic need exists independently?
2. What does Biblical Hebrew itself naturally say?
3. Which semantic models could satisfy the need?
4. Did A choose the current model because of those answers, or because a familiar programming-language structure was already in mind?
5. Can the construct be explained to a Biblical-Hebrew reader without first translating a modern programming term?

Classification values:

- LANGUAGE-DERIVED
- COMPUTATION-DERIVED
- IMPLEMENTATION-ONLY
- CONVENTION-BORROWED
- POSSIBLY-IMITATIVE
- UNJUSTIFIED

An item may have a primary classification plus a secondary source.

## 2. Executive findings

### 2.1 The workstream is NOT globally a Hebrew reskin of C/Python/etc.

Several of the strongest decisions are genuinely language-derived:

- punctuation/layout have no syntax;
- bare waw is not sequencing;
- `ואחרי כן` explicitly expresses temporal sequence;
- ambiguous anaphora is rejected rather than resolved by nearest-reference rules;
- `עד אשר` was NOT mapped automatically to `while`/`do while`;
- `אם ... ואם לא ...` was taken from Biblical conditional structure rather than translated from `if/else` punctuation;
- arithmetic roles use overt Biblical valency (`הוסיף ... על`, `גרע ... מן`);
- exact equality avoids importing Modern-Hebrew mathematical `שווה`;
- zero avoids importing Modern-Hebrew cardinal `אפס`;
- anonymous multi-action branch scope was not invented from braces/indentation.

These survive the audit well.

### 2.2 A7 contains a proof-witness structure that must not become the language model

The A7 mapping:

    Register-Machine label -> named `מצוה`
    transition edge -> command call
    DECJZ helper -> helper `מצוה`
    cycle -> mutual recursion

is COMPUTATION-DERIVED as a universality witness.

It is NOT evidence that normal programs should be organized as label commands.

A-RM-001 is therefore reclassified as:

    PROOF-ONLY / NOT A GENERAL SURFACE DESIGN RULE

The successful witness is preserved; its architecture is quarantined from general language design.

### 2.3 The largest imitation risks are not `if` or sequence

They are:

1. the B-derived "mutable cell/location" ontology surfaced as `מקום`;
2. parameter/activation machinery that resembles a conventional call frame;
3. `return` as "produce value AND terminate current action";
4. declaration-before-definition / all-definitions-before-execution regions;
5. restrictions introduced solely to hide strict/eager argument evaluation;
6. the reserved-word ban on names;
7. the arbitrary literal upper bound 9999.

These are reopened or downgraded below.

## 3. Audit table

| רכיב | המודל הנוכחי | מקור ההצדקה | סיווג / חשד לחיקוי | חלופות שנבדקו | החלטה אחרי audit |
|---|---|---|---|---|---|
| M0 one-way human/compiler meaning | legal code must mean what the Biblical-Hebrew reader understands | language charter | LANGUAGE-DERIVED | permissive NLP/heuristics | נשמר ללא שינוי |
| ambiguity rejection | semantics-changing ambiguity is compile error | language charter | LANGUAGE-DERIVED | nearest antecedent, types, ranking | נשמר ללא שינוי |
| lexical transparency | only Hebrew letters + whitespace significant outside strings | explicit project condition | LANGUAGE-DERIVED | punctuation/layout syntax | נשמר ללא שינוי |
| no newline/indentation syntax | follows transparency condition | charter | LANGUAGE-DERIVED | statement-per-line, blocks by indentation | נשמר ללא שינוי |
| no strings in Core v0.1 | M1 does not require them | minimal proof scope | COMPUTATION-DERIVED | premature string syntax | נשמר כ-Core restriction בלבד |
| atomic action as controlled imperative | human instruction is naturally imperative | Biblical grammar | LANGUAGE-DERIVED | hidden actionhood by word order | נשמר; person/number review still possible |
| canonical 2ms imperative only | controlled subset / morphology closure | language simplification | LANGUAGE-DERIVED with restrictive design choice | plural/feminine/finite aliases | נשמר ל-Core; not a full-language claim |
| complete valency frames | roles must be linguistically visible | ambiguity charter + Hebrew valency | LANGUAGE-DERIVED | nearest preposition / type inference | נשמר ללא שינוי |
| `ואחרי כן` sequence | overt Biblical temporal relation | Hebrew | LANGUAGE-DERIVED | bare waw, layout order only | נשמר ללא שינוי |
| source order alone as execution order | rejected | charter | LANGUAGE-DERIVED rejection | normal programming statement order | rejection נשמר |
| one-word CoreName | intrinsic word boundary without punctuation | lexical constraints | LANGUAGE-DERIVED controlled restriction | unrestricted multiword names | נשמר ל-Core בלבד |
| proper-name slot `שמו/שמה NAME` | slot itself marks proper-name function | Hebrew naming construction | LANGUAGE-DERIVED | capitalization / identifier token class | נשמר |
| open-class coined proper names | general language needs fresh finite name supply; name slot makes category human-readable | computation + language | COMPUTATION-DERIVED + LANGUAGE-DERIVED | finite Biblical-name lexicon | נשמר |
| finite Biblical-name lexicon | earlier A1 model | parser safety | POSSIBLY-IMITATIVE / overly lexicalized | open proper-name slot | already superseded; remains rejected |
| reserved Core words forbidden as names (A-NAME-009) | parser avoids collisions | implementation convenience | UNJUSTIFIED | explicit `שמו/שמה` can disambiguate | נפתח מחדש; no longer normative until adversarial proof |
| duplicate visible names forbidden | unique human referent | ambiguity charter | LANGUAGE-DERIVED | shadowing/scoped qualification | נשמר ל-Core; richer explicit qualification may later relax |
| bare name not a reference | no identifier magic | one-way meaning | LANGUAGE-DERIVED | C-like/Python-like bare identifier lookup | נשמר strongly |
| numeral canonicalization | one form per value in controlled subset | Hebrew has multiple genuine variants; parser must be deterministic | LANGUAGE-DERIVED | accept all variants | נשמר |
| literal range 1..9999 | convenience / enough for tests | no linguistic boundary at 9999 | UNJUSTIFIED as normative language rule | smaller proof subset; productive larger grammar | נפתח מחדש; 9999 becomes fixture/tool limit only |
| reject cardinal `אפס` | Biblical `אפס` ≠ Modern cardinal zero | Hebrew lexicon | LANGUAGE-DERIVED | modern zero word | נשמר |
| zero as 1−1 | need exact zero without later lexeme | arithmetic identity | COMPUTATION-DERIVED | empty place, `אין`, `אפס` | נשמר as Core derivation |
| `N פעמים` finite repetition | Biblical counted recurrence | Hebrew | LANGUAGE-DERIVED | `for` syntax | נשמר where exact morphology is proven |
| 3..9-only repeat counts | morphology was easiest/clearest | corpus caution | LANGUAGE-DERIVED provisional, but incomplete | 1,2,10+ forms | נשמר only as proven subset, not conceptual limit |
| `עד אשר` not auto-loop | test point not linguistically determined | Hebrew temporal semantics | LANGUAGE-DERIVED rejection | `while`, `do while`, repeat-until conventions | נשמר strongly |
| generic `END` rejected | semantically empty terminator would be compiler-only | charter | LANGUAGE-DERIVED | `}` / `end` translation | נשמר strongly |
| `מצוה` as reusable executable unit | something one `עושה`; command content can be described | Hebrew | LANGUAGE-DERIVED + COMPUTATION-DERIVED need for reusable computation | `מעשה`, modern "function" noun | נשמר as promising Core abstraction |
| imperative call `עשה את המצוה...` | ordinary "perform the command" | Hebrew | LANGUAGE-DERIVED | bare function-name call | נשמר |
| infinitival body content | definition describes what command is to do | Hebrew morphology | LANGUAGE-DERIVED | body after colon/newline, imperative block | נשמר |
| definitions before executable region (A-ACT-013) | clean declaration/execution split | familiar language organization + boundary convenience | POSSIBLY-IMITATIVE | interleaved discourse, collective program framing | נפתח מחדש; not needed as universal language rule |
| predeclare every command before all definitions (A-ACT-014..018) | solves mutual recursion/forward labels in A7 | RM witness + conventional prototypes | POSSIBLY-IMITATIVE / witness-driven | collective introduction, later explicit reference, different recursive organization | downgraded to PROOF-ROUTE CANDIDATE; reopen for general language |
| one declaration ↔ one definition | supports A7 command graph | conventional declaration model | POSSIBLY-IMITATIVE | a command introduced directly with content; collective named set | retain only inside predeclaration proof scheme, not general norm |
| all declarations before all definitions | region organization | parser/prototype convention | POSSIBLY-IMITATIVE | other word-marked structures | reopen |
| mutual recursion capability | some general computations require cyclic reusable definitions; B supports it | computation | COMPUTATION-DERIVED | dedicated iteration, self-recursion | capability may remain; A7 syntax not thereby justified |
| parameter concept as named placeholder | reusable computation needs varying input | computation | COMPUTATION-DERIVED at capability level; surface model POSSIBLY-IMITATIVE | named roles, environmental facts, substitution descriptions | current placeholder surface remains PROPOSED and reopened |
| named argument association, never positional | words should identify semantic role | ambiguity charter | LANGUAGE-DERIVED | positional arguments | נשמר as design preference/Core constraint |
| read-only parameters (A-PARAM-002) | chosen to match B pass-by-value cleanly | B call model | CONVENTION-BORROWED / POSSIBLY-IMITATIVE | mutable role state; immutable named value; no formal parameter abstraction | reopened pending B audit |
| pure atomic actuals (A-PARAM-005) | hides observable eager/ordered evaluation | B strict evaluation | CONVENTION-BORROWED workaround | explicitly ordered evaluation words; semantics with unspecified order; non-expression input model | reopened; cannot remain normative solely to mask B convention |
| `המעשה הזה` as current activation | maps dynamic call instance / local frame | deictic Hebrew + stack-frame-like semantic need | POSSIBLY-IMITATIVE | explicit ownership by named performance/event; no local frame model | reopened; deictic phrase remains candidate only |
| lexical local `מקום המעשה הזה` | local cell per activation | B lexical scope / fresh frame | POSSIBLY-IMITATIVE | state threaded explicitly, named event-local data, other scope models | reopened pending B audit |
| mutable state as named `מקום` | persistent entity whose occupant changes | Hebrew `מקום` + B Location/Store | POSSIBLY-IMITATIVE because it directly mirrors B's cell/location ontology | named quantity/state relation, history/version model, state transformer without cell identity | downgraded from settled norm to REOPENED-B-DEPENDENT candidate |
| exact one value per `מקום` | mirrors B cell | B | POSSIBLY-IMITATIVE | other state models | reopened with A-BIND-001 |
| assignment as replacement `שים ... תחת ...` | explicit state replacement | Hebrew substitution + B Assign | LANGUAGE-DERIVED surface over POSSIBLY-IMITATIVE semantic model | state transition without persistent cell | surface phrase retained as candidate; normative semantics reopened with B |
| no implicit dereference | human must say whether place or value is meant | one-way meaning | LANGUAGE-DERIVED | C-like automatic variable-value reading | נשמר strongly |
| literal `המספר אשר הוא N` | noun-clause identifies number value | Hebrew + boundary need | LANGUAGE-DERIVED | bare expression token | נשמר |
| calculated value `המספר הנחשב...` | reckon/compute lexical family | Hebrew | LANGUAGE-DERIVED | symbolic operators | נשמר |
| Add/Sub role frames | `הוסיף ... על`, `גרע ... מן` | Hebrew valency | LANGUAGE-DERIVED | infix `+/-`, operand-position convention | נשמר |
| arithmetic as pure new value before state replacement | mathematical operation need separated from state transition | computation + ontology | COMPUTATION-DERIVED; also B-aligned | mutating arithmetic command | retained provisionally; independent mathematical justification exists |
| one-layer arithmetic only | avoid ambiguous nesting | surface readability | LANGUAGE-DERIVED restriction | precedence rules / parentheses | נשמר ל-Core; not full language |
| no precedence table | roles/boundaries expressed in words | charter | LANGUAGE-DERIVED | C-like operator precedence | נשמר strongly |
| equality `VALUE_A הוא VALUE_B` | identity noun-clause | Hebrew | LANGUAGE-DERIVED | `==`, Modern `שווה` | נשמר |
| binary conditional `אם P A ואם לא B` | directly Biblical conditional + imperative alternatives | Hebrew | LANGUAGE-DERIVED | translated `if (...) {}` | נשמר |
| false branch mandatory in early Core | avoided branch/continuation boundary ambiguity | language boundary problem | LANGUAGE-DERIVED restriction | optional else | keep only until richer scope is proven |
| exactly one atomic action per branch | prevents anonymous block ambiguity | language boundary problem | LANGUAGE-DERIVED restriction | braces/indentation blocks | נשמר ל-Core |
| factoring branch work into named command | solves branch complexity | general decomposition + A7 proof | COMPUTATION-DERIVED but can overfit RM witness | explicit linguistic block, other composition | allowed technique, NOT mandatory general style |
| `return` = output + cease action (A-RET-001) | matched B `Return` | familiar function semantics + words | POSSIBLY-IMITATIVE / B-leak | result delivery independent of completion; named product/result relation; continuation after producing result | REOPENED; no longer normative candidate until independently justified |
| terminal return restriction | follows return-statement model | B + conventional function control | POSSIBLY-IMITATIVE | result production without terminal control transfer | reopened with A-RET-001 |
| fall-through Unit / no result | B command model | semantic implementation model | IMPLEMENTATION/B-ONLY for A | surface may simply omit result claim | remove Unit-language from A normative design; keep "no implicit result" independently |
| current result immediately after call | avoids historical ambiguity | language reference need | LANGUAGE-DERIVED, but tied to result model | explicit named product/object | remains candidate, dependent on reopened result semantics |
| normal self-completion `לחדל מעשות...` | words explicitly cease named activity | Hebrew | LANGUAGE-DERIVED | implicit function end, `return`, exit | retained as an available completion construction; not required for every reusable computation |
| program skeleton globals→decls→defs→entry | A7 witness organization | RM translation + familiar compilation unit structure | POSSIBLY-IMITATIVE | other discourse/program organizations | PROOF-ONLY, not language norm |
| command-per-label RM translation | constructive universality witness | M1 | COMPUTATION-DERIVED PROOF-ONLY | program-counter/while proof; other universal models | preserve as witness, quarantine from surface design |
| recursion as unbounded repetition route | general recursion is computationally universal | computation | COMPUTATION-DERIVED, not language-specific | condition-controlled recurrence, explicit repeated process | valid proof route; does not imply recursion is preferred human control model |
| Boolean value type on surface | not introduced | — | NO LEAK FOUND | propositions directly in condition | continue avoiding unnecessary Boolean surface type |
| `while` / `for` surface | not introduced | — | NO LEAK FOUND | linguistic repetition studied directly | continue |
| arrays / records / objects | not introduced | — | NO LEAK FOUND | future capability-driven design | no action now |
| zero-/one-based indexing | not introduced | — | NO LEAK FOUND | future collection semantics | no action now |
| exceptions | not introduced | — | NO LEAK FOUND | future failure/alternative-result needs | no action now |
| modules/imports | not introduced | — | NO LEAK FOUND | future organization/reuse needs | no action now |
| stdout / exit codes | not introduced | — | NO LEAK FOUND | future observable I/O needs | no action now |

## 4. Mandatory re-openings

The following prior "NORMATIVE" decisions are NOT carried forward as settled A-Core rules after this audit.

### A-AUDIT-001 — A-NAME-009 reopened

Prior rule:
reserved Core forms may not be CoreNames.

Audit result:
UNJUSTIFIED as a language rule.

Because a name occurs in an explicit name slot, e.g.

    המצוה אשר שמה עשה

the word `עשה` can in principle be understood as the proper name "Aseh" rather than as the imperative predicate.

The parser inconvenience is not sufficient justification for a language prohibition.

New status:
OPEN / adversarial review required.

### A-AUDIT-002 — A-NUM-001 range cap reopened

Prior rule:
Core numeric literals cover exactly 1..9999.

Audit result:
the exact upper bound 9999 has no linguistic or computational justification.

New status:
- the canonical forms already defined remain useful fixtures;
- 9999 is a tooling/test boundary only;
- the normative magnitude grammar is OPEN.

This does not block M1 because the proof needs only finitely many small literal constants.

### A-AUDIT-003 — A-BIND-001 family reopened pending B audit

Prior model:
mutable state = named `מקום` containing one Value.

Audit result:
the Biblical surface is coherent, but the semantic choice maps almost one-for-one to B's Env/Location/Store model.

Because B is itself undergoing the new anti-imitation audit, A cannot treat that internal model as independent linguistic necessity.

New status:
REOPENED-B-DEPENDENT CANDIDATE.

Preserved evidence:
if B independently retains a persistent state-location model, `מקום` remains a strong Biblical surface candidate.

### A-AUDIT-004 — parameter activation machinery reopened

Affected:
A-PARAM-001/002/004/005/007, A-REF-ACT-001, local `מקום המעשה הזה`.

Audit result:
the need "reusable computation receives varying data" is real.
The formal/actual/call-frame decomposition is not automatically required.

Especially suspicious:
- read-only formal solely because B is pass-by-value;
- pure atomic actuals solely to hide B's strict ordered evaluation;
- current activation phrased to mirror a stack frame.

New status:
capability retained; current machinery PROPOSED/REOPENED.

### A-AUDIT-005 — Return model reopened

Affected:
A-RET-001/002/003 and result-capture constructions that depend on them.

The need is:

> a computation may make a result available to another computation.

The prior model additionally assumed:

> delivering that result terminates the current reusable computation immediately.

That second proposition is conventional `return` semantics, not part of the abstract need.

New status:
REOPENED.

The words `להוציא ...` and `לחדל ...` remain useful linguistic evidence, but they must be analyzed as TWO potentially independent relations:
- product/result delivery;
- completion/cessation.

### A-AUDIT-006 — declaration/definition regions reopened

Affected:
A-ACT-013, A-ACT-014..018 as GENERAL LANGUAGE rules, A-ACT-015, A-ACT-016, program skeleton.

They were heavily motivated by:
- forward references;
- mutual recursion;
- A7's label graph;
- familiar prototype/declaration organization.

New status:
- retained inside the A7 proof witness as one valid controlled program form;
- reopened for the general Core surface.

### A-AUDIT-007 — A7 witness quarantined

The A7 Register-Machine translator remains valid evidence that the CURRENT candidate pieces can simulate M1.

It must not be used to argue that:
- labels should be commands;
- programs should be command graphs;
- all recursive definitions require predeclaration;
- command calls are the preferred everyday repetition mechanism.

## 5. Items explicitly checked from the new instruction

### "Variables"

A did not simply introduce a bare identifier whose r-value/l-value meaning is compiler knowledge.

However, A5's named `מקום` currently mirrors a conventional mutable cell closely.

Status:
REOPENED-B-DEPENDENT.

Abstract need:
persistent state that later computation can observe after a change.

### Assignment

The surface phrase itself (`שים ... תחת ...`) is linguistically explicit.

But "assignment to a stable cell" is only one state-transition model.

Status:
surface wording candidate retained; semantic model reopened.

### Lexical scope

A has used uniqueness and `המעשה הזה` rather than braces/indentation.

But lexical activation-local cells came from B's conventional model.

Status:
scope NEED is computation-derived; current activation model reopened.

### Stack frames

Not named on the surface, but A4b's `המעשה הזה` + fresh locals behaves very much like an activation record.

Status:
POSSIBLY-IMITATIVE / B-derived.

### Positional parameters

Explicitly rejected.

Status:
good anti-imitation result.

### Return statement

Found as a genuine leakage risk.

Status:
REOPENED.

### Expressions vs statements

A uses two linguistic categories:
- noun phrases describing Values;
- imperative/infinitival clauses describing actions.

These are independently motivated by Hebrew grammar.

Do NOT promote the meta-terms "expression" and "statement" into normative surface ontology.

Status:
LANGUAGE-DERIVED categories; modern labels are analysis-only.

### Boolean values

No Boolean surface type is required by current A.
Conditions can be propositions directly.

Status:
no leakage found.

### if/else

The modern analytical label is incidental.
The actual construction comes from Biblical `אם ... ואם לא ...`.

Status:
LANGUAGE-DERIVED.

### while / for

Not imported.
A explicitly refused to assign `עד אשר` hidden pre-/post-test semantics.

Status:
no leakage found.

### indexing / arrays / records / objects

Not designed yet.

Status:
no assumptions to preserve.

### exceptions

Not designed on the surface.

Status:
no assumptions to preserve.

### modules/imports

Not designed.

Status:
no assumptions to preserve.

### precedence

A deliberately avoids symbolic precedence by using full valency and restricted nesting.

Status:
no leakage found.

### eager evaluation

A4b did leak B's strict evaluation indirectly by restricting arguments to pure atoms.

Status:
REOPENED. Surface cannot be constrained merely to hide an unexamined semantic convention.

### call-by-value

A4b was explicitly aligned to B pass-by-value.

Status:
CONVENTION-BORROWED / B-dependent; reopen until B's own audit closes it independently.

### mutable cells

See A-BIND-001 reopening.

### global/local

"Global" and "local" are analysis terms only.
A's linguistic need is:
- state available to a larger discourse/program;
- state belonging only to a particular performance or subcomputation.

The current exact model is reopened with B.

### standard output / exit codes

Not introduced.

Status:
no leakage found.

## 6. Conventional-language leakage adversaries for E

E should add a family named:

    CONVENTIONAL-LANGUAGE LEAKAGE

Mandatory tests include:

### LEAK-A-001 — reserved identifier intuition

Source in explicit name slot:
    הנה מצוה ושמה עשה

A compiler must not reject it *merely* because mainstream languages reserve keywords.
Either Biblical/name-slot ambiguity independently rejects it, or it is legal.

### LEAK-A-002 — hidden positional arguments

Two input-role descriptions in a call may not be mapped by order unless the words themselves establish order.

### LEAK-A-003 — hidden left-to-right evaluation

Two effectful input computations may not receive left-to-right semantics merely because their phrases appear left-to-right.

Until A specifies linguistic order, either:
- the construction is illegal; or
- semantics must be order-insensitive.

### LEAK-A-004 — implicit return

The final Value phrase in a reusable computation does not become a result merely because many languages return the last expression.

### LEAK-A-005 — return implies termination

A phrase that makes a product/result available may not terminate the current action unless cessation is also linguistically expressed and independently justified.

### LEAK-A-006 — implicit variable dereference

`המקום אשר שמו X` is not silently converted to the Value currently associated with it.

### LEAK-A-007 — nearest `else`

Nested ambiguous `אם` constructions are not repaired with a dangling-else convention.

### LEAK-A-008 — loop test convention

`עד אשר P` does not secretly choose pre-test or post-test semantics.

### LEAK-A-009 — declaration region as magic

If declarations/definitions remain in some future form, their semantic effect must come from the Hebrew discourse construction, not because "declarations conventionally come first."

### LEAK-A-010 — Register-Machine style contamination

A general-purpose example that is not a Register Machine must not be forced into:
- one command per state/label;
- helper command per branch;
- explicit program-counter-like command graph.

### LEAK-A-011 — stack-frame leakage

A reference such as `המעשה הזה` may not be resolved by "top stack frame" as an implementation rule.
Its referent must follow the source-language deictic rule.

### LEAK-A-012 — C-like statement order

Two clauses separated only by source order/newline/punctuation do not acquire sequential execution.

## 7. Revised abstraction vocabulary for A

The following analytical terms are permitted internally, but each is now paired with its actual requirement:

| Analysis term | A should start from |
|---|---|
| variable | persistent observable state that may later differ |
| assignment | explicit transition from one state content to another |
| function | reusable described computation/action |
| parameter | varying input role of a reusable computation |
| call | request/performance of a previously described computation |
| return | making a result available; completion is a separate question |
| local variable | state/data belonging only to a delimited subcomputation/performance |
| Boolean | proposition/truth needed to choose behavior; a Boolean Value type is optional |
| if/else | choice of one course based on a proposition |
| loop | recurrence with an unbounded a-priori number of steps |
| block | linguistic delimitation of which actions belong to a larger action |
| scope | linguistic/referential domain in which a name/description has a unique referent |
| array | runtime-sized ordered collection capability, if later required |
| module | organization/reuse across larger program units, if later required |

## 8. What remains solid after the audit

The following foundation remains strong enough to continue without restarting A:

1. the M0 language charter;
2. lexical transparency consequences;
3. controlled morphology rather than root guessing;
4. explicit valency and constituent containment;
5. explicit temporal sequencing;
6. canonical controlled numeral parsing (but not the 9999 cap);
7. refusal to treat `אפס` as Biblical zero;
8. counted recurrence where Biblical morphology is exact;
9. refusal to map `עד אשר` automatically onto a conventional loop;
10. `מצוה` / `עשה את המצוה` as a strong reusable-action surface family;
11. Hebrew-derived arithmetic noun phrases and role marking;
12. exact number identity through a noun clause;
13. conditional choice through `אם ... ואם לא ...`;
14. negative-grammar-first discipline.

## 9. What A8 must NOT do

Until the reopened items are independently resolved, A must not:

- promote the A7 command graph to a general program architecture;
- require declaration/prototype regions globally;
- make pass-by-value a surface fact merely because B currently does;
- require read-only parameters for that reason;
- make result delivery imply termination;
- state that mutable state *is* a named cell/location as a settled language fact;
- retain 9999 as a normative literal-language limit;
- forbid a name solely because its consonants match a grammar word.

## 10. Immediate continuation after audit

The next A work should proceed on parts independent of reopened B assumptions:

1. consolidate the language-derived core grammar;
2. adversarially test arithmetic/conditional/action wording;
3. perform Megillah surface audit using the revised abstraction vocabulary;
4. keep the A7 Register-Machine generator as a proof fixture, explicitly labeled PROOF-ONLY;
5. wait for / consume B's own anti-imitation audit before re-freezing state, call, parameter, local-scope, and result semantics.

No restart of A0–A7 is required.


# A12 freeze addendum

## Convergence accepted only after re-derivation

After A8, A independently re-derived:
- named reusable acts;
- named changeable places;
- conditional choice;
- post-action recurrence;
- named input roles;
- result production.

Their superficial resemblance to familiar programming capabilities does not make them imitative.

## Additional leakage found at A12

### Positional multi-result leakage
A11 permitted multiple numeric outputs and referred to them as first/second.

Classification:
POSSIBLY-IMITATIVE / unnecessary positional convention.

Action:
removed from frozen Core.
Core has zero or one numeric output.
Future multiple outputs require independently justified linguistic distinctions.

### "Words of the act" body framing
A11 used `דברי המעשה`.

Classification:
LANGUAGE QUALITY DEFECT, not conventional-language imitation.

Action:
replaced by singular `דבר המעשה` framing:
`זה דבר המעשה... / עד הנה דבר המעשה...`.

### Local state
A11 introduced performance-owned mutable local places.

Classification:
COMPUTATIONALLY PLAUSIBLE but not necessary for M1 and not yet linguistically strong enough for freeze.

Action:
removed from frozen Core; future work remains open.

## Freeze conclusion

No frozen A12 construction requires a reader to know:
- l-value/r-value convention;
- positional argument matching;
- stack-frame identity;
- Boolean storage;
- pre-test while;
- abrupt return;
- tuple return;
- braces/indentation;
- operator precedence.

The A12 candidate therefore passes A's internal anti-imitation gate.
External E adversarial validation is still required.

# A13 final anti-imitation closure

## Whole-program composition
**Need:** establish referents/descriptions, then unambiguously say what is to be done.

Alternatives audited:
1. execute all top-level forms in textual order — rejected as conventional statement-file semantics;
2. distinguished principal `main` act — rejected because no Hebrew/computational need requires a magic name;
3. preparatory discourse followed by `ועתה` principal execution — chosen.

`ועתה` itself marks the shift into what is to be done now. Multiple actions still need `ואחרי כן`.

## Visibility
Hoisting, braces/indentation lexical scope and dynamic caller lookup were considered and rejected for
Core. A13 uses ordinary discourse introduction-before-use. A later source reference can refer to an
already introduced entity; an earlier source phrase cannot refer to a future introduction.

## Lifetime
Top-level places/acts persist as source referents from completed introduction through program
completion. A role identity persists after declaration, while its associated numeric value exists only
during one performance. No stack address, allocation or deallocation becomes source ontology.

## Completion
HALT keyword, host `exit`, and conventional function return were not assumed. Finite execution ends by
ordinary exhaustion of what the source explicitly requested. Proof-model HALT therefore maps to normal
completion.

## Subtraction
Automatically extending Natural subtraction into negative integers because common languages/maths do
so would be a convention leak. A13 retains the Natural Core domain; B12 defines domain failure.

## Verdict
A13 closure requires no `main`, top-level statement order, hoisting, stack frame, Boolean Value,
`return`, positional argument, or HALT primitive. Similar capabilities arise from independently stated
needs and Biblical-Hebrew constructions.
