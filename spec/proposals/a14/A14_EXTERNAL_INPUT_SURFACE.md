# A14 — External Input Surface

Status: **PREFERRED_SURFACE_CANDIDATE / AWAITING_B13 INTEGRATION ACCEPTANCE**

## Need

The Megillah describes one reusable computation over two externally supplied day values:
- calculation day;
- target day.

A13 can initialize places internally but has no program/host boundary contract.

## B13 reconciliation

B13 head `3c47a57debd381c2b4e41d00d12c792ae43debe8` selects **Program Input Roles**:
- one immutable association per required semantic identity;
- association before Preparation;
- named, never positional;
- not a mutable place;
- no stdin/argv/HTTP semantics.

A14 accepts that distinction as the semantic basis for the surface candidate.

## Preferred surface direction

A14 proposes a program-level role declaration built around the ordinary idea that a value **will be
given to this work**.

Schematic controlled-Biblical candidate:

    למלאכה הזאת ינתן מספר ושמו יוםהמעשה

    למלאכה הזאת ינתן מספר ושמו יוםהשאלה

Candidate typed references:

    המספר אשר ינתן למלאכה הזאת ושמו יוםהמעשה

    המספר אשר ינתן למלאכה הזאת ושמו יוםהשאלה

These forms are not FROZEN in A14. They express the intended relations:
- owner: this whole work/program, not a caller act;
- domain: numeric input in the current B13 Megillah profile;
- role identity: explicit one-word Marak name;
- external association: `ינתן`, not local state mutation.

The host binds the resolved role identity. It does not bind the visible declaration by ordinal
position or by raw source spelling alone.

## Why not a place

A14's initial draft considered externally establishing a named `מקום`. B13 showed a real semantic
difference: an input association is immutable invocation context, while a place is state-bearing and
replaceable.

A14 therefore **withdraws the external-place direction**.

If mutable working state is needed, Preparation may explicitly establish a place from the input Value
after the binding exists.

## Relation to A13 roles

This deliberately resembles A13 role-addressed association only at the level independently justified
by the need: explicit semantic identity and value domain.

It is not:
- act argument position;
- a synthetic `main` call;
- an argv slot;
- a stream read.

## Remaining surface audit

Before freeze, A/B integration must confirm:
1. whether `המלאכה הזאת` is the preferred deictic head for the complete Marak program;
2. whether `ינתן` alone sufficiently distinguishes declaration from an executable giving action in
   Preparatory discourse;
3. whether future non-Natural Program Input Roles require an explicit domain noun in the declaration.

No runtime semantic question remains beyond acceptance of the B13 Program Input Role model.

## Negative grammar

Reject:
- first binding = calculation day by position;
- declaration order as host association;
- stdin/argv/file/network transport as language semantics;
- replacing the input association as if it were a `מקום`;
- principal execution with a required role unbound.
