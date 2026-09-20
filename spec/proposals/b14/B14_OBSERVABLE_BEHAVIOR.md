# B14 Integrated Observable Behavior

B12 observations remain normal completion, semantic state, explicit act outputs, defined runtime error,
and divergence. Trace, stack depth, addresses, backend registers, capacity and instruction count remain
unobservable.

Symbol: semantic output is a Symbol in its declared domain; canonical presentation uses normalized
counted label metadata. Raw punctuation/layout and source entity name are not observable. Label metadata
is not Text and is not program-inspectable.

BidirectionalIndex: observation distinguishes BeforeZero(n), ZeroIndex and AfterZero(n) exactly.
Machine sign representation is unobservable.

Collection: observation is finite count, order, and recursively observable element values. Layout,
capacity, sharing and allocation identity are unobservable.

Counted recurrence: effects and ordinary act-output events occur in iteration order. No loop index is
observable. Separate act occurrences may each output once; multiple direct output in one occurrence
remains forbidden.

Program inputs: ProgramInputId→Value associations are invocation context. Binding/declaration order and
transport are unobservable. InvalidInvocation produces no Preparation effect.

B13 observation is semantically coherent for all domains, but A15 lacks non-Natural output surfaces;
that absence is a surface-compositional blocker, not an implementation representation choice.
