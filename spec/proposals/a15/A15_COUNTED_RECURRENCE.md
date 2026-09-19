# A15 — Exact Counted Recurrence

Status: **INTEGRATED_SURFACE_READY** for D-LANGUAGE-REQUEST-006.

## 1. Literal count profile

A15 retains A3 direction and A14 morphology:

    פעם אחת ATOMIC_ACTION
    שתי פעמים ATOMIC_ACTION
    REPEAT_COUNT פעמים ATOMIC_ACTION

The third profile is for admitted exact counts N>=3. `REPEAT_COUNT` uses controlled feminine count morphology. Direct count phrases share the A15 numeral-edition magnitude frontier, but the semantic `RepeatExactly` count itself is an unbounded Natural and may be computed dynamically.

The modifier consumes exactly one following atomic action. A composite computation must be a named `מעשה`; performing that one act is then the repeated action.

## 2. Dynamic count profile — closed in A15

Canonical dynamic wording is:

    פעמים COUNT_AS_NUMBER ATOMIC_ACTION

`COUNT_AS_NUMBER` is not a second numeric value category. It is the corresponding admitted Natural Value description with its initial typed head `המספר` inflected by prefixed kaf as `כמספר`. Thus:

    המספר אשר במקום אשר שמו מנין
    -> כמספר אשר במקום אשר שמו מנין

and:

    המספר הנחשב בהוסיף את A על B
    -> כמספר הנחשב בהוסיף את A על B

A complete example is:

    פעמים כמספר אשר במקום אשר שמו מנין
    עשה את המעשה אשר שמו טחון

Line breaks are documentary only. The count-description boundary is exactly the boundary of the corresponding admitted Natural Value description after this head inflection; the next complete atomic action is the sole repeated body.

This keeps the historically attested Megillah relation `פעמים כמספר ...` while moving the whole count modifier before the action, preserving the already-audited A3 attachment direction without producing the linguistically defective double head `כמספר המספר`.

The historical postposed form `ACTION פעמים כמספר VALUE` is not an A15 alias.

## 3. Semantic mapping

Both profiles map to B13 `RepeatExactly(N,A)`:

1. determine N once at recurrence entry;
2. if determination errors/diverges, no iteration starts;
3. N=0 performs A zero times;
4. N=1 performs A once;
5. otherwise perform the same admitted action exactly N times unless an iteration errors/diverges;
6. mutations performed by A do not cause the count expression to be observed again;
7. no implicit result collection is formed.

The zero case exists for dynamic/computed N even though A15 still has no direct cardinal zero literal.

## 4. Attachment

`פעמים COUNT_AS_NUMBER` cannot attach backward. It modifies only the immediately following complete atomic action by grammar. An explicit later `ואחרי כן B` lies outside the recurrence unless the first action is itself a named act that performs a composite sequence.

No layout, punctuation, or nearest-clause heuristic affects this boundary.

## 5. Evidence and controlled deviation

The Megillah repeatedly says `פעמים כמספר ...`, including `קח אבן החיטה פעמים כמספר המעשה`. Biblical counted-action evidence includes 2 Kings 13:19 `שלש פעמים תכה`. A15's prefix-only dynamic profile is a controlled deviation made to preserve the already frozen A3 count-before-action attachment direction.

## 6. Rejection

Reject bare `פעמים`, wrong gender count forms such as `שבעה פעמים`, postposed dynamic count, the redundant/noncanonical `פעמים כמספר המספר ...`, reevaluation of the dynamic count per iteration, implicit loop index, implicit block scope, or zero being treated like A13's execute-once post-action recurrence.
