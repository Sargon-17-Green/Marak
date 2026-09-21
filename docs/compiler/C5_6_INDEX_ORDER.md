# C5.6 — Strict BidirectionalIndex Order

Status: production-integration candidate.

## Surface

C5.6 admits one new proposition surface:

```text
INDEX_VALUE_A לפני INDEX_VALUE_B
```

This is proposition satisfaction, not a Boolean Value.

## Semantic representation

The minimal new semantic nodes are:

- `HastIndexLTProposition(left, right)`
- `IRIndexLTProposition(left, right)`

Both operands are existing semantic Values and must independently have domain `BIDIRECTIONAL_INDEX`.

The resolver does not use expected type to rescue malformed source.

## Order law

Runtime evaluation is centralized in `compiler.models.values.index_lt`.

The strict total order is the B13/B16 law:

1. every BeforeZero value precedes Zero and every AfterZero value;
2. Zero precedes every AfterZero value;
3. among BeforeZero values, larger magnitude is earlier;
4. among AfterZero values, smaller magnitude is earlier;
5. equal values never satisfy strict order.

The helper deliberately operates on the existing side/magnitude semantic representation. It does not expose a signed host integer, Natural coercion, source profile, or object identity.

## Runtime parity

The same helper is used by:

- HAST reference runtime;
- canonical-IR reference runtime;
- portable backend.

No independent per-runtime order algorithm is maintained.

## Domain validation

HAST domain validation requires both operands to be `BIDIRECTIONAL_INDEX` and emits semantic code `DOMAIN_INDEX_LT` for forged wrong-domain HAST.

Canonical IR validation independently requires both operands to be `BIDIRECTIONAL_INDEX` and emits `IR_INDEX_LT_DOMAIN` for forged wrong-domain IR.

HAST proposition validation is shared by conditional and post-action recurrence contexts; canonical IR already validates propositions in both contexts.

## Parsing boundary

The production is:

```text
IndexValue לפני IndexValue
```

and therefore interacts with `לפני` inside Index literals and predecessor expressions.

The source suite includes the explicit case:

```text
מעלה אחת לפני מעלת היתד לפני מעלת היתד
```

and requires the parser to resolve the full left `IndexValue` before the proposition separator.

No longest-match heuristic or expected-type repair is added.

## Same-position adequacy

C5.6 does not add Index equality.

Actual Marak source proves three-way classification through:

1. `A לפני B`;
2. false branch performs one named decision act;
3. that act tests `B לפני A`;
4. false again means same position.

This respects frozen Core's atomic branch-action rule.

## Distance boundary

No distance primitive is present.

The C5.6 source suite contains a constructive small-distance algorithm using:

- strict Index order;
- general successor/predecessor;
- retained Natural counter;
- named acts;
- ordinary Core conditionals and recursive performances.

It covers forward zero crossing, backward zero crossing, and same-position zero distance.
