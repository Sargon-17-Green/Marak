# Marak Language Charter

Marak source is controlled Biblical Hebrew.

Outside string literals, only the 27 Hebrew letters and normative whitespace are semantically meaningful. Every non-empty whitespace run collapses to one space; other characters are transparent. Punctuation, Markdown, indentation, line breaks, Latin letters, Arabic digits, niqqud and cantillation cannot carry semantics outside strings.

If a source text is valid Marak, its compiler meaning must agree with the meaning a competent reader of Biblical Hebrew would understand from the admitted controlled construction. Marak need not accept every intelligible Biblical-Hebrew sentence.

A source whose plausible readings can change computation is invalid. The compiler must not resolve such ambiguity by confidence, nearest-antecedent heuristics, layout, or conventions imported from another programming language.

The language must be computationally universal. The existing Megillah is intended to become a Marak program after ordinary local source corrections rather than by adding Megillah-specific compiler rules.

Implementation techniques may be conventional internally, but they do not define the language ontology. In particular, familiar concepts such as function, return, Boolean value, positional argument, while-loop, main function, stack frame, or variable assignment are not assumed unless independently justified by Marak's semantics and source language.
