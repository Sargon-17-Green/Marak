# C5.7 — HANDOFF TO MASTER

Workstream:
`C5.7 — Multi-word Declared Source Names Production Integration`

Canonical baseline:
`5679fbe861bc2d30aba479e32fd042bf196295ca`

Branch:
`workstream-c/c5-7-multi-word-source-name-integration`

Draft PR:
`#23`

Route:
`D4-LANG-002 → A18 → B17 → C5.7`

Status:
`C5.7 PRODUCTION INTEGRATION COMPLETE — READY FOR MASTER REVIEW`

## Implemented

- added production `SourceNameTerminal` without rewriting frozen historical registries;
- migrated all 115 current name occurrences / all 11 roles in C5.7;
- preserved legacy one-word names unchanged;
- added exact counted A18 form with direct Natural count >= 2;
- consumed exactly N payload words;
- canonicalized payload spelling by one U+0020 between normalized words;
- handed only canonical payload spelling to existing static resolution;
- preserved all six identity families and owner scopes;
- preserved declaration-before-use and duplicate semantics;
- preserved Program Input binding by resolved `ProgramInputId`;
- preserved Symbol source identity versus visible-label separation;
- preserved ambiguity rather than ranking it.

## Explicitly not introduced

- no runtime Name/String domain or object;
- no dynamic name lookup;
- no longest-match name selection;
- no expected-type rescue;
- no declaration-known tokenization;
- no nearest-name resolution;
- no welded/spaced alias;
- no visible-label alias;
- no HAST/IR/artifact schema field or multiword flag;
- no Megillah edit.

Version changes are limited to compiler/package and construction registry:
`0.5.7-alpha.1`, `0.5.7a1`, `c5.7-a18-b17.1`.

HAST, IR and artifact versions remain at the accepted 0.7 candidate contracts.

## Verification receipt

- C5.7 targeted: **14/14 PASS**;
- B17 reference/compatibility: **40/40 PASS**;
- full pytest: **557 passed + 126 subtests passed**;
- affected current-version/portability subset: **52/52 PASS**;
- B13: **28/28 PASS**;
- B14: **22/22 PASS**;
- A16: **2,548 checks PASS**;
- A17: **4,415 checks PASS**;
- B15: **29/29 PASS**;
- C5.6/B16 semantic regressions: **28/28 PASS**;
- B16 required gates: **4/4 PASS**;
- D3/D4 frozen regressions: **29/29 PASS**;
- registry SHA-256:
  `3c8e6f179d9259c2f84be34f80b215925d72d6d07fc9bcb7d8e5d4279dd1da17`;
- `py_compile` and `git diff --check`: PASS.

CI contains a dedicated Ubuntu/Windows C5.7 job reproducing the targeted,
B17, full-suite, inherited-gate, D3/D4, and canonical-byte checks.

## Scope receipt

Production/compiler/registry/tests/docs/CI were changed only as required for
C5.7. A18/B17 proposal content was not edited. A16/A17 generated result files
were restored after local gate execution. No Megillah file was changed.

This PR remains intentionally Draft. C5.7 does not merge itself and makes no
`MASTER ACCEPTED` claim.

Master routing request:
`C5.7 → ACCEPT / RETURN / REJECT`.
