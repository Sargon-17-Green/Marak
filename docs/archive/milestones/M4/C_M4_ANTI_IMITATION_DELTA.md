# C M4 — Anti-Imitation Delta

| Component | Classification | M4 conclusion |
|---|---|---|
| `CoreProgram` Preparation/Principal split | LANGUAGE-DERIVED | follows A13 `ועתה`; not a conventional main function |
| preparation order | LANGUAGE/SEMANTICS-DERIVED | discourse visibility/dependency only; not executable statement order |
| Place identity/current fact | SEMANTICS-DERIVED | no exposed variable/cell/pointer ontology |
| typed PlaceId/ActId/RoleId | IMPLEMENTATION-ONLY representation of specified identities | stable IDs remove string lookup; do not add user-visible types |
| Act occurrence | LANGUAGE + SEMANTICS-DERIVED | not a user-visible stack frame/function activation |
| role association | LANGUAGE-DERIVED | identity correspondence; positional ABI may exist only internally |
| output product | LANGUAGE + SEMANTICS-DERIVED | not abrupt `return`; later body actions execute |
| proposition | SEMANTICS-DERIVED | branch judgment, not Boolean Value |
| post-action recurrence | LANGUAGE + SEMANTICS-DERIVED | dedicated checkpoint semantics; backend loop is implementation-only |
| checked subtraction | SEMANTICS-DERIVED | Natural-domain obligation; signed host arithmetic cannot leak |
| canonical IR | IMPLEMENTATION-ONLY | low-level representation may be conventional, but each opcode corresponds to an already justified semantic distinction |
| portable VM registers/stack/control | IMPLEMENTATION-ONLY | not reflected into A/B ontology |

Static audit finds no canonical class/function ontology named `Function`, `Parameter`, `Return`, `Frame`, `While`, `BooleanValue` or `Statement`, no canonical import from historical `reference_models`, and no Megillah/calendar-specific special case.
