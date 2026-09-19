# B14 Anti-Imitation Audit — Integrated A15+B13

| Need | Familiar analogue tested | Integrated model | Verdict |
|---|---|---|---|
| fixed runtime names | enum/string | finite atomic Symbol + label metadata | independently justified |
| numbering across zero | signed int | BidirectionalIndex | no generic signed arithmetic |
| ordered books | list/array | immutable finite ordered value | no mutation/capacity/zero index |
| comparison | bool operator | proposition | no Boolean Value |
| N-times execution | for-loop | count-once one-action recurrence | no iterator/index |
| supplied program values | main/function parameters | Program Input Roles | named contract; no stdin/position |
| mutable working data | variable syntax | state-bearing referent + explicit replacement | semantic need, wording still A-owned |
| reusable data flow | typed parameters/return | named roles + zero/one production + provenance | no stack-frame/return semantics |

The composition does not accidentally reconstruct a conventional language. The blockers exist because
B14 refuses conventional genericization: numeric places are not assumed polymorphic variables, numeric
roles are not assumed generic parameters, numeric output is not assumed a polymorphic return, year
literals are not signed integers, and ordinal book positions are not array indexes.

A16 must close the gaps with independently justified Hebrew constructions, not generic type syntax,
function signatures, mutable-list conventions, or implicit coercions.
