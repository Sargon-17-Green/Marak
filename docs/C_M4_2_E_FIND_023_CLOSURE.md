# C M4.2 — E-FIND-023 Closure

## Defect

M4.1 removed host recursion but supplied `DEFAULT_MAX_ACTIVE_PERFORMANCES = 10_000`. This caused finite legal programs to return `IMPLEMENTATION_RESOURCE_EXHAUSTION` solely because an arbitrary counter reached a constant.

## Correction

All execution layers now define `DEFAULT_MAX_ACTIVE_PERFORMANCES = None`. Quota checks execute only when a caller explicitly supplies a finite value. The explicit-budget outcome detail identifies the boundary as `caller-imposed`.

## Evidence

- finite recursion depths 5,000, 10,001 and 20,000 complete normally in all three execution layers;
- 20,001 sequential completed performances run with no cumulative-count ceiling;
- Python recursion limit 80 does not affect depth-1,000 Marak recursion;
- self recursion without fuel remains executing until external subprocess timeout in each execution layer;
- explicit caller budget 100 still stops execution as a tooling/resource-control outcome, while the same program is Normal under defaults;
- completed engines report zero active performances.

No maximum Marak recursion/performance depth was introduced.
