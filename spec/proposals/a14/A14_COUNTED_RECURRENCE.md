# A14 — Exact Counted Recurrence

Status: **literal profile SURFACE_READY; runtime-count profile PREFERRED_SURFACE_CANDIDATE / AWAITING_B** — B13 semantics reviewed; final dynamic wording awaits A/B integration acceptance.

## Need

The Megillah uses counted action wording throughout, including:
- small counts;
- 125 and 127;
- 149, 179, 193 and 197;
- runtime-dependent forms such as `פעמים כמספר המעשה`.

Replacing each occurrence with explicit counters/recursion is computationally possible but not a
reasonable local source repair.

## Written-count canonical form

A14 **extends A3 without reversing it**. The count phrase precedes the one repeated atomic action.

Canonical profiles:

    פעם אחת ATOMIC_ACTION
    שתי פעמים ATOMIC_ACTION
    REPEAT_COUNT פעמים ATOMIC_ACTION

where `REPEAT_COUNT` covers admitted exact counts ≥3.

Examples:

    שבע פעמים עשה את המעשה אשר שמו טחון

    מאה ועשרים וחמש פעמים עשה את המעשה אשר שמו בלול

The count phrase modifies exactly the following complete atomic action. This preserves A3's already
audited attachment direction and the Biblical order attested by `שלש פעמים תכה את ארם`.

Genesis 33:3 also attests the reverse free-discourse order, but A14 does not
add it as a second Marak alias. D may rewrite historical Megillah postposed counts to the one canonical
profile.

## Canonical repeat-count morphology

`REPEAT_COUNT` is a dedicated count grammar agreeing with feminine `פעמים`; it is not the A13 direct
numeral phrase copied unchanged.

For 3–9, A3's forms remain: `שלש`, `ארבע`, `חמש`, `שש`, `שבע`, `שמנה`, `תשע`.

A14 extends this productively:
- 10: `עשר`;
- 11–19: `אחת עשרה`, `שתים עשרה`, `שלש עשרה`, ...;
- tens: `עשרים`, `שלשים`, ...;
- hundreds and larger scales follow the same descending magnitude structure as A14 direct numerals,
  while a terminal 1–9 component uses the feminine form required by `פעמים`;
- e.g. 125: `מאה ועשרים וחמש`; 197: `מאה ותשעים ושבע`.

Two is never bare `פעמים`: canonical exact two is `שתי פעמים`. This preserves A3's rejection of
bare `פעמים`, whose exact dual reading would depend on erased vocalization.

## Exactness in controlled Marak

Free Biblical discourse can sometimes use round-number `פעמים` expressions rhetorically. Marak's
admitted construction is narrower: the admitted repeat count is exact.

## Scope

The prefix count consumes exactly one following atomic action. It never grows by looking ahead.

Thus:

    שבע פעמים ACTION_A ואחרי כן ACTION_B

means repeat ACTION_A seven times, then perform ACTION_B once.

To repeat a composite procedure, describe that procedure as a named `מעשה` and repeat its one explicit
performance action.

## Runtime count candidate

Megillah evidence:

    קח אבן החיטה פעמים כמספר המעשה

proves that a runtime-derived count is a real source need. A14 deliberately does **not** freeze a
canonical dynamic-count word order yet. Candidates include a count phrase built around `כמספר VALUE`
and the historical postposed family, but B must first determine the semantic observation model.

B must define:
- whether VALUE is observed once before any recurrence;
- whether later state changes can change the count;
- what happens if evaluating VALUE errors/diverges;
- zero-count semantics;
- whether only Natural counts are accepted.

## Zero repetitions

The written-count profile has no zero-count phrase because A14 still has no direct zero numeral. `פעם אחת` is the explicit count-one form and `שתי פעמים` the explicit count-two form.

For runtime count zero, A recommends **zero executions**, because the count phrase is a modifier of the
action and does not contain an independent first-action command like A13's post-action `וכן תעשה עד אשר`.

This recommendation is `AWAITING_B_SEMANTICS`, not frozen by A alone.

## Negative grammar

Reject:
- attaching one count phrase to an unbounded preceding sequence;
- treating `פעמים` alone as exact two;
- using source order to choose which action the count modifies;
- reevaluating a runtime count on each iteration merely by implementation convention;
- interpreting zero as one execution because A13 post-action recurrence happens to execute once.


## B13 reconciliation

B13 selects `RepeatExactly(N,A)`: observe one Natural count exactly once at recurrence entry; zero
performs A zero times; error during count observation starts no iteration; completed earlier
iterations remain committed if a later iteration fails; one admitted action is the repeat body.

This accepts A14's semantic recommendation. The written-count prefix profile remains SURFACE_READY.
For runtime-derived count, only the **wording/attachment** remains an A-side question; there is no
remaining semantic ambiguity about reevaluation or zero count once B13 is accepted.
