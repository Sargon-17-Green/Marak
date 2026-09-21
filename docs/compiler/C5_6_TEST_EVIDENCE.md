# C5.6 — General BidirectionalIndex Production Integration — Test Evidence

Status: production integration candidate validated on exact implementation HEAD `0dd3e270bf769a9028df3fbf7d64cafd6a09f677`.

## Baseline

- repository: `Sargon-17-Green/Marak`
- baseline: `f7c1be2e913d73c4722f92d8c27c8c7e6dd26a91`
- branch: `workstream-c/c5-6-general-bidirectional-index-surface`
- Draft PR: #19
- A17 reviewed dependency: `50155cbf86c1cdc1111dde45464e7a9a1605f9df`
- B16 reviewed dependency: `8c164c50084a0d029cda9c9ee397b0c96d2c63c2`

## Contract matrix

- package: `0.5.6a1`
- compiler: `0.5.6-alpha.1`
- language edition: `core-0.1-integration-candidate-a13-b12`
- registry: `c5.6-a17-b16.1`
- HAST: `core-hast-0.7-candidate-1`
- IR: `core-ir-0.7-candidate-1`
- artifact: `core-artifact-0.7-candidate-1`
- IR reference: `core-ir-reference-0.7-candidate-1`
- portable backend: `portable-ir-vm-0.7-candidate-1`

## Source-first coverage

The C5.6 source suite covers:

- general origin, before and after literals;
- productive A15 feminine-count magnitude at 99,999,999;
- Program Input declaration/read in both cross-profile directions;
- place state in both cross-profile directions;
- roles in both cross-profile directions;
- all four output/immediate-result profile combinations;
- general successor/predecessor and zero crossing;
- strict Index order grid, equality-false cases, far magnitudes, and origin crossings;
- strict order in conditional and post-action recurrence contexts;
- actual same-position classification using two strict-order tests and one named decision act;
- constructive distance composition with retained Natural counter and named acts;
- existing year-oriented Collection<BidirectionalIndex> append accepting a general-profile Index Value;
- explicit `לפני` ambiguity case.

Important positive programs compare:

`HAST reference == IR reference == portable backend`.

## Negative, scope, IR, and artifact coverage

The suite rejects malformed general heads, mixed-profile literals, invented order/equality/distance surfaces, generic Index collection heads, and expected-type rescue attempts in typed state, replacement, role association, output, Program Input reference, and proposition operand contexts.

A17 words remain legal in explicit NameTerminal slots; no global reserved-word list is introduced.

Direct forged HAST verifies `DOMAIN_INDEX_LT`; direct forged IR verifies `IR_INDEX_LT_DOMAIN`. HAST proposition validation covers conditional and post-action recurrence contexts.

Artifact 0.7 adversarial coverage includes `IRIndexLTProposition` round-trip, stale artifact/IR versions, unknown proposition tag, extra/missing fields, semantic-node substitution, malformed source spans, and wrong-domain IR operands. C5.5 adversarial tests remain in full pytest.

## Registry and canonical bytes

`CURRENT_REGISTRY` points to `C5_6_REGISTRY`.

The registry snapshot contains 59 declarations and 172 productions. The nine canonical artifacts are committed under artifact/IR 0.7.

Run #402 regenerated the registry and artifacts independently on Ubuntu and Windows, reported the same canonical hashes on both platforms, and passed:

`git diff --exit-code -- spec/CURRENT_CONSTRUCTION_REGISTRY.json artifacts`

Registry SHA-256:

`ea1174516e0f3955b697fe15db3f2436ea0fcc0795e083899df8fe7c8e5ac1d8`

Canonical artifact SHA-256 values:

- `basic_update`: `94745237d81f30dbd2d6e6342db4f2e96b399efdcf64a39dfc595511b0f380b1`
- `immediate_result`: `211474de52d03bd3d1c291affba657ec9b875317bfe179ffcd9ef5a68b29cc58`
- `natural_subtraction`: `dbd33c08ca4f2176d717b3b0bb25d166c6e2dd362a9a00d5903b0cb85ecb049b`
- `normal_completion`: `d7dc26c066b60e5f29abc30e33824b79cdff2ea662e43688c671cd832acf1fdf`
- `output_not_return`: `83890ce7901e4209dc67cf505b9e0b688b62a651c3a7e532f60589d43defe257`
- `post_action_countdown`: `d3d393db40819d6ed8c494f2249622bbed3e45f9d408f7ac9d780b15e26f76ec`
- `recursive_countdown`: `a3650ea2f609d8f6cc3a054b9432a97a3d88d5e94e40efcf331290b19525e78c`
- `role_association`: `ec0891fe6a97acff06298ee8c680eecf288108693358a3c7150b8c5d9e28a892`
- `tiny_rm`: `26cedf10858fcf01e2769475e716b394732b9fad25a32685506fb7a0f8249ad9`

## Scope evidence

Comparison against the exact baseline shows no changes under:

- `spec/proposals/a17/**`;
- `spec/proposals/b16/**`;
- `megillah/original/**`;
- `megillah/candidates/**`;
- `megillah/analysis/**`.

No second Index domain, profile runtime tag, equality surface, distance primitive, signed arithmetic, generic Index Collection kind, or Day/Date/Time/Timestamp type was added.

## Frozen Megillah evidence

Candidate SHA-256:

`afc6eda11a8d7f4b6499cf643d2ef5b36581bcad61b5fce761a7709274d2d643`

Compiler frontier remains:

- normalized token 105;
- candidate line 11;
- original line 35 by inherited D4 provenance;
- `PARSE0002`.

No Megillah file was changed.

## GitHub Actions evidence

Exact implementation HEAD:

`0dd3e270bf769a9028df3fbf7d64cafd6a09f677`

Run:

- workflow run #402
- run ID `35590226318`
- event: push
- result: **17/17 jobs SUCCESS**

Dedicated C5.6 jobs:

### Windows

- targeted C5.6: **65 passed**
- full pytest: **543 passed, 126 subtests passed**
- B16 semantic regressions: **28/28 PASS**; the two B16 frozen identity receipts are intentionally excluded because they pin the pre-C5.6 C5.5 compiler/registry identity
- B16 required regression gates: **4/4 PASS**
- D3/D4 tests inside C5.6 job: **29 passed**
- registry/artifact regeneration: **PASS / clean diff**

### Ubuntu

- targeted C5.6: **65 passed**
- full pytest: **543 passed, 126 subtests passed**
- B16 semantic regressions: **28/28 PASS**; the two B16 frozen identity receipts are intentionally excluded because they pin the pre-C5.6 C5.5 compiler/registry identity
- B16 required regression gates: **4/4 PASS**
- D3/D4 tests inside C5.6 job: **29 passed**
- registry/artifact regeneration: **PASS / clean diff**

The workflow also reports success for core, tooling portability on Ubuntu/Windows, C5.1–C5.5 on Ubuntu/Windows, and D4 Megillah conformance on Ubuntu/Windows.

A documentation-only handoff commit follows this validated implementation HEAD and must receive its own exact-HEAD CI before Master handoff.
