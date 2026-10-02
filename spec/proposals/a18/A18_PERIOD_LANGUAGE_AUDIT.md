# A18 — Period-language and normalization audit

## Method

A18 follows the project evidence hierarchy used by A17:

1. primary Biblical Hebrew text for lexical/naming evidence;
2. existing accepted Marak constructions for controlled composition;
3. explicit labeling of controlled new composition where no direct full-phrase attestation is claimed;
4. no Modern-Hebrew punctuation, quote, escape, identifier or type convention used as normative
   evidence.

## Biblical naming evidence

### Genesis 2:19

The naming relation ends with:

    ... וכל אשר יקרא לו האדם נפש חיה הוא שמו

This directly supports `שם/שמו` as ordinary naming vocabulary and a predicative identity relation.
It does not supply a programming delimiter, and A18 does not claim that it does.

### Jeremiah 23:6

The verse contains:

    וזה שמו אשר יקראו יהוה צדקנו

The designation following the naming frame is multi-word in the normalized word stream. This is
important evidence that a proper designation in Biblical Hebrew need not be one orthographic word or
be surrounded by quotation syntax.

The Masoretic/editorial punctuation visible in editions is not used by A18 as a boundary; under the
Marak Charter it cannot carry grammar.

### Job 8:10

The verse contains `ומלבם יוצאו מלים`. A15 already used this as lexical evidence for `מלים`.
A18 reuses that accepted Biblical noun rather than inventing a modern term such as “tokens” or
“identifier parts”.

## Controlled A18 composition

Selected frame:

    שם אשר מספר המלים אשר בו הוא COUNT והמלים הן WORDS

A18 does **not** claim this full sentence occurs in the Hebrew Bible. It is controlled composition from:

- ordinary `שם` naming vocabulary;
- the already accepted Marak `מספר ... הוא ...` nominal identity/equality pattern;
- accepted `מלים` vocabulary;
- A15's already audited use of explicit word count when machine recovery of an otherwise natural
  word sequence requires a boundary.

The controlled deviation is explicit: Biblical prose can rely on discourse and human interpretation
for where a designation ends; Marak cannot, because punctuation and layout are semantically
transparent and computationally different plausible readings must be rejected.

## Why the count frame is linguistically preferable to modern identifier delimiters

A quotation mark, bracket pair, backtick, escape character, capitalization rule, underscore or
hyphen-as-separator would require knowledge of a modern writing/programming convention and would
either disappear under normalization or violate the Charter's lexical ontology.

The selected construction instead says in Hebrew what the compiler must know: this is a name, it
contains a stated number of words, and those words follow.

Its verbosity is a linguistic cost, but not a semantic disguise.

## Why `הוא שמו` is not adopted as a terminator

Genesis gives direct evidence for the phrase as a naming predicate, but not as a repeatable closing
delimiter after arbitrary names.

If A18 made it a terminator, the normalized payload could itself contain `הוא שמו`. The language
would then need to reserve that sequence, escape it, or choose one occurrence. None follows from the
Biblical evidence.

Thus the evidence supports naming vocabulary but does not solve the machine boundary problem.

## Number and agreement

The selected frame predicates the count of the name's words:

    מספר המלים ... הוא COUNT

The grammatical subject is `מספר`; this avoids inventing a new inflected “N words” family for A18.
It can reuse the current admitted exact direct Natural spelling.

The counted source-name form is restricted to count >= 2. Count 1 is not prohibited for linguistic
reasons; it is excluded for canonical-source reasons, because the legacy one-word SourceName already
provides the unique one-word form.

## Normalization audit

PASS at proposal level.

After Charter normalization:

- frame words remain ordinary Hebrew orthographic words;
- all normative whitespace runs collapse to single spaces;
- line breaks cannot alter the name;
- punctuation cannot close the name;
- maqaf cannot create a word boundary;
- niqqud/cantillation cannot distinguish names;
- the explicit count still determines the number of payload words.

Examples:

    מספר<TAB>טיפה<NBSP>גלויה

inside a count-3 payload canonicalizes to:

    מספר טיפה גלויה

while:

    מספר־טיפה־גלויה

with transparent maqaf canonicalizes to one word:

    מספרטיפהגלויה

and therefore is a different source name.

## Construction-word collision audit

PASS by explicit count.

The payload can contain any admitted orthographic word, including current grammar words:

    מעשה
    מקום
    אשר
    שמו
    שם
    ועתה
    עד
    הנה

No reserved-word list is introduced.

## Modernisms rejected

A18 rejects:
- `"multi word name"`;
- brackets/backticks;
- underscores;
- escapes;
- capitalization;
- Unicode quoting distinctions;
- treating maqaf as an identifier separator;
- “identifier”, “token”, “string” ontology in the source language;
- a generic END marker translated into Hebrew solely to imitate a programming delimiter.

## Conclusion

The selected mechanism is not directly attested as one Biblical sentence; it is a controlled Marak
composition. Its lexical pieces and naming relation are period-compatible, and its explicitness
addresses a machine-boundary problem created by Marak's own normalization rules rather than importing
modern identifier syntax.
