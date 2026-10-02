# A18 — Evidence map

| Claim | Repository / primary evidence |
|---|---|
| canonical baseline | GitHub `main` resolved to `5a5f8dae0dd8c3526de5f21f84a3a7b2aba984e3` before branch creation |
| one-word normative Core name | `spec/surface/A_SURFACE_CORE_SPEC.md`, A-NAME-001 |
| exact whitespace normalization | `spec/LANGUAGE_CHARTER.md`; `spec/surface/A13_WHITESPACE_NORMATIVE_SET.md`; `docs/C_SOURCE_NORMALIZATION.md` |
| one-token NameTerminal | `compiler/parse/grammar.py::NameTerminal`; `compiler/parse/parser.py::_match_terminal` |
| no global reserved-name filter | `compiler/parse/grammar.py::NameTerminal`; `spec/proposals/a17/A17_LEXICAL_PRIVILEGE_AUDIT.md` |
| ambiguity-preserving parser | `compiler/parse/parser.py` |
| one-word restriction was Core-only | `spec/surface/ANTI_IMITATION_AUDIT.md`, one-word CoreName row |
| current registry name-site count | `spec/CURRENT_CONSTRUCTION_REGISTRY.json`: 61 name-bearing productions, 115 occurrences, 11 roles |
| six static identity families | `compiler/models/symbols.py`; `compiler/models/domains.py`; `compiler/resolve/a13_program.py` |
| static duplicate/owner scopes | `compiler/resolve/a13_program.py`; `spec/surface/A_REFERENCE_AND_SCOPE.md` |
| Program Input identity not positional/raw-spelling binding | `spec/proposals/a15/A15_PROGRAM_INPUT_ROLES.md`; production resolver |
| Symbol source identity vs visible label | `spec/proposals/a15/A15_SYMBOL_SURFACE.md`; resolver Symbol member tables |
| existing counted visible-label boundary | `compiler/parse/grammar.py::CountedLabelTerminal`; parser counted-label branch |
| D4 gap | PR #20 head `megillah/analysis/D4_FINDINGS.json`, D4-LANG-002 |
| real welded evidence | PR #20 candidate, `מספרטיפהגלויה` and other scaffolding |
| latest repository T16 receipt | PR #20 `D4_FRONTIER_LEDGER.json`: token 20,196; 76 targeted tests |
| Biblical naming relation | Genesis 2:19 |
| multi-word Biblical designation after naming frame | Jeremiah 23:6, `וזה שמו אשר יקראו יהוה צדקנו` |
| Biblical `מלים` | Job 8:10 |
| existing A15 period audit of counted label vocabulary | `spec/proposals/a15/A15_SYMBOL_SURFACE.md` |

## Primary online text consulted

- https://mechon-mamre.org/i/t/x/x0102.htm — Genesis 2
- https://mechon-mamre.org/i/t/x/x1123.htm — Jeremiah 23
- https://new.mechon-mamre.org/i/t/x/x2708.htm — Job 8

No Modern Hebrew usage is used as normative evidence.
