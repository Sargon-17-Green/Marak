# C Source Normalization

Status: normative for A13 Core v0.1 integration candidate.

Outside future strings, the only retained letters are the explicit 27 Hebrew forms. No NFC/NFKC or broad Hebrew-block regex is applied.

The exact A13 whitespace separator set is:

- U+0009..U+000D
- U+0020
- U+0085
- U+00A0
- U+1680
- U+2000..U+200A
- U+2028
- U+2029
- U+202F
- U+205F
- U+3000

Every nonempty run collapses to one ASCII space. Every other non-27-letter character is transparent/deleted. In particular U+200B ZERO WIDTH SPACE is deleted and is not a separator.

The implementation uses a closed constant table. `str.isspace()`, regex `\s`, host Unicode version and locale are not normative sources. `WhitespacePolicy` remains injectable only as a conformance/testing seam; the normal compiler default is exactly the A13 normative policy.

Source maps preserve original file, code-point offset, UTF-8 byte offset, line, column and spans through deletion/collapse.
