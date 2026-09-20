# C5.4 — General Exact Counted Recurrence — Test Evidence

Status: implementation candidate verified on branch `workstream-c/c5-4-exact-counted-recurrence`.

## Baseline and scope

- Production baseline: `a63acfb52b73357bbbf42d1df4d49d068f8f7f51`.
- C5.1, C5.2 and C5.3 are treated as frozen production dependencies.
- C5.4 integrates only A15/B13 general exact counted recurrence (`RepeatExactly`).
- No Program Input source grammar, Megillah edits, Collection feature expansion, generic Integer, Boolean Value, iterator/cursor/loop-index Value, implicit block syntax, generic while/for, transport semantics, or C5.5 work is included.

## Versioned contracts

C5.4 changes serialized compiler contracts, so the candidate dimensions advance coherently:

- compiler: `0.5.4-alpha.1`
- HAST: `core-hast-0.5-candidate-1`
- IR: `core-ir-0.5-candidate-1`
- artifact: `core-artifact-0.5-candidate-1`
- portable backend: `portable-ir-vm-0.5-candidate-1`
- IR reference: `core-ir-reference-0.5-candidate-1`
- construction registry: `c5.4-a15-b13.1`
- language edition: unchanged, `core-0.1-integration-candidate-a13-b12`

Artifact 0.4 is rejected rather than silently reinterpreted.

## Surface and lowering evidence

The current registry admits exactly these new counted-consequence profiles:

- `פעם אחת ATOMIC_ACTION`
- `שתי פעמים ATOMIC_ACTION`
- A15 controlled feminine `REPEAT_COUNT פעמים ATOMIC_ACTION`
- `פעמים COUNT_AS_NUMBER ATOMIC_ACTION`

`CountAsNumber` is mechanically derived from existing admitted Natural `NumberValue` productions by changing only the initial numeric head to `כמספר`; it lowers through the original Natural resolver. Collection count is included through the already-Natural `מספר הדברים ...` production. No second numeric value category or expected-type rescue is introduced.

Canonical representation is explicit:
- `HastRepeatExactly(count: HastNumber, action: HastExecutable)`
- `IRRepeatExactly(count: IRNumber, action: IRAction)`

The count expression remains present in IR/artifact. Dynamic current-place tests assert the IR operand remains `IRReadCurrentFact`; computed counts remain arithmetic IR rather than a compile-time host integer.

## Exact-law source-first evidence

`tests/test_c5_4_recurrence.py` covers end-to-end:
`source -> normalize -> lex -> parse -> resolve -> validate -> HAST -> IR -> artifact -> verify -> execute`,
with HAST reference / IR reference / portable backend observables compared.

Covered cases include:
- literal 1 and 2;
- literal 3, 7, 10, 1000;
- direct morphology frontier 99,999,999 (compile/IR proof);
- dynamic arithmetic count beyond that frontier, 99,999,999 + 1 (compile/IR proof; no semantic cap);
- dynamic current-place count;
- dynamic arithmetic count over mutable places;
- dynamic count from Collection count;
- computed zero and dynamic one;
- count place mutated by the repeated body, proving once-at-entry evaluation;
- repeated named-act performances;
- exact accumulated effects;
- repeated Collection operation;
- repeated Index-bearing and Symbol-bearing act occurrences;
- recursive act as repeated action under the fuel harness;
- error at an iteration boundary;
- count-evaluation error before the first iteration;
- output ordering, no-output occurrences, immediate-result provenance expiry, and failure after output;
- following `ואחרי כן` outside the recurrence boundary.

## Single-evaluation proof

The principal adversarial source initializes `מנין=3`, uses its current Natural value as the recurrence count, and increments `מנין` in each repeated action. All three engines terminate after exactly three iterations with `מנין=6`. Re-evaluating the count per iteration would not produce that result and would not terminate under that mutation pattern.

A second case computes the count from two mutable places and then mutates both from the body. The number of occurrences is determined from the entry values, not from later state.

IR/artifact shape contains a single count operand on `IRRepeatExactly`; forged per-iteration re-evaluation metadata is rejected as a wrong artifact field set.

## Zero, error, divergence, and effect ordering

- computed Natural zero executes the repeated action zero times;
- dynamic one executes it once;
- count-evaluation runtime underflow occurs before the first body action;
- an action completed before the recurrence remains committed after count failure;
- body destination state is unchanged when count evaluation fails;
- later continuation is suppressed after fatal runtime error;
- on iteration-k failure, effects committed by prior iterations and the ordinary committed prefix of the failing action remain;
- later iterations do not begin;
- recursive/diverging body under fuel never advances to a later iteration.

No transaction or rollback layer was added.

## Outputs and provenance

- repeated `Perform(act)` occurrences produce their ordinary zero/one output events in occurrence order;
- no implicit output Collection is created;
- no-output occurrences remain no-output;
- direct verifier-level `RepeatExactly(2, Produce)` in one occurrence produces the first output and then reaches the existing `CORE_OUTPUT_CARDINALITY_ERROR` on the second Produce;
- an output emitted before a later failure in the same occurrence remains observable;
- a recurrence as a whole does not manufacture “last iteration” immediate-result provenance; an immediate result reference after the recurrence is rejected by the existing structural provenance rule.

## Attachment and negative grammar

Negative/adversarial cases reject:
- bare `פעמים`;
- wrong gender morphology such as `שבעה פעמים`;
- postposed dynamic counts;
- `פעמים כמספר המספר ...`;
- non-Natural typed heads such as an Index head after `כמספר`;
- invented direct zero count syntax;
- generic `repeat`, `for`, `while`;
- Arabic digits as semantic count syntax;
- implicit second/multi-action body material;
- punctuation/newline-defined scope.

Charter transparency variants preserve the same recurrence meaning and boundary.

## Artifact trust boundary

`tests/test_c5_4_artifact_adversarial.py` includes valid-digest tampering for:
- Index count operand;
- Collection count operand;
- Symbol count operand;
- composite/multiple repeated body;
- unknown recurrence tag;
- missing count;
- forged `reevaluate_each_iteration` metadata;
- previous artifact schema/version.

Non-Natural count operands that survive decoding are categorized as `RECURRENCE_COUNT_DOMAIN_ERROR`; statically knowable domain mismatches are rejected by canonical validation before execution.

## Runtime/resource architecture

All three runtimes use an explicit continuation frame for `RepeatExactly`. Finite N does not recurse through Python `execute()`/`action()` depth. Scope guards reject recurrence-specific semantic caps such as `MAX_REPEAT`, `MAX_ITERATIONS`, repeat limits/caps, hidden iterators, or loop-index Values.

Resource sanity is observational only; no threshold is a language contract.

Ubuntu, 4096 iterations:
- compile: 5.041 ms
- execute: 12.297 ms
- traced peak: 261,136 bytes

Windows, 4096 iterations:
- compile: 5.409 ms
- execute: 12.538 ms
- traced peak: 261,136 bytes

Additional sampled iterations were 64, 256, and 1024. Execution growth is consistent with explicit finite iteration and no recurrence-depth stack growth in these observations.

## CI evidence

GitHub Actions run `35524819230` (run #206) on the implementation/evidence code head before this documentation commit completed with all 11 jobs successful:

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

C5.4 Ubuntu:
- targeted: 35 passed in 0.78s
- full pytest: 411 passed + 126 subtests in 15.54s

C5.4 Windows:
- targeted: 35 passed in 0.91s
- full pytest: 411 passed + 126 subtests in 16.79s

Required proposal regressions passed on both C5.4 jobs:
- A13: 289 checks PASS
- B12: semantic suite 33 tests + RM witness PASS
- A15: 335,280 case checks PASS; frozen A13 numerals checked: 9,999
- B13: 28 reference tests PASS
- B14: 22 integration tests PASS
- A16: 2,548 checks (2,518 positive + 30 negative) PASS
- B15: 29 tests PASS

## Canonical generation

Registry SHA-256:
`cef84d06ff6f3f1a9212e812ceb3a8326c3687f75d0c7da093ed782febdb28af`

Canonical artifacts:
- basic_update: `f08809a1733acad3b1d374e4eaa1dc48d850b7dd5bd2f4285ad106cf9ecb0ea2`
- immediate_result: `70d7003a69c7d471fbf0446a73f211a5a7921c9b7c05add1a69baa46b96ae5b0`
- natural_subtraction: `9f44ed2d87d57cfb5de2c2032f6e0ae6fdf731916e7b435060c687d0a58d7da0`
- normal_completion: `40b53b5b70e7c617ecc4f1de3bc53fd3ef08b23ec89ff0a7f9d1323cc8821c00`
- output_not_return: `4470b098429ffc5033add4cecea5c91051f4d00192d2906d7d134ef1ee34398e`
- post_action_countdown: `0e021b67477c4c1c9f3bcce679c69e61b5cad90c773574fb7560e23236037944`
- recursive_countdown: `48929ba55a5556b5b1738a72f531e9a96390c69a7f1dd3b3763e85f36655181b`
- role_association: `028242102ced06bb3e58fe5d453e90a02f010c85a1e30f0cfda28042b77e7886`
- tiny_rm: `7aada7cd3987f6ffd24c9c337b076aee59d93e2b0f56033835705b3efd402b4b`

Ubuntu and Windows regeneration produced the same registry/artifact hashes, and committed-byte `git diff --exit-code` verification passed.

## Resolved integration findings

During integration, CI exposed and C5.4 resolved:
1. the current-registry family predicate initially omitted `c5.4-`, so valid whole programs parsed but were not lowered to HAST;
2. the 0.5 contract bump required canonical artifact/registry regeneration and explicit portability expectation updates;
3. an early count-error test used a constant underflow and correctly hit static B12 rejection instead of the intended runtime boundary; the proof now uses dynamic mutable-place reads;
4. the resource sanity script initially imported test-only helpers and was made standalone;
5. an over-broad recursion scope test was narrowed to the actual guarantee: recurrence cardinality must not recurse through runtime `execute/action`.

All are resolved on the review branch.

## Known issues

No known C5.4 semantic blocker remains. Resource timings are observations, not guarantees. Master review remains independent, and the Draft PR is intentionally unmerged.


# C5.4-MR-001 remediation evidence

Master finding `C5.4-MR-001` identified resolver/runtime canonical-provenance drift at recurrence entry. The remediation code commit is:

`cd34efdf0bf2d05c0e135addc6d1af8c5b1d2d12`

## Root cause and production correction

`compiler/resolve/a13_program.py` previously passed the enclosing sequence's `recent_act` into recurrence bodies. This disagreed with frozen B12 semantics, canonical IR validation, and all three runtimes, which start recurrence bodies without incoming immediate-result provenance.

The resolver now applies the same contract consistently:

- `C54.REPEAT.ONE/TWO/MANY/DYNAMIC`: dynamic `CountAsNumber` still lowers with incoming `recent_act`; the repeated `AtomicAction` lowers with `recent_act=None`.
- historical `A10.REPEAT.COUNTED`: the repeated action lowers with `recent_act=None`.
- `A10.RECURRENCE.AFTER_UNTIL`: the repeated action lowers with `recent_act=None`; its proposition receives only provenance produced by that just-completed repeated action when it is a `Perform`.

No runtime, artifact, IR, HAST, registry, language-edition, or semantic-cap change was required.

## New source regressions

`tests/test_c5_4_recurrence.py` now proves:

1. an immediate result from a performance before `RepeatExactly` is statically unavailable inside its body and yields `REF0112`;
2. that same incoming result may remain valid as the dynamic recurrence count;
3. the count can observe incoming provenance while iteration 1 cannot reuse it;
4. historical fixed counted recurrence has the same fresh-body provenance boundary;
5. post-action recurrence does not inherit pre-recurrence provenance in its repeated action, while the post-action proposition can observe provenance freshly produced by the repeated `Perform`;
6. source resolution and `validate_canonical_ir()` agree at the recurrence boundary: the invalid case is rejected by source resolution, while a valid dynamic-count case lowers to canonical IR successfully.

## Remediation CI

GitHub Actions run #211 / `35527803256` on the remediation code commit completed with all 11 jobs successful.

C5.4 Ubuntu:
- targeted source/artifact/scope: 41 passed in 0.48s
- full pytest: 417 passed + 126 subtests in 10.17s
- resource sanity at 4096: compile 2.552 ms, execute 6.159 ms, traced peak 261,136 bytes

C5.4 Windows:
- targeted source/artifact/scope: 41 passed in 0.99s
- full pytest: 417 passed + 126 subtests in 16.61s
- resource sanity at 4096: compile 5.148 ms, execute 12.297 ms, traced peak 261,136 bytes

Required proposal regressions passed:
- A13: 289 checks
- B12: 33 semantic tests + RM witness
- A15: 335,280 case checks; 9,999 frozen A13 numerals
- B13: 28 tests
- B14: 22 tests
- A16: 2,548 checks
- B15: 29 tests

C5.1, C5.2, C5.3, core, and tooling-portability jobs also passed on their required platforms in run #211.

## Canonical regeneration after remediation

Registry SHA-256 is unchanged:

`cef84d06ff6f3f1a9212e812ceb3a8326c3687f75d0c7da093ed782febdb28af`

Ubuntu and Windows regenerated byte-identical canonical artifacts with the existing hashes:

- basic_update: `f08809a1733acad3b1d374e4eaa1dc48d850b7dd5bd2f4285ad106cf9ecb0ea2`
- immediate_result: `70d7003a69c7d471fbf0446a73f211a5a7921c9b7c05add1a69baa46b96ae5b0`
- natural_subtraction: `9f44ed2d87d57cfb5de2c2032f6e0ae6fdf731916e7b435060c687d0a58d7da0`
- normal_completion: `40b53b5b70e7c617ecc4f1de3bc53fd3ef08b23ec89ff0a7f9d1323cc8821c00`
- output_not_return: `4470b098429ffc5033add4cecea5c91051f4d00192d2906d7d134ef1ee34398e`
- post_action_countdown: `0e021b67477c4c1c9f3bcce679c69e61b5cad90c773574fb7560e23236037944`
- recursive_countdown: `48929ba55a5556b5b1738a72f531e9a96390c69a7f1dd3b3763e85f36655181b`
- role_association: `028242102ced06bb3e58fe5d453e90a02f010c85a1e30f0cfda28042b77e7886`
- tiny_rm: `7aada7cd3987f6ffd24c9c337b076aee59d93e2b0f56033835705b3efd402b4b`

On both hosts, `git diff --exit-code -- spec/CURRENT_CONSTRUCTION_REGISTRY.json artifacts` passed.

The remediation remains pending independent Master re-review. It is not a claim of Master acceptance and does not authorize C5.5.
