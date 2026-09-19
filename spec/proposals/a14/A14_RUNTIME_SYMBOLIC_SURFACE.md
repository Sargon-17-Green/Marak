# A14 — Runtime Symbolic Surface

Status: **PREFERRED_SURFACE_CANDIDATE / AWAITING_B** — B13 semantics reviewed; A/B integration acceptance and final surface wording remain.

## Need

The Megillah must compute and expose calendar labels such as cutlet and month names. Some labels are
multiword. These are runtime results, not merely source identifiers.

A13 source names (`PlaceId`, `ActId`, `RoleId`) are not Values and may not be implicitly converted to
runtime text.

## Alternatives

### Numeric code only
Rejected as the sole language answer. It can implement the algorithm but changes the stated external
result unless an external normative name table is treated as part of the system.

### Source identifier spelling becomes data
Rejected. This would silently convert compile-time identity spelling to runtime data and collapse the
A13 name/value distinction.

### General arbitrary strings
Not justified yet. D2 needs a finite family of symbolic calendar labels, not arbitrary text editing,
concatenation, substring operations or Unicode text processing.

### Closed symbolic `שם` values
Preferred.

The semantic idea is an atomic symbolic datum whose human-visible designation is explicitly declared.
It is not a source name merely because it has a spelling.

## Surface requirements for the eventual construction

Any accepted declaration must expose all three roles:

1. a source-resolvable identity for the declaration;
2. the fact that the declared datum is a runtime `שם`;
3. the human-visible name content.

No role may be supplied by punctuation, quote marks or capitalization.

For example only as a schematic, NOT frozen syntax:

    [introduce runtime name datum NAME-ID]
    [state its visible name content NAME-PHRASE]

A reference must have a typed head meaning "the name datum ...", not a bare source word.

## Why exact literal syntax is not frozen

The historical month labels include:
- one-word names;
- multiword names (`שלושה חלקים מחמישה`, `הדלת הסגורה`);
- forms whose punctuation/niqqud is transparent under the Charter.

If B chooses an atomic Symbol whose payload is merely a declared symbolic identity, A can design a
word-level declaration without general text delimiters.

If B chooses a TextSequence Value whose spelling/content is observable as text, A must explicitly
define the lexical exception and its entry/exit boundaries. That is a materially larger language
decision.

## Required invariants

- No implicit source-name→symbol conversion.
- Symbol equality, if provided, must not be smuggled in as string comparison.
- A symbolic name cannot be used as a numeric Value.
- Multiword name content must have an intrinsic word-level boundary.
- Punctuation remains transparent unless a future text-literal model normatively changes the Charter.
- No quoted-string proposal is accepted merely because quote marks are conventional.

## B question

Is the required object:
1. an atomic closed-domain Symbol/NameValue with declared presentation;
2. an observable text sequence;
3. another semantic relation?

A freezes no literal grammar until B answers this distinction.


## B13 reconciliation

B13 head `3c47a57debd381c2b4e41d00d12c792ae43debe8` independently selects a finite declared atomic
`Symbol(DomainId,MemberId)` model, with canonical visible-label metadata and no implicit source-name
conversion. This matches A14's preferred semantic direction and rejects general Text as unnecessary.

The remaining A-side issue is purely surface: a controlled word-level declaration/reference for symbol
domain members, including multiword visible labels, whose boundary does not depend on punctuation or
layout. A14 therefore keeps the exact declaration syntax as PREFERRED rather than FROZEN.
