# B13 Observable Behavior

B12 observation remains the base: normal completion, defined runtime error, divergence, semantic state, and explicit act outputs.

## Symbol
Observable output identifies the declared Symbol member through its canonical external label. Allocation address, intern-table slot, compiler symbol index, and source entity name are not observable.

## BidirectionalIndex
Observation distinguishes `BeforeZero(n)`, Zero, and `AfterZero(n)` with exact unbounded magnitude. Host signed width and sign encoding are unobservable.

## Collection
Observation is finite length, order, and recursively observable element values. Capacity, node shape, backing array/list, hash, sharing, and allocation identity are not observable.

## Ordering propositions
Only satisfaction and consequent control effects are observable. There is no first-class Boolean result.

## Counted recurrence
Observable behavior is ordinary action effects/outputs in iteration order and the final outcome. There is no observable loop index, iterator object, hidden counter, or host call depth.

## Program inputs
The association between each ProgramInputId and supplied value is part of invocation context. Transport format and binding order are not observable. Bad association sets fail as InvalidInvocation before Preparation.

## Trace
B12 remains unchanged: internal execution trace, stack depth, activation layout, backend registers, and instruction count are not program-visible.
