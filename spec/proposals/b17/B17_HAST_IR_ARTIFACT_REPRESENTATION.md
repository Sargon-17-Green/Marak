# B17 — HAST / IR / Artifact Representation

## HAST

No HAST shape change is semantically required.

Existing IDs already carry `spelling: str`:
- ActId
- PlaceId
- RoleId
- ProgramInputId
- SymbolDomainId
- SymbolMemberId

For a counted A18 name, C5.7 must store only the canonical single-space payload spelling in that field.

The count and fixed frame do not enter HAST semantic identity.

HAST version bump required: NO.

## IR

No IR shape change is semantically required.

Existing `IRSymbol.spelling` and the existing domain/input ID dataclasses can carry U+0020 inside the spelling string. IR references continue to use allocated integer serials where they already do so.

IR version bump required: NO.

## Artifact

The existing tagged canonical JSON encoder already represents spelling as a JSON string and does not impose a one-word structural schema.

A space inside a spelling value is therefore data inside an existing field, not a new field/tag/type.

Artifact schema bump required: NO.
Artifact version bump required: NO.

C5.7 must add targeted round-trip/adversarial tests proving:
- multi-word spellings serialize and decode losslessly;
- spaced and welded spellings remain distinct;
- ProgramInputId ownership remains exact;
- Symbol source spelling remains independent of external_label;
- no new optional field or multiword flag is accepted.

## Parser-to-semantic boundary

C5.7 may choose parser architecture, but the semantic handoff must expose one resolved SourceName value per name slot with:
- canonical payload spelling;
- source mapping sufficient for diagnostics.

Name-specific diagnostics should identify the payload occurrence. Count/frame provenance may remain parse/source provenance, but must not be copied into semantic identity.

## Versions owned by C5.7

B17 requires a construction-registry version bump when the accepted SourceName production is integrated: YES.

B17 requires a compiler/package version bump for C5.7 production integration: YES.

B17 finds no semantic need to change the current language-edition identifier merely because the post-M2 construction registry grows; existing C5.2–C5.6 precedent already separates those concerns.

Exact version strings remain C5.7 implementation metadata.
