# C M4 — A13/B12 Reconciliation

A13 owns surface admission and source-discourse rules. B12 owns Core observable semantics. C implements their intersection without substituting conventional language concepts.

| Topic | A13/B12 result | C M4 implementation |
|---|---|---|
| whitespace | exact closed 25-code-point set | fixed table; no `isspace()`/`\s` source of truth |
| program | Preparation then exactly one `ועתה` Principal | `HastCoreProgram(preparation, principal)` |
| sequencing | only explicit `ואחרי כן` relation | `HastThen` / `IRThen`; adjacency rejected |
| place introduction | identity + initial establishment | `HastPlaceIntroduction` / `IRInitialFact` |
| replacement | later executable current-fact replacement | distinct `HastReplaceCurrentFact` / `IRReplaceCurrentFact` |
| visibility | introduced-before-use, no hoisting | static resolver with typed IDs |
| roles | Act-owned, occurrence-specific, named | `RoleId`, identity-addressed associations |
| propositions | judgment, not Boolean datum | separate HAST/IR proposition kind |
| subtraction | Natural `B-A` iff `A<=B` | static proof rejection + checked runtime op |
| recurrence | post-action checkpoint | dedicated recurrence node/op, not canonical `while` |
| output | optional occurrence product, nonterminal | produce-product action; body continues |
| immediate result | just-completed occurrence provenance | structural stale-reference rejection + dynamic no-output error |
| completion | exhaustion | no source/canonical HALT/return/main-exit value |

No divergence from A13/B12 is currently known.
