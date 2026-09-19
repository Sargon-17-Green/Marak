# B13 Anti-Imitation Audit

| Request | Actual need | Familiar analogue | Alternatives considered | Chosen semantic model | Independent justification |
|---|---|---|---|---|---|
| 001 | fixed runtime calendar labels | string/enum | general Text; numeric codes; atoms | finite declared Symbol values | source has closed named sets and no text-editing requirement |
| 002 | count through zero both ways | signed int | generic Integer; Year primitive; exposed sign/magnitude pair | BidirectionalIndex | required operations are successor/predecessor/order around zero, not general signed arithmetic |
| 003 | runtime ordered books/permutations | list/array | numeric encoding; mutable list; records | immutable finite ordered homogeneous Collection | source observes order/content, not storage identity/mutation |
| 004 | רב/ימעט decisions | comparison operator returning bool | subtraction encoding; Boolean comparison | ordering propositions | source states relations used by control; B12 proposition model already fits |
| 005 | large Biblical numerals | big-int literal | fixed-width literal; separate big-number type | no new B model | B12 Natural already has arbitrary magnitude |
| 006 | exactly N performances | for-loop | recursion rewrite; changing count; hidden index | count-once exact recurrence | phrase denotes requested cardinality, no iterator/index need |
| 007 | supplied named day values | function args/stdin | external places; positional inputs; environment variables | Program Input Roles | source describes named external inputs; transport/mutability are separate concerns |

## Leakage checks
- no Python `str`, `int`, `list`, tuple, or iterator is normative;
- reference code may use host structures only as a witness;
- no conventional `main`, input stream, exception stack, or stack-frame ontology is added;
- no generic Integer is added merely because years resemble signed integers;
- Symbol equality is not spelling equality;
- collection positions are not inherited from host zero-based indexing;
- counted recurrence has no hidden loop variable.

No preferred B13 model remains `POSSIBLY-IMITATIVE`; remaining similarities are implementation techniques only.
