# D4 Canonical Source-Name Cleanup

## Scope

This record canonicalizes source-declared identities in the live T18 Megillah candidate only. It does not advance Luach Fifteen, change grammar, compiler semantics, HAST/IR/artifact schemas, algorithms, owners, scopes, or values.

Starting accepted checkpoint: `T18`
Starting HEAD: `5f35e8cb9b8d4c16db1797c4832c6300791dc2c1`
Starting candidate SHA-256: `f55785a16a659c2c4423a255da051bb1f16481280519596011c1537b7d6e46ec`
Starting semantic boundary: `Luach Fifteen / original line 895`
Starting syntactic frontier token: `28,438`

## Inventory result

- total source-declared identities: **261**
- genuine single-word identities: **87**
- artificially welded identity instances: **173**
- distinct welded spellings removed: **158**
- already-canonical multi-word identities: **1**
- uncertain identities: **0**
- welded aliases retained: **NONE**
- semantic identity families added: **NONE**

Machine-readable decision ledger: `megillah/analysis/D4_CANONICAL_SOURCE_NAME_INVENTORY.json`.

## Method

Each identity was reviewed against the live T18 candidate, immutable original and D4 provenance. Multi-word replacements prefer source wording when the source names the concept directly; otherwise they use simple controlled Hebrew composition preserving the existing semantic identity. No automatic Hebrew-word detector and no mechanical compound splitter is used.

All canonical multi-word names use the accepted counted SourceName form:

`שם אשר מספר המלים אשר בו הוא COUNT והמלים הן WORD_1 ... WORD_N`

The semantic spelling is the normalized payload joined with one U+0020 space. No welded alias remains.

## Canonical replacements

| Historical live spelling at T18 | Canonical semantic payload | Words |
|---|---|---:|
| `אבןרבועעבודה` | `עבודת רבוע האבן` | 3 |
| `אבניטיפות` | `אבני הטיפות` | 2 |
| `אדומהחדשה` | `אדומה חדשה` | 2 |
| `אדומהישנה` | `אדומה ישנה` | 2 |
| `אותויום` | `אותו יום` | 2 |
| `אחבדוק` | `בדוק אח` | 2 |
| `אחהוסף` | `הוסף לאח` | 2 |
| `אחמחסר` | `מחסר האח` | 2 |
| `אחמספר` | `מספר האח` | 2 |
| `אחעבודה` | `עבודת האח` | 2 |
| `אחרייום` | `טפל ביום שאחרי היסוד` | 4 |
| `אתחלקערות` | `אתחל קערות` | 2 |
| `בחירהיעד` | `יעד הבחירה` | 2 |
| `בחירהמונה` | `מונה הבחירה` | 2 |
| `בחירהמועמד` | `מועמד הבחירה` | 2 |
| `בחירהספר` | `ספר הבחירה` | 2 |
| `בחירהתוצאה` | `תוצאת הבחירה` | 2 |
| `בחרבדוק` | `בדוק בחירה` | 2 |
| `בחרהבא` | `הבא בבחירה` | 2 |
| `בחרמערכה` | `בחר מערכה` | 2 |
| `בחרפנוי` | `בחר פנוי` | 2 |
| `בחרקערה` | `בחר קערה` | 2 |
| `בנהאבנים` | `בנה אבנים` | 2 |
| `בנהטיפות` | `בנה טיפות` | 2 |
| `בנהנסתרות` | `בנה נסתרות` | 2 |
| `גדולעבודה` | `עבודת המספר הגדול` | 3 |
| `דרךהכרע` | `הכרעת הדרך` | 2 |
| `דרךכפל` | `כפל הדרך` | 2 |
| `הכרעהיום` | `הכרעת יחס היום` | 3 |
| `זוגותחדשים` | `זוגות חדשים` | 2 |
| `זוגותמסודרים` | `זוגות מסודרים` | 2 |
| `חיבורכפל` | `כפל החיבור` | 2 |
| `חיטהחדשה` | `חיטה חדשה` | 2 |
| `חיטהישנה` | `חיטה ישנה` | 2 |
| `חלקגרע` | `גרע בחלוקה` | 2 |
| `חלקלולאה` | `לולאת החלוקה` | 2 |
| `חלקמחלק` | `מחלק החלוקה` | 2 |
| `חלקמנה` | `מנת החלוקה` | 2 |
| `חלקעבודה` | `עבודת החלוקה` | 2 |
| `חלקשארית` | `שארית החלוקה` | 2 |
| `חשבאבן` | `חשב אבן` | 2 |
| `חשבגדול` | `חשב המספר הגדול` | 3 |
| `חשבמלאקערה` | `חשב מלא הקערה` | 3 |
| `חשבנסתרת` | `חשב נסתרת` | 2 |
| `חשבציקה` | `חשב ציקה` | 2 |
| `חשבקערהאחרי` | `חשב קערה לאחר הטיפה` | 4 |
| `טחינהעבודה` | `עבודת הטחינה` | 2 |
| `טחןטיפה` | `טחן טיפה` | 2 |
| `טחןטיפהפעם` | `טחן טיפה פעם` | 3 |
| `טחןנסתרת` | `טחן נסתרת` | 2 |
| `טחןפעם` | `טחן פעם` | 2 |
| `טיפההבאה` | `הטיפה הבאה` | 2 |
| `טיפהעבודה` | `עבודת הטיפה` | 2 |
| `טיפהקודמתאחת` | `הטיפה אשר לפניה` | 3 |
| `טיפהקודמתשביעית` | `הטיפה השביעית אשר לפניה` | 4 |
| `טיפהקודמתשלישית` | `הטיפה השלישית אשר לפניה` | 4 |
| `טיפהקערותעבודה` | `טיפה לעיבוד הקערות` | 3 |
| `טיפהראשית` | `ראשית הטיפה` | 2 |
| `טיפותגלויות` | `הטיפות הגלויות` | 2 |
| `טיפותנסתרות` | `הטיפות הנסתרות` | 2 |
| `יוםמעשה` | `יום המעשה` | 2 |
| `יוםשאלה` | `היום אשר עליו תשאל` | 4 |
| `כלטיפות` | `כל הטיפות` | 2 |
| `כפלאחד` | `כפל ועוד אחד` | 3 |
| `כפלאחת` | `כפל אחת` | 2 |
| `כפלבחר` | `בחר בכפל` | 2 |
| `כפלגדול` | `כפל המספר הגדול` | 3 |
| `כפלהוסף` | `הוסף כפל` | 2 |
| `כפלראשון` | `כפל ראשון` | 2 |
| `כפלרד` | `רד בכפל` | 2 |
| `כפלשאר` | `מנין הכפל הנותר` | 3 |
| `כפלשביעית` | `כפל שביעית` | 2 |
| `כפלשלישית` | `כפל שלישית` | 2 |
| `לפנייום` | `טפל ביום שלפני היסוד` | 4 |
| `לקחתמאחיו` | `לקחת מספר מאחיו` | 3 |
| `לקחתפעמים` | `לקחת מספר פעמים` | 3 |
| `מהיררד` | `רד בדרך הקצרה` | 3 |
| `מהירתוצאה` | `תוצאת הדרך הקצרה` | 3 |
| `מלאישן` | `מלא ישן` | 2 |
| `מלאעבודה` | `עבודת מלא הקערה` | 3 |
| `מלאקערות` | `מלא הקערות` | 2 |
| `מלחחדשה` | `מלח חדשה` | 2 |
| `מלחישנה` | `מלח ישנה` | 2 |
| `מספרגדול` | `המספר הגדול` | 2 |
| `מספרדרך` | `מספר הדרך` | 2 |
| `מספרחיבור` | `מספר החיבור` | 2 |
| `מספרטיפה` | `מספר הטיפה` | 2 |
| `מספרטיפהגלויה` | `מספר הטיפה הגלויה` | 3 |
| `מספרטיפהקערות` | `מספר הטיפה לקערות` | 3 |
| `מספריום` | `חשב מספר היום` | 3 |
| `מספרמערכה` | `מספר המערכה` | 2 |
| `מספרמעשה` | `מספר המעשה` | 2 |
| `מספרמרחק` | `מספר המרחק` | 2 |
| `מספרקערה` | `מספר הקערה` | 2 |
| `מספרשאלה` | `מספר השאלה` | 2 |
| `מענהיום` | `מספר היום המחושב` | 3 |
| `מערכהנבחרה` | `קערה נבחרה` | 2 |
| `מערכהנבחרו` | `קערות שנבחרו` | 2 |
| `מערכהנוכחית` | `המערכה הנוכחית` | 2 |
| `מערכהשאר` | `שאר מספר המערכה` | 3 |
| `מערכהתוצאה` | `תוצאת המערכה` | 2 |
| `מערכתטיפהאחרונה` | `מערכת הטיפה האחרונה` | 3 |
| `מצאמערכה` | `מצא את המערכה` | 3 |
| `מקוםבדוק` | `בדוק מקום` | 2 |
| `מקוםהבא` | `המקום הבא` | 2 |
| `מקוםיעד` | `יעד המקום` | 2 |
| `מקוםמונה` | `מונה המקום` | 2 |
| `מקוםספר` | `מערכה לחיפוש` | 2 |
| `מקוםקערה` | `מקום הקערה` | 2 |
| `מקוםתוצאה` | `תוצאת המקום` | 2 |
| `מרהחדשה` | `מרה חדשה` | 2 |
| `מרהישנה` | `מרה ישנה` | 2 |
| `מרחקאחורה` | `מרחק אחורה` | 2 |
| `מרחקהכרע` | `הכרעת כיוון המרחק` | 3 |
| `מרחקהכרעאחור` | `הכרעת כיוון המרחק לאחור` | 4 |
| `מרחקיעד` | `יעד המרחק` | 2 |
| `מרחקכפל` | `כפל המרחק` | 2 |
| `מרחקמונה` | `מונה המרחק` | 2 |
| `מרחקסיום` | `סיום המרחק` | 2 |
| `מרחקסמן` | `סמן המרחק` | 2 |
| `מרחקצעדאחורה` | `צעד מרחק אחורה` | 3 |
| `מרחקצעדקדימה` | `צעד מרחק קדימה` | 3 |
| `מרחקקדימה` | `מרחק קדימה` | 2 |
| `נותרגרע` | `גרע לנותר` | 2 |
| `נותרלולאה` | `לולאת הנותר` | 2 |
| `נותרמהר` | `הנותר בדרך הקצרה` | 3 |
| `נותרמחלק` | `מחלק הנותר` | 2 |
| `נותרעבודה` | `עבודת הנותר` | 2 |
| `נסתרעבודה` | `עבודת הנסתרת` | 2 |
| `נסתרתאחת` | `הנסתרת האחת` | 2 |
| `נסתרתחמישית` | `הנסתרת החמישית` | 2 |
| `נסתרתרביעית` | `הנסתרת הרביעית` | 2 |
| `נסתרתשביעית` | `הנסתרת השביעית` | 2 |
| `נסתרתשלישית` | `הנסתרת השלישית` | 2 |
| `נסתרתשנית` | `הנסתרת השנית` | 2 |
| `נסתרתששית` | `הנסתרת הששית` | 2 |
| `ערבבטיפה` | `ערבב טיפה` | 2 |
| `ערבבכלטיפות` | `ערבב כל הטיפות` | 3 |
| `ערבובעבודה` | `עבודת הערבוב` | 2 |
| `עשהטיפהגלויה` | `עשה טיפה גלויה` | 3 |
| `עשהנסתרת` | `עשה נסתרת` | 2 |
| `צוקטיפה` | `צוק טיפה` | 2 |
| `ציקהאחת` | `ציקה אחת` | 2 |
| `ציקהעבודה` | `עבודת הציקה` | 2 |
| `ציקהשלש` | `ציקה שלש` | 2 |
| `ציקהשתים` | `ציקה שתים` | 2 |
| `צעדאחורה` | `צעד אחורה` | 2 |
| `צעדקדימה` | `צעד קדימה` | 2 |
| `קודמתאחת` | `הטיפה אשר לפניה` | 3 |
| `קודמתשביעית` | `הטיפה השביעית אשר לפניה` | 4 |
| `קודמתשלישית` | `הטיפה השלישית אשר לפניה` | 4 |
| `קערותטיפההבאה` | `קערות הטיפה הבאה` | 3 |
| `ראשיתטיפה` | `חשב ראשית הטיפה` | 3 |
| `שאלהכפל` | `כפל השאלה` | 2 |
| `שמורעבודה` | `עבודת שמור` | 2 |
| `שמותמספרים` | `חשב שמות המספרים` | 3 |
| `שעורהחדשה` | `שעורה חדשה` | 2 |
| `שעורהישנה` | `שעורה ישנה` | 2 |

## Frontier and source boundary

After source-name canonicalization only:

- candidate SHA-256: `9a048d98a03b5df02359bfcb21a0c28677621c7b67be16d72159c19b17dba755`
- normalized token count: `62,821`
- syntactic frontier token: `57,767`
- semantic/source boundary: `Luach Fifteen / original line 895`
- source advancement beyond T18: **NO**

The token frontier moved mechanically from `28,438` to `57,767` because counted SourceName spellings expand each name occurrence. Candidate line 466 remains the Luach Fifteen heading, and no Luach Fifteen executable source was admitted.

## Historical evidence

Frozen C5.6 fixtures, A18/B17 proposal evidence, and historical D4-PATCH descriptions are not rewritten merely to erase the spellings that existed at those historical checkpoints. Live candidate source, live D tests, and the current canonical naming ledger use only the canonical spellings.

## Verification

Local verification before push:

- anti-weld inventory regression: **4 passed**
- D3 + D4 conformance + cleanup regression: **33 passed**
- C5.7 multi-word SourceName + Program Input/Symbol regressions: **34 passed**
- live D4 post-C5.6 suite: **55 passed**
- T17/T18 focused Luach 13/14 suite: **8 passed, 47 deselected**
- full pytest: **622 passed, 126 subtests passed**
- frontier probe: **57,767**, candidate line **466**, same semantic/source boundary **Luach Fifteen / original line 895**
- original SHA-256 remains **7b834f4a444e021bb65164282b851af960a6dbc0be3d458c2412181773b9db7b**

The T18 final bowl receipt remains exactly:

`[36108001607085984155684996137766958104, 148814309144118602128584347831122254145, 146577346212655508303902655220312506515, 113571227321377053045622633394311758065, 156703568566579726750728213438464676042, 87934172320087745809620382672045550969]`

The anti-weld live-D regression is inventory-based and contains no NLP/word-validity heuristic. Ubuntu D4, Windows D4 and overall workflow status are recorded in the Master handoff after push/CI.
