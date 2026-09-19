# ANTI_IMITATION_AUDIT.md

Status: C workstream audit, 2026-09-19
Scope: existing C architecture through M2 plus M3 design inputs A1–A3 and B1–B4

## Rule

C may use conventional compiler engineering. C may not turn a familiar programming-language model into a language fact merely because it is familiar. A feature is admitted into canonical HAST/IR only after its semantic distinction is justified by A+B. B metanotation may be implemented in an isolated reference adapter without forcing an isomorphic surface construct.

## Classification

| רכיב | המודל הנוכחי | מקור ההצדקה | חשד לחיקוי | חלופות שנבדקו | החלטה |
|---|---|---|---|---|---|
| Compiler pipeline | normalization → lex/morphology → parse → resolve → validate → HAST/IR → backend | implementation separation and testability | none material | monolithic parser/compiler; direct Hebrew→backend | **IMPLEMENTATION-ONLY — keep** |
| 27-letter normalization | exact admitted letters; other non-whitespace code points transparent | lexical charter | none | Hebrew Unicode block; NFC/NFKC | **LANGUAGE-DERIVED — keep** |
| Explicit whitespace policy | deterministic code-point table, currently provisional | determinism; charter says whitespace matters | low, but exact Unicode set is not settled | host `isspace`; locale; normative enumerated set | **IMPLEMENTATION-ONLY/OPEN — keep provisional; Master/A decision still required** |
| Source map | normalized offsets map to original bytes/code points/line/column | diagnostics/provenance requirement | none | discard source positions | **IMPLEMENTATION-ONLY — keep** |
| Orthographic word lexer | spaces give word spans, but word ≠ semantic token | normalized-source structure | low | semantic-token lexer; character-level parser | **LANGUAGE-DERIVED + IMPLEMENTATION-ONLY — keep** |
| Morphology lattice | all licensed analyses retained; no confidence winner | ambiguity rule | none | probabilistic tagger; best analysis | **LANGUAGE-DERIVED — keep** |
| Numeral subsystem | separate exact parser driven by A grammar | Biblical-Hebrew numeral morphology and ambiguity needs | none if grammar comes from A | regex; greedy longest match | **LANGUAGE-DERIVED — keep** |
| Earley/chart parser | exact parse forest, no heuristic winner | ambiguity must be detected | none; algorithm is implementation detail | GLR, combinators, constraint parser | **IMPLEMENTATION-ONLY — keep** |
| Explicit parse forest | preserve all parses until semantic equivalence established | M0 ambiguity requirement | none | best parse; confidence ranking | **LANGUAGE-DERIVED/COMPUTATION-DERIVED — keep** |
| `semantic_id` on productions | stable compiler metadata for operation family | explainability/tooling | mild: can become a premature semantic taxonomy | opaque production IDs only; later semantic fingerprint | **IMPLEMENTATION-ONLY — keep, but never treat as semantic equivalence** |
| SymbolId | stable post-resolution internal identity | deterministic references, no later string matching | none | repeated text lookup | **IMPLEMENTATION-ONLY — keep** |
| Scope graph | inspectable graph only for scopes licensed by A/B | deterministic resolution | medium if C predeclares “block/function/local” scope kinds | constraint graph; direct resolved edges | **IMPLEMENTATION-ONLY FRAMEWORK — keep; no scope kinds invented by C** |
| “Variable” | no canonical C node; B1 models binding/state | capability needed: retain changed state | **high if surfaced as conventional variable** | direct state threading; named quantities; immutable succession; cells | **POSSIBLY-IMITATIVE as language concept — keep abstract as binding/state capability; A/B must justify surface** |
| Assignment | no canonical C node yet; B1 distinguishes binding creation/update | changing retained state may be required | medium | functional state transition; explicit replacement wording; simultaneous update | **COMPUTATION-DERIVED capability, SPEC-DEPENDENT form — do not predeclare `HastAssign`** |
| Env→Location→Store / mutable cells | B1 normative reference model; cells not user-visible | clean mutable-state formalization | **medium-high**: classic store semantics and possibly over-specified if aliases are absent | SymbolId→Value rebinding; state-passing semantics; SSA-like semantic model | **POSSIBLY-IMITATIVE imported B input — reference adapter allowed; IR/backend must not require cells** |
| Lexical scope | B4 says lexical, not dynamic | stable meaning independent of caller chain | medium | explicit fully resolved references without a user-visible “scope” concept; dynamic scope | **COMPUTATION-DERIVED goal (stable reference); exact lexical-region model requires A/B review** |
| Global/local distinction | not hard-coded in C | none yet beyond resolved nonlocal/local references | medium | resolved reachability without “global/local” categories | **UNJUSTIFIED as language taxonomy — do not add until A/B require it** |
| Stack frames | not normative; B4 requires fresh activation only | recursive/reentrant execution | **high if treated as semantics** | heap activation; CPS; trampoline; stack | **IMPLEMENTATION-ONLY — explicitly forbid semantic dependence on stack** |
| Action/function | B4 “Action” is static callable entity; C has not made canonical node | reusable computation capability | medium | named procedure/activity; macro-like expansion; recursion relation; first-class callable | **COMPUTATION-DERIVED capability; terminology/model SPEC-DEPENDENT — isolate B adapter** |
| Parameters | B4 formal parameters with fresh cells | reusable computation over supplied data | **medium-high**, especially positional/mutable formal cells | named-role inputs; record-like input; lexical referents; immutable bindings | **POSSIBLY-IMITATIVE — do not bake positional parameter lists into canonical HAST before A action syntax** |
| Positional argument correspondence | B4 preserves semantic list order | deterministic effect order | **high unless A supplies linguistic ordering/correspondence** | named roles; explicit pairings; syntactic clauses with fixed valency | **POSSIBLY-IMITATIVE — requires A/Master validation; C should prefer resolved ParamId→argument mapping internally** |
| Call-by-value | B4 fresh parameter cells after argument evaluation | no caller-cell aliasing | **medium-high**: familiar default calling convention | call-by-reference; call-by-name; immutable value substitution; named argument evaluation | **POSSIBLY-IMITATIVE imported B input — implement only in reference adapter until anti-imitation review closes** |
| Eager argument evaluation | B4 ordered strict evaluation | deterministic effects/errors | medium | lazy; explicit evaluation staging; pure-only args | **CONVENTION-BORROWED / independently justified if effects observable; B/Master should re-derive from requirements** |
| Return statement | C has no node; B3/B4 use `Return(value)` completion | need for a reusable computation to deliver a result | **high**: “Return” and nearest call boundary mirror mainstream function semantics; B4 rationale explicitly cited ordinary function-call semantics | result clause; named yielded value; final result relation; continuation delivery | **POSSIBLY-IMITATIVE — do not add `HastReturn`; require A surface and B anti-imitation re-justification** |
| Call as expression | B4 metanotation | result-producing reusable computation | **high**: expression/statement dichotomy may be imported | uniform computation model; value-producing activity node; explicit result use | **POSSIBLY-IMITATIVE — canonical HAST remains neutral** |
| Expression vs statement | M2 HAST previously used field name `statements`; no semantic hierarchy existed | none | **high** | uniform `unit` / computation nodes | **UNJUSTIFIED — corrected now: `HastProgram.units`; no Expr/Stmt hierarchy** |
| Boolean values | B1 has first-class Boolean | conditions need determinate truth result | medium-high: a first-class Boolean type is not the only semantic model | proposition/condition category not storable; two-valued result internal only | **POSSIBLY-IMITATIVE imported B input — C keeps tagged adapter but does not infer surface Boolean type** |
| if/else | B3 abstract `If`; A conditionals determine eventual surface | need conditional branching for universality/general use | medium | guarded action; conditional relation; one-sided condition; multi-branch cases | **COMPUTATION-DERIVED capability; exact binary `if/else` shape SPEC-DEPENDENT** |
| `while` | B3 uses pre-test While semantics; A3 explicitly rejects importing while/do-while from `עד אשר` | unbounded conditional repetition capability | **high** | recursion; explicit TEST→ACTION→REPEAT relation; post-test repetition | **POSSIBLY-IMITATIVE metanotation — never expose `HastWhile` solely from B3 name; await A mapping / B review** |
| `for` | no such construct in C; A3 has exact counted repetition 3..9 of one atomic action | finite repetition in language evidence | none for A3 form | counter loop; iteration variable | **LANGUAGE-DERIVED A3 counted repetition — keep; do not create conventional for-loop model** |
| Counted repetition | A3 `NUM פעמים ATOMIC_ACTION` (3..9) | Biblical evidence and unambiguous action boundary | none | compiler `for`; general block repeat | **LANGUAGE-DERIVED — safe to add to registry without inventing atomic action** |
| Zero-/one-based indexing | no decision | none | would be high if defaulted | explicit ordinal/position wording; mathematical index; no indexing primitive | **OPEN — no C default** |
| Array | no array construct; B1 has immutable Sequence | general ordered collection capability may be useful | medium | linked sequence; finite mapping; text-like sequence; domain-specific collections | **POSSIBLY-IMITATIVE if called array/indexed storage — C retains only abstract Sequence input from B** |
| Record/object | no decision/implementation | none | high if added by default | named aggregate; product value; namespace-free grouping | **OPEN — do not add** |
| Exceptions | no exception stack; B errors are fatal/uncatchable in Core | deterministic failure semantics | low in C | error value; completion status; recovery construct later | **SPEC-DEPENDENT — no conventional exception machinery inferred** |
| Runtime error completion | B2/B3 explicit Error completion | invalid operation needs defined behavior | low | compile-time rejection where decidable; explicit error values | **COMPUTATION-DERIVED, B-defined — adapter allowed** |
| Modules/imports | future architecture placeholder only | organizing large programs is a possible future need | high if modeled after existing module systems | named writings/collections; linked compilation units; explicit inclusion | **OPEN — no language module semantics in C** |
| Operator precedence | explicitly forbidden unless A specifies it | one-way linguistic contract | none | grammatical constructions with explicit grouping/valency | **LANGUAGE-DERIVED — hidden precedence remains forbidden** |
| Evaluation order | B2/B4 specify observable operand/argument order | deterministic effects and errors | medium if “left-to-right” comes from token order by convention | A-determined semantic role order; simultaneous/pure evaluation | **COMPUTATION-DERIVED need for determinacy; exact order must trace to B+A, not host convention** |
| Simultaneous/snapshot update | still open | Megillah may need cross-dependent updates | none | sequential updates; explicit snapshot construct; library action | **OPEN — C representation extension point only** |
| Standard output | no core stdout semantics; output is runtime/interface concern | host CLI needs channels | high if treated as language primitive | explicit I/O capability later; returned Text; environment adapter | **IMPLEMENTATION-ONLY for compiler stdout/stderr; language I/O remains open** |
| Exit codes | CLI returns host process status | shell/tool integration | none material | exceptions; always-zero tooling | **IMPLEMENTATION-ONLY — keep out of language semantics** |
| Artifact format | versioned verified data, no executable deserialization | security/reproducibility | none | native binary only; pickle/eval | **IMPLEMENTATION-ONLY — keep** |
| Optimizer | semantics-preserving passes only | implementation performance | none | no optimization | **IMPLEMENTATION-ONLY — keep** |
| Register Machine | proof witness only | M1 universality proof | **risk if IR/HAST mirrors registers/pc** | lambda calculus, Turing machine, recursion proof | **COMPUTATION-DERIVED proof tool only — must not dictate HAST/IR/surface** |
| CLI `check/run/compile/explain` | conventional developer tooling | usability and testing | low; not language semantics | other command names/UI | **CONVENTION-BORROWED with independent tooling justification — keep** |

## Re-opened items sent to Master/B

The following are not rejected by C, but their current B1–B4 formulation deserves explicit anti-imitation re-derivation before C freezes canonical lowering around them:

1. **B-STATE-001 / mutable cells** — state is required, but `Env→Location→Store` may be a formal model rather than a necessary language-level ontology.
2. **B-BOOL-001** — two-valued conditions are needed; first-class storable Boolean values are a stronger choice.
3. **B-CTRL-005 pre-test While** — the capability is required, but A3 specifically warns against importing a while/do-while test-point convention from `עד אשר`.
4. **B-PARAM-001/003** — ordered strict positional call-by-value is plausible, but formal/actual correspondence and aliasing behavior should be re-derived from the action language, not conventional defaults.
5. **B-RET-005** — result delivery is required; a `Return` completion caught by the nearest action boundary is one model. The B4 rationale “ordinary function-call semantics” is not independently sufficient under the new rule.
6. **B-ACT-005 call as expression** — value-producing reusable computation is required; the expression/statement taxonomy is not.
7. **B-VAL-001 Sequence** — an ordered runtime-sized collection may be useful, but inclusion in the minimal Core should be justified as a capability requirement rather than “normal language completeness”.

C can continue implementing these as **reference-semantics adapters** for testing B as written. C will not let their names or data structures become mandatory HAST/IR taxonomy until the review closes.

## Immediate C changes made by this audit

- `HastProgram.statements` renamed to neutral `HastProgram.units`.
- Canonical HAST is guarded against prematurely introducing `Statement`, `Expression`, `Variable`, `Assign`, `If`, `While`, `For`, `Return`, `Function`, `CallFrame`, `Array`, `Record`, `Object`, `Exception`, `Module`, or `Import` classes.
- Decision log now records that B metanotation and C canonical representation are distinct boundaries.
- Stack frames are explicitly implementation-only; recursion may lower to stack, heap activations, CPS, or trampoline.
- Positional parameter/call structure is not to be copied into canonical HAST until A provides a linguistically determinate action form.

## Work impact

No completed M1/M2 implementation needs to be discarded. Normalization, source maps, lexing, morphology-candidate preservation, parser forest, construction registry, diagnostics, packaging boundaries, and canonical model ownership survive unchanged.

M3 work that modeled B1–B4 directly with conventional node names must be treated as **reference-evaluator work**, not canonical HAST design. The amount of rework is limited: adapters/evaluator data classes may remain; only the boundary into canonical HAST/IR must stay neutral until A/B anti-imitation review completes.

## Post-audit integration addendum — A8 / B6

After this C audit, A and B completed their own anti-imitation audits. Their result strengthens rather than weakens the C boundary adopted above.

B6 explicitly demotes the former B1–B5 `Env/Location/Store`, `Expr/Cmd`, activation-record, Call/Return and If/While calculi to **reference encodings**. C therefore moved the executable B4 action calculus into `compiler.reference_models` and added an import firewall preventing canonical compiler layers from depending on it.

A8 independently retains the Hebrew-derived `עשה/לעשות את המצוה אשר שמה NAME` family. C now parses the imperative form as a real normative surface construction using an explicit `NameTerminal`. This does not create a conventional identifier lexer: a bare name remains meaningless as a reference, and a token matching a grammar word is not rejected merely because mainstream languages would reserve it.

The key new implementation distinction is:

> **surface admission != semantic readiness**

A source may have a fully normative A8 parse while B6 still leaves its computational ontology open. Such a source is preserved in the parse forest and receives `SEM0001` rather than being misreported as a syntax error or silently lowered through historical B4 semantics.

This is now a permanent C design rule unless Master explicitly supersedes it.

## A9/B7/B8/A10/B9 re-derivation update

The later A/B workstreams closed several questions that C had correctly reopened. C has incorporated those results without restoring the old conventional ontology.

| רכיב | המודל הנוכחי | מקור ההצדקה | חשד לחיקוי | חלופות שנבדקו | החלטה |
|---|---|---|---|---|---|
| Changeable state | source-resolved state-bearing referent with explicit current facts/query/replacement; A10 source uses named `מקום` | B7 independent state re-derivation + A10 Hebrew place/occupancy analysis | superficial resemblance to mutable cell, but implementation cell is explicitly non-normative | cell/store; immutable snapshots; old/new versions; written history; possession | **LANGUAGE + COMPUTATION-DERIVED — retain neutral referent model; do not expose Location/Cell ontology** |
| Truth | proposition satisfaction/non-satisfaction; no Boolean data value | B8 logical need + A9 numeric-identity proposition | Boolean conventions explicitly rejected | storable Boolean; truthiness; proposition judgment | **COMPUTATION/LANGUAGE-DERIVED — proposition judgment retained** |
| Conditional | select one consequence from proposition judgment; A9 paired `אם ... ואם לא ...` shell | Biblical conditional construction + B8 | no `if/else` import needed | dangling else; optional else; expression-valued conditional | **LANGUAGE-DERIVED — shell retained; no `HastIf` taxonomy** |
| Unbounded recurrence | semantic checkpoints; A10 closes one post-action `וכן תעשה עד אשר` family | B9 recurrence capability + A10 Biblical anaphora/endpoint analysis | resembles do-while only after the fact | pre-gated; post-gated; recursion; continuation prescription | **LANGUAGE + COMPUTATION-DERIVED — retain A10 after-gated family; never generalize bare `עד אשר`** |
| Reusable computation noun | `מעשה`, not A8 `מצוה` | A10 independent lexical/semantic comparison + Megillah evidence | prior `מצוה` choice could preserve old design by inertia | `מעשה`; `מצוה`; source `יהי שם מעשה` | **LANGUAGE-DERIVED — supersede current A8 `מצוה`; keep A8 historical only** |
| Reusable action execution | `עשה את המעשה אשר שמו NAME` | A10 explicit typed Hebrew reference/performance | call analogy remains possible in backend only | bare name; `מצוה`; named deed performance | **LANGUAGE-DERIVED surface — parse now; semantic body/input/result still BLOCKED** |
| Result relation | provenance `... אשר יצא מן המעשה ...`; does not imply cessation | A10 result analysis | abrupt Return was convention-heavy | hidden last result; abrupt Return; provenance relation | **LANGUAGE/COMPUTATION-DERIVED principle — preserve; no `Return` node** |
| Numeral ceiling | no fixed 9999 language maximum | A9 corpus and linguistic boundary audit | old cap was fixture-driven | fixed cap; productive Biblical magnitude grammar | **UNJUSTIFIED old ceiling — removed; productive grammar remains OPEN** |

### Concrete work invalidated rather than preserved for compatibility

C deliberately removed A8 `עשה את המצוה אשר שמה NAME` from the **current** registry after A9/A10 superseded that ontology. The A8 registry and tests remain frozen historical evidence. No compatibility alias was added.

This is an explicit application of the user's rule that prior implementation investment does not justify retaining an unsupported language decision.

## A12 frozen-candidate update

A12 provides a useful test of the anti-imitation rule because C had already implemented broader A11 shapes. C deliberately removed those shapes from the **current** registry rather than preserving them for implementation convenience.

| רכיב | המודל הנוכחי | מקור ההצדקה | חשד לחיקוי | חלופות שנבדקו | החלטה |
|---|---|---|---|---|---|
| direct numeric literals | frozen Biblical-Hebrew spellings 1..9999 inside `המספר אשר הוא ...`; semantic numbers unbounded | A-NUM-001..003 + frozen A1 lexicon | generic decimal tokenizer would be convention-borrowed | generated decimal syntax; arbitrary ceiling; exact frozen lexicon | **LANGUAGE-DERIVED; exact lexicon terminal, all boundaries preserved** |
| act body | `זה דבר המעשה... / עד הנה דבר המעשה...` | A-BODY-001..002 linguistic re-analysis | preserving A11 plural form for compatibility would be implementation inertia | plural A11 form; layout; braces/indentation | **LANGUAGE-DERIVED; A11 alias removed** |
| outputs | zero or one explicit `הוצא מן המעשה הזה...`; output does not terminate | A-OUT-001..003 | multiple positional/ordinal outputs resembled tuple/return convention | ordinal outputs; named future roles; single Core output | **RE-DERIVED; A11 ordinal model removed** |
| local mutable state | no performance-local mutable place in frozen Core | A12 freeze audit | retaining it because frames usually have locals would be imitative pressure | global named place; future independently justified local ownership | **REOPENED FOR FULL LANGUAGE; removed from Core** |
| cessation in tiny witness | unresolved exact surface | A12 prose vs witness mismatch | adding a `return/halt`-like rule solely to satisfy RM witness would be witness-driven imitation | ordinary body exhaustion; explicit independently justified cessation | **BLOCKED; C refuses witness-specific syntax** |
| whole-program aggregation | unresolved | A12 anti-imitation audit and open large-program organization | conventional declaration section/program block would be imitation risk | discourse collection; explicit relations; future program framing | **BLOCKED; no adjacency-as-program rule invented** |

This update also demonstrates that historical compiler work is not treated as a compatibility constraint on the language design. A11 remains available as evidence and regression history, but its removed constructions do not leak into A12.

## B10/B11 closure addendum

B10/B11 independently re-derived reusable computation after the anti-imitation audit. This closes several items that C previously kept open without restoring the conventional ontology that triggered the review.

| רכיב | המודל הנוכחי | מקור ההצדקה | חשד לחיקוי | חלופות שנבדקו | החלטה |
|---|---|---|---|---|---|
| reusable computation identity | opaque described `מעשה` identity | A12 named act + B10/B11 semantic derivation | low once separated from host function object | function object; procedure symbol; semantic deed identity | **LANGUAGE + COMPUTATION-DERIVED — retain semantic act identity** |
| one execution | semantic performance occurrence with provenance | A12 `המעשה הזה` + B-ACT-R02/R03 | could have collapsed into stack frame | frame; dynamic call record; event/occurrence relation | **LANGUAGE-DERIVED occurrence; backend frame remains IMPLEMENTATION-ONLY** |
| inputs | named role relations associated with exact values | A12 role wording + B-ROLE-R01..R05 | positional parameter convention explicitly rejected | positional arguments; map by role name; relation set | **LANGUAGE-DERIVED — named non-positional association** |
| result | zero/one explicit numeric product of a performance; production does not complete | A12 output wording + B-OUT rules | host `return` model directly contradicted by continued execution after output | abrupt return; accumulator; output relation | **LANGUAGE + COMPUTATION-DERIVED — product relation, not Return** |
| completion | ordinary completion at body exhaustion; separately licensed cessation may exist | A12 body delimiters + B-ACT-R04/R05 | implicit Return/end-of-function analogy unnecessary | exhaustion; explicit cessation; host return | **LANGUAGE-DERIVED — exhaustion is current Core completion rule** |
| immediate result | result of the explicitly resolved just-completed performance | A12 `עתה ... מן המעשה` + B-OUT-R06..R08 | hidden `last_result` register rejected | global accumulator; caller frame slot; provenance relation | **LANGUAGE-DERIVED provenance; no hidden global register** |

Consequently the A12 reusable-act semantic gates are now `READY`. This readiness must not be misread as permission to introduce canonical `Function`, `Parameter`, `CallFrame`, `Return`, or stack semantics. C's `compiler.semantic_core.performance` intentionally names the re-derived relations directly.

Two unresolved A12 witness issues remain **surface/discourse** questions, not semantic-model gaps: the un-frozen `חדל מעשות...` phrase and the missing whole-program aggregation grammar. C will not use B11 closure as a pretext to invent either.


## C M4 A13/B12 closure delta

| Component | Classification | M4 conclusion |
|---|---|---|
| `CoreProgram` Preparation/Principal split | LANGUAGE-DERIVED | follows A13 `ועתה`; not a conventional main function |
| preparation order | LANGUAGE/SEMANTICS-DERIVED | discourse visibility/dependency only; not executable statement order |
| Place identity/current fact | SEMANTICS-DERIVED | no exposed variable/cell/pointer ontology |
| typed PlaceId/ActId/RoleId | IMPLEMENTATION-ONLY representation of specified identities | stable IDs remove string lookup; do not add user-visible types |
| Act occurrence | LANGUAGE + SEMANTICS-DERIVED | not a user-visible stack frame/function activation |
| role association | LANGUAGE-DERIVED | identity correspondence; positional ABI may exist only internally |
| output product | LANGUAGE + SEMANTICS-DERIVED | not abrupt `return`; later body actions execute |
| proposition | SEMANTICS-DERIVED | branch judgment, not Boolean Value |
| post-action recurrence | LANGUAGE + SEMANTICS-DERIVED | dedicated checkpoint semantics; backend loop is implementation-only |
| checked subtraction | SEMANTICS-DERIVED | Natural-domain obligation; signed host arithmetic cannot leak |
| canonical IR | IMPLEMENTATION-ONLY | low-level representation may be conventional, but each opcode corresponds to an already justified semantic distinction |
| portable VM registers/stack/control | IMPLEMENTATION-ONLY | not reflected into A/B ontology |

Static audit finds no canonical class/function ontology named `Function`, `Parameter`, `Return`, `Frame`, `While`, `BooleanValue` or `Statement`, no canonical import from historical `reference_models`, and no Megillah/calendar-specific special case.

Historical A12/B11 blockers described above are superseded for the current A13/B12 Core frontier. They remain in the audit as lineage evidence, not current status.

## M4.1 remediation delta

See `C_M4_1_ANTI_IMITATION_DELTA.md`. The explicit continuation stack is IMPLEMENTATION-ONLY; semantic observation excludes allocator serials; role target/value separation remains correspondence-based; the verifier enforces A13/B12 invariants and does not create new language ontology.

## C M4.2 remediation delta

The explicit activation/continuation machinery remains **IMPLEMENTATION_ONLY**. Removing the fixed 10,000-active-performance quota is not a new language feature; it removes an implementation convention that had incorrectly become an observable semantic ceiling. Optional caller budgets and active-performance counters are tooling/debug controls only and are excluded from the semantic observation quotient. Actual resource failure remains outside the Marak language error ontology.
