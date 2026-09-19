# A14 — Negative Grammar

This file collects A14-specific near misses. A13 negatives remain in force.

## Runtime symbols

Reject:
- a source act/place/role name used directly as a runtime symbolic datum;
- quoted punctuation as a text delimiter without a new lexical specification;
- an unbounded multiword symbolic literal whose end is inferred from punctuation or newline;
- treating a numeric month code as automatically equal to its human name.

## Year designations

Reject:
- `מינוס NUMERAL` as an A14 integer literal;
- treating `אין` as the general numeric zero token;
- treating `שנת אין` as absence/null;
- applying numeric subtraction to a year designation unless B explicitly defines such arithmetic.

## Ordered data

Reject:
- any plural noun becoming a collection Value merely because it is plural;
- collection order from source declaration order alone;
- zero-based or one-based indexing by convention;
- "latest write wins" semantics unless the source collection construction says how change occurs;
- `הראשון`/`האחרון` without a unique owning ordered relation.

## Numeric ordering

Reject:
- `רב A מן B`;
- `A רב B`;
- `A רב מן B מן C`;
- automatic `מעט`/`ימעט` aliasing;
- a storable Boolean result from comparison.

## Productive numerals

Reject:
- Arabic digits as semantic numeral source;
- a second accepted spelling merely because it is understandable Biblical Hebrew;
- `רבבה` as an A14 canonical alias to the controlled `אלף`/`אלף אלפים` system;
- a scale component following a smaller scale in canonical form;
- repeated same magnitude slots;
- direct zero `אפס`.

## Counted recurrence

Reject:
- `פעמים` without an exact admitted count;
- `שבעה פעמים` where the controlled REPEAT_COUNT requires `שבע פעמים`;
- a count phrase whose repeated action boundary is selected by nearest-clause heuristic;
- `שבע פעמים A ואחרי כן B` as repetition of both A and B;
- dynamic count reevaluation by implementation default;
- assuming count zero executes once because another recurrence construct does.

## External input

Reject:
- positional binding;
- declaration-order binding;
- stdin/argv/file semantics inferred from "external";
- principal execution beginning with a required input unbound;
- an external binding mutating a random same-spelled referent of another typed kind.

## Punctuation/layout

For every A14 construction outside any future text-literal boundary:
- punctuation remains transparent;
- Markdown remains transparent;
- A13 whitespace normalization remains exact;
- line breaks do not establish attachment, ordering or scope.
