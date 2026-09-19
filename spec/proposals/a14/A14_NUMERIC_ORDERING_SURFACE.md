# A14 — Numeric Ordering Surface

Status: **SURFACE_READY**

## Need

The Megillah repeatedly needs a proposition that distinguishes which of two numeric Values is larger.

Equality is already frozen in A13. Encoding strict order through repeated subtraction or recursion is
computable but is not a local or linguistically faithful repair.

## Preferred canonical construction

    VALUE_A רב מן VALUE_B

Semantic relation requested from B:

    A > B

Valency is fixed:

| Surface role | Semantic role |
|---|---|
| VALUE_A | compared number asserted to be greater |
| `רב` | strict greater relation |
| `מן VALUE_B` | comparison baseline |

Biblical Hebrew directly uses this comparative frame, e.g. `עם רב ממך` and `כי רב ממך הדרך`.

## Less-than

A14 adds no independent `מעט מן` canonical predicate.

To express A < B:

    VALUE_B רב מן VALUE_A

This keeps one strict-order relation and prevents two surface forms from becoming inconsistent.

`מעט`, `ימעט` and similar historical Megillah forms remain D repair evidence, not aliases accepted by
A14.

## Equality and non-strict order

Equality remains:

    A הוא B

A14 does not add ≤ or ≥. If later source work demonstrates that a single non-strict proposition is
needed, that is a separate request. Combining two propositions must use admitted control language; no
new Boolean algebra is inferred.

## Proposition boundary

`A רב מן B` is a proposition used by control. It is not:
- a Boolean runtime Value;
- a number;
- a symbolic comparison result;
- a `<`/`>` token with Hebrew spelling.

## Negative grammar

Reject:
- `רב A מן B` as an alias;
- `A רב B` without `מן`;
- `A רב מן B מן C`;
- using `מעט` as automatic inverse syntax;
- operand reversal inferred from type or expected result;
- storing the proposition as a Value absent a later feature.

## A/B integration

A's surface relation is ready. B must supply the straightforward strict order judgment over whatever
numeric domain is active in the integration edition. For A13 Naturals this is ordinary strict natural
order.
