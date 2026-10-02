# B17 — Backward Compatibility

## One-word programs

Every existing legal one-word name retains exactly the same canonical spelling string.

No existing one-word declaration/reference is rewritten.
No counted alias with count 1 is added.
No new reserved-name vocabulary is introduced.

## Existing ownership and scopes

Unchanged:
- duplicate act name: reject in the program;
- duplicate place name: reject in the program;
- duplicate role name: reject within one owner act;
- duplicate Program Input role spelling: reject within the owning program contract/discourse;
- duplicate Symbol domain: reject in the program;
- duplicate Symbol member source name: reject within one Symbol domain.

Cross-kind same spelling remains governed by explicit typed referring descriptions.

## Introduction-before-use

Unchanged. Multi-word support grants no hoisting and no implicit forward declaration.

## Welded compatibility

A legacy/source spelling such as `מספרטיפהגלויה` is one word.

The A18 payload `מספר טיפה גלויה` is three words.

They are distinct identities. No compatibility alias exists in either direction.

## Whitespace

B17 consumes the result of existing A13 normalization.

Within a counted payload, any source whitespace already normalized to U+0020 yields the same canonical name sequence and therefore the same semantic spelling.

Punctuation, maqaf, niqqud/cantillation and layout do not become semantic delimiters.

## Prefix names

Prefix-related names are legal because the A18 count determines the payload length at each occurrence.

No longest-match compatibility rule is introduced.

## Artifact compatibility

Existing one-word artifacts remain structurally valid under the same HAST/IR/artifact schemas.

A future C5.7 artifact carrying a multi-word spelling uses the same existing string field. No structural reinterpretation of old artifacts is required.
