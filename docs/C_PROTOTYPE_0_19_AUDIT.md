# Prototype 0.19 audit

Input SHA-256: `5ccad0fe984e50a7006e4ef7bcadf9d664a8041f8121375faaa4dba88633b900`.

## Baseline

All fourteen historical test groups were rerun against the unmodified extracted research package: 210 tests total, all green.  This establishes that the package was recovered intact.  It does **not** establish conformance to M0/A/B.

## Architectural mismatch

`00_README.md` states that the recovered source program is the authority.  M0 now states the opposite ordering: specification → compiler → reference program.  Therefore the reverse-engineering front-end cannot be adopted as the production language definition.

## Concrete defects / incompatibilities

1. `49_RAW_FRONTEND_0_11.py` uses a broad Hebrew-block regex (`U+0590–U+05FF`) and Arabic digits as tokens.  That violates the exact 27-letter charter.
2. The same front-end applies NFC/NFKC normalization.  That can turn compatibility Hebrew presentation forms into meaningful letters; the charter instead names the 27 admitted code points and makes every other character transparent.
3. Morphological prefix splitting is deliberately overgenerating and source-grounded rather than A-registry-grounded.  It is valid research machinery, not yet a production grammar.
4. `59_CHART_CONSTRAINT_RESOLVER_0_13.py` explicitly resolves `אשר` toward the “nearest following strong predicate within a short window” and uses analogous first-predicate windows for control markers.  M0 forbids such generic nearest/ranking heuristics.
5. Numbered modules repeatedly use `importlib.util.spec_from_file_location` to load the same implementation under different module identities.  The known class-identity failure was reproduced: IR classes loaded by IR, optimizer and backend are distinct Python class objects and `isinstance` fails across them.
6. Many 0.13–0.19 relations are explicitly labelled HYPOTHESIZED or are recovered from the Megillah.  They cannot silently become A grammar or B semantics.

## Reuse classification

| Research component | Disposition | Reason |
|---|---|---|
| 12 Reference Interpreter | RESEARCH_ONLY | Useful executable semantic evidence, but `Hand/Result/World/Trace` and domain behavior are not yet B-Core primitives. |
| 27 Validated IR | REWRITE | Useful lessons on internal sorts/effects/checks, but coupled to research semantics and dynamic module loading. |
| 31 Optimizer | ADAPT methodology / BLOCKED_ON_SPEC passes | Pass discipline and equivalence tests are valuable; actual legality depends on B observability/error/nontermination semantics. |
| 37 Portable register backend | ADAPT after IR | Strong oracle/backend candidate, but current type ownership and opcode contract are research-specific. |
| 42 Artifact | ADAPT | Data-only round-trip and verifier ideas are valuable; schema must be rebuilt around canonical IR/versioning. |
| 49 Raw front-end | REWRITE | Violates lexical charter and is Megillah-derived. |
| 52 Raw→artifact pipeline | REWRITE | Stage composition idea is useful; direct source-island semantics are not production contracts. |
| 59 Chart/constraint resolver | RESEARCH_ONLY | Contains forbidden nearest/short-window heuristics. |
| 62 Resolver→artifact islands | RESEARCH_ONLY | Useful differential fixture lineage, not general compilation architecture. |
| 65 Symbol resolver | ADAPT concepts | Explicit unresolved results/provenance are good; binding rules await A. |
| 75 Qualified resolver | ADAPT concepts | Conservative exact-prior uniqueness is informative; still not normative without A scope/reference rules. |
| 82 Reference-expression HAST | ADAPT representation ideas | Exact spans/structured unresolved references are useful; concrete reference forms remain A-owned. |
| 84 Valency refiner | ADAPT architecture | Valency-frame separation is the right boundary; current frames are research-derived until A approves them. |
| 86 Naming resolver | RESEARCH_ONLY / ADAPT provenance | Provenance accounting useful; naming boundaries and reference rules remain open in A. |
| Historical tests/fixtures | KEEP as research regression corpus | They protect recovered behavior but are explicitly not conformance tests. |

## Canonical identity reproduction

The audit log records:

```text
ir.IRExpr is opt.ir.IRExpr: False
opt.ir.IRExpr is be.ir.IRExpr: False
isinstance external IRExpr vs optimizer class: False
```

The new tree has a regression test forbidding dynamic source-file imports and verifying single canonical HAST/IR identity.
