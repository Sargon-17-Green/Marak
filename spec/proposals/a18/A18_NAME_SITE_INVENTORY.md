# A18 — Name-site inventory

Baseline: `5a5f8dae0dd8c3526de5f21f84a3a7b2aba984e3`

## Registry receipt

`spec/CURRENT_CONSTRUCTION_REGISTRY.json` at the baseline contains:

- 172 total productions;
- 61 productions with at least one `kind: name` terminal;
- 115 total name-terminal occurrences;
- 11 syntactic name roles.

Occurrence counts:

| role | occurrences |
|---|---:|
| ActionName | 2 |
| PlaceName | 24 |
| RoleOwnerActionName | 23 |
| AssociatedRoleName | 8 |
| DeclaredRoleName | 10 |
| BodyActionName | 2 |
| ResultActionName | 6 |
| PerformedActionName | 1 |
| SymbolDomainName | 20 |
| SymbolMemberName | 3 |
| ProgramInputRoleName | 16 |

These are syntactic-use roles, not eleven semantic identity domains.

## Identity-family mapping

### Named act — YES

Syntactic roles:
- `ActionName`
- `RoleOwnerActionName`
- `BodyActionName`
- `ResultActionName`
- `PerformedActionName`

All resolve to `ActId` in the current resolver. Multi-word naming must apply uniformly. It would be
incorrect to allow a multi-word act declaration but not permit the exact same `SourceName` in body
open/close, role ownership, performance, or immediate-result references.

Productions:
- A10.ACT.IDENTITY
- A10.ACT.PERFORM
- A11.NUMBER.CURRENT.ROLE
- A11.ROLE.DECLARATION
- A12.BODY.DEFINITION
- A12.RESULT.IMMEDIATE.SINGLE
- C52.ACT.PERFORM.ROLES
- C52.INDEX.CURRENT.ROLE
- C52.ROLE.ASSOC.MORE
- C52.ROLE.ASSOC.ONE
- C52.ROLE.DECLARE.INDEX
- C52.ROLE.DECLARE.SYMBOL
- C52.SYMBOL.CURRENT.ROLE
- C52.SYMBOL.IMMEDIATE
- C53.CURRENT.ROLE
- C53.IMMEDIATE
- C53.ROLE.DECLARE
- C54.COUNT_AS.A11_NUMBER_CURRENT_ROLE
- C54.COUNT_AS.A12_RESULT_IMMEDIATE_SINGLE
- C56.INDEX.GENERAL.CURRENT.ROLE
- C56.INDEX.GENERAL.IMMEDIATE
- C56.ROLE.DECLARE.INDEX

The same act source identity is owner-qualified nowhere else; `ActId` itself is program-level static
identity.

### Named place — YES

Syntactic role: `PlaceName`.

All variants use `PlaceId`; the value domain carried by the place does not change source-name
identity.

Productions:
- A10.PLACE.CURRENT_NUMBER
- A10.PLACE.REPLACE
- A13.PREP.PLACE.INTRODUCE
- C52.INDEX.CURRENT.PLACE
- C52.PLACE.REPLACE.INDEX
- C52.PLACE.REPLACE.SYMBOL
- C52.PREP.PLACE.INDEX
- C52.PREP.PLACE.SYMBOL
- C52.SYMBOL.CURRENT.PLACE
- C53.CURRENT.PLACE
- C53.PLACE.REPLACE
- C53.PREP.PLACE
- C54.COUNT_AS.A10_PLACE_CURRENT_NUMBER
- C56.INDEX.GENERAL.CURRENT.PLACE
- C56.PLACE.REPLACE.INDEX

There are 24 `PlaceName` occurrences because several productions repeat the same name for explicit
co-reference.

### Act-owned role — YES

Syntactic roles:
- `DeclaredRoleName`
- `AssociatedRoleName`

Static identity is `RoleId(serial, owner ActId, spelling)`. Duplicate scope is per owner act.
Multi-word role names therefore apply to both declaration and every qualified reference, but the
owner remains part of role identity exactly as today.

Productions using declared role names:
- A11.ROLE.DECLARATION
- C52.ROLE.DECLARE.INDEX
- C52.ROLE.DECLARE.SYMBOL
- C53.ROLE.DECLARE
- C56.ROLE.DECLARE.INDEX

Productions using associated role names:
- A11.NUMBER.CURRENT.ROLE
- C52.INDEX.CURRENT.ROLE
- C52.ROLE.ASSOC.MORE
- C52.ROLE.ASSOC.ONE
- C52.SYMBOL.CURRENT.ROLE
- C53.CURRENT.ROLE
- C54.COUNT_AS.A11_NUMBER_CURRENT_ROLE
- C56.INDEX.GENERAL.CURRENT.ROLE

### Program Input role — YES

Syntactic role: `ProgramInputRoleName`.

Static identity is `ProgramInputId(serial, spelling, program_contract)`. Program Input host binding
is already by resolved identity, not positional order or raw spelling lookup. A18 changes only the
source spelling surface.

Productions:
- C55.INPUT.COUNT_AS.NATURAL
- C55.INPUT.DECLARE.COLLECTION
- C55.INPUT.DECLARE.INDEX
- C55.INPUT.DECLARE.NATURAL
- C55.INPUT.DECLARE.SYMBOL
- C55.INPUT.READ.COLLECTION
- C55.INPUT.READ.INDEX
- C55.INPUT.READ.NATURAL
- C55.INPUT.READ.SYMBOL
- C56.INPUT.DECLARE.INDEX
- C56.INPUT.READ.INDEX

### Symbol domain — YES

Syntactic role: `SymbolDomainName`.

Static identity is `SymbolDomainId(serial, spelling)`. The domain source name occurs not only in its
declaration, but in member declarations/references, Symbol typed heads, Collection kinds/order, places,
roles, outputs and Program Inputs. Multi-word support must therefore be global to this role.

Productions:
- C52.PLACE.REPLACE.SYMBOL
- C52.ROLE.DECLARE.SYMBOL
- C52.SYMBOL.CURRENT.PLACE
- C52.SYMBOL.CURRENT.ROLE
- C52.SYMBOL.DOMAIN
- C52.SYMBOL.IMMEDIATE
- C52.SYMBOL.MEMBER
- C52.SYMBOL.ORDER
- C52.SYMBOL.REF
- C53.APPEND.NESTED.SYMBOL
- C53.APPEND.SYMBOL
- C53.EMPTY.NESTED.SYMBOL
- C53.EMPTY.SYMBOL
- C53.KIND.NESTED.SYMBOL
- C53.KIND.SYMBOL
- C53.ORDER.LEX.SYMBOL
- C53.ORDER.SYMBOL
- C55.INPUT.DECLARE.SYMBOL
- C55.INPUT.READ.SYMBOL

### Symbol member source identity — YES

Syntactic role: `SymbolMemberName`.

Static identity is `SymbolMemberId(serial, spelling)` resolved under one `SymbolDomainId`.

Productions:
- C52.SYMBOL.MEMBER
- C52.SYMBOL.REF

The source member name is **not** its visible label.

## Naming-like mechanisms that are not SourceName

### Symbol visible label — NO

`CountedLabelTerminal` consumes a direct Natural, exact `והמלים הן`, and exactly that many words.
It produces canonical visible-label metadata. The runtime Symbol identity remains
`(SymbolDomainId, SymbolMemberId)`; label text is not a source reference.

A18 may independently reuse the *boundary principle* of an explicit word count, but must not merge
the two mechanisms or let labels become aliases.

### Current act occurrence — NO

`המעשה הזה` is deictic. It has occurrence semantics and no declaration-name identity.

### Typed domain heads — NO

`מספר`, `מעלה`, `ספר ...`, Symbol-family heads and similar constructions identify value/domain
shape. They are not user-declared names.

### Numerals and counted recurrence — NO

Multi-word numeral terminals have lexical value semantics, not source identity.

### Program contract / serial identity — NO

Compiler-generated serials and the Program Input owning contract are static semantic/artifact
machinery. They are not name syntax and remain outside A18.

## Resolver identity evidence

Current resolver maps exact spelling strings as follows:

- `places: dict[str, PlaceId]`;
- `acts: dict[str, ActId]`;
- `roles: dict[(owner.serial, str), RoleId]`;
- `symbol_domains: dict[str, SymbolDomainId]`;
- `symbol_members: dict[(domain.serial, str), ...]`;
- `program_inputs: dict[str, ProgramInputId]`.

This is evidence that all six families already use static declaration/reference identity. It is **not**
a normative requirement that C5.7 continue using Python strings as keys.

A18's normative key is the canonical normalized word sequence, with owner qualification where the
existing semantic identity already has an owner.
