# B12 Natural Subtraction Failure

A13 surface construction:

`גרע A מן B`

has semantic order:

\[
B-A.
\]

## Success

For \(A,B\in\mathbb N\):

\[
A\le B
\]

implies:

\[
SubFrom(A,B)=B-A\in\mathbb N.
\]

Examples:
- \(3-2=1\);
- \(3-3=0\).

## Domain failure

If:

\[
A>B,
\]

no Core value exists for this operation.

The stable semantic error category is:

`ARITHMETIC_DOMAIN_ERROR`

### Validation-time proof

If a sound validator proves \(A>B\) before execution:

\[
Program\Rightarrow InvalidProgram(ARITHMETIC\_DOMAIN\_ERROR).
\]

This is not a runtime exception.

### Execution-time discovery

If the relation depends on runtime state/role values and execution reaches the operation with
\(A>B\):

\[
\langle SubFrom(A,B),S\rangle\Downarrow RuntimeError(ARITHMETIC\_DOMAIN\_ERROR).
\]

## Forbidden alternatives

The implementation must not:
- wrap;
- clip to zero;
- produce a negative Core value;
- promote to signed integer;
- leak a backend exception;
- invoke undefined behavior.

## Effect boundary

Core numeric descriptions are pure.

For executable replacement:

1. compute replacement datum;
2. only after successful computation, establish the replacement transition.

Thus, if RHS subtraction fails, the replacement itself performs no state transition.

If:

\[
S_0\xrightarrow{A_1}S_1
\]

and the RHS of \(A_2\) fails, the error state is \(S_1\).

There is:
- no rollback to \(S_0\);
- no partial state of \(A_2\);
- no continuation to later `ואחרי כן` actions.

## Preparation

The same numeric rule applies to preparatory initial-value calculations.

A preparation-time domain failure prevents principal execution.

Earlier completed preparatory establishments are not retroactively rolled back; the program outcome is
an error and no executable phase begins.
