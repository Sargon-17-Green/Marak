# A14 — Post-M2 Surface Expansion for Megillah Requirements

Status: **A14 READY FOR A/B INTEGRATION REVIEW**

Baseline: A13 — A-Core v0.1 Integration-Frozen Candidate / M2 complete.

A14 is proposal work only. It does not modify or supersede the frozen A13 surface in place and is not
a declaration of Marak 0.2.

## Scope

D2 identified seven genuine language needs in the historical Megillah. A14 treats each D request as
evidence of a computational/surface need, not as a feature specification.

The disposition is:

| D request | Need classification | A13 sufficient? | A14 readiness |
|---|---|---:|---|
| 001 runtime calendar labels | VALID_SURFACE_NEED + NEEDS_NEW_SURFACE + SEMANTICS_REQUIRED_FROM_B | no | AWAITING_B |
| 002 year numbering across zero | VALID_SURFACE_NEED + NEEDS_NEW_SURFACE + SEMANTICS_REQUIRED_FROM_B | no | AWAITING_B |
| 003 finite ordered runtime data | VALID_SURFACE_NEED + NEEDS_NEW_SURFACE + SEMANTICS_REQUIRED_FROM_B | no | AWAITING_B |
| 004 numeric ordering | VALID_SURFACE_NEED + NEEDS_NEW_SURFACE | no | SURFACE_READY |
| 005 productive large numerals | VALID_SURFACE_NEED + NEEDS_NEW_SURFACE | no | SURFACE_READY |
| 006 exact N-times recurrence | VALID_SURFACE_NEED + NEEDS_NEW_SURFACE; runtime-count profile also SEMANTICS_REQUIRED_FROM_B | no | AWAITING_B |
| 007 external day binding | VALID_SURFACE_NEED + NEEDS_NEW_SURFACE + SEMANTICS_REQUIRED_FROM_B | no | AWAITING_B |

No request is rejected as a general-language need outright. Several deliberately receive a smaller
capability than the modern-language analogue suggested by their English description.

## Strong A-only closures

### Numeric ordering
Preferred canonical proposition:

    VALUE_A רב מן VALUE_B

means strictly A > B.

Less-than needs no second surface primitive:

    A < B

is expressed by:

    B רב מן A

Equality remains the frozen proposition `A הוא B`. No Boolean Value type is introduced.

### Productive numeral extension
A14 defines one controlled, canonical, productive direct-numeral grammar through 99,999,999, including
the Megillah's largest fixed number 14,777,149.

It preserves the frozen A13 1..9999 spellings unchanged and adds controlled thousand/million
composition. It deliberately does not admit every historically attested Biblical variant.

### Literal counted recurrence
For a written admitted natural count:

    REPEAT_COUNT פעמים ATOMIC_ACTION

means exact counted performance of that one atomic action.

A composite repeated procedure must still be a named `מעשה` whose performance is the atomic action.

B13 now supplies the observation/zero/failure model for runtime-computed counts. A14 still does not freeze the final dynamic word order until that proposed semantic model is accepted in A/B integration review.

## Findings that constrain B-facing work

1. Runtime calendar names should not be generalized prematurely into arbitrary strings.
2. Years before zero can be represented as a year-relative relation; generic signed integers are not
   required by the Megillah need itself.
3. The Megillah naturally presents ordered finite data as `ספר` with head/successor/last relations;
   this is smaller than an array API.
4. External inputs are a program-boundary association problem, not stdin/argv or positional function
   arguments.
5. B13 proposes the needed runtime counted-recurrence semantics (observe one Natural once; zero means
   zero performances). A14 therefore leaves only final dynamic Hebrew wording/integration acceptance open.

## Anti-imitation outcome

A14 explicitly considered familiar analogues — string, signed integer, array/list, comparison
operators, for-loop, parameters/stdin — and did not use those analogues as starting axioms.

The two surface-ready additions (ordering and large numerals) have independent Biblical-Hebrew
motivation. The remaining proposals stop at the boundary where B must decide the semantic object.

## No A13 reopening

A14 does not change:
- the 27-letter/whitespace lexical charter outside any future text literal;
- A13 program composition and `ועתה`;
- propositions versus Values;
- role-addressed invocation;
- `הוצא` versus return;
- explicit sequencing;
- introduction-before-use;
- normal completion.


## Final baseline and B13 coordination

A14 was rebased before handoff onto canonical main:
`45ac2aebe391f7aa83792e1e501dcd69da884710`.

B13 was then reviewed at:
`3c47a57debd381c2b4e41d00d12c792ae43debe8`.

Its semantic models independently converge with A14's preferred directions. The only substantive
correction is external input: Program Input Roles replace the initial external-place sketch.
Dependent constructions remain proposal-level until A/B integration acceptance; A13 remains untouched.
