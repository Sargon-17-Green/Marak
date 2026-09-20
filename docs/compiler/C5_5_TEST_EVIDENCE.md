# C5.5 — Program Input Source & Binding Integration — Test Evidence

Status: implementation code candidate verified on branch `workstream-c/c5-5-program-input-binding`.

## Baseline and scope

- canonical production baseline: `aede14151708d71b25235ed89fb81cba71e95ed5`
- post-audit code evidence head: `3dbed236f77a3b9937789f09cce6ba11962dfd96`
- Draft PR: #15
- C5.1–C5.4 remain frozen dependencies.
- Workstream D / Megillah conformance is not started.
- No Megillah source or semantics are modified.
- No transport, CLI parameter mapping, HTTP/JSON/stdin/argv/environment/file binding syntax, positional parameters, defaults, mutable Program Inputs, generic Integer/Boolean, modules, I/O, new loops, iterator/cursor, or new Collection capability is introduced.

## Candidate contract versions

- compiler: `0.5.5-alpha.1`
- Python package: `0.5.5a1`
- HAST: `core-hast-0.6-candidate-1`
- IR: `core-ir-0.6-candidate-1`
- artifact: `core-artifact-0.6-candidate-1`
- portable backend: `portable-ir-vm-0.6-candidate-1`
- IR reference: `core-ir-reference-0.6-candidate-1`
- construction registry: `c5.5-a15-b13.1`
- language edition: unchanged, `core-0.1-integration-candidate-a13-b12`

Artifact 0.5 is rejected rather than silently reinterpreted as 0.6.

## Source-first declaration and reference evidence

The current production registry admits Program Input declarations only as top-level `PreparatoryUnit` productions.

Supported declarations:
- Natural — `מספר`
- Symbol(D) — exact previously visible Symbol domain
- BidirectionalIndex — `מספר שנה`
- Collection — the exact C5.3 admitted `CollectionKind`, including admitted nested books

Supported reads:
- Natural — `HastProgramInputNumber` / `IRReadProgramInputNumber`
- Symbol, Index and Collection — `HastProgramInputValue` / `IRReadProgramInputValue` with exact domain metadata

The Collection reference receives its recursive domain from the input declaration; no consumer-side expected-type rescue is used. Symbol reads independently name their Symbol domain and must match the declared input contract.

C5.4 composition is explicit: a Natural Program Input read may flow through the existing dynamic `CountAsNumber` recurrence path. This is a composition production, not a second numeric category.

## Source identity, ownership and visibility evidence

Program Input Roles are resolved semantic identities, not host dictionary keys or positional slots.

Tests prove:
- declaration role-name repetition must match;
- duplicate Program Input role declaration is rejected;
- reference before declaration is rejected;
- undeclared reference is rejected;
- named act body visibility is snapshotted at definition time; no hoisting is added;
- two same-domain inputs remain distinct identities;
- caller binding order is irrelevant;
- raw role spelling cannot construct a valid `InputBinding`;
- a `ValidatedInvocation` validated for Program A is revalidated and rejected for Program B when identities do not belong to B.

### Canonically verifiable program ownership

C5.5 found and remediated an ownership weakness during adversarial review: merely storing an owner string in `ProgramInputId` was not sufficient, because a valid-digest forged artifact could otherwise change both the Program Input contract and its reads consistently.

The final implementation derives Program Input ownership from a canonical SHA-256 fingerprint of source-independent IR semantics:

- source spans are excluded;
- the owner field itself is excluded to avoid circular hashing;
- Program Input serial/spelling and the rest of program IR semantics participate;
- the verifier recomputes the fingerprint from decoded IR;
- all Program Input identities in one program must carry that exact owner.

A dedicated valid-digest adversarial test changes both declaration and read ownership consistently and is rejected with `IR_PROGRAM_INPUT_OWNERSHIP`.

Deeper forged-domain/read tests recompute the canonical owner after tampering so that ownership validation succeeds and the independent `IR_PROGRAM_INPUT_READ` / domain gates are still exercised.

Charter-invariance tests verify punctuation, line breaks, Markdown, niqqud, and irrelevant Latin/Arabic-digit material do not change the semantic Program Input contract identity.

## Invocation lifecycle and pre-Preparation boundary

The production lifecycle is tested as:

1. compile source and Program Input contract;
2. supply semantic `InputBinding` values;
3. validate all bindings;
4. form immutable `ValidatedInvocation` only on success;
5. begin Preparation only after validation;
6. begin Principal after Preparation.

Invalid invocation returns a distinct `InvalidInvocation`, never a Marak `RuntimeError`, `InvalidProgram`, or generic host failure.

The frozen categories are preserved exactly:
- `MISSING_INPUT_BINDING`
- `EXTRA_INPUT_BINDING`
- `DUPLICATE_INPUT_BINDING`
- `INPUT_DOMAIN_MISMATCH`

The critical phase-order test uses a program whose Preparation would raise the existing Natural arithmetic runtime error under a valid binding. Missing, extra, duplicate, and wrong-domain invocations instead return `InvalidInvocation` before that initializer is evaluated. No partial Preparation state is exposed.

## Production API evidence

Program Input is not hidden behind a test-only helper.

Production paths exercised:
- `run_source(..., bindings=...)`
- `run_reference(..., bindings=...)`
- `execute_reference(..., bindings=...)`
- `execute_ir_reference(..., bindings=...)`
- `execute_ir(..., bindings=...)`

`run_source` is directly tested for:
- successful semantic binding;
- a Natural much larger than fixed-width host integer ranges (`10**200 + 12345`);
- missing binding returning a distinct `InvalidInvocation`.

Programs with no Program Inputs continue to execute with the existing default/no-binding call path.

## Typed flow evidence

End-to-end source-first tests compare HAST reference, canonical-IR reference, and portable backend observations.

Natural:
- Program Input -> Preparation Place initializer;
- Program Input -> mutable working state;
- direct Principal arithmetic/use;
- named act body;
- two same-domain inputs with reversed caller binding order;
- repeated reads after Place mutation;
- Natural input as exact C5.4 recurrence count;
- huge unbounded Natural through public `run_source`.

Symbol(D):
- input -> typed Place;
- typed named role association;
- output;
- immediate-result read;
- exact Symbol domain preserved.

BidirectionalIndex:
- input -> typed state;
- existing Index successor operation;
- reread after state mutation proves input immutability.

Collection:
- input -> state carrier;
- existing append/count/select operations;
- append creates a new value and does not mutate the input.

Nested Collection:
- `Collection<Collection<Natural>>` input preserves recursive element-domain metadata;
- nested select/count behavior uses the existing C5.3 operations.

## Static source negatives

The source contract suite rejects:
- role-name mismatch in declaration;
- duplicate Program Input role;
- reference before declaration;
- reference to undeclared role;
- wrong typed reference head;
- wrong Symbol domain;
- declaration after `ועתה`;
- declaration embedded in act-body material;
- positional/“first argument” forms;
- “first given number” forms;
- stdin/input wording;
- generic type notation;
- `main`;
- hidden/default input wording;
- Program Input replacement/mutation wording.

Scope guards verify the new production family is limited to `C55.INPUT.*`, with only preparatory/value/read composition categories and no new executable action family.

## Artifact adversarial evidence

`tests/test_c5_5_artifact_adversarial.py` includes valid-digest or canonical-IR adversarial cases for:
- undeclared ProgramInputId read;
- forged ProgramInputId;
- consistently forged program owner;
- duplicate Program Input contracts;
- conflicting Program Input contracts;
- mixed program owners;
- Natural read against non-Natural contract;
- typed Index read against incompatible contract;
- Symbol read against wrong Symbol domain;
- Collection element-domain forgery;
- nested Collection element-domain forgery;
- unknown Program Input read tag;
- missing required read fields;
- forged optional/default metadata;
- forged bound invocation value in reusable artifact;
- prior artifact version 0.5.

Reusable artifacts contain contracts and reads, never invocation values.

## Differential runtime evidence

For each relevant execution case, the test helpers project and compare:
- HAST reference outcome;
- canonical IR reference outcome;
- portable backend outcome.

Agreement is checked for successful Natural/Symbol/Index/Collection/nested Collection flows, InvalidInvocation categories, binding-order independence, and cross-program ownership.

All three engines validate invocation before evaluator/VM Preparation.

## CI evidence — implementation code head

GitHub Actions push run #269 / ID `35531901936` completed with **13/13 jobs successful** on implementation evidence head `b2b6e558a61cd2ded9173c042f435377b232f217`:

- core — PASS
- Tooling portability Ubuntu — PASS
- Tooling portability Windows — PASS
- C5.1 domain infrastructure Ubuntu — PASS
- C5.1 domain infrastructure Windows — PASS
- C5.2 Symbol/Index/Ordering Ubuntu — PASS
- C5.2 Symbol/Index/Ordering Windows — PASS
- C5.3 Finite Ordered Collections Ubuntu — PASS
- C5.3 Finite Ordered Collections Windows — PASS
- C5.4 Exact Counted Recurrence Ubuntu — PASS
- C5.4 Exact Counted Recurrence Windows — PASS
- C5.5 Program Input Binding Ubuntu — PASS
- C5.5 Program Input Binding Windows — PASS

C5.5 Ubuntu:
- targeted C5.5 source/invocation/artifact/scope: **33 passed in 0.61s**
- full pytest: **450 passed + 126 subtests in 13.49s**

C5.5 Windows:
- targeted: **33 passed in 0.91s**
- full pytest: **450 passed + 126 subtests in 17.57s**

Required proposal regressions on both C5.5 jobs:
- A13: **289 checks PASS**
- B12: **33 semantic tests + RM witness PASS**
- A15: **335,280 case checks PASS**, including **9,999** frozen A13 numerals
- B13: **28 reference tests PASS**
- B14: **22 integration tests PASS**
- A16: **2,518 positive + 30 negative = 2,548 checks PASS**
- B15: **29 independent tests PASS**

## Canonical regeneration and cross-platform hashes

Run #269 regenerated the current registry and all canonical artifacts on both Ubuntu and Windows and then ran committed-byte verification with `git diff --exit-code`.

Registry SHA-256 on both hosts:

`9e1c9aae709697b3a10f3b49f97cd38fa9374712cc6c2a26f95b1b41f237ff45`

Canonical artifact SHA-256 values on both hosts:

- basic_update: `3a83a79e589cd1817f0aa57ad87e1c8f0fd0bfbf4a739c8f1db6c708611012b5`
- immediate_result: `0fec6c2eca232dd5e9529c82dbbfed12aab27eae24859f45c797b6e726b75fae`
- natural_subtraction: `8c3ac9f94de428da8f73e571b6f79186ec7ff0bfd1867f07562d121accf218a1`
- normal_completion: `5d7ee246af63453f2d5666c83cd5e492a631769ac0dd591961e2a25da4ad13ae`
- output_not_return: `145d64b4c7c2068622e41dbef0da1f58fcaa153195e20595783a8d256efec3a1`
- post_action_countdown: `bad69bea452fd5f929708a6f88a6e62c20a2b038d8622611e4bbe6b7fe31eb44`
- recursive_countdown: `b5277c6d1e0e34a28012c23240045597eb06c60f162f4da5293f716b9724ebe7`
- role_association: `48db096b29caa6dad55f0ff4aff71d4c686cbef055c4568779cf1d7cb0e84782`
- tiny_rm: `a6d5cd1f430d92355deee1125b19033bd974821d1075d056f243ee591c10aad2`

The registry was deliberately regenerated again after adding the C5.5 Natural-read-to-C5.4-`CountAsNumber` composition production. That changed only the expected registry bytes/hash; canonical artifacts stayed stable after the 0.6 regeneration.

## Resource observations

Resource sanity is observational, not a language threshold.

Ubuntu (run #269):
- compile: **6.309 ms**
- 64 iterations: **0.212 ms**
- 256: **0.629 ms**
- 1024: **2.470 ms**
- 4096: **70.364 ms**
- traced peak at 4096: **1,944 bytes**

Windows (run #269):
- compile: **8.644 ms**
- 64 iterations: **0.273 ms**
- 256: **0.837 ms**
- 1024: **3.261 ms**
- 4096: **178.617 ms**
- traced peak at 4096: **1,944 bytes**

No semantic input-size or recurrence-size limit was added.

## Resolved integration findings

C5.5 integration exposed and resolved:

1. **Program ownership collision weakness** — the inherited C5.1 `ProgramInputId(serial, spelling)` could collide across distinct programs. C5.5 adds an owning reusable-program contract.
2. **Owner metadata was initially not self-verifiable** — storing an owner string alone did not defeat consistent valid-digest artifact forgery. The final owner is recomputed from source-independent canonical IR and checked at artifact/canonical-IR validation.
3. **Contract bump fallout** — HAST/IR/artifact/backend/reference/registry/package versions and frozen version fixtures were aligned with 0.6/0.5.5.
4. **Abstract C5.1 fixture compatibility** — C5.1's preparation-independent abstract Program Input contract fixture was kept valid; production source programs receive a canonical owner during successful checking, while canonical IR remains strict.
5. **Canonical registry regeneration drift** — adding the explicit Natural-input-to-`CountAsNumber` composition production changed registry bytes after an earlier regeneration. Registry was regenerated again and portability expectation updated to `9e1c9a...`.
6. **Adversarial test layering** — once owner verification was strengthened, deep domain-forgery fixtures failed earlier at ownership. Fixtures now recompute the canonical owner after semantic tampering when the purpose is to exercise the deeper read/domain validator; a separate test preserves the ownership-forgery check.
7. **Same-program ProgramInput identity collision gap** — canonical IR initially rejected only duplicate full `ProgramInputId` objects. Post-handoff audit proved that a valid-digest artifact could otherwise encode two source-unrepresentable inputs with the same semantic serial but different spelling, or the same role spelling with different serials. Canonical validation now rejects both collision classes, with a dedicated adversarial regression.

No known semantic blocker remains on the implementation side at the code-evidence head. Independent Master review remains required.
