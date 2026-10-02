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
`C5.7 REMEDIATION COMPLETE — READY FOR MASTER REVIEW`

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

## MASTER REMEDIATION FINDINGS

Previous reviewed HEAD:
`e45d1cedef3b02eb9dafa96caa8473512f62672a`

### C5.7-A18-001 — COUNTED_SOURCE_NAME_SPAN_DOES_NOT_COVER_COMPLETE_CONSTRUCTION

Previous behavior:
- counted `ParseLeaf.text` correctly carried canonical payload spelling only;
- `token_index`, normalized span and original/source span began at the first payload word.

Exact remediation:
- counted `ParseLeaf.text` remains unchanged as `" ".join(payload_words)`;
- `token_index` now identifies the opening frame token `שם`;
- `normalized_start` now begins at that same frame token;
- `normalized_end` remains the end of the final payload token;
- `original` now spans from the opening frame token through the final payload token.

Proof:
- direct production test verifies payload text `מספר טיפה גלויה`;
- normalized and original spans cover the complete counted construction;
- whitespace/newline and maqaf normalization retain complete original provenance;
- duplicate-name diagnostics now expose the complete counted occurrence;
- HAST spelling remains canonical payload only.

Frame/count semantic identity: **NO**.

Status: **CLOSED_CANDIDATE**.

### C5.7-TEST-001 — EXPLICIT MULTIWORD PRODUCTION COVERAGE_FOR_ALL_11_NAME_ROLES_INCOMPLETE

A valid production fixture now uses counted multi-word SourceName occurrences for every role.
The successful path mapping is:

| Role | Successful production path |
| --- | --- |
| `ActionName` | `A10.ACT.IDENTITY` |
| `PlaceName` | `C52.PREP.PLACE.INDEX` |
| `RoleOwnerActionName` | `C56.ROLE.DECLARE.INDEX` |
| `AssociatedRoleName` | `C56.INDEX.GENERAL.CURRENT.ROLE` |
| `DeclaredRoleName` | `C56.ROLE.DECLARE.INDEX` |
| `BodyActionName` | `A12.BODY.DEFINITION` |
| `ResultActionName` | `C56.INDEX.GENERAL.IMMEDIATE` |
| `PerformedActionName` | `C52.ACT.PERFORM.ROLES` |
| `SymbolDomainName` | `C52.SYMBOL.DOMAIN` |
| `SymbolMemberName` | `C52.SYMBOL.MEMBER` |
| `ProgramInputRoleName` | `C55.INPUT.DECLARE.NATURAL` |

The fixture compiles as one valid program and every mapped leaf has counted multi-word
source provenance. Repeated role/name positions co-refer through the existing canonical
spelling rules. A dedicated `ResultActionName` test additionally performs a counted-name
act, reads its immediate result using `C56.INDEX.GENERAL.IMMEDIATE`, and obtains identical
observable results from HAST reference, IR reference and portable backend execution.

Status: **CLOSED_CANDIDATE**.

Only Master may mark these findings finally CLOSED.

## Verification receipt

- C5.7 targeted: **18/18 PASS**;
- B17 reference/compatibility: **40/40 PASS**;
- full pytest: **561 passed + 126 subtests passed**;
- affected current-version/portability subset: **52/52 PASS**;
- B13: **28/28 PASS**;
- B14: **22/22 PASS**;
- A16: **2,548 checks PASS**;
- A17: **4,415 checks PASS**;
- B15: **29/29 PASS**;
- C5.6/B16 semantic regressions: **28/28 PASS**;
- B16 required gates: **4/4 PASS**;
- Program Input remediation rerun: **26/26 PASS**;
- Symbol production regression: **18/18 PASS**;
- D3/D4 frozen regressions: **29/29 PASS**;
- registry SHA-256:
  `3c8e6f179d9259c2f84be34f80b215925d72d6d07fc9bcb7d8e5d4279dd1da17`;
- `py_compile` and `git diff --check`: PASS.

CI contains a dedicated Ubuntu/Windows C5.7 job reproducing the targeted,
B17, full-suite, inherited-gate, D3/D4, and canonical-byte checks.

## Scope receipt

Relative to the previous reviewed HEAD `e45d1cedef3b02eb9dafa96caa8473512f62672a`,
remediation changes exactly five files:
- `compiler/parse/parser.py` — full-construction provenance for counted SourceName;
- `tests/test_c5_7_multiword_source_names.py` — span/diagnostic proofs and explicit 11-role production coverage;
- `docs/compiler/C5_7_MULTIWORD_SOURCE_NAMES.md` — corrected semantic-text versus provenance contract;
- `docs/compiler/C5_7_TEST_EVIDENCE.md` — remediation evidence;
- `docs/compiler/C5_7_HANDOFF_TO_MASTER.md` — Master findings closure candidate.

There is no `megillah/**` diff, no A18/B17 proposal diff, no registry semantic
change, and no HAST/IR/artifact model or schema change. A16/A17 generated
test-result side effects were restored after local gate execution.

This PR remains intentionally Draft. C5.7 does not merge itself and makes no
`MASTER ACCEPTED` claim.

Master routing request:
`C5.7 → ACCEPT / RETURN / REJECT`.
