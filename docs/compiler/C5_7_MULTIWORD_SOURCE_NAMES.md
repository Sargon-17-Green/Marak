# C5.7 — Multi-word Declared Source Names Production Integration

Baseline: `5679fbe861bc2d30aba479e32fd042bf196295ca`

Route: `D4-LANG-002 → A18 → B17 → C5.7`

C5.7 integrates the Master-accepted A18/B17 SourceName surface into production.
It does not reopen C5.1–C5.6, A18, or B17.

## Production shape

Historical `NameTerminal` remains unchanged for frozen registries.
C5.7 introduces `SourceNameTerminal(role, count_lexicon_id)` and derives
`C5_7_REGISTRY` from `C5_6_REGISTRY` by replacing every historical
name terminal in the current production set.

The migration is exhaustive:
- 115 source-name terminal occurrences;
- 61 name-bearing productions;
- 11 syntactic roles;
- six existing static identity families.

## Two accepted forms

Legacy form:
`NAME_WORD`

Counted form:
`שם אשר מספר המלים אשר בו הוא COUNT והמלים הן WORD_1 ... WORD_N`

Rules:
- COUNT is the existing admitted direct Natural spelling;
- COUNT must be at least 2;
- exactly N following normalized words form the payload;
- frame and count are boundary syntax only;
- the parser emits one source-name leaf whose text is the payload joined by U+0020;
- the emitted semantic text is the canonical payload only, while token/normalized/original provenance covers the complete counted SourceName construction from the opening `שם` through the final payload word;
- construction words remain legal payload words;
- the legacy and counted branches are both retained when structurally possible.

No longest-match, expected-type rescue, declaration-known tokenization,
nearest-name policy, welded/spaced alias, label alias, or runtime lookup was added.

## Static identity continuity

Resolvers continue to consume canonical spelling strings. Existing identity
types and owner scopes are unchanged:
- `ActId`;
- `PlaceId`;
- owner-qualified `RoleId`;
- program-contract-qualified `ProgramInputId`;
- `SymbolDomainId`;
- domain-qualified `SymbolMemberId`.

Program Input host binding remains by resolved `ProgramInputId`.
Symbol member source identity remains independent of visible-label metadata.
Declaration-before-use and duplicate rules remain unchanged.

## Version disposition

Changed:
- compiler/package: `0.5.7-alpha.1` / `0.5.7a1`;
- construction registry: `c5.7-a18-b17.1`.

Unchanged:
- HAST: `core-hast-0.7-candidate-1`;
- IR: `core-ir-0.7-candidate-1`;
- artifact: `core-artifact-0.7-candidate-1`;
- runtime backend/reference contracts.

Megillah files are not modified by C5.7.
