# A13_WHITESPACE_NORMATIVE_SET.md

Status: NORMATIVE — A-CORE-004

Outside future strings the exact whitespace set is:

- U+0009–U+000D
- U+0020
- U+0085
- U+00A0
- U+1680
- U+2000–U+200A
- U+2028
- U+2029
- U+202F
- U+205F
- U+3000

Every nonempty run becomes one U+0020 SPACE, including a run at the beginning or end of source. Transparent characters are deleted and do not split an otherwise contiguous whitespace run after transparency normalization. Every scalar that is neither one of the fixed 27 Hebrew
letters nor in this table is transparent/deleted outside strings.

U+200B ZERO WIDTH SPACE is not whitespace: `יהי\u200Bמקום` normalizes to `יהימקום`, not `יהי מקום`.

No implementation predicate (`isspace()`, locale, ICU/Unicode-library behavior, etc.) defines the
language. Strings remain OPEN_AFTER_M2.
