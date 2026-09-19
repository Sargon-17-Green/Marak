# C M4.2 Anti-Imitation Delta

| Component | Classification | Reason |
|---|---|---|
| explicit activation/continuation stack | IMPLEMENTATION_ONLY | prevents host recursion; not a Marak stack-frame ontology |
| removal of fixed performance quota | COMPUTATION/SEMANTICS-DERIVED | preserves A13/B12 absence of a semantic depth limit; introduces no feature |
| optional caller budget | IMPLEMENTATION_ONLY | harness/sandbox control, disabled by default |
| `IMPLEMENTATION_RESOURCE_EXHAUSTION` | IMPLEMENTATION_ONLY boundary | host/tool failure, not a language Error or catchable exception |
| active-performance counter | IMPLEMENTATION_ONLY debug state | not in semantic observation quotient |
| canonical IR/backend iteration | IMPLEMENTATION_ONLY | conventional low-level machinery does not imply `while`/call-stack constructs in Marak |

No A13 or B12 rule was changed in M4.2.
