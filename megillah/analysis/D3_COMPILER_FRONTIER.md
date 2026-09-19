# D3 Compiler Frontier

Baseline main: 4471b8e50d850bd3548af091134c16895c781ac9
Branch: workstream-d/d3-core-repair
Compiler: 0.4.2-alpha.1
Edition: core-0.1-integration-candidate-a13-b12

## Historical original
Normalization succeeds.

marak check:
- PROG0001;
- PARSE0002;
- furthest normalized token: 0;
- source location: original line 1;
- resolve/validate/execute: not reached.

## D3 tranche 1 — approved local patches only
Candidate snapshot commit: 8e01e109fce6c48df79814b20ba7d4dc1ce59bb4.

Applied D-PATCH-0001..0004 only. The frontier remained:
- PROG0001;
- PARSE0002;
- furthest normalized token: 0.

This is expected: local repairs later in the source cannot bypass the Hebrew front matter at source start.

## D3 tranche 2 — documentary traceability + addition structural repair
Current candidate: megillah/candidates/Megilat_HaItim_Marak_Candidate.md

Normalization succeeds.

marak check:
- PROG0001 remains because no legal whole-program principal transition exists yet;
- PARSE0002;
- furthest normalized token: 105;
- candidate line: 11;
- mapped original line: 35;
- first failing historical text begins ותבחר מפלצת הספגטי המעופפת יום אחד...;
- resolve/validate/execute for the whole candidate: not reached.

## Meaning of the advance
The complete repaired דבר החיבור is now accepted as A13 Preparation:
- named act;
- two named roles;
- explicit body;
- one numeric result.

The next frontier is the first substantive יום היסוד material, not front-matter prose.

No whole-program compilation claim is made.
