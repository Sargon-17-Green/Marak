# B12 Whole-Program Semantics

## Abstract object

After A/C parsing and resolution, B consumes an abstract object:

\[
Program(Preparation,Principal).
\]

There is no `MainFunction`.

## Phase 1 — Preparatory Establishment

Preparation is source-discourse elaboration and initial-state establishment.

It may:
- introduce typed identities;
- establish an initial current numeric fact for a place;
- register act identity;
- register role identity owned by an act;
- associate one body definition with an act.

It is **not** a sequence of executable actions.

Source-discourse order matters for:
- validity;
- introduced-before-use;
- initial-value dependency.

This order is not observable `A then B` action sequencing.

### Initial place

A complete initialized-place preparatory unit has two conceptual effects:

1. source identity exists after the complete introduction;
2. the pure initializer establishes its first current numeric fact.

This is not ordinary executable assignment.

A place cannot read itself from its own initializer because its identity is not yet available at that
source point.

An initializer may read an earlier introduced place.

### Preparatory failure

A statically provable failure is `InvalidProgram`.

An execution-time initialization failure yields:

\[
Error(S,E)
\]

before Principal begins.

## Phase 2 — Principal Execution

The single principal computation identified by A13 begins after successful preparation.

B does not interpret the source word `ועתה`; it consumes the already-identified principal action.

For explicit sequence:

\[
A\ then\ B
\]

B starts only if A completes normally.

If A errors or diverges, B never starts.

## Program completion

If Principal exhausts normally, including every performed act on the reached path, and no continuation
remains:

\[
Program\Downarrow Normal(S,O).
\]

No exit code, HALT value, or main return is manufactured.
