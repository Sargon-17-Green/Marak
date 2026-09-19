# Diagnostic Catalog

Diagnostics are stable, structured, bilingual and source-mapped where applicable.

| Code | Meaning |
|---|---|
| `LEX0001` | string syntax requested but not specified (outside Core) |
| `PARSE0001` | selected historical snapshot has no admitted root grammar |
| `PARSE0002` | admitted grammar exists but source has no complete parse |
| `AMBIG0001` | multiple legal parses remain without proven equivalence |
| `AMBIG0002` | multiple legal parses have proven distinct semantics |
| `PROG0001` | no top-level principal `ועתה` |
| `PROG0002` | multiple top-level principal transitions |
| `PROG0003` | preparatory material after principal transition |
| `PROG0004` | unsequenced principal executable material |
| `REF0001` | explicit co-reference slots disagree |
| `REF0101` | reference before introduction / no hoisting |
| `REF0102` | duplicate Place identity |
| `REF0103` | duplicate Act identity |
| `REF0104` | duplicate Role for one Act |
| `REF0105` | duplicate Act body |
| `REF0106` | self initializer |
| `REF0107` | role owner not introduced |
| `REF0108` | role declared after body boundary |
| `REF0109` | body owner not introduced |
| `REF0110` | role value outside owning performance occurrence |
| `REF0111` | invalid/incomplete/duplicate role association profile |
| `REF0112` | structurally stale immediate result reference |
| `REF0113` | immediate result names wrong directly preceding Act |
| `REF0114` | output production outside current performance |
| `SEM0012` | more than one Core output production on a performance path |
| `SEM0201` | statically provable Natural subtraction domain failure |
| `INTERNAL0001` | canonical model/module ownership violation |

Runtime semantic codes are distinct from source diagnostics. Current defined runtime errors include `ARITHMETIC_DOMAIN_ERROR` and `RESULT_PROVENANCE_ERROR`; malformed validated-IR contexts have defensive internal codes but are rejected by normal compiler/verifier paths.
