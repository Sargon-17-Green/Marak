# B13 General Exact Counted Recurrence

## B-REP-R06 (PROPOSED)
`RepeatExactly(N,A)` determines a Natural count once at recurrence entry and then performs one admitted executable action A exactly that many times unless an iteration errors or diverges.

## Count determination
The count description is evaluated exactly once before iteration. "N times" fixes the requested cardinality at entry; re-evaluating mutable state each iteration would describe a different continuation rule.

If count determination fails, no iteration begins.

## Laws
- `RepeatExactly(0,A,S)=Normal(S)` and A is not performed.
- `RepeatExactly(1,A,S)` has the outcome of one A.
- `RepeatExactly(n+1,A,S)`: perform A once; only on Normal successor state repeat n more times.
- finite N has no semantic upper bound and does not itself imply divergence; A may diverge.

## Effects/errors
If iteration k errors, completed effects and outputs from iterations 1..k-1 remain; the failing action uses its ordinary B12 commit boundary; later iterations never occur. If A diverges, the recurrence diverges.

Count must be Natural. A non-Natural count surviving validation yields `RECURRENCE_COUNT_DOMAIN_ERROR`.

## Output interaction
There is no implicit collection of results. Repeated `Perform(act)` occurrences may each produce their ordinary zero/one output events in performance order. If recurrence would directly execute `Produce` multiple times in one enclosing occurrence, the existing zero/one-per-occurrence rule still applies; B13 does not weaken it.

## Body boundary
B13 recommends one admitted executable action, not an implicit statement block. Composite work can be named as an act and that performance repeated. This preserves A13's explicit action-boundary discipline while covering D2's `N פעמים` cases.
