# B17 — Multi-word Declared Source Names Semantic Integration

Status: B17 semantic/reference workstream.

Canonical baseline:
`9abd731ba7c80fd714900219e1af4c8d9c41797b`

Accepted A18 reviewed HEAD:
`37e7591dcc42eeeb757a4b79b0dc752162e77079`

Finding:
`D4-LANG-002 — MULTI_WORD_DECLARED_NAMES_NOT_REPRESENTABLE`

B17 does not redesign the accepted A18 surface. It defines how the accepted counted SourceName participates in existing Marak static identity, ownership, visibility, Program Input, Symbol, HAST, IR and artifact contracts.

Production compiler/parser/runtime/registry and Megillah files are out of scope. C5.7 is not opened here.

## Semantic conclusion

The existing semantic model generalizes without a new identity kind:

`one normalized source word`
becomes
`one-or-more normalized source words`.

The abstract source-name identity component is the canonical normalized payload word sequence.

The current concrete metadata representation remains one string:
the payload words joined by exactly one U+0020 SPACE.

That serialization is injective because an orthographic name word contains no whitespace after the existing A13 normalization boundary. The A18 count and frame are syntax only and do not survive into semantic identity.

## No runtime-name ontology

B17 introduces no Text/String domain, no runtime Name value, no dynamic lookup and no runtime "multiword" flag.

All lookup remains static and typed.

## D evidence absorbed

D's read-only reconnaissance adds important stress evidence:
- at least one 10-word natural designation occurs;
- construction words occur inside names;
- punctuation/layout cannot delimit names;
- no new language gap beyond D4-LANG-002 was established;
- one forward use ("אות החסר") exists, but B17 does not change introduction-before-use.

Those observations reinforce the accepted counted boundary; they do not create new semantic identity families.
