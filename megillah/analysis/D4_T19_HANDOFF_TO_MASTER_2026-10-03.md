# D4 T19 HANDOFF TO MASTER — Luach Fifteen

## Status

**T19 / Luach Fifteen: COMPLETE / PASS.**

This handoff covers only T19. Luach Sixteen / T20 has not been started.

## Canonical baseline and branch

- canonical main used for this continuation: `35e954d8c08da68a205cfea654b2597a4a77a714`
- D branch: `workstream-d/d4-post-c56-megillah-conformance`
- PR: **#20 — Draft, open, unmerged**
- accepted executable/evidence head: `c6adce2bcc4c59dc7b35e0406935962b5dd10e84`
- immutable original SHA-256: `7b834f4a444e021bb65164282b851af960a6dbc0be3d458c2412181773b9db7b`
- final T19 candidate SHA-256: `8e57e223d7cdcd4cba299a828e1d409f0ed2061b0e7b25362bfedaec2d645f90`

The original file is unchanged. PR #20 was not merged.

## Authorized T19 source span

- Luach Fifteen: original lines **895–995**
- separator: original line 997
- Luach Sixteen begins at original line **999** and is outside this tranche

The Luach Fifteen section headings were classified as documentary organization; their executable requirements are retained by D4-PATCH-020.

## Implemented semantics

The repair introduces no new language capability.

1. Eleven question seals are represented as ordinary Naturals: **1, 10, 11, 12, 20, 21, 22, 30, 31, 32, 33**.
2. Seal 40 is deliberately absent, exactly as the source requires.
3. The successor bowl is determined from `מערכת הטיפה האחרונה`, the arrangement chosen by visible drop 46. The arrangement produced by the twelfth post-drop blend is not used for this purpose.
4. First answer:
   `keep((F_q + s + 181)^2 + 179*F_successor + s)`.
5. Direction probe:
   `keep((a1 + s + 1 + 193)^2 + 193*a1 + 197*F_6)`, followed by the source-authorized remainder-by-2 route.
6. Remainder 1 fixes forward direction; remainder 0 fixes backward direction.
7. Later answers step by one cyclically in that fixed direction, including `M→1` and `1→M`.
8. The query path preserves bowl fills, the visible-drop-46 arrangement, and the current post-drop arrangement.
9. All new multi-word declared names use counted SourceName. No welded identifier was reintroduced.

## Language / compiler classification

`SOURCE_REPAIR_ONLY / CURRENT_LANGUAGE_ALREADY_SUFFICIENT`.

No change to:
- parser or grammar;
- construction registry;
- compiler;
- HAST or IR;
- artifact schema;
- semantic type system;
- identity families.

The only acceptance-time defect after the source repair was a test-fixture spelling of repeated role associations: the helper emitted `בהיות` twice where the existing language requires `בהיות ... ובהיות ...`. Commit `c6adce2...` fixes only that test helper; candidate source bytes do not change.

## Verification

GitHub Actions run `37150104605` (#562):

- Ubuntu focused T19: **4 passed**
- Windows focused T19: **4 passed**
- Ubuntu combined D3+D4: **92 passed**
- Windows combined D3+D4: **92 passed**
- post-M2 proposal regressions: **PASS** on both D4 jobs
- core full pytest: **626 passed, 126 subtests passed**
- A13 selftest: **289 checks PASS**
- semantics integrated suite: **PASS**

The focused tests include:
- exact 11-seal matrix against an independent oracle;
- successor lookup from the visible-drop-46 arrangement;
- explicit protection against using the current/post-drop arrangement;
- state preservation;
- both directions;
- `M→1` and `1→M` wrap cases;
- canonical counted SourceName checks.

## Final frontier

- normalized token count: **66,769**
- furthest normalized token: **62,110**
- candidate line: **507**
- original line: **999**
- diagnostic: `PARSE0002`
- next blocker: **# לוח ששה עשר: לבחור אחת מדרכים רבות**

This is the expected post-T19 frontier: the entire Luach Fifteen block has been admitted and verified.

## Provenance synchronization

This handoff accompanies:
- `D4-PATCH-020` in the patch ledger;
- reconciliation of the previously missing machine-readable `D4-PATCH-019` entry;
- a new T19 frontier entry;
- T19 source-provenance mapping and documentary heading entries;
- updated T19 analysis and test evidence.

## Master action

Review/accept T19 as a verified D4 source-repair tranche.

Do **not** infer acceptance or implementation of Luach Sixteen from this handoff. T20 remains the next source tranche and was not started here.

Do **not** merge PR #20 solely because this handoff exists; it remains Draft/open unless Master separately decides otherwise.
