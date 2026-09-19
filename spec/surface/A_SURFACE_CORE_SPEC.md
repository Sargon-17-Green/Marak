# A_SURFACE_CORE_SPEC.md

Status: **A-Core v0.1 A13 INTEGRATION-FROZEN CANDIDATE**
Workstream: A — Surface Language
Integration closure: A13

A13 is a closure revision of A12, not Language 0.2 and not a Practical-Core expansion.
It is ready for Master integration review but is NOT a declaration of M2 or final language closure.

# 1. Charter

## A-CORE-001 — NORMATIVE
Legal source is Controlled Biblical Hebrew.

For every legal source construction, a competent Biblical-Hebrew reader must be able to obtain the
same computation that the compiler assigns, without knowing conventions from C, Python, JavaScript,
Lisp, Pascal, ML, assembly, or another programming language.

## A-CORE-002 — NORMATIVE
If two natural admitted readings change computation, the source is illegal.

No rescue by:
- nearest antecedent;
- nearest noun;
- dangling-else convention;
- expected type;
- intended algorithm;
- parser ranking;
- statistical/NLP confidence;
- Megillah compatibility.

## A-CORE-003 — NORMATIVE
Outside future string syntax, only:
- the 27 Hebrew letter forms;
- the closed normative whitespace set in A-CORE-004

are lexically significant.

Every other Unicode scalar value is transparent and is erased before grammatical analysis.

Therefore punctuation, niqqud, cantillation, Markdown, Latin letters, Arabic digits, brackets,
backticks and similar material cannot establish syntax.

## A-CORE-004 — NORMATIVE — A13 WHITESPACE CLOSURE
The normative Core whitespace set is exactly:

- U+0009–U+000D
- U+0020
- U+0085
- U+00A0
- U+1680
- U+2000–U+200A
- U+2028
- U+2029
- U+202F
- U+205F
- U+3000

Every nonempty run consisting only of these code points normalizes to one U+0020 SPACE.

This list is the language definition. It is not defined by a host predicate such as `isspace()` and
is not changed by the Unicode library/version used by an implementation.

U+200B ZERO WIDTH SPACE is not normative whitespace. Outside strings it is transparent and is erased.
Thus `יהי<U+200B>מקום` normalizes to `יהימקום`, not to `יהי מקום`.

# 2. Names

## A-NAME-001 — NORMATIVE CORE
A Core name is one normalized Hebrew orthographic word occurring in an explicit naming/name-reference
construction.

Bare words do not become identifiers merely because they were used as names elsewhere.

## A-NAME-002 — NORMATIVE
There is no global "reserved keyword" ban merely for parser convenience.

A proposed name is illegal only when using it in the complete construction creates another admitted
natural parse whose computation differs.

## A-NAME-003 — NORMATIVE
Where one referring description can denote two simultaneously available source referents, the source
is illegal unless further Hebrew words distinguish them.

# 3. Numeric values

## A-NUM-001 — NORMATIVE CORE
A tested direct-literal subset uses the canonical written-number grammar already frozen for 1..9999.

This is an **admission frontier for Core v0.1 direct literals**, not:
- a semantic bound;
- a claim that Biblical numerals stop there;
- a limit on numbers the computation can produce.

Semantic natural numbers are unbounded.

## A-NUM-002 — NORMATIVE
General literal value:

    המספר אשר הוא NUMERAL

## A-NUM-003 — NORMATIVE
`אפס` is not a Core cardinal zero literal.

Canonical derived zero:

    המספר הנחשב בגרע את המספר אשר הוא אחד מן המספר אשר הוא אחד

# 4. State-bearing places

## A-STATE-001 — NORMATIVE CORE
A named `מקום` is a source-language state-bearing referent.

Identity:

    המקום אשר שמו NAME

Current numeric content:

    המספר אשר במקום אשר שמו NAME

These are different referents.
There is no implicit dereference.

The surface does NOT expose a memory address, pointer, machine cell, alias token, or allocation identity.

## A-STATE-002 — NORMATIVE
Initialized numeric place:

    יהי מקום ושמו NAME
    ובמקום אשר שמו NAME
    יהי VALUE לבדו

No observable uninitialized state exists.

## A-STATE-003 — NORMATIVE
Replacement:

    שים במקום אשר שמו NAME
    את NEW_VALUE
    תחת המספר אשר במקום אשר שמו NAME

This says:
- destination;
- new content;
- displaced current numeric content.

It does not define an implementation-level assignment operator.

# 5. Pure numeric calculation

## A-CALC-001 — NORMATIVE
Addition:

    המספר הנחשב בהוסיף את A על B

means the exact number obtained by adding A to B.

## A-CALC-002 — NORMATIVE — A13 NATURAL-DOMAIN CLOSURE
Subtraction:

    המספר הנחשב בגרע את A מן B

is Core natural subtraction.

If A and B denote natural numbers and A ≤ B, the construction denotes exactly the natural number B−A.

If A > B, this construction does not thereby denote a negative Core value. Core v0.1 has no negative
integer value surface and no negative literal syntax.

The semantic failure policy when A ≤ B cannot be established before execution is a B12 dependency:
B must define the specified arithmetic-domain failure behavior and whether a statically provable
violation is rejected before execution.

Core arithmetic operands are restricted to admitted numeric atoms where required by the frozen
A6 grammar; arbitrary precedence/nesting is not inferred.

## A-EQ-001 — NORMATIVE
Exact numeric equality:

    VALUE_A הוא VALUE_B

No `שוה` alias is admitted for Core exact equality.

# 6. Explicit sequence

## A-SEQ-001 — NORMATIVE
Temporal sequence:

    ACTION_A ואחרי כן ACTION_B

ACTION_A completes before ACTION_B begins.

Bare source order, a newline, indentation or bare waw do not create this relation.

# 7. Conditional choice

## A-COND-001 — NORMATIVE CORE
Binary alternative:

    אם PREDICATE ACTION_TRUE ואם לא ACTION_FALSE

where:
- PREDICATE is one complete admitted proposition;
- each branch is one complete atomic action in Core v0.1.

No nearest-`אם` convention exists.
Ambiguous nesting is illegal.

# 8. Finite counted recurrence

Previously validated exact `N פעמים` forms remain admitted only for counts whose Biblical morphology
has individually passed the controlled-language audit.

No generic `for` abstraction is implied.

# 9. Unbounded post-action recurrence

## A-REP-001 — NORMATIVE CORE
Canonical narrow form:

    ATOMIC_ACTION וכן תעשה עד אשר PREDICATE

Meaning:
1. perform ATOMIC_ACTION once;
2. after completion observe PREDICATE;
3. if it holds, recurrence is complete;
4. otherwise perform the same ATOMIC_ACTION again;
5. repeat the post-action observation.

If the predicate held before entry, the explicit first action is still performed.

`ACTION עד אשר P` alone does not have this meaning.

## A-REP-002 — NORMATIVE
The antecedent of `כן` is exactly the one atomic action belonging to this construction.

To repeat a composite procedure, perform one named `מעשה` as the atomic repeated action.

# 10. Reusable described acts

## A-ACT-001 — NORMATIVE CORE
Introduce a reusable described act:

    יהי מעשה ושמו NAME

Typed reference:

    המעשה אשר שמו NAME

Perform it:

    עשה את המעשה אשר שמו NAME

No bare-name call exists.

## A-BODY-001 — NORMATIVE — A12 CORRECTION
Body opener:

    זה דבר המעשה אשר שמו NAME

Body closer:

    עד הנה דבר המעשה אשר שמו NAME

The closer repeats the exact act name.

This supersedes A11's `אלה דברי המעשה ... / עד הנה דברי המעשה ...`.

Rationale:
- `דבר` here is the matter/content of the act, matching the Megillah's productive `זה דבר ...` family;
- Biblical `עד הנה + thematic noun phrase` can explicitly close a discourse topic;
- it avoids treating a non-speaking `מעשה` as the possessor of "words".

No layout contributes to the boundary.

## A-BODY-002 — NORMATIVE
Core v0.1 does not nest act definitions.

Multiple executable body units require explicit admitted relations such as `ואחרי כן`.

Normal exhaustion of the body produces ordinary completion.
Completion itself does not create an output value.

# 11. Numeric input roles

## A-ROLE-001 — NORMATIVE CORE
A reusable act may have a named numeric input role.

Canonical role declaration:

    יהי במעשה אשר שמו ACT דבר ושמו ROLE
    ובעשות את המעשה אשר שמו ACT
    יעמד מספר תחת הדבר אשר במעשה אשר שמו ACT שמו ROLE

The `דבר` is a role, not a mutable number.

## A-ROLE-002 — NORMATIVE
Performance with an association:

    עשה את המעשה אשר שמו ACT
    בהיות VALUE
    תחת הדבר אשר במעשה אשר שמו ACT שמו ROLE

Every required role receives exactly one associated Value.
No role is matched by position.

Core role VALUES are pure numeric Value descriptions.
Association denotes the mathematical Value for that performance; it does not expose a parameter cell,
pointer or caller alias.

## A-ROLE-003 — NORMATIVE
Inside the currently performed act:

    המעשה הזה

is a narrowly defined deictic for the current performance occurrence.

Current Value fulfilling ROLE:

    המספר אשר במעשה הזה
    עומד תחת
    הדבר אשר במעשה אשר שמו ACT שמו ROLE

`המעשה הזה` is not a runtime stack-frame query.
The expression is legal only while that act body is being performed.

# 12. Numeric result production

## A-OUT-001 — NORMATIVE CORE
Produce the Core numeric result of the current performance:

    הוצא מן המעשה הזה את VALUE

This does **not** terminate the act.

Later body actions may follow through explicit sequence.

## A-OUT-002 — NORMATIVE — A12 CORRECTION
Core v0.1 permits **at most one numeric result** from one performance.

A performance may produce:
- no numeric result; or
- exactly one numeric result.

This is a minimal Core restriction, not a claim that the full language must be single-result.

A11's ordinal/positional multi-result scheme is removed from the frozen Core because it reintroduced
position as an externally significant result convention without independent linguistic need.

Future multi-result design must use independently justified explicit distinctions, preferably named
roles/descriptions.

## A-OUT-003 — NORMATIVE
Immediately after a completed performance known to have produced exactly one numeric result:

    המספר אשר יצא עתה מן המעשה אשר שמו ACT

denotes that result.

The reference is legal only in the fixed immediate post-performance position.
There is no global "last result register".

If later use is needed, the caller must explicitly establish retained state or another admitted
referent.

# 13. Cessation and result are independent

`הוצא ...` means result production.
It does not imply cessation.

Where a construction explicitly says that performing an act ceases, cessation has its own meaning.
The Core does not contain an implicit `return` statement.

# 14. Register-Machine witness

The frozen Core has a constructive Register-Machine translation.

That translation is PROOF-ONLY.

Its organization:
- register → named place;
- label → named act;
- helper acts for composite branches;
- recursive call graph;

does not prescribe normal program architecture.


# 15. Whole-program composition — A13

## A-CORE-005 — NORMATIVE
A complete executable Core program is one controlled Hebrew discourse with two semantic parts:

1. a preparatory discourse containing zero or more introductions and definitions;
2. exactly one principal execution clause introduced by the word `ועתה`.

The abstract source shape is:

    PREPARATORY_DISCOURSE ועתה EXECUTABLE_SEQUENCE

`ועתה` is a Biblical discourse transition into the instruction that is to be carried out now.
It is not a reserved function name and does not identify a `main` act.

## A-CORE-006 — NORMATIVE
Preparatory units do not execute merely because they occur in the document.

Frozen Core preparatory units are:
- initialized place introduction;
- named act introduction;
- named input-role declaration;
- named act body definition.

An initialized-place introduction establishes an initial state-bearing referent and its initial current
numeric fact for the coming execution. It is not an executable body action.

Act introduction, role declaration and body definition establish source referents/contracts; they do
not perform the described act.

## A-CORE-007 — NORMATIVE
The one principal execution begins only at the unique top-level `ועתה`.

After top-level `ועתה`, no new Core introduction, role declaration or act body definition is legal.

A complete executable Core program with no top-level `ועתה`, or with more than one top-level `ועתה`,
is invalid.

## A-CORE-008 — NORMATIVE
The principal execution contains one executable unit or an explicitly sequenced executable series.

Two top-level executable units do not acquire observable order merely because one is written first.

If both are to run in order, the words must say so, using the already frozen construction:

    ACTION_A ואחרי כן ACTION_B

Punctuation, newline and indentation never substitute for `ואחרי כן`.

## A-CORE-009 — NORMATIVE
A Core program completes normally when its principal execution and every performed act required by it
have completed, and no explicitly sequenced executable unit remains.

No surface `HALT`, `exit`, `main-return`, or exit code is required.

For the Register-Machine proof, a machine HALT state is represented by ordinary language completion.
The proof may use a frozen state-preserving action before body exhaustion solely to satisfy the
nonempty Core body grammar; that proof-only action is not a HALT primitive and is outside the projected
machine state.

A result produced by an act is not automatically an exit code or stdout.

# 16. Discourse visibility and lifetime — A13

## A-NAME-004 — NORMATIVE
Core visibility is introduction-before-use within the same complete program discourse.

A place or act name becomes available only after its complete introduction has ended.
A role identity becomes available only after its complete role declaration has ended.

Textual position matters here only as ordinary discourse availability: a later reference may refer to
an entity already introduced; an earlier reference may not refer to an entity that the discourse has
not yet introduced.

This does not create execution order among preparatory units.

## A-NAME-005 — NORMATIVE
A second introduction of a place with the same place name in the same Core program is invalid.
A second introduction of an act with the same act name is invalid.
A second role declaration with the same role name for the same owning act is invalid.

The same one-word spelling may be used by different typed kinds where every legal reference remains
linguistically distinguished, for example `המקום אשר שמו X` versus `המעשה אשר שמו X`.

## A-ACT-002 — NORMATIVE
A body definition may be given only for an act already introduced by `יהי מעשה ושמו NAME`.

Each introduced Core act has exactly one body definition before top-level `ועתה`.
All role declarations belonging to that act occur after its act introduction and before its body
definition.

## A-ACT-003 — NORMATIVE
Direct self-reference is legal without a special forward-reference rule because the act identity has
already been introduced before its body definition.

## A-ACT-004 — NORMATIVE
A reference to an act, place or role that has not yet been introduced at that source point is invalid,
even if an introduction appears later in the document.

Core v0.1 has no hoisting and no implicit forward declaration.

## A-ACT-005 — NORMATIVE
Mutual recursion requires no separate forward-reference feature.

It is legal only when all participating act identities are explicitly introduced before any body that
refers to them. Their body definitions may then refer to those already introduced identities.

## A-ROLE-004 — NORMATIVE
A role identity belongs to its named act from the end of the role declaration through the remainder of
the Core program discourse.

The number associated with that role exists only for one performance occurrence: it becomes associated
when that performance begins, remains the same mathematical value during that performance, and ceases
to be associated when that performance completes.

This is source lifetime, not stack-frame lifetime.

## A-BODY-003 — NORMATIVE
The act body begins at:

    זה דבר המעשה אשר שמו NAME

and ends only at the matching:

    עד הנה דבר המעשה אשר שמו NAME

with the same explicit act name.

Nested conditionals, recurrence and explicit sequence do not close the body. A later top-level
definition cannot be swallowed into an earlier body because the earlier matching closer is mandatory.
Core introductions and definitions are not legal body units.

# 17. Core proposition boundary — A13 confirmation

A proposition used by `אם ... ואם לא ...` or by recurrence is not thereby a first-class Boolean value.

Core v0.1 introduces no `true`/`false` literals, no storable Boolean type, and no implicit truthiness.

# 18. Integration revision boundary

A13 changes no Core feature merely for convenience.

It closes:
- normative whitespace membership;
- natural subtraction domain;
- whole-program composition;
- discourse visibility/lifetime;
- normal program completion.

Strings and a full comment/documentation model remain OPEN_AFTER_M2.

# 19. Freeze boundary

The following are NOT part of frozen A-Core v0.1 and must not be inferred:

- first-class Boolean values;
- implicit truthiness;
- positional arguments;
- mutable parameter cells;
- caller-local runtime lookup;
- user-visible stack frames;
- first-class locations/pointers;
- `while` or `for` keywords;
- abrupt return;
- multi-result positional tuple semantics;
- arrays/records/objects;
- exceptions;
- modules/imports;
- stdout;
- exit codes;
- operator precedence;
- punctuation/layout blocks;
- documentation/comment syntax.

Some belong to future language milestones.
Their absence does not weaken the M1 universality witness.
