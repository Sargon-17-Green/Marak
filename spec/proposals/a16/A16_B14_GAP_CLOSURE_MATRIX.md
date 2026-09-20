# A16 — B14 Gap Closure Matrix
A16 may claim only closure for B15 review.

| Gap | Exact construction(s) | B13 target | Positive evidence | Negative evidence | Ambiguity | Status |
|---|---|---|---|---|---|---|
| B14-A-SURFACE-GAP-001 | typed initializer; typed current-place heads; typed `שים ... תחת ...` | B-VAL-POST-001 state carrier over one fixed domain | Programs A/B/C + state tests | wrong-domain init/replace; implicit deref | resolved by typed initializer + explicit heads | CLOSED_FOR_B15_REVIEW |
| B14-A-SURFACE-GAP-002 | `יעמד DOMAIN_HEAD תחת הדבר`; typed `בהיות`; typed current-role head | B-VAL-POST-001 occurrence role association | Programs A/B/C + role tests | wrong domain; role identity as Value | owner+role+domain explicit | CLOSED_FOR_B15_REVIEW |
| B14-A-SURFACE-GAP-003 | typed `הוצא`; typed `... אשר יצא עתה ...` | B-VAL-POST-001, B-OBS-002 zero/one product + provenance | Programs A/B/C + output tests | wrong head; stale; second output; mixed sites | one exact act output domain | CLOSED_FOR_B15_REVIEW |
| B14-A-SURFACE-GAP-004 | `מספר השנה אשר אחר I`; `מספר השנה אשר לפני I` | B-IDX-001 succ/pred | zero-crossing grid + Program B | Natural operand/underflow promotion/standalone אין | year-profile operand required | CLOSED_FOR_B15_REVIEW |
| B14-A-SURFACE-GAP-005 | typed `SYMBOL_A הוא SYMBOL_B` within one D | B-SYM-001 identity equality | Program A + label-collision test | Text/label/id/cross-domain operands | operand domains source-resolved | CLOSED_FOR_B15_REVIEW |

No semantic mismatch or new Master question is asserted by A16; B15 must independently verify every mapping.
