# A18 — Surface options

## Decision criteria

A18 compared candidates against the same requirements for every static source-name family:
parse determinism, readability, backward compatibility, normalization stability, collision behavior,
declaration/reference symmetry, construction-word interaction, period-language plausibility, future
implementation complexity, and diagnostics.

| Candidate | Determinism | Construction words inside name | Decl/ref symmetry | Backcompat | Period fit | Future implementation | Diagnostics | Disposition |
|---|---|---|---|---|---|---|---|---|
| explicit word count at every occurrence | strong: endpoint known before payload | unrestricted | exact | additive | controlled but justified | bounded local terminal/nonterminal | local and precise | SELECTED |
| terminator / closing phrase | weak under open-class payload unless terminator words banned | collision-prone | possible | additive only with new restrictions | some Biblical resumptive evidence | scan + collision policy | endpoint errors are contextual | REJECT |
| structural frame with no count | incomplete: still needs endpoint rule | collision-prone | possible | additive | potentially literary | outer-grammar dependent | poor | REJECT |
| match previously declared names | declaration-set dependent | unrestricted only with overlap policy | asymmetric parse/resolve coupling | semantically static but parse-sensitive | surface itself says no boundary | two-phase/semantic tokenization | poor | REJECT |
| quotes/punctuation/layout/maqaf/escaping | Charter-invalid or imported convention | n/a | n/a | incompatible with Charter | poor | easy but irrelevant | misleading | REJECT |

## Selected count frame

    שם אשר מספר המלים אשר בו הוא COUNT והמלים הן WORD_1 ... WORD_N

The frame is not selected because it is easy to implement. Its decisive property is that the source
itself states the payload extent before any payload word is consumed.

That remains true when the payload is:

    מעשה מקום אשר שמו

No word needs global reservation.

## Interaction with the existing Symbol visible-label count

A15 already uses an explicit count to delimit multi-word **visible-label metadata**:

    מספר המלים אשר בשמו הנראה יהיה COUNT
    והמלים הן LABEL_WORDS

A18 considered that precedent but does not infer that source identity must therefore use the same
mechanism. The two cases differ:

- a Symbol label is metadata attached to an already statically identified member;
- a SourceName is itself part of the static declaration/reference relation;
- a label never participates in lookup;
- a SourceName necessarily participates in compile-time resolution.

After independent comparison, A18 selects the same **boundary principle**—overt count before a fixed
number of words—because it uniquely meets the open-class collision requirement. It does **not** reuse
label identity or make labels aliases.

The A18 source-name frame is separately grammatical and separately normalized. C5.7 must not
implement it by pretending a source name is a Symbol label.

## Prefix/overlap stress cases

Declarations of both:

    א ב
    א ב ג

are not an ambiguity when written through counted SourceName occurrences, because count 2 and count 3
are explicit at every reference.

By contrast, the declaration-known candidate would see the raw reference:

    א ב ג ...

and would have to decide between the two declarations by longest-match, continuation success,
expected kind, or another forbidden heuristic.

## Construction-word stress cases

The selected candidate permits payloads such as:

    מעשה מקום אשר שמו
    שם אשר שמו מקום
    ועתה מעשה
    עד הנה

because the count determines where the payload ends. These words retain their ordinary grammatical
force only after the counted payload is complete.

The terminator candidate cannot provide the same freedom without either:
1. banning its terminator phrase from names; or
2. adding an escape mechanism; or
3. choosing one of several terminator occurrences.

All three are contrary to A18 requirements.

## Why a universal terminator is weaker

A fixed closing phrase looks attractive because Biblical discourse has resumptive naming clauses.
But Marak's open name class makes the closing words legal payload words too. A fixed terminator
therefore either becomes a reserved sequence or requires positional choice.

The problem is structural, not merely stylistic. Even a historically attested phrase such as
`הוא שמו` cannot by itself identify which occurrence is the boundary when the same words can be
inside the declared name.

## Why “next construction marker” is not a boundary

Construction markers are not globally reserved tokens. A17 explicitly preserved names such as
`מעלה` inside name slots even though the same spelling has construction-local grammatical force.

Therefore “stop when the next construction word appears” would silently reverse the lexical-freedom
policy and make names depend on an evolving set of grammar words.

## Why declaration-known matching is not accepted

The current resolver is static, but static resolution must not be confused with syntax segmentation.
Making tokenization depend on previously declared identities would mean that adding a declaration can
change the parse of later source without changing those later words.

A18 rejects that coupling even though it would not be runtime lookup.

## Count errors

The explicit count is authoritative syntax, not a hint.

- too few payload words: parse failure;
- extra words: they belong to outer syntax and must parse there;
- a different count in a reference: a different payload extent and therefore no automatic
  co-reference;
- two complete computational parses: ambiguity rejection.

No count is repaired from the declaration, surrounding type, or intended algorithm.
