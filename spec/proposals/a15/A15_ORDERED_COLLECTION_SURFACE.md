# A15 — Finite Ordered Collection Surface

Status: **INTEGRATED_SURFACE_READY** for D-LANGUAGE-REQUEST-003.

## 1. Semantic target

Every A15 `ספר` Value in this profile maps to B13 `Collection<D> = <v1,...,vn>`: finite, ordered, immutable, homogeneous, structurally equal by contents, with no observable storage identity. A15 does not add an array, mutable list object, capacity, pointer, iterator object, or zero-based indexing convention.

Duplicates are legal collection contents. A source algorithm may separately impose uniqueness.

## 2. Typed book kinds

A15 uses ordinary Hebrew noun heads rather than generic type notation. The current admitted kinds are:

    ספר מספרים
    ספר מספרי שנים
    ספר שמות ממשפחת השמות אשר שמה DOMAIN
    ספר ספרי מספרים
    ספר ספרי מספרי שנים
    ספר ספרי שמות ממשפחת השמות אשר שמה DOMAIN

The last three expose the one nested level needed by the Megillah's books-of-books operations. Deeper semantic nesting remains possible in B13 but gains no source profile in A15 without independent need.

The head determines the one element domain. A book is not heterogeneous merely because the language has several Value domains.

## 3. Empty construction

Every admitted typed book kind has an empty form:

    BOOK_KIND אשר אין בו ELEMENT_HEAD

where `ELEMENT_HEAD` is fixed by that book kind. Representative exact forms are:

    ספר מספרים אשר אין בו מספר
    ספר מספרי שנים אשר אין בו מספר שנה
    ספר שמות ממשפחת השמות אשר שמה DOMAIN אשר אין בו שם
    ספר ספרי מספרים אשר אין בו ספר
    ספר ספרי מספרי שנים אשר אין בו ספר
    ספר ספרי שמות ממשפחת השמות אשר שמה DOMAIN אשר אין בו ספר

This wording was ambiguity-audited. In isolation `ספר שאין בו דבר` could leave the permitted member kind unclear. Here the book-kind head first fixes the only legal member domain, and the following clause denies a member of exactly that domain. Therefore the Value is empty, not a heterogeneous book whose other contents are unknown.

No null/absence Value is created by `אין בו`.

## 4. Pure append / extension

Canonical constructive append is a Value description:

    BOOK_KIND אשר בו כל אשר ב BOOK_VALUE כסדרו ואחר כלם ITEM_VALUE

It denotes a new book containing every occurrence of `BOOK_VALUE` in the same order, followed by one `ITEM_VALUE`. `ITEM_VALUE` must belong to the book's declared element domain.

The original book is unchanged. The wording is deliberately not imperative: A15 does **not** admit `הוסף לספר ...` as a mutating collection action.

If an integrated program later keeps a Collection in a state-bearing referent, replacement of that referent must be an explicit B12/A13-style state operation after the pure book Value has been computed. A15 does not make the book itself mutable.

## 5. Count and membership

Count:

    מספר הדברים אשר בתוך BOOK_VALUE

This maps to `count(C)` and returns a Natural.

Membership proposition:

    ITEM_VALUE כתוב בתוך BOOK_VALUE

This is true iff an equal member occurs at least once. It does not return an index or occurrence object.

`כתוב בספר` is independently Biblical (`כל הנמצא כתוב בספר`, Daniel 12:1) and is already present in the Megillah's book vocabulary.

## 6. First and last

First:

    ELEMENT_HEAD אשר בראש BOOK_VALUE

Last:

    ELEMENT_HEAD האחרון אשר בתוך BOOK_VALUE

`ELEMENT_HEAD` is the typed singular head belonging to the book kind: `המספר`, `מספר השנה`, `השם`, or `הספר`.

On an empty collection these descriptions fail with B13 `COLLECTION_POSITION_ERROR`; they do not yield null.

## 7. Ordinal selection

The Megillah genuinely needs repeated head/successor traversal, including nested books. A15 therefore exposes a positive ordinal relation, not an index operator:

    ELEMENT_HEAD אשר מספרו בסדר BOOK_VALUE הוא POSITION_VALUE

`POSITION_VALUE` is a Natural. The valid semantic interval is exactly `1..count(C)`. Position zero and positions above the count yield `COLLECTION_POSITION_ERROR`.

This is not bracket syntax, random-access machine imagery, or a zero origin. The source says that the element's **number in the order of the book** is the given positive Natural.

## 8. Successor and traversal

A15 intentionally does not admit bare `הדבר אשר אחריו` as a general collection primitive. With duplicate Values, a Value alone does not identify which occurrence is meant.

The canonical successor of the occurrence at ordinal K is expressed by ordinal selection at K+1:

    ELEMENT_HEAD אשר מספרו בסדר BOOK_VALUE הוא
    המספר הנחשב בהוסיף את POSITION_VALUE על המספר אשר הוא אחד

At the last position this yields `COLLECTION_POSITION_ERROR`.

Traversal requires no `for`/iterator construct. A source computation keeps a positive Natural position, selects the element whose number in the book's order is that position, advances the Natural explicitly, and stops after the count. Existing named acts and exact recurrence may package that composite computation. Order is always the book's stored semantic order, never textual source order.

## 9. Deterministic ordering

### Natural members

Pure ascending order is:

    הספר הערוך מן BOOK_VALUE מן המעט אל הרב

It maps to B13 `order(C, NaturalLT)`.

### Symbol members

Symbols have no spelling order. When their domain has a valid explicit A15 adjacent-order chain, use:

    הספר הערוך מן BOOK_VALUE כמשפט משפחת השמות אשר שמה DOMAIN

It maps to B13 `order(C, R_domain)`.

### Nested books — lexicographic profile

For a book of books whose leaf members have an admitted order:

    הספר הערוך מן BOOKS_VALUE מראש כל ספר ועד אחריתו מן המעט אל הרב

for Natural leaves, or:

    הספר הערוך מן BOOKS_VALUE מראש כל ספר ועד אחריתו כמשפט משפחת השמות אשר שמה DOMAIN

for Symbol leaves.

These map to B13 `order(C, Lex(R))`: compare the first unequal member; a strict prefix is less; structurally equal inner books tie. There is no executable comparator callback.

## 10. Evidence and controlled deviation

Megillah evidence is direct: `ספר ימי חודשים`, `ספר שמות חודשים`, `השם אשר בראש`, `השם אשר אחריו`, `החודש האחרון`, `ערוך את כל הספרים`, and lexicographic comparison by successive positions.

A15 preserves `ספר`, `בראש`, `אחרון`, and ordered comparison. It replaces the historically convenient bare `אחריו` with an occurrence-safe ordinal relation because B13 explicitly permits duplicates. That is a controlled clarification, not an array imitation.

## 11. Negative grammar

Reject implicit collection creation from a plural noun, order from declaration/text order, bracket/index syntax, position zero, mutation verbs as collection semantics, bare successor of an unlocated duplicate Value, hidden iteration state, inferred Symbol spelling order, arbitrary comparator acts, and heterogeneous append.
