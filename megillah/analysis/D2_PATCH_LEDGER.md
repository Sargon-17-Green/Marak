# D2 Patch Ledger

No patch is applied to `megillah/original/`. Approval states describe evidence only.

| Patch | Span(s) | Classification | Preservation | Approval | Replacement |
|---|---|---|---|---|---|
| D-PATCH-0001 | line 1267 | SOURCE_PROGRAMMING_BUG | ALGORITHM_CHANGE | MASTER_APPROVAL_REQUIRED | `חמשת אלפים ושבע מאות ושבעים ושמנה` |
| D-PATCH-0002 | line 23, line 147 | SOURCE_AMBIGUITY | DISAMBIGUATION_ONLY | MECHANICALLY_CONFIRMED | `יהי מעשה ושמו NAME` |
| D-PATCH-0003 | line 237 | SOURCE_AMBIGUITY | DISAMBIGUATION_ONLY | PROPOSED | `וכן תעשה עד אשר` |
| D-PATCH-0004 | line 173, line 341 | SOURCE_NOT_LANGUAGE | SEMANTIC_EQUIVALENT | PROPOSED | `ואחרי כן` |

## Important
D-PATCH-0001 is semantically well supported but changes the erroneous algorithmic bound and therefore remains Master-gated.
D-PATCH-0002 repairs only act identity introduction; it does not repair body/roles.
D-PATCH-0003 and D-PATCH-0004 do not make their surrounding historical clauses Core-valid by themselves.
