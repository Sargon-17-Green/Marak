# A17 — Lexical Privilege Audit

## 1. Actual current lexical model

A17 does **not** model Marak as a language with a C/Python-style reserved-word table.

At baseline `e8f766889676b219f0abf5c9e4f08fad3034fa5b`:

- `compiler/lex/words.py` explicitly says an orthographic word is **not assumed to be a semantic token**.
- `NameTerminal` in `compiler/parse/grammar.py` is an open one-word name slot and explicitly says reserved-word filtering is absent.
- `WordTerminal` has force only at an exact position in an admitted production.
- the parser preserves ambiguity instead of ranking or guessing.
- normalization retains only the 27 admitted Hebrew letters and normative whitespace; punctuation and other characters cannot create lexical privilege.

The production registry snapshot `c5.5-a15-b13.1` contains 155 productions and **115 distinct exact WordTerminal spellings**. This is a construction-local privilege inventory, not a global reserved list:

`אחר אחרי אחריתו אחת אין אל אם ארבע אשר את ב בגרע בהוסיף בהיות בו במעשה במקום במשפחת במשפט בסדר בראש בשמו בתוך דבר האחרון הדבר הדברים הוא הוצא הזאת הזה המלאכה המלים המספר המעט המעשה הנה הנחשב הנראה הספר הערוך הרב השם השמות השנה ואחר ואחרי ואם ואשר ובהיות ובטרם ובמקום ובעשות וכן ולשם ועד ועתה ושמה ושמו זה חמש יהי יהיה יעמד יצא כל כלם כמספר כמשפט כן כסדרו כתוב לא לבדו למלאכה לפני מיד ממשפחת מן מספר מספרו מספרי מספרים מעשה מקום מראש משפחת ספר ספרי עד עומד על עשה עתה פעם פעמים רב שבע שים שלש שם שמה שמו שמות שמנה שנה שנים שנת שש שתי תהי תחל תחת תעשה תשע`

Other privileged terminal classes are:
- 11 explicit `NameTerminal` roles;
- numeral lexicons `a15-direct-1-99999999` and `a15-feminine-count-3-99999999`;
- counted Symbol-label terminal using the A15 direct numeral lexicon;
- nonterminals that compose already-admitted constructions.

No active production uses a `MorphTerminal` at this baseline.

## 2. New orthographic forms proposed by A17

The selected surface introduces these exact normalized forms not present in the current 115 WordTerminal set:

| form | role | privilege | global reservation? |
|---|---|---|---|
| `מעלה` | generic Index typed head; singular counted literal | construction-local typed-head/literal | NO |
| `מעלות` | plural counted Index literal | construction-local | NO |
| `מעלת` | construct singular in origin literal | construction-local | NO |
| `המעלה` | definite typed reference head / succ-pred head | construction-local typed head | NO |
| `היתד` | fixed second word of origin literal | construction-local fixed phrase | NO |
| `תעמד` | feminine agreement in declarations | construction-local structural word | NO |
| `עומדת` | feminine current-role/input agreement | construction-local structural word | NO |
| `יצאה` | feminine immediate-result agreement | construction-local structural word | NO |

Existing forms reused include `אחת`, `שתי`, `לפני`, `אחרי`, `אחר`, `אשר`, `תחת`, `הדבר`, `במקום`, `במעשה`, `למלאכה`, `הזאת`, `שמו`, `עתה`, `מן`, `המעשה`, `שים`, `הוצא`, `יהי`, and the existing A15 feminine-count numeral lexicon.

## 3. Identifier collision analysis

No new A17 word is globally reserved. A source name may still have the consonants `מעלה`, `היתד`, `תעמד`, etc. when it appears in an explicit `NameTerminal` slot such as `ושמו NAME`.

The parser must reject a complete source if the **whole normalized construction**, not a single word, has multiple computational readings. A17 does not add keyword filtering to avoid that obligation.

Examples:
- `יהי מקום ושמו מעלה ...` remains a legal use of `מעלה` as a place name because the grammar position after `ושמו` is a name slot.
- bare `מעלה` is not an Index Value.
- bare `היתד` is not an Index Value.
- `מעלת היתד` is one fixed Index literal and is not obtained by treating either word as a universal keyword.

## 4. Prefix / normalization ambiguity

`מעלה`, `מעלות`, `מעלת`, and `המעלה` are separate orthographic words; the Charter does not stem or prefix-strip them. No selected new phrase normalizes to an existing year literal or Natural literal.

Potential unpointed homography of `מעלה` with verbal morphology is controlled by the full construction:
- literal uses counted nominal frames;
- declaration places it after feminine `תעמד`;
- references use definite `המעלה` plus a relative clause.

No expected-type rescue is allowed.

## 5. Lexical freedom impact

**Result: no global lexical freedom is removed.**

A17 increases only the set of complete admitted constructions. Existing entity names are not invalidated merely because their spelling matches a new A17 WordTerminal. A future C implementation must preserve the current “name slot, not reserved-word list” model.

## 6. Registry impact

A17 does **not** update `spec/CURRENT_CONSTRUCTION_REGISTRY.json` or production parser tables. This audit is proposal evidence only for B16 and any later C5.6 implementation.
