# A18 — Backward compatibility and collision audit

Baseline: `5a5f8dae0dd8c3526de5f21f84a3a7b2aba984e3`.

## Existing one-word source

No currently legal one-word SourceName changes.

For every current declaration/reference:
- the same normalized word remains legal;
- the same typed identity family applies;
- introduction-before-use is unchanged;
- owner qualification is unchanged;
- the same static referent is resolved;
- no new global keyword reservation is introduced.

The legacy source branch remains exactly one normalized orthographic word.

## No alternate one-word counted spelling

The new counted form requires count >= 2.

This is a canonical-source restriction. Without it, both:

    פלוני

and a counted one-word frame carrying `פלוני` would encode the same payload sequence. A18 avoids
creating that unnecessary surface alias.

## Canonical multi-word identity

For payload words `w1 ... wn`, identity spelling is the normalized sequence joined by one U+0020
SPACE.

Thus:
- multiple normative spaces collapse;
- tabs/newlines from the normative whitespace set collapse;
- punctuation cannot distinguish identities;
- niqqud/cantillation cannot distinguish identities;
- maqaf is not a separator and cannot create a multi-word identity.

## Welded forms are distinct

    מספר טיפה גלויה

and:

    מספרטיפהגלויה

are not aliases.

The first has three canonical words; the second has one. Existing D4 welded spellings therefore remain
their own one-word source identities until D4 is later authorized to repair them.

## Construction words remain legal in names

A18 does not reserve:
- `מעשה`;
- `מקום`;
- `אשר`;
- `שמו`;
- `שם`;
- `ועתה`;
- any other current/future WordTerminal merely because it has grammatical force elsewhere.

A counted name can contain those words because the explicit count establishes the payload endpoint.

## Cross-kind collisions

Existing A-NAME-005 behavior is preserved.

The same canonical word sequence may be used for an act and place when every admitted reference remains
linguistically distinguished:

    המעשה אשר שמו SOURCE_NAME
    המקום אשר שמו SOURCE_NAME

A18 does not impose one global identifier namespace.

## Owner-qualified collisions

Existing scopes remain:
- role spelling duplicate only within one owner act;
- Symbol member spelling duplicate only within one Symbol domain;
- Program Input identity remains program-owned;
- act/place/Symbol-domain duplicate rules remain as today.

## Prefix overlap

Two names:

    א ב
    א ב ג

are not ambiguous under the selected surface because every occurrence states the payload count.

A18 does not ban prefix-related names. It bans **ambiguous source**. If future grammar changes make a
complete source admit two computational readings despite the count frame, that source must be
rejected.

## Simple-name/frame collision

Because one-word names are open-class, `שם` itself remains a legal simple name. Therefore a token
stream beginning with the counted frame may initially license both a simple-name prefix and a counted
branch in an ambiguity-preserving parser.

The normative rule is full-parse based:
- if only the counted branch completes, accept it;
- if only the legacy branch completes, accept it;
- if both complete with computationally distinct readings, reject the source.

No precedence is assigned to the counted branch and no longest-match preference is introduced.

## Symbol labels

A multi-word Symbol source member name does not change its visible label.

Equal normalized words between source identity and visible label do not create an alias. A reference
must still use the domain-qualified Symbol source-name construction.

## Program Inputs

The source role spelling may become multi-word, but invocation remains identity-based. The host must
not bind by a raw space-containing string or by token sequence. B17 must reaffirm the existing
`ProgramInputId` contract.

## Compatibility conclusion

A18 is additive at the language-surface level and preserves every currently admitted one-word source
identity. Its only new parse possibilities are explicitly introduced counted SourceName constructions.
