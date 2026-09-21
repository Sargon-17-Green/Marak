# B16 Megillah Anti-Imitation Audit

| A17 capability | Primitive relation/value in need? | Source-defined algorithm erased? | Inherent B13 structure? | General utility | Verdict |
|---|---:|---:|---:|---:|---|
| generic Index literals | yes: coordinate Values | no | yes | yes | ACCEPT |
| distinguished origin | yes: ZeroIndex | no | yes | yes | ACCEPT |
| strict order | yes: before/after relation | no | yes | yes | ACCEPT |
| succ/pred | yes: one-step adjacency/traversal | no; preserves counting | yes | yes | ACCEPT |
| generic typed carrier | data-flow necessity | no | B15 domain flow | yes | ACCEPT |
| Program Input profile | external coordinate input necessity | no | B13 input model | yes | ACCEPT |
| role flow | composition necessity | no | B15 role flow | yes | ACCEPT |
| output/result profile | composition necessity | no | B15 provenance | yes | ACCEPT |
| direct distance | no: Megillah says count | **yes** | mathematically available | yes, but over-primitive here | REJECT SURFACE |
| Index equality | not independently needed | no | identity theorem | yes | DO NOT ADD; order suffices |

## Addition precedent

The earlier `חיבור` repair establishes the relevant principle: when the source text defines a
computation as an act, the compiler must not silently replace that source algorithm with a magical
primitive merely because the operation is mathematically familiar.

B16 applies that precedent to direct Index distance: the Megillah describes counting, so direct
distance remains source work.

The precedent does not mechanically ban order or succ/pred. Those are not procedures defined by the
Megillah; they are primitive relational/adjacency structure of the already accepted
`BidirectionalIndex` domain and are the minimal means by which the source can perform the described
count itself.

## Overall verdict

A17 does not turn Marak into a modern unit/type system, signed-integer language, or convenience API.
The accepted operations preserve rather than replace the Megillah algorithm.
