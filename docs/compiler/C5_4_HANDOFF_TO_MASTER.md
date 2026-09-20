C5.4 READY FOR MASTER REVIEW

baseline:
`a63acfb52b73357bbbf42d1df4d49d068f8f7f51`

branch:
`workstream-c/c5-4-exact-counted-recurrence`

PR:
#14 — Draft, open, unmerged
https://github.com/Sargon-17-Green/Marak/pull/14

HEAD:
Use the branch HEAD containing this handoff document. The final delivery message records its exact SHA after documentation-only verification.

compiler version:
`0.5.4-alpha.1`

HAST version:
`core-hast-0.5-candidate-1`

IR version:
`core-ir-0.5-candidate-1`

artifact version:
`core-artifact-0.5-candidate-1`

registry version:
`c5.4-a15-b13.1`

language edition:
unchanged — `core-0.1-integration-candidate-a13-b12`

literal recurrence:
Implemented the three A15 profiles: `פעם אחת A`, `שתי פעמים A`, and controlled feminine `N פעמים A` for admitted direct N>=3. Direct count morphology reaches the A15 frontier; tests separately prove that this frontier is not a semantic RepeatExactly ceiling.

dynamic recurrence:
Implemented `פעמים COUNT_AS_NUMBER A`. CountAsNumber is derived from the existing Natural Value grammar by inflecting only the initial numeric head to `כמספר`, then lowered through the same Natural resolver/domain machinery. Place reads, arithmetic and Collection count are covered. No second numeric value category was added.

single-evaluation proof:
PASS. A count read from a Place that the body mutates is evaluated once at entry; entry 3 executes exactly three iterations and ends at 6. A second proof uses a computed count over two mutable places. IR/artifact preserve the count expression rather than a per-iteration query.

zero/one/large semantics:
PASS. Computed zero performs no body action; dynamic one performs one; practical finite execution covers 4096 iterations; direct 99,999,999 and dynamic 100,000,000 are admitted at compile/IR level without a semantic maximum.

error/divergence effects:
PASS. Count failure occurs before the first iteration; earlier completed effects remain, body effects are zero, and later continuation does not run. Iteration-k failure preserves completed prior iterations and the ordinary committed prefix of the failing action. Diverging body prevents later iterations. No rollback transaction was introduced.

output interaction:
PASS. Repeated named-act performances produce ordinary zero/one outputs per occurrence and in order; no implicit result Collection exists. No-output occurrences stay empty. Failure after output retains the completed output. Recurrence does not manufacture “last-iteration” immediate-result provenance. Direct multiple Produce in one occurrence retains the existing `CORE_OUTPUT_CARDINALITY_ERROR`.

source-first differential tests:
PASS — C5.4 targeted suite runs source through normalize/lex/parse/resolve/validate/HAST/IR/artifact/verify/execute and compares HAST reference, IR reference and portable backend. Run #206: 35 targeted tests PASS on Ubuntu and Windows.

negative/attachment tests:
PASS — wrong gender, bare פעמים, postposed count, double numeric head, non-Natural head, invented direct zero, generic repeat/for/while, Arabic-digit count syntax, implicit multi-action body, layout/punctuation scope, and backward/extra attachment are rejected. Charter transparency variants preserve meaning.

artifact trust tests:
PASS — valid-digest non-Natural Index/Collection/Symbol count operands, composite body, unknown tag, missing count, forged re-evaluation metadata, and previous schema/version are rejected. Artifact 0.4 is not reinterpreted as 0.5.

scope guards:
PASS — no Program Input source grammar, Megillah special case, iterator/cursor Value, loop index, generic while/for, mutable Collection semantics, implicit output collection, transport semantics, recurrence-specific semantic cap, or recurrence-depth Python execute/action recursion.

C5.1 regression:
PASS on Ubuntu and Windows in run #206.

C5.2 regression:
PASS on Ubuntu and Windows in run #206.

C5.3 regression:
PASS on Ubuntu and Windows in run #206.

A13/B12/A15/B13/B14/A16/B15:
PASS. Evidence includes A13 289 checks; B12 33-test semantic suite + RM witness; A15 335,280 case checks and 9,999 frozen A13 numerals; B13 28 tests; B14 22 tests; A16 2,548 checks; B15 29 tests.

Ubuntu CI:
PASS — C5.4 targeted 35/35; full pytest 411 + 126 subtests; all required proposal regressions; resource sanity; registry/artifact regeneration and clean committed-byte verification.

Windows CI:
PASS — C5.4 targeted 35/35; full pytest 411 + 126 subtests; all required proposal regressions; resource sanity; registry/artifact regeneration and clean committed-byte verification.

registry/artifact regeneration:
PASS cross-host. Registry SHA-256:
`cef84d06ff6f3f1a9212e812ceb3a8326c3687f75d0c7da093ed782febdb28af`
Ubuntu and Windows report identical hashes for the registry and all nine canonical artifacts; committed-byte diff checks pass.

resource observations:
Observational only, no threshold. At 4096 iterations:
- Ubuntu: compile 5.041 ms; execute 12.297 ms; traced peak 261,136 bytes.
- Windows: compile 5.409 ms; execute 12.538 ms; traced peak 261,136 bytes.
Runtime uses explicit recurrence continuation frames rather than Python recursion by N.

known issues:
No known C5.4 semantic blocker. Performance values are observations, not language contracts.

integration findings:
Resolved during C5.4: current-registry family recognition for `c5.4-`; coherent 0.5 canonical-byte regeneration; corrected adversarial error-boundary fixture; standalone resource tool; precise recurrence-recursion scope guard.

The PR remains Draft and unmerged. This handoff does not claim MASTER ACCEPTED and does not authorize C5.5.
