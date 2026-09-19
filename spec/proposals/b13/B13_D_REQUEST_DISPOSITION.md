# B13 D2 Request Disposition

| ID | Need accepted? | Core workaround viable? | Preferred model | Main rejected alternatives | New capability | A dependency | Status |
|---|---|---|---|---|---|---|---|
| 001 | yes | computable but not local/reasonable | finite declared Symbol domains | numeric codes only; general Text now | Symbol values | symbol/member declaration and denotation | SEMANTIC_MODEL_READY |
| 002 | yes | sign+magnitude encoding possible but material rewrite | BidirectionalIndex | generic Integer Core; calendar-specific Year primitive; exposed pair encoding | bidirectional index | before/zero/after-zero denotation | SEMANTIC_MODEL_READY |
| 003 | yes | Gödel encoding possible but unacceptable | immutable finite ordered homogeneous Collection | mutable list/array; heterogeneous universal container; record requirement | collection values | construction/selection/order/traversal | SEMANTIC_MODEL_READY |
| 004 | yes | equality/recursion encoding possible but non-local | Natural LT/GT, derived LE/GE propositions | Boolean comparisons; machine-width compare | ordering propositions | operand direction/strictness | SEMANTIC_MODEL_READY |
| 005 | yes | computed constants possible but source-distorting | no B change; exact Natural literal denotation has no ceiling | fixed-width literal; new large-number type | none | productive Biblical numeral grammar | AWAITING_A |
| 006 | yes | named recursion works but is non-local | count once; repeat one admitted action exactly N times | host `for`; re-evaluate N; hidden iterator/index | counted recurrence | unambiguous action/count boundary | SEMANTIC_MODEL_READY |
| 007 | yes | hard-coded places work only for fixed query | named immutable Program Input Roles per invocation | stdin/argv; positional args; externally writable places | invocation contract | input declaration + named association | SEMANTIC_MODEL_READY |

### B12 interaction
001–003 extend available declared value domains; they do not reinterpret Natural. REQUEST-004 plugs into existing proposition/conditional semantics. REQUEST-006 composes existing action outcomes. REQUEST-007 establishes an immutable invocation context before B12 Preparation. REQUEST-005 is surface-only from B's perspective.

No request changes `megillah/original/` in B13.
