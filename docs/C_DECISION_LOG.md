# C decision log

| ID | Class | Status | Decision | Rationale / dependency | Tests |
|---|---|---|---|---|---|
| C-ARCH-001 | IMPLEMENTATION | ACCEPTED | strict staged pipeline with explicit data contracts | prevents parser/resolver/backend semantic leakage | package boundary tests |
| C-ARCH-002 | IMPLEMENTATION | ACCEPTED | canonical HAST/IR ownership under `compiler.models`; ordinary imports only | fixes 0.19 duplicate-class identity bug | canonical ownership + no dynamic import tests |
| C-TOOL-001 | TOOLING | ACCEPTED | retain Python 3.11+ for initial productionization | correctness/reuse/testing dominate current performance needs | full unit suite |
| C-NORM-001 | IMPLEMENTATION / SPEC-DERIVED | ACCEPTED | no NFC/NFKC; match exact 27 code points | direct consequence of exact lexical charter | presentation-form/niqqud tests |
| C-NORM-002 | IMPLEMENTATION | ACCEPTED | one map unit per normalized code point; UTF-8 bytes + code-point positions | deterministic provenance | source-map suite |
| C-NORM-003 | SPEC_DEPENDENT | PROVISIONAL | explicit Unicode White_Space 15.1 table | deterministic now; exact spec version awaiting C-BLOCK-001 | whitespace variants |
| C-PARSE-001 | IMPLEMENTATION | ACCEPTED | parser/forest preserves alternatives; no score/ranking | M0 ambiguity rule | ambiguity/left-recursion tests |
| C-PARSE-002 | SPEC_DEPENDENT | ACCEPTED | A0 has zero admitted positive productions | A's atomic imperative and `ואחרי כן` remain PROPOSED | A0 registry tests + PARSE0001 |
| C-PARSE-003 | IMPLEMENTATION | ACCEPTED | exact Earley-style chart engine over word/morph/nonterminal symbols | supports recursion and ambiguity without syntax heuristics | synthetic CFG tests |
| C-PARSE-004 | SPEC_DERIVED | ACCEPTED | only positive constructions with `NORMATIVE` declaration status reach production parsing | compiler must not promote A candidates into language rules | proposed-production exclusion test |
| C-PARSE-005 | IMPLEMENTATION / SPEC_SAFETY | ACCEPTED | equal `semantic_id` is not semantic equivalence; equivalence requires explicit later fingerprint | construct family identity does not determine resolved operands/references/meaning | unresolved/equal/distinct fingerprint tests |
| C-PARSE-006 | IMPLEMENTATION | ACCEPTED WITH LIMITATION | M2 stores exact explicit derivation trees; packed SPPF is deferred | correctness first; no pruning is permitted to solve growth | 14-way synthetic ambiguity probe |
| C-PARSE-007 | TOOLING | ACCEPTED | parse metrics are deterministic structural counts, not timings/scores | exposes explosion without affecting semantics | metrics/order-determinism tests |
| C-DIAG-001 | TOOLING | ACCEPTED | stable structured bilingual diagnostics + JSON | CLI/IDE/conformance needs | CLI tests |
| C-DIAG-002 | SPEC_SAFETY | ACCEPTED | distinguish `PARSE0001` (spec has no admitted grammar) from `PARSE0002` (source fails an existing grammar) | avoids mislabeling a specification dependency as a user syntax error | parser failure tests |
| C-IR-001 | SPEC_DEPENDENT | BLOCKED | no concrete IR opcodes/effects before B | avoids disguised language decisions | ownership shell only |
| C-CLI-001 | TOOLING | ACCEPTED | check/run/compile/explain/version command surface exists early | stable workflow while semantics grow | CLI tests |
| C-CLI-002 | TOOLING | ACCEPTED | `explain` exposes normalization/parse/resolve/semantic/all levels; unavailable later stages say so explicitly | explainability without fake results | explain parse-level test |
| C-AI-001 | SPEC_SAFETY | ACCEPTED | canonical HAST uses neutral `units`, not a built-in expression/statement partition | the surface/semantic model has not justified that conventional dichotomy | anti-imitation canonical-model guard |
| C-AI-002 | SPEC_SAFETY | ACCEPTED | conventional semantic labels (`Return`, `While`, call frame, positional parameter) may appear only in spec adapters/reference models until A+B justify their language mapping | prevents B/reference metanotation from becoming de facto surface design | forbidden-name guard in canonical HAST |
| C-AI-003 | IMPLEMENTATION | ACCEPTED | stack/heap/trampoline/activation representation remains backend/runtime choice | B's recursive-call behavior does not normatively require a machine stack | architecture review |
| C-AI-004 | SPEC_DEPENDENT | REVIEW_REQUIRED | B1 mutable-cell `Env→Location→Store`, Boolean values, Sequence values, B3 pre-test repetition, and B4 call/result/parameter choices are imported semantic inputs, not C-originated language facts | several are plausible but resemble conventional PL models; anti-imitation re-derivation belongs to B/Master | ANTI_IMITATION_AUDIT.md |
| C-AI-005 | SPEC_SAFETY | ACCEPTED | C may implement an adapter/reference evaluator for a B construct without creating a same-named HAST/IR node | internal lowering need not dictate the human-language conceptual model | contract tests / code review |
| C-AI-006 | TOOLING | ACCEPTED | CLI exit codes/stdout/stderr are host-tool behavior, not program-language semantics | conventional OS interface is appropriate implementation tooling | CLI tests |

| C-AI-007 | IMPLEMENTATION / SPEC_SAFETY | ACCEPTED | historical B1–B5 executable semantics live only under `compiler.reference_models`; canonical compiler layers have an import firewall against that namespace | B6 explicitly demotes Env/Location/Store, Expr/Cmd, activation records, Call/Return and If/While to reference encodings | reference-model isolation tests + B4 candidate tests |
| C-AI-008 | SPEC_SAFETY | ACCEPTED | surface admission and semantic readiness are represented separately; a normative parse may be preserved while `check` emits `SEM0001` | A8 retains action-performance wording while B6 reopens its input/result/state ontology | A8 semantic-gate tests |
| C-AI-009 | LANGUAGE-DERIVED / IMPLEMENTATION | ACCEPTED | `NameTerminal` matches one admitted Hebrew word only in an explicit grammar name slot; it creates no identifier token class and applies no reserved-keyword filter | A-NAME-007/008 survive; A8 reopens A-NAME-009 reserved-word exclusion | grammar-word-as-name, bare-name rejection tests |
| C-AI-010 | SPEC_SAFETY | ACCEPTED | A0/A3 registry snapshots pin their historical language-edition strings instead of importing the current compiler edition | historical spec evidence must not mutate when current frontier advances | snapshot equality tests |
| C-SEM-001 | SPEC_DEPENDENT | BLOCKED | do not lower A8 reusable-action performance to canonical Call/Frame/Return semantics yet | B6 B-AI-Q04..Q08 | `SEM0001` + no canonical conventional nodes |

| C-AI-011 | SPEC_SAFETY | ACCEPTED | current registries may supersede formerly normative historical surface decisions without compatibility aliases; historical registries remain immutable evidence | anti-imitation correctness outranks source compatibility before Core freeze; A10 supersedes A8 `מצוה` with independently rederived `מעשה` | A8 snapshot + A10 rejection tests |
| C-PARSE-008 | IMPLEMENTATION | ACCEPTED | parser may start from an explicit grammar category for conformance/tooling while `check` continues to use program roots only | tests NumberValue/Proposition constituents without declaring them standalone programs | A9 fragment-vs-program tests |
| C-SEM-002 | LANGUAGE/COMPUTATION-DERIVED | ACCEPTED | canonical numeric/proposition HAST contains exact integer, add/subtract denotation and numeric-identity proposition only after A9+B8 overlap | these distinctions were independently justified; no general Expression/Statement/Boolean ontology follows | source→HAST→judgment tests |
| C-SEM-003 | LANGUAGE/COMPUTATION-DERIVED | ACCEPTED | B7 state substrate is referent/current-fact/query/replacement; any cells/maps/SSA are implementation refinements | closes former C-BLOCK-005 without restoring Env→Location→Store as language ontology | equal-content separation, co-reference, unrelated-fact preservation tests |
| C-SEM-004 | LANGUAGE/COMPUTATION-DERIVED | ACCEPTED | B8 truth is proposition satisfaction, not storable Boolean/truthiness | closes former C-BLOCK-006 | zero-not-truthiness, equality judgment, proposition-error tests |
| C-SEM-005 | LANGUAGE/COMPUTATION-DERIVED | ACCEPTED | B9 recurrence is checkpoint semantics; A10's `A וכן תעשה עד אשר P` maps to initial occurrence then post-occurrence cease-when-P checkpoint | closes former recurrence-ontology blocker without introducing While/do-while language construct | initial-occurrence-even-if-P-held, no-hidden-counter tests |
| C-RESOLVE-001 | LANGUAGE-DERIVED | ACCEPTED | when one admitted A10 construction explicitly repeats the same named place, C checks exact required co-reference; it does not search for a nearest compatible name | source words license equality constraint directly | mismatched-state-name REF0001 tests |
| C-PARSE-009 | SPEC_DERIVED | ACCEPTED | A8 `מצוה` performance is absent from the current A10 registry; `מעשה` is current | A-ACT-021/022/026 supersede older choice | old-mitzvah rejection + new-maaseh parse tests |
| C-A12-001 | SPEC_DERIVED / SPEC_SAFETY | ACCEPTED | current surface registry follows the A12 frozen candidate exactly and does not preserve superseded A11 plural-body, ordinal-result or performance-local-state aliases | pre-Core compatibility must not override the frozen candidate, especially after anti-imitation review | A12 rejection tests + immutable A11 snapshot |
| C-PARSE-010 | IMPLEMENTATION | ACCEPTED | A12 direct numerals use a versioned multi-word lexicon terminal that emits every licensed boundary rather than selecting the longest match | implements the frozen 1..9999 surface without inventing generic decimal syntax or greedy lexical precedence | all 9999 lexicon entries + `מאה ואחד עשר` shorter-boundary test |
| C-RESOLVE-002 | LANGUAGE-DERIVED | ACCEPTED | A12 body opener and closer are constrained to the same explicit act name; mismatch is `REF0021` and is never repaired by a nearest-body rule | explicit repeated Hebrew description licenses exact co-reference | A12 BODY_MISMATCH fixture |
| C-VALIDATE-001 | SPEC_DERIVED | ACCEPTED | A12 body may syntactically contain result-production units, but more than one numeric output in one body fails semantic validation `SEM0012` | A-OUT-002 is an at-most-one semantic restriction; no ordinal/multiple-result convention survives | DOUBLE_OUTPUT_CORE fixture |
| C-A12-002 | SPEC_SAFETY | BLOCKED_ON_MASTER | C does not add `חדל מעשות...` merely to make the A12 tiny RM witness parse | the witness uses the phrase, but the frozen construction inventory does not normatively admit it | `A12_TINY_PARSE_BLOCKER.log` |
| C-A12-003 | SPEC_SAFETY | BLOCKED_ON_MASTER | C does not invent a whole-program declaration/definition aggregation grammar from adjacency | A12 rejects bare source order as sequencing and leaves large-program organization open, while the tiny witness juxtaposes top-level units | full tiny-source parse blocker evidence |
| C-SEM-006 | LANGUAGE/COMPUTATION-DERIVED | ACCEPTED | B11 closes the frozen A12 reusable-act semantic ontology as described-act identity + performance occurrence + named role relations + zero/one output + completion provenance, without Function/Frame/Return or positional-call requirements | B10/B11 post-anti-imitation derivation + `B_A12_EXACT_MAPPING.md`; every frozen A12 family maps exactly except explicit subtraction-domain clarification | B11 gate-readiness tests, role-permutation/performance/output tests, E6 adversarial |
| C-A12-002 | SPEC_DEPENDENT | BLOCKED | do not invent `חדל מעשות את המעשה אשר שמו NAME` solely to satisfy the A12 tiny RM witness | phrase is used by the witness but absent from the frozen construction inventory | A12 tiny-witness blocker evidence |
| C-A12-003 | SPEC_DEPENDENT | BLOCKED | do not infer whole-program aggregation or execution sequencing from adjacency of top-level A12 units | A12 denies bare source-order sequencing and freezes no discourse-root grammar | A12 tiny-witness blocker evidence |


## C M4 A13/B12 delta

| ID | Class | Status | Decision |
|---|---|---|---|
| C-M4-NORM-001 | SPEC-DERIVED | ACCEPTED | A13 exact 25-code-point whitespace set is normative; host Unicode whitespace predicates are not authoritative. |
| C-M4-PROG-001 | SPEC-DERIVED | ACCEPTED | canonical program separates Preparation from Principal selected by one top-level `ועתה`. |
| C-M4-RESOLVE-001 | SPEC-DERIVED / IMPLEMENTATION | ACCEPTED | source visibility is introduced-before-use; resolved references become typed stable IDs; no hoisting/runtime name lookup. |
| C-M4-HAST-001 | SEMANTICS-DERIVED | ACCEPTED | expand canonical HAST only for A13/B12 distinctions; retain anti-imitation naming firewall. |
| C-M4-IR-001 | IMPLEMENTATION | ACCEPTED | assign `core-ir-0.1-candidate-1`; structured deterministic IR preserves B12 observable distinctions. |
| C-M4-ARITH-001 | SEMANTICS-DERIVED | ACCEPTED | Natural subtraction is checked; provable underflow is static `SEM0201`, dynamic underflow is `ARITHMETIC_DOMAIN_ERROR`. |
| C-M4-RUNTIME-001 | SEMANTICS-DERIVED | ACCEPTED | outcomes are Normal/Error/Divergence; no language exit value and no catchable Core exception. |
| C-M4-REF-001 | IMPLEMENTATION | ACCEPTED | add an independent canonical-IR reference evaluator rather than using the backend as its own oracle. |
| C-M4-ART-001 | IMPLEMENTATION | ACCEPTED | assign explicit tagged canonical JSON artifact `core-artifact-0.1-candidate-1` with verifier and payload digest. |
| C-M4-BACKEND-001 | IMPLEMENTATION | ACCEPTED | portable VM may use conventional host control machinery internally but consumes IR only and does not define language ontology. |
| C-M4-OPT-001 | IMPLEMENTATION | ACCEPTED | M4 optimizer remains identity-preserving to avoid changing errors/effects/divergence timing. |
| C-M4-PKG-001 | TOOLING | ACCEPTED | all fixtures are repository-relative; relocation and byte-identical wheel builds are release gates. |

## M4.1 remediation
See `C_M4_1_DECISION_LOG_DELTA.md` for C-RUNTIME-0041, C-ARTIFACT-0041, C-RESOLVE-0041, C-OBSERVE-0041 and C-DIAG-0041.

## C M4.2 remediation

- **C-RUNTIME-006 — ACCEPTED:** default `max_active_performances` is `None` in HAST reference, IR reference and portable backend. A finite default quota is not permitted by A13/B12.
- **C-RUNTIME-007 — ACCEPTED:** explicit finite `max_active_performances=N` is a caller-imposed implementation/harness control and its exhaustion is not a Marak language Error.
- **C-RUNTIME-008 — ACCEPTED:** actual host allocation/resource exhaustion remains an implementation-resource category; iterative activation architecture remains implementation-only.
- **C-PACKAGE-004 — ACCEPTED:** canonical source root contains no generated handoff manifest/checksum ledger or handoff payload directories. Handoff metadata lives outside `source/`.
- **C-PACKAGE-005 — ACCEPTED:** current human-facing project/distribution/CLI metadata uses Marak / `marak` / MIT; historical snapshots are not rewritten.
