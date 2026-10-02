# B17 — A18 Semantic Integration Review

## 1. Decision

A18 is semantically admissible as a minimal generalization of existing static source identity.

For every source-name occurrence, let the canonical post-normalization payload be:

`N = (w1, ..., wn)`, with `n >= 1`.

For the legacy simple form, `n = 1`.
For the accepted counted form, `n >= 2` and the source count must equal `n`.

The semantic name component is exactly `N`.

The current implementation-facing spelling metadata is:

`Spell(N) = w1 + U+0020 + ... + U+0020 + wn`.

The A18 frame and count are not members of `N` and are not semantic identity material.

## 2. Abstract static identity

B17 distinguishes source identity from allocation identity.

Source resolution keys remain typed and owner-qualified:

- act: (ACT, N)
- place: (PLACE, N)
- role: (ROLE, owner ActId, N)
- Program Input: (PROGRAM_INPUT, owning program contract, N)
- Symbol domain: (SYMBOL_DOMAIN, N)
- Symbol member: (SYMBOL_MEMBER, owner SymbolDomainId, N)

Existing allocated IDs may continue to carry positive serials. Serials remain implementation identities used after successful source resolution; they do not create a new source naming rule.

## 3. Equality and co-reference

Two name occurrences co-refer exactly when:
1. they occur in the same existing typed identity family;
2. their existing owner/scope requirements are equal where applicable; and
3. their canonical payload word sequences are equal.

There is no fuzzy equality, spelling correction, stem equality, prefix equality, welded/spaced alias or visible-label alias.

Repeated equal names in one reference chain resolve to the same already declared identity.

## 4. Count and frame

Count semantic: NO.
Frame semantic: NO.

A counted occurrence with count 3 and payload `א ב ג` denotes the same name component wherever it legally occurs, independent of source whitespace variants already collapsed by A13.

Count mismatch is a source/parse validity failure. The resolver must never repair it.

Count 1 in the counted branch remains invalid because A18 deliberately reserves one-word names to the legacy form.

## 5. Prefix names and construction words

Names `א ב` and `א ב ג` may coexist.

The explicit count makes their local payload endpoints distinct. B17 adds:
- no longest-match rule;
- no declaration-known matching;
- no expected-type rescue;
- no nearest declaration preference.

Construction words remain legal payload words. D provides concrete evidence containing words such as `מספר`, `אשר`, `כל`, `ספר` and `שנת`, including a 10-word designation. Therefore no keyword-based end rule is semantically admissible.

## 6. Visibility and forward references

A18 changes name width, not visibility.

Existing introduction-before-use remains normative:
- places become visible after complete introduction;
- acts after introduction;
- roles only after owner introduction and role declaration;
- Program Inputs after declaration;
- Symbol domains/members after their respective declarations.

D's `אות החסר` evidence contains a use before explicit naming. B17 does not legalize that source pattern. Later D repair must express it using already admitted visibility rules or route a distinct finding with independent evidence.

## 7. Cross-kind and owner-qualified collisions

The same canonical name sequence may remain legal across explicitly distinguished kinds, exactly as before.

Roles with the same name under different owner acts remain distinct.
Symbol members with the same name under different Symbol domains remain distinct.
Program Input identity remains owned by the reusable program contract.

No global identifier namespace is introduced.

## 8. Program Input

Program Input binding remains by resolved `ProgramInputId`, never by raw source text.

The canonical multi-word spelling is metadata inside the existing ID.
The owning program-contract fingerprint continues to include that canonical spelling through existing IR semantic material.

Consequences:
- A13-whitespace variants that normalize to the same payload sequence produce the same spelling material;
- welded and spaced names produce different spelling material and therefore different identities/contracts where that identity participates;
- count/frame syntax is absent from the contract fingerprint because it is absent from IR semantics.

No runtime string lookup is added.

## 9. Symbol source identity versus visible label

These remain separate.

A Symbol member source identity is still `SymbolMemberId(serial, spelling)` under one Symbol domain.
Its visible label remains independent declaration metadata.

A multi-word source name does not change, infer, or alias the visible label.
A multi-word visible label does not become a source name.

## 10. Runtime observability

Runtime name object: NONE.
Dynamic lookup: NONE.
Runtime multiword flag: ABSENT.

Existing spelling metadata may continue to appear where current language/debug observables already expose source spelling. B17 adds no new observable bit that distinguishes one-word from multi-word identity.

## 11. Anti-imitation result

PASS.

The model does not import:
- quoted identifiers;
- strings as names;
- symbol-table lookup at runtime;
- conventional lexical shadowing;
- longest-token identifier matching;
- parser precedence based on expected type.

It is the existing explicit Hebrew referring-description model with a wider static name payload.
