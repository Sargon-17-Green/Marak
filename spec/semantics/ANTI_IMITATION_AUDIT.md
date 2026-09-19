# B Anti-Imitation Audit — Current through B12

| Component | Current model | Source of justification | Imitation risk | Alternatives checked | Decision |
|---|---|---|---|---|---|
| numeric data | exact Naturals | A13 + M1 | low | signed integer promotion | ℕ Core |
| subtraction | partial Natural operation | A13 | medium | wrap/clip/signed promotion | defined domain failure |
| state | referent + current fact | computation/A language | low | variable/cell | retained |
| replacement | explicit state transition | A13 | low | assignment operator ontology | retained |
| proposition | satisfaction judgment | control need/A13 | low | Boolean Value/truthiness | retained |
| sequence | explicit temporal relation | Hebrew surface | low | source statement order | retained |
| recurrence | post-action source checkpoint | A13 | low | while/do-while default | retained |
| act | described reusable computation | A13 | medium | function object | retained as act/occurrence |
| role input | occurrence-specific named relation | A13 | low | positional parameter/cell | retained |
| output | optional occurrence product | A13 | medium | abrupt return/stdout | retained |
| program | Preparation + Principal | A13 discourse | medium | main/top-level statements | selected |
| visibility | introduced-before-use typed identity | A13 discourse | medium | hoisting/dynamic lookup | selected |
| completion | ordinary exhaustion | A13 | medium | HALT/exit/main return | selected |
| runtime failure | fatal defined outcome | partial operation need | medium | exception stack/UB | defined error without exceptions |
| trace | internal diagnostic | no source observation | low | observable execution log | non-observable |

Detailed B12-specific reasoning is in `B12_ANTI_IMITATION_DELTA.md`.

No B12 decision is justified solely by "ordinary languages do it this way."
