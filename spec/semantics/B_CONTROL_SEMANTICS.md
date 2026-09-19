# B-Core v0.1 Control Semantics — A13

## Sequence

Only explicit A13 temporal sequence has execution-order force.

A then B:
- A Normal → B starts in successor state;
- A Error → B not started;
- A Divergence → B not started.

## Proposition

Control observes a proposition by satisfaction:

\[
S\models P.
\]

No Boolean Value is required.

## Conditional
Determine proposition once for that conditional occurrence and execute exactly one selected action.

## Fixed counted recurrence
Individually A-audited Natural counts perform the designated action exactly that many times.

## Post-action recurrence
A13 construction:
1. action once;
2. proposition on successor state;
3. if satisfied, complete;
4. otherwise repeat.

This is not a generic `while`.

## Failure
A control construct propagates fatal runtime error and does not select/continue past the failure.
