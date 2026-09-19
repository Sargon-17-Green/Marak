# B12 Completion and Outcome

## Core execution outcome

Conceptually:

\[
Outcome = Normal(S,O)\mid Error(S,E)\mid Divergence.
\]

`S` is the semantic state at successful completion or at the point a fatal defined error stops
execution.

`O` is the projection of explicit act-produced outputs defined by Core semantics.

`Divergence` has no final state.

## Normal completion

Normal completion is exhaustion of the computation explicitly requested by the source.

For an act:
- all reached body units complete;
- no further body continuation remains.

For a program:
- Principal exhausts;
- every performed act needed on the reached path completed;
- no explicit continuation remains.

Normal completion is not:
- HALT;
- exit;
- return;
- Unit;
- exit code.

## Runtime error

A defined fatal Core runtime error:
- stops the current execution;
- is not a value;
- is not an act output;
- is not catchable in Core v0.1;
- prevents later sequence continuation;
- preserves effects of already completed actions;
- does not commit the failing action's not-yet-completed state write.

## Divergence

Divergence is legal nontermination.

It is not a runtime error.

A test harness may use fuel to witness continuing execution, but fuel exhaustion is not a language
error or language result.

## Result production

`הוצא` establishes the optional numeric output of the current occurrence.

It does not terminate the occurrence.

A later body action may still execute.

A13 Core permits zero or one output per occurrence.
