# B13 Requirements for A14

B13 selects no Biblical wording. A14 must make these semantic distinctions recoverable from source.

## Symbol
- distinguish runtime Symbol member declaration from compile-time entity naming;
- establish member/domain identity and a canonical observable label;
- never imply automatic entity-name→Symbol conversion;
- permit an explicit symbol-domain order/rank where the source needs it.

## BidirectionalIndex
- distinguish Index from Natural;
- unambiguously denote zero, before-zero, and after-zero values;
- preserve explicit conversion boundaries; Natural underflow must not silently become Index.

## Collections
- distinguish construction from reference to an existing collection;
- identify append/selection/count/traversal meanings;
- preserve positive 1..count semantic positions;
- make ordering relation and operand direction explicit;
- permit nested homogeneous collections needed by books-of-books/permutations.

## Numeric ordering
Strict less/greater direction must be unique. If non-strict constructions are admitted, they map to LE/GE without first-class Boolean values.

## Large numerals
Define productive Biblical numeral denotation beyond 9999, exact over Natural and without semantic ceiling.

## Counted recurrence
Identify exactly one repeated admitted action and one Natural count description; the count is fixed once on entry; no hidden loop index. Composite work must be explicitly named/performed if A keeps the one-action boundary.

## Program inputs
- distinguish Program Input Roles from act roles and mutable places;
- each input has identity and declared semantic domain;
- external association is named, never positional;
- source does not prescribe stdin/argv/HTTP transport;
- Preparation may read input roles but cannot replace them.

## Cross-domain use
A must give the resolver enough linguistic information to know the semantic domain of non-Natural places, roles, inputs, and outputs. This need not look like a conventional type annotation.
