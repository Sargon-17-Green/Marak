# A18 — Multi-word Declared Source Names

Status: **A18 SURFACE PROPOSAL READY FOR MASTER REVIEW**

Baseline: `5a5f8dae0dd8c3526de5f21f84a3a7b2aba984e3`  
Branch: `workstream-a/a18-multi-word-declared-source-names`

## Scope

A18 addresses only `D4-LANG-002 — MULTI_WORD_DECLARED_NAMES_NOT_REPRESENTABLE`.

It proposes a general language-level surface for multi-word static source names across:
- acts;
- places;
- act-owned roles;
- Program Input roles;
- Symbol domains;
- Symbol member source identities;
- every corresponding reference site.

A18 changes no compiler/parser/resolver/runtime production code, no current construction registry, no
Megillah source, and does not open B17 or C5.7.

## Selected direction

Existing one-word names remain unchanged.

A multi-word source name uses an explicit counted frame at **every** declaration and reference:

    שם אשר מספר המלים אשר בו הוא COUNT והמלים הן WORD_1 ... WORD_N

with `COUNT = N >= 2`.

The static identity is the canonical normalized payload word sequence only. The frame and count are
boundary syntax, not identity.

Examples:

    יהי מקום ושמו
    שם אשר מספר המלים אשר בו הוא שלשה והמלים הן מספר טיפה גלויה

    המקום אשר שמו
    שם אשר מספר המלים אשר בו הוא שלשה והמלים הן מספר טיפה גלויה

No alias exists between `מספר טיפה גלויה` and `מספרטיפהגלויה`.

## Documents

- `A18_MULTIWORD_SOURCE_NAMES.md` — complete proposal and Master-facing normative delta;
- `A18_NAME_SITE_INVENTORY.md` — all current NameTerminal sites and identity-family mapping;
- `A18_SURFACE_OPTIONS.md` — alternatives and rejection analysis;
- `A18_PERIOD_LANGUAGE_AUDIT.md` — Biblical/controlled-language and normalization audit;
- `A18_BACKWARD_COMPATIBILITY.md` — compatibility/collision consequences;
- `A18_EVIDENCE_MAP.md` — repository and primary-text evidence map;
- `A18_HANDOFF_TO_MASTER.md` — final A18 handoff.

## Non-goals

A18 does not add:
- Text/String values;
- runtime name lookup;
- string-based symbol lookup;
- dynamic symbols;
- aliases;
- quoting/escaping syntax;
- punctuation/layout boundaries;
- a generic END delimiter;
- Megillah-specific grammar.

## Routing

`D4-LANG-002 → A18 → B17 → C5.7 → D4/T17`

Only Master may accept A18 and advance that route.
