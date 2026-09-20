# A15 — Negative Grammar

A13 negatives remain in force. This file adds the exclusions required by the seven post-M2 families.

## Symbols

Reject a bare source identity as a Symbol Value; a visible label as a member reference; punctuation/quotes/maqaf/newline as label delimiters; omitted label word count; dynamic symbol minting; source-name-to-symbol conversion; label-based equality; order from spelling or declaration order.

## BidirectionalIndex year profile

Reject standalone `אין`; `אפס` as index origin; `מינוס N`; untyped `N לפני אין`; generic signed arithmetic; implicit Natural/BidirectionalIndex conversion; use of B12 Natural subtraction to obtain before-origin Values.

## Collections

Reject a plural noun becoming a collection by itself; heterogeneous books; source declaration order becoming runtime order; bracket/subscript notation; zero-origin positions; mutation of a book Value; bare value-successor where duplicates can make occurrence ambiguous; deletion/slicing/capacity/storage identity; comparator callbacks; sorting Symbols by label spelling.

The phrases `ספר מספרים אשר אין בו מספר` and analogous typed empty forms are admitted only because the preceding book-kind head fixes the sole possible element domain. Untyped `ספר שאין בו דבר` is not an A15 empty constructor.

## Numeric ordering

Reject `רב A מן B`, `A רב B`, automatic `מעט` or `ימעט` aliases, source-visible LE/GE in this edition, symbolic comparison operators, Boolean result storage, and mixed-domain comparison by expected type.

## Numerals

Reject Arabic digits as source numerals; `רבבה` as an A15 alias; a larger magnitude after a smaller one; repeated magnitude slots; direct cardinal `אפס`; interpreting 99,999,999 as a Natural semantic maximum.

## Counted recurrence

Reject bare `פעמים`; incorrect count agreement; postfix dynamic `ACTION פעמים כמספר VALUE`; dynamic count reevaluation per iteration; hidden loop counter; count attachment by punctuation or nearest-clause heuristic; implicit block scope; treating dynamic zero as one performance.

## Program Input Roles

Reject positional association; declaration-order association; caller raw-spelling association without resolved role identity; `main`; stdin/argv/HTTP/environment semantics; a mutable input role; input replacement wording; principal execution with a missing required binding; hidden defaults.

## Charter invariance

For every A15 construction, punctuation is erased, Markdown is irrelevant, normative whitespace runs collapse, line breaks do not create scope, Latin letters and Arabic digits are transparent, and niqqud/cantillation do not carry syntax. A15 creates no text-literal exception.
