# E-FIND-023 Closure

## Original defect
C M4.1 replaced Python stack dependence with explicit activations but imposed a fixed default 10,000 active-performance ceiling. This created an artificial semantic-depth boundary.

## M4.2 independent checks
- All three exported defaults and signatures use `max_active_performances=None`.
- Runtime-source scan found no alternate finite default/fallback in the three execution engines.
- Independent finite recursion: depth 4,999, 5,000, 10,001, 20,000 and 25,000 all complete normally in HAST reference, IR reference and portable backend.
- 20,001 sequential performances complete normally; therefore there is no cumulative total-performance quota.
- `sys.setrecursionlimit(80)` does not affect Marak depth 1,000.
- No-fuel infinite self recursion remains executing in all three layers until an external E timeout terminates the subprocess.
- Explicit caller `max_active_performances=100` still produces implementation-resource exhaustion labelled `caller-imposed`; the identical source without that option completes normally.
- After deep finite execution, `active_performances == 0`; repeated runs do not leak activation state.
- Deep semantic observations are equal across all three execution layers.

## Host failure boundary
The implementation still maps `MemoryError`/host resource failures to implementation-resource exhaustion. E did not attempt unsafe real OOM induction.

## Verdict
**E-FIND-023 CLOSED.** No fixed/artificial default recursion or performance-count ceiling was found.
