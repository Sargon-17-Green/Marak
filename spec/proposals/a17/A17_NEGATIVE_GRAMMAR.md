# A17 — Negative Grammar

The following are not admitted by the A17 proposal.

## Incomplete / malformed literals

- bare `מעלה`
- bare `מעלות`
- bare `מעלת`
- bare `היתד`
- `מעלת יתד`
- `מעלה היתד`
- `מעלה אחת`
- `אחת לפני מעלת היתד`
- `מעלה אחת לפני היתד`
- `שתי מעלה לפני מעלת היתד`
- zero-distance encoded as `אפס מעלות לפני מעלת היתד`
- zero-distance encoded as `אפס מעלות אחרי מעלת היתד`
- `מעלת אין`
- `מעלה אין`
- unary-minus forms such as `מינוס מעלה אחת`

## Mixed profiles

Reject:
- `שנה אחת לפני מעלת היתד`
- `מעלה אחת לפני שנת אין`
- `מספר השנה אשר ...` as a rescue for a malformed generic literal
- `המעלה אשר ...` as a rescue for malformed year source
- doubled heads such as `מספר השנה המעלה ...`
- expected-context interpretation of a bare numeral as Index

The year and generic profiles share semantic domain but their source phrases are independently closed.

## Typed carrier errors

Reject:
- declaration `יעמד מעלה ...` (wrong masculine agreement in the selected generic profile);
- reference `המעלה אשר עומד ...`;
- immediate result `המעלה אשר יצא עתה ...`;
- bare place identity where `המעלה אשר במקום...` is required;
- bare role identity where `המעלה ... עומדת תחת...` is required;
- positional Program Input binding or transport syntax.

These are surface-profile agreement rules, not new runtime types.

## Operations not admitted

Reject as A17 primitives:
- generic Index equality `INDEX_A הוא INDEX_B`;
- alternate strict-order spelling `INDEX_A אחרי INDEX_B`;
- direct built-in distance phrase;
- Natural subtraction that yields BeforeZero;
- implicit Natural -> Index;
- generic signed addition/subtraction/multiplication;
- `++` / `--`;
- generic `ספר מעלות` / `ספרי מעלות` collection kinds.

“A אחרי B” remains expressible as the canonical proposition `B לפני A`; it is not accepted as a second canonical order production.

## Ambiguity policy

No expected type, nearby carrier, punctuation, line break, Markdown, or capitalization may resolve a malformed phrase. If the normalized words admit two computational parses, the source is invalid rather than guessed.
