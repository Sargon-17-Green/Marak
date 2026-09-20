# A16 — Anti-Imitation Audit
Status: proposal evidence for B15.

| Capability | A16 source model | Conventional imitation rejected | Result |
|---|---|---|---|
| typed state | `מקום` + typed initializer/content description | typed variable/address/cell | PASS |
| replacement | `שים ... תחת CURRENT` | assignment operator/mutable collection | PASS |
| act roles | named `דבר`, domain stated by `יעמד ... תחת` | parameter slots/positional args | PASS |
| current role | `המעשה הזה` occurrence deixis | stack frame/caller lookup | PASS |
| output | `הוצא מן המעשה הזה את ...` | return statement/unwind | PASS |
| immediate result | `... אשר יצא עתה מן המעשה ...` | function return register/global last-result | PASS |
| Index step | `אחר` / `לפני` year relation | `++`, `--`, signed Integer arithmetic | PASS |
| Symbol equality | typed copular `הוא` | string comparison/Boolean operator | PASS |

Places have one source-declared semantic domain but expose no address, pointer, alias token, object slot, or dynamic type.
Collections remain immutable values; state changes only when a place holding a newly computed Collection is explicitly replaced.
Roles remain immutable occurrence associations by semantic role identity.
Output domain is recovered from typed source output sites, not a conventional function signature.
Symbol labels remain presentation metadata, not Text, and are not equality keys.
The year-specific Index surface remains a deliberate A15 narrowing rather than a built-in Year object.
Overall anti-imitation result: PASS_FOR_B15_REVIEW.
