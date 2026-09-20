# B15 Anti-Imitation Integration Audit

The five repairs provide capabilities familiar from conventional languages, but their semantics remain
independently justified by Marak source needs.

## Typed variables?
Places now have fixed semantic domains, but there is no generic type declaration, implicit
dereference, reference alias, object identity or polymorphic assignment. The domain contract is needed
to make non-Natural source descriptions unambiguous.

## Function parameters?
Named act roles carry typed values, but association is source-named and occurrence-specific, immutable,
non-positional, non-aliased, and not a parameter cell.

## Return types?
An act output domain is derived from all resolved output sites; there is no declared return type.
`הוצא` is nonterminal and completion remains body exhaustion.

## Enum/string equality?
Symbol equality compares semantic member identity. Visible labels remain non-Text presentation metadata.

## Signed integers?
BidirectionalIndex supports only the justified Index algebra; succ/pred crossing zero does not import
generic signed arithmetic or Natural promotion.

Verdict: **no imitation-driven semantic widening**.
