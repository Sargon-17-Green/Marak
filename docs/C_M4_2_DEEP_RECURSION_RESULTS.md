# C M4.2 Deep Recursion Results

Direct C-side remediation tests exercise all three execution layers.

| Scenario | Result |
|---|---|
| depth 5,000 | Normal in HAST / IR reference / backend |
| depth 10,001 | Normal in all three |
| depth 20,000 | Normal in all three |
| 20,001 sequential performances | Normal; no cumulative quota |
| Python `recursionlimit=80`, Marak depth 1,000 | Normal in all three |
| explicit `max_active_performances=100` | caller-imposed ResourceExhaustion in all three |
| same program with default budget | Normal |
| infinite self recursion, no fuel | remains executing until external timeout |
| completed depth 5,000 engines | `active_performances == 0` |

The maximum finite depth actually tested in M4.2 is **20,000**.
