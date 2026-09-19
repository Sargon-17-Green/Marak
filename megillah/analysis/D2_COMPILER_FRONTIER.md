# D2 Compiler Frontier

Baseline commit: `8a3a25e2fb5e438b01fef9694570f20d16a34ff3`
Compiler: `0.4.2-alpha.1`
Edition: `core-0.1-integration-candidate-a13-b12`

## Original source
`marak check megillah/original/Megilat_HaItim_Yehuda_FINAL_2026-09-18.md`:
- normalization: succeeds;
- parse/program composition: fails;
- `PROG0001`: exactly one recognized top-level `ועתה` required; grammar marker count = 0;
- `PARSE0002`: no admitted construction at normalized token 0, source line 1;
- resolve: not reached; validate: not reached; execute: not reached.

The source contains one lexical `ועתה` at physical line 169, but it is not recognized as the program transition because the preceding document is not valid A13 Preparation and many definitions follow it.

## Iteration 2 — diagnostic probe only
A scratch probe removed the documentary prefix before historical line 23 and changed only `יהי שם מעשה חיבור` to `יהי מעשה ושמו חיבור`.
The parser advanced to normalized token 4 and then failed at the following `וזה דבר החיבור...`.
This shows that the next concrete frontier is A13 act-body/role structure, not Markdown alone.

No probe is an accepted source patch.
