C5.5 READY FOR MASTER REVIEW

baseline:
`aede14151708d71b25235ed89fb81cba71e95ed5`

branch:
`workstream-c/c5-5-program-input-binding`

PR:
`#15 — Draft, open, unmerged`
`https://github.com/Sargon-17-Green/Marak/pull/15`

HEAD:
Review the branch HEAD containing this handoff document. The implementation code evidence head before the final documentation-only commit is:
`b2b6e558a61cd2ded9173c042f435377b232f217`

compiler version:
`0.5.5-alpha.1`

HAST version:
`core-hast-0.6-candidate-1`

IR version:
`core-ir-0.6-candidate-1`

artifact version:
`core-artifact-0.6-candidate-1`

registry version:
`c5.5-a15-b13.1`

language edition:
`core-0.1-integration-candidate-a13-b12` — unchanged.

source declaration:
Top-level Preparation-only required Program Input declaration:
`יהי למלאכה הזאת דבר ושמו ROLE ובטרם תחל המלאכה הזאת יעמד DOMAIN_HEAD תחת הדבר אשר למלאכה הזאת שמו ROLE`.
The two ROLE occurrences must resolve to the same role name. No executable Program Input declaration/action is introduced.

Natural reference:
`המספר אשר עומד תחת הדבר אשר למלאכה הזאת שמו ROLE`

Symbol reference:
`השם אשר במשפחת השמות אשר שמה DOMAIN עומד תחת הדבר אשר למלאכה הזאת שמו ROLE`

Index reference:
`מספר השנה אשר עומד תחת הדבר אשר למלאכה הזאת שמו ROLE`

Collection reference:
`הספר אשר עומד תחת הדבר אשר למלאכה הזאת שמו ROLE`
The declared Program Input contract supplies the exact recursive Collection domain.

ProgramInput identity model:
Resolved `ProgramInputId` contains serial, spelling metadata, and an owning reusable-program contract. Invocation uses resolved identity, not position, declaration order, raw spelling, or host dictionary keys.

program ownership:
Production programs finalize the owner as `marak-ir-contract-sha256:<digest>`, computed from source-independent canonical IR semantics with source spans and the owner field excluded. Canonical IR verification recomputes the fingerprint. A consistently forged declaration+read owner is rejected with `IR_PROGRAM_INPUT_OWNERSHIP`.

introduced-before-use:
PASS. No hoisting. Reads before declaration and undeclared reads are rejected. Named act body resolution sees only Program Inputs visible when the body is defined.

immutability:
PASS. Invocation association is immutable for the invocation. Repeated reads after Place mutation recover the same input. Collection append is pure and does not mutate the bound Collection.

invocation production API:
Production paths accept semantic bindings through `run_source`, `run_reference`, HAST reference execution, IR reference execution, and portable `execute_ir`. No transport adapter is added.

validated invocation:
`ValidatedInvocation` is contextual, not a bearer token. Every execution path revalidates its bindings against the target program.

pre-Preparation validation:
PASS. Missing/extra/duplicate/wrong-domain bindings return `InvalidInvocation` before any Place initializer runs. A control program proves that a valid invocation can reach a Preparation `ARITHMETIC_DOMAIN_ERROR`, while invalid invocation suppresses that Preparation entirely.

binding order independence:
PASS. Two same-domain input roles supplied in reverse caller order produce the same identity-correct result.

missing binding:
`MISSING_INPUT_BINDING` — PASS.

extra binding:
`EXTRA_INPUT_BINDING` — PASS.

duplicate binding:
`DUPLICATE_INPUT_BINDING` — PASS.

domain mismatch:
`INPUT_DOMAIN_MISMATCH` — PASS.

cross-program binding test:
PASS. Two distinct programs are constructed with colliding input serial/spelling metadata. Their canonical program owners differ. Program A's binding is extra for B and B's own binding is missing. A `ValidatedInvocation` from A is also revalidated and rejected by all three B execution paths.

Natural flow:
PASS: Preparation initializer, mutable working state, Principal use, named act body, binding-order test, immutable rereads, production `run_source`, C5.4 exact recurrence count composition, and a `10**200 + 12345` Natural.

Symbol flow:
PASS: exact Symbol(D) input -> typed Place -> typed role -> output -> immediate-result flow.

Index flow:
PASS: BidirectionalIndex input -> typed state -> existing Index operation -> immutable reread.

Collection flow:
PASS: Collection<Natural> input -> state carrier -> append/count/select; input remains unchanged.

nested Collection flow:
PASS: admitted `Collection<Collection<Natural>>` input preserves recursive domain and executes existing nested Collection operations.

HAST/IR input-read representation:
HAST: `HastProgramInputNumber`, `HastProgramInputValue`.
IR: `IRReadProgramInputNumber`, `IRReadProgramInputValue`.
Natural remains a Natural expression; typed reads retain exact domain.

canonical validation:
PASS. Canonical IR independently checks input contract uniqueness, exact domains, declared Symbol domains, recursive Collection domains, read-contract agreement, and recomputed program ownership.

artifact contract:
`core-artifact-0.6-candidate-1`. Reusable artifacts retain Program Input identity, owning program contract, declared domain and required nature; bound invocation values are absent. Artifact 0.5 is rejected.

artifact adversarial:
PASS. Corpus includes undeclared/forged ProgramInputId, consistent owner forgery, duplicate/conflicting/cross-owner contracts, Natural/Symbol/Index/Collection/nested-domain forgery, unknown read tag, missing fields, optional/default metadata, serialized bound value, and old artifact version.

source negatives:
PASS. Includes positional forms, “first given number”, transport/input wording, mutation/replacement, declaration after `ועתה`, body-embedded declaration, role mismatch, duplicate declaration, use-before-declaration, undeclared role, wrong typed head, wrong Symbol domain, generic type, `main`, and default syntax.

charter invariance:
PASS. Line breaks, punctuation, Markdown, niqqud, and irrelevant Latin/Arabic-digit material do not create scope/binding semantics and preserve canonical Program Input program-contract identity.

scope guards:
PASS. New source family is restricted to `C55.INPUT.*` declaration/reference/composition productions. No transport, positional/default/mutable/main/Megillah special case. Language edition unchanged.

HAST reference:
PASS.

IR reference:
PASS.

portable backend:
PASS.

differential execution:
PASS. Successful typed flows and InvalidInvocation/cross-program cases are projected and compared across all three engines.

C5.1 regression:
PASS — Ubuntu + Windows in run #264.

C5.2 regression:
PASS — Ubuntu + Windows in run #264.

C5.3 regression:
PASS — Ubuntu + Windows in run #264.

C5.4 regression:
PASS — Ubuntu + Windows in run #264.

A13/B12/A15/B13/B14/A16/B15:
PASS on both C5.5 jobs:
A13 289 checks;
B12 33 semantic tests + RM witness;
A15 335,280 case checks and 9,999 frozen A13 numerals;
B13 28;
B14 22;
A16 2,548 = 2,518 positive + 30 negative;
B15 29.

Ubuntu CI:
PASS on implementation evidence run #264 / `35531901936`.
C5.5 targeted: 32 passed in 0.83s.
Full pytest: 449 passed + 126 subtests in 17.02s.

Windows CI:
PASS on implementation evidence run #264 / `35531901936`.
C5.5 targeted: 32 passed in 0.89s.
Full pytest: 449 passed + 126 subtests in 17.04s.

registry regeneration:
PASS on Ubuntu + Windows. SHA-256:
`9e1c9aae709697b3a10f3b49f97cd38fa9374712cc6c2a26f95b1b41f237ff45`

artifact regeneration:
PASS on Ubuntu + Windows. Committed-byte verification is clean. Artifact 0.5 is not reinterpreted as 0.6.

cross-platform hashes:
Both hosts produced the same registry and nine artifact hashes:
- basic_update `3a83a79e589cd1817f0aa57ad87e1c8f0fd0bfbf4a739c8f1db6c708611012b5`
- immediate_result `0fec6c2eca232dd5e9529c82dbbfed12aab27eae24859f45c797b6e726b75fae`
- natural_subtraction `8c3ac9f94de428da8f73e571b6f79186ec7ff0bfd1867f07562d121accf218a1`
- normal_completion `5d7ee246af63453f2d5666c83cd5e492a631769ac0dd591961e2a25da4ad13ae`
- output_not_return `145d64b4c7c2068622e41dbef0da1f58fcaa153195e20595783a8d256efec3a1`
- post_action_countdown `bad69bea452fd5f929708a6f88a6e62c20a2b038d8622611e4bbe6b7fe31eb44`
- recursive_countdown `b5277c6d1e0e34a28012c23240045597eb06c60f162f4da5293f716b9724ebe7`
- role_association `48db096b29caa6dad55f0ff4aff71d4c686cbef055c4568779cf1d7cb0e84782`
- tiny_rm `a6d5cd1f430d92355deee1125b19033bd974821d1075d056f243ee591c10aad2`

resource observations:
Observational only; no performance/language threshold.
Ubuntu: compile 8.379ms; execute 64/256/1024/4096 = 0.278/0.809/3.150/89.535ms; traced peak 1,944 bytes.
Windows: compile 8.513ms; execute 64/256/1024/4096 = 0.274/0.871/3.254/180.075ms; traced peak 1,944 bytes.

known issues:
No known semantic blocker remains on the workstream side. Resource timings are observations only. Independent Master review of the actual Draft PR and final review HEAD is still required.

integration findings:
Resolved during C5.5:
1. inherited ProgramInputId serial/spelling alone was insufficient for cross-program ownership;
2. owner metadata alone was insufficient against consistent valid-digest artifact forgery, so ownership is now a recomputable canonical-IR fingerprint;
3. the 0.6 serialized-contract bump required coherent version/fixture/artifact regeneration;
4. the frozen C5.1 abstract Program Input fixture required compatibility without weakening production canonical IR;
5. adding Natural Program Input as C5.4 dynamic recurrence count changed registry bytes and required a second explicit registry regeneration;
6. adversarial fixtures were split so ownership and deeper read/domain validation are each independently exercised.

This handoff does not claim MASTER ACCEPTED.
PR #15 remains Draft/open/unmerged.
No Workstream D / Megillah conformance work has been started.
