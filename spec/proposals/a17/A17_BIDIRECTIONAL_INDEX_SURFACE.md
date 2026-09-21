# A17 — General BidirectionalIndex Surface

## 1. Semantic target

Every construction in this document maps only to the already-existing B13 `BidirectionalIndex` domain:

- `ZeroIndex`
- `BeforeZero(n)` for positive Natural `n`
- `AfterZero(n)` for positive Natural `n`

No new semantic domain or runtime representation is proposed.

## 2. General literal profile

Canonical generic/non-year origin:

    מעלת היתד

Canonical distances from the origin:

    מעלה אחת לפני מעלת היתד
    שתי מעלות לפני מעלת היתד
    COUNT מעלות לפני מעלת היתד

    מעלה אחת אחרי מעלת היתד
    שתי מעלות אחרי מעלת היתד
    COUNT מעלות אחרי מעלת היתד

For the productive form, `COUNT >= 3` uses the exact existing A15 feminine-count morphology. Mapping is exact:

- `מעלת היתד` -> `ZeroIndex`
- `N מעלות לפני מעלת היתד` -> `BeforeZero(N)`
- `N מעלות אחרי מעלת היתד` -> `AfterZero(N)`

`מעלה` is a surface noun, not a new type object. `יתד` is the controlled anchor metaphor for the distinguished origin; it is not a source-declared entity and not a runtime value of its own.

## 3. Generic typed carrier head

The non-year typed head is the feminine noun `מעלה`.

Program Input declaration:

    יהי למלאכה הזאת דבר ושמו ROLE
    ובטרם תחל המלאכה הזאת
    תעמד מעלה
    תחת הדבר אשר למלאכה הזאת שמו ROLE

Program Input reference:

    המעלה אשר עומדת תחת הדבר אשר למלאכה הזאת שמו ROLE

State current value:

    המעלה אשר במקום אשר שמו PLACE

State initialization keeps the A16 carrier frame:

    יהי מקום ושמו PLACE
    ובמקום אשר שמו PLACE יהי INDEX_VALUE לבדו

Replacement:

    שים במקום אשר שמו PLACE את INDEX_VALUE
    תחת המעלה אשר במקום אשר שמו PLACE

Named-act role declaration:

    יהי במעשה אשר שמו ACT דבר ושמו ROLE
    ובעשות את המעשה אשר שמו ACT
    תעמד מעלה
    תחת הדבר אשר במעשה אשר שמו ACT שמו ROLE

Current role value:

    המעלה אשר במעשה הזה עומדת
    תחת הדבר אשר במעשה אשר שמו ACT שמו ROLE

Performance association remains the existing profile-neutral construction:

    עשה את המעשה אשר שמו ACT
    בהיות INDEX_VALUE
    תחת הדבר אשר במעשה אשר שמו ACT שמו ROLE

Output production remains:

    הוצא מן המעשה הזה את INDEX_VALUE

Immediate result:

    המעלה אשר יצאה עתה מן המעשה אשר שמו ACT

The line breaks above are documentary only.

## 4. Strict chronological/index order

A17 proposes one canonical strict-order proposition:

    INDEX_VALUE_A לפני INDEX_VALUE_B

It maps to B13 strict Index order `A < B`.

A17 does **not** add a second canonical `A אחרי B` proposition. “A is after B” is expressed by operand reversal:

    B לפני A

This avoids two canonical source propositions for the same relation while still covering the Megillah's before/after need.

## 5. Total neighboring step

The existing A16 year-specific step family is generalized with the new typed head:

    המעלה אשר אחר INDEX_VALUE
    המעלה אשר לפני INDEX_VALUE

These map respectively to:

- `succ(INDEX_VALUE)`
- `pred(INDEX_VALUE)`

Both remain total and cross the origin without special syntax.

## 6. Year profile compatibility and canonicality

A15/A16 year forms remain byte-for-byte and meaning-for-meaning unchanged:

    שנת אין
    N שנים לפני שנת אין
    N שנים אחרי שנת אין
    מספר השנה ...

The year and `מעלה` profiles are **not semantic subtypes**. Both denote the same B13 `BidirectionalIndex` values. Surface profile is syntactic provenance only; it is not observable runtime data and does not change equality, order, output, or binding semantics.

Both profiles are canonical **within their own linguistic construction families**. Neither is sugar for the other. A future source formatter that is preserving source must preserve the resolved source profile. A formatter synthesizing source from a bare semantic Index Value cannot infer “year” versus “general”; it must be given an explicit target surface profile. A17 does not add runtime profile tags.

A17 introduces no static “unit type” preventing a generic Index value from flowing through a year-profile carrier or vice versa; doing so would be new semantics and belongs, if ever justified, to B rather than A17.

## 7. Deliberately absent surfaces

No A17 surface is proposed for:

- Index equality;
- direct `distance(i,j)`;
- Natural -> Index or Index -> Natural conversion;
- generic signed arithmetic;
- generic Index collection kind;
- arbitrary noun/profile parameters;
- Day/Date/Time/Timestamp.

The Megillah can derive exact distance algorithmically by selecting direction with strict order and stepping by `succ`/`pred` while retaining a Natural count. B16 must review whether that algorithm/surface boundary is appropriate, but A17 does not preempt it.
