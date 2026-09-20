# A15 — Symbol Surface

Status: **INTEGRATED_SURFACE_READY** for D-LANGUAGE-REQUEST-001.

## 1. Semantic target

This surface maps only to B13 `Symbol(DomainId, MemberId)`. A Symbol is atomic. It is not a source identifier and it is not Text. A15 adds no string literal, string concatenation, substring, text comparison, or dynamic symbol minting.

## 2. Exact declarations

A finite Symbol domain is introduced by:

    תהי משפחת שמות ושמה DOMAIN

`DOMAIN` is one ordinary Marak source name and therefore one normalized Hebrew orthographic word.

A member is introduced, and its canonical visible label is declared, by one preparatory unit:

    יהי במשפחת השמות אשר שמה DOMAIN שם ושמו MEMBER
    ולשם אשר במשפחת השמות אשר שמה DOMAIN שמו MEMBER
    מספר המלים אשר בשמו הנראה יהיה LABEL_WORD_COUNT
    והמלים הן LABEL_WORDS

The line breaks above are documentary only. The construction is the normalized word sequence.

`MEMBER` is the source identity of the member. It is one Marak source name. `LABEL_WORD_COUNT` is a positive admitted direct Natural literal. Immediately after `והמלים הן`, exactly that many normalized Hebrew orthographic words belong to the visible label. The next word, if any, is outside the label and must begin or continue another admitted construction.

Example:

    יהי במשפחת השמות אשר שמה חדשים שם ושמו חלקים
    ולשם אשר במשפחת השמות אשר שמה חדשים שמו חלקים
    מספר המלים אשר בשמו הנראה יהיה שלשה
    והמלים הן שלושה חלקים מחמישה

The runtime Symbol is still `Symbol(חדשים, חלקים)`. Its observable canonical label metadata is the three-word sequence `שלושה חלקים מחמישה`.

## 3. Runtime reference

The only A15 member reference is typed and domain-qualified:

    השם אשר במשפחת השמות אשר שמה DOMAIN שמו MEMBER

A bare `MEMBER`, `שם MEMBER`, or the visible label itself is not a Symbol reference.

The source spelling of `MEMBER` may equal one label word. That equality of spelling has no semantic conversion effect.

## 4. Multiword label boundary

A15 deliberately does not use quotation marks, maqaf, Markdown, newline, capitalization, or punctuation to delimit a label. The label boundary is determined by the declared word count after Charter normalization.

Thus the documentary spelling `משחת־שיניים` cannot use U+05BE MAQAF as a semantic separator. If the canonical visible label contains two words, A15 source writes the two words with normative whitespace and declares count two.

This is not a text-literal exception. The words are declaration metadata for one finite atomic Symbol member. No Text Value is created and no operation can inspect the words as a runtime sequence.

## 5. Same visible label

Two different domains may declare members with the same visible label. Their values remain distinct because identity is `(DomainId, MemberId)`:

    Symbol(חדשים, דלת) != Symbol(קציצות, דלת)

References remain unambiguous because the full source reference names the owning domain and member. Label text is never used for source resolution.

A15 also does not redefine B13 identity if two members happen to have equal label metadata: equality remains domain/member identity, not label equality.

## 6. Optional explicit Symbol order

Symbols have no order from spelling, visible label, or declaration order. When a Symbol domain must be used as an ordering relation, A15 admits explicit adjacent-order facts:

    במשפט משפחת השמות אשר שמה DOMAIN
    יהיה SYMBOL_A מיד לפני SYMBOL_B

`SYMBOL_A` and `SYMBOL_B` are complete domain-qualified Symbol references. If this ordering profile is used, the declared adjacency facts must form exactly one chain containing every member of the domain once. Its transitive closure is the admitted strict total relation for B13 ordering. A partial chain, cycle, fork, or member omission is invalid source; the compiler does not repair it by declaration order.

This is declarative order metadata, not an executable comparator callback.

## 7. Evidence and controlled deviation

Megillah evidence includes the 17 cutlet names, 47 month names, and explicit statements that multiword forms such as `שלושה חלקים מחמישה` and `הדלת הסגורה` are one name. Jeremiah 23:6 supplies the Biblical naming frame `וזה שמו אשר יקראו ...`; Job 8:10 supplies Biblical `מלים` as a word-level noun. A15's counted-label field is a controlled deviation: Biblical prose does not need a machine-recoverable boundary, while Marak must recover one after punctuation erasure.

The explicit domain noun `משפחת שמות` is controlled Marak terminology chosen to expose the B13 finite-domain relation without importing enums, strings, intern tables, or tags.

## 8. Errors / rejection

Reject at surface or validation time:

- source identity used directly as a Symbol Value;
- visible label used as a reference to a member;
- omitted or zero label-word count;
- too few label words;
- extra words being silently swallowed into a label;
- punctuation or layout being treated as a label boundary;
- dynamic creation of an undeclared member;
- inferred Symbol order from spelling, label, or declaration order.

No production compiler change is made by A15.
