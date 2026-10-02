# B17 — C5.7 Implementation Requirements

These are semantic requirements, not a parser implementation prescription.

## SourceName boundary

Implement the accepted A18 two-form SourceName:
- legacy one-word branch unchanged;
- counted branch with count N >= 2 and exactly N normalized orthographic payload words.

No fixed semantic upper bound on N is introduced by B17. D evidence already reaches 10 words.

All existing name roles covered by A18 must use the same SourceName abstraction consistently.

## Canonical handoff

After parsing, every source-name slot must expose one canonical spelling:
`" ".join(payload_words)` using exactly U+0020 between normalized words.

Frame/count must not be stored as semantic identity.

## Resolver

Generalize current string keys from one-word spellings to canonical one-or-more-word spellings without changing namespaces or owners.

Preserve:
- declaration-before-use;
- duplicate rules;
- act/body/role owner rules;
- Program Input owner contract;
- Symbol member domain ownership;
- repeated-name co-reference;
- explicit cross-kind distinction.

Do not add:
- longest match;
- expected-type rescue;
- declaration-known tokenization;
- nearest-name resolution;
- welded/spaced aliases;
- visible-label aliases.

## Program Input

Continue binding only by resolved ProgramInputId.

Canonical multi-word spelling participates in the existing source-independent IR program-contract fingerprint exactly where spelling already participates.

The host API must not accept a raw source string as identity.

## HAST / IR / artifact

Reuse current spelling fields.

No new SourceName runtime value, HAST identity node, IR identity opcode, artifact tag, schema field or multiword flag is required.

Required version effects:
- construction registry: BUMP;
- compiler/package: BUMP;
- HAST: NO BUMP;
- IR: NO BUMP;
- artifact: NO BUMP;
- language edition: no semantic bump required by B17.

## Diagnostics and negative cases

Add targeted diagnostics/tests for:
- count < 2 in counted form;
- payload shorter than promised count;
- extra payload word that cannot belong to outer syntax;
- declaration/reference payload mismatch;
- prefix-related names;
- construction words inside names;
- multi-word name at every A18 role;
- illegal forward reference remains illegal;
- duplicate same canonical name in each existing duplicate scope.

## Required regression gates

At minimum:
- B13 reference suite;
- B15 reference suite;
- B16 semantic suite and required gates;
- A17 proposal suite;
- A18 proposal/reference checks if present at implementation time;
- Program Input production regressions;
- Symbol production regressions;
- full pytest;
- D3/D4 frozen regressions.

C5.7 must not edit Megillah while integrating the language feature.
