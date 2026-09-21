# C5.6 — General / Non-Year BidirectionalIndex Surface

Status: production-integration candidate on `workstream-c/c5-6-general-bidirectional-index-surface`.

## Governing dependency

C5.6 implements the already accepted A17 surface and B16 semantic integration. It does not redesign either proposal.

There is exactly one semantic domain:

`BidirectionalIndex`.

The year-oriented and general/non-year forms are source-level linguistic profiles only. They lower into the same existing HAST/IR/value/domain/runtime path.

## General literals

The admitted origin is:

```text
מעלת היתד
```

which lowers to the existing zero Index representation.

Before/after forms are:

```text
מעלה אחת לפני מעלת היתד
שתי מעלות לפני מעלת היתד
COUNT מעלות לפני מעלת היתד

מעלה אחת אחרי מעלת היתד
שתי מעלות אחרי מעלת היתד
COUNT מעלות אחרי מעלת היתד
```

Productive COUNT reuses `A15_FEMININE_COUNT_LEXICON_ID`. C5.6 adds no numeral table and no A17-fixture-sized semantic cap.

All of these lower to the existing `HastIndexValue` and `IRIndexValue`.

## Program Input

General declaration:

```text
יהי למלאכה הזאת דבר ושמו ROLE
ובטרם תחל המלאכה הזאת תעמד מעלה
תחת הדבר אשר למלאכה הזאת שמו ROLE
```

General read:

```text
המעלה אשר עומדת תחת הדבר אשר למלאכה הזאת שמו ROLE
```

Both use the existing `ProgramInputId -> BIDIRECTIONAL_INDEX` contract.

Year declaration + general read and general declaration + year read are both legal because each head independently denotes the same domain. No profile field or profile-mismatch error exists.

## Place/state

General current value:

```text
המעלה אשר במקום אשר שמו PLACE
```

General displaced-value replacement head:

```text
שים במקום אשר שמו PLACE את INDEX_VALUE
תחת המעלה אשר במקום אשר שמו PLACE
```

No new place-introduction production was added. The existing typed Index initializer already consumes `IndexValue` and therefore admits either source profile.

## Named roles

General declaration:

```text
יהי במעשה אשר שמו ACT דבר ושמו ROLE
ובעשות את המעשה אשר שמו ACT תעמד מעלה
תחת הדבר אשר במעשה אשר שמו ACT שמו ROLE
```

General current value:

```text
המעלה אשר במעשה הזה עומדת
תחת הדבר אשר במעשה אשר שמו ACT שמו ROLE
```

Role association remains the existing profile-neutral `AssociationValue` path. The semantic role contract remains only `RoleId -> BIDIRECTIONAL_INDEX`.

## Output and immediate result

C5.6 does not add a second output action. Existing:

```text
הוצא מן המעשה הזה את INDEX_VALUE
```

continues to consume `IndexValue`.

The new general immediate-result head is:

```text
המעלה אשר יצאה עתה מן המעשה אשר שמו ACT
```

and lowers to the existing typed immediate-result carrier with `BIDIRECTIONAL_INDEX`.

## Successor and predecessor

General forms:

```text
המעלה אשר אחר INDEX_VALUE
המעלה אשר לפני INDEX_VALUE
```

lower to the existing `HastIndexSuccessor` / `HastIndexPredecessor` and `IRIndexSuccessor` / `IRIndexPredecessor`.

They are total and use the existing zero-crossing semantics.

## Collections boundary

No generic Index Collection noun was added.

Existing year-oriented Collection<BidirectionalIndex> grammar remains unchanged. Operations whose existing grammar already consumes `IndexValue` accept a value originating from the general profile because the value is semantically the same BidirectionalIndex.

No `ספר מעלות`, `ספר מעלה`, or new nested generic Index collection kind exists.

## Explicit non-features

C5.6 does not add:

- Index equality;
- direct Index distance;
- Natural↔Index source conversion;
- signed arithmetic;
- unary minus;
- ++ / --;
- generic Integer;
- runtime profile tags;
- profile mismatch errors;
- user-defined profile/unit nouns;
- Day/Date/Time/Timestamp;
- a second `A אחרי B` order primitive.

Distance remains an algorithm composed from existing language machinery.
