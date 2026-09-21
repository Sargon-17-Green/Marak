# A17 — General / Non-Year BidirectionalIndex Surface

Status: **A17 PERIOD-LANGUAGE SURFACE READY FOR MASTER REVIEW**

Baseline: `e8f766889676b219f0abf5c9e4f08fad3034fa5b`  
Branch: `workstream-a/a17-general-bidirectional-index-surface`

## Scope

A17 addresses only `D4-LANG-001`: a truthful non-year source exposure of the already-existing B13 `BidirectionalIndex` semantic domain. It does not create a Day, Date, Time, Timestamp, Integer, signed Natural, or host-time domain. It changes no production grammar, registry, compiler, runtime, artifact schema, or Megillah source.

The selected surface is a general **מעלה** profile. Its distinguished origin is **מעלת היתד**. The year profile from A15/A16 remains unchanged and independently canonical in the year linguistic profile.

## Selected family

- origin: `מעלת היתד`
- BeforeZero(1): `מעלה אחת לפני מעלת היתד`
- BeforeZero(2): `שתי מעלות לפני מעלת היתד`
- BeforeZero(N>=3): `COUNT מעלות לפני מעלת היתד`
- AfterZero(1): `מעלה אחת אחרי מעלת היתד`
- AfterZero(2): `שתי מעלות אחרי מעלת היתד`
- AfterZero(N>=3): `COUNT מעלות אחרי מעלת היתד`
- strict order: `INDEX_A לפני INDEX_B`
- successor: `המעלה אשר אחר INDEX_VALUE`
- predecessor: `המעלה אשר לפני INDEX_VALUE`

`COUNT` reuses the existing A15 feminine-count morphology; A17 does not add a numeral system.

Typed carrier forms use `מעלה` / `המעלה` with feminine agreement where a verb or participle is present: `תעמד`, `עומדת`, `יצאה`.

## Deliberately not surfaced

A17 does not propose Index equality, direct distance, Natural↔Index conversion, generic Index collections, a generic signed arithmetic family, or an arbitrary user-supplied profile noun. Those capabilities either lack independent source need or would turn algorithmic work into language syntax.

B16 owns semantic integration and anti-imitation acceptance.
