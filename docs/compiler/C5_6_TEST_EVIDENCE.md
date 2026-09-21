# C5.6 — General BidirectionalIndex Production Integration — Test Evidence

Status: implementation candidate; final GitHub Actions verification is pending runner allocation.

## Baseline

- repository: `Sargon-17-Green/Marak`
- baseline: `f7c1be2e913d73c4722f92d8c27c8c7e6dd26a91`
- branch: `workstream-c/c5-6-general-bidirectional-index-surface`
- Draft PR: #19
- A17 reviewed dependency: `50155cbf86c1cdc1111dde45464e7a9a1605f9df`
- B16 reviewed dependency: `8c164c50084a0d029cda9c9ee397b0c96d2c63c2`

## Current contract matrix

- package: `0.5.6a1`
- compiler: `0.5.6-alpha.1`
- language edition: `core-0.1-integration-candidate-a13-b12`
- registry: `c5.6-a17-b16.1`
- HAST: `core-hast-0.7-candidate-1`
- IR: `core-ir-0.7-candidate-1`
- artifact: `core-artifact-0.7-candidate-1`
- IR reference: `core-ir-reference-0.7-candidate-1`
- portable backend: `portable-ir-vm-0.7-candidate-1`

## Source-first coverage implemented

The C5.6 source suite contains production-source programs for:

- general origin, before and after literals;
- productive A15 feminine-count magnitude at 99,999,999;
- Program Input declaration/read in both cross-profile directions;
- place state in both cross-profile directions;
- roles in both cross-profile directions;
- all four output/immediate-result profile combinations;
- general successor/predecessor and zero crossing;
- strict Index order grid, equality-false cases, far magnitudes, and origin crossings;
- strict order in both conditional and post-action recurrence contexts;
- actual same-position classification using two strict-order tests and one named decision act;
- constructive distance composition with retained Natural counter and named acts;
- existing year-oriented Collection<BidirectionalIndex> append accepting a general-profile Index Value;
- explicit `לפני` ambiguity case.

Each important positive helper compares:

`HAST reference == IR reference == portable backend`.

## Negative and rescue coverage implemented

The negative suite rejects malformed general heads, mixed-profile literals, invented order/equality/distance surfaces, generic Index collection heads, and expected-type rescue attempts in typed state, replacement, role association, output, Program Input reference, and proposition operand contexts.

A17 words remain legal in explicit NameTerminal slots; no global reserved-word list is introduced.

## Canonical HAST/IR adversarial coverage implemented

Direct forged HAST verifies `DOMAIN_INDEX_LT`.

Direct forged IR verifies `IR_INDEX_LT_DOMAIN`.

HAST proposition validation covers conditional and post-action recurrence contexts.

## Artifact adversarial coverage implemented

The 0.7 artifact suite covers:

- explicit `IRIndexLTProposition` round trip;
- stale artifact 0.6;
- stale IR 0.6;
- unknown proposition tag;
- extra field;
- missing field;
- semantic-node substitution;
- malformed source span;
- direct wrong-domain IR operand.

All C5.5 adversarial tests remain part of full pytest.

## Registry and canonical bytes

`CURRENT_REGISTRY` points to `C5_6_REGISTRY`.

The registry snapshot contains 59 declarations and 172 productions after adding the C5.6 family.

The nine canonical artifacts are committed under artifact/IR 0.7. CI regenerates both registry and artifacts and requires a clean diff.

## Scope evidence

Repository comparison against the exact baseline shows no changes under:

- `spec/proposals/a17/**`;
- `spec/proposals/b16/**`;
- `megillah/original/**`;
- `megillah/candidates/**`;
- `megillah/analysis/**`.

No second Index domain, profile runtime tag, equality surface, distance primitive, signed arithmetic, generic Index Collection kind, or Day/Date/Time/Timestamp type was added.

## Frozen Megillah evidence

The C5.6 scope suite pins candidate SHA-256:

`afc6eda11a8d7f4b6499cf643d2ef5b36581bcad61b5fce761a7709274d2d643`.

It also re-measures the compiler frontier and requires:

- normalized token 105;
- candidate line 11;
- `PARSE0002`.

The inherited D4 provenance maps that frontier to original line 35.

## CI status

Dedicated C5.6 Ubuntu/Windows jobs are present and run:

- targeted C5.6 tests;
- full pytest;
- A13/B12/B13/A15/A16/A17/B15/B16 proposal regressions;
- D3/D4 Megillah tests;
- current registry and artifact regeneration;
- canonical-byte diff check and hash reporting.

At the time this evidence file was created, current-head pull-request run #383 / ID `35585002102` remained `queued`; therefore this document makes no final PASS claim yet.
