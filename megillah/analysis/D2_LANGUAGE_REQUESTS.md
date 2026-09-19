# D2 Language Requests

These are Master-routing requests only. D does not implement any of them.

## D-LANGUAGE-REQUEST-001 — Runtime symbolic/text labels for calendar names
- Computational need: The canonical result contains cutlet/month names; compile-time Marak names are not runtime data and Core strings are absent.
- Source examples: שם הקציצה, שם החודש, 17 cutlet names, 47 month names
- Why Core repair is unsatisfactory: Numeric codes alone would change the externally stated result unless a separate normative name mapping remains outside the program.
- Anti-imitation audit: The need is symbolic named output explicitly demanded by the source, not a generic wish for strings.

## D-LANGUAGE-REQUEST-002 — Signed year-number representation
- Computational need: The year sequence crosses year zero and continues to years before it; Core Values are naturals.
- Source examples: אחר שנה אחת תבוא שנת אין, אחת לפני אין, אות החסר
- Why Core repair is unsatisfactory: Sign+magnitude can be encoded in several naturals but is a material source/result rewrite.
- Anti-imitation audit: The need comes from the calendar's explicit negative-year numbering, not from assuming an Integer type.

## D-LANGUAGE-REQUEST-003 — Finite ordered runtime collections or equivalent general data relation
- Computational need: The algorithm constructs, orders, selects, and traverses runtime collections of candidates, books, permutations, and weavings.
- Source examples: ספר ימי חודשים, ספר שמות חודשים, ערוך את כל הספרים, בחר אחת מן השנים
- Why Core repair is unsatisfactory: Gödel-style numeric encodings are computable but would cease to be ordinary/local Megillah repair.
- Anti-imitation audit: No array/list implementation is prescribed; only source-visible ordered finite collection behavior is requested.

## D-LANGUAGE-REQUEST-004 — General numeric ordering propositions
- Computational need: The Megillah repeatedly branches/orders by רב/ימעט; Core freezes equality/zero but no general numeric order proposition.
- Source examples: אם רב המספר, הספר אשר ... ימעט, השנה אשר ימיה מעטים
- Why Core repair is unsatisfactory: Possible encodings are non-local and awkward under natural-subtraction domain failure; they obscure rather than locally repair the source.
- Anti-imitation audit: The request is the explicit Biblical relation רב/מעט, not a symbolic > or < operator.

## D-LANGUAGE-REQUEST-005 — Productive direct Biblical numeral grammar beyond 9999
- Computational need: A-NUM-001 explicitly leaves >9999 as future full-language/Megillah compatibility work.
- Source examples: large fixed constants in the sauce/calendar rules
- Why Core repair is unsatisfactory: Values can be computed from smaller literals, but systematically replacing written numerals would be large and historically distortive.
- Anti-imitation audit: This extends Biblical numeral language, not machine-literal syntax.

## D-LANGUAGE-REQUEST-006 — General exact counted recurrence N פעמים for arbitrary admitted natural N
- Computational need: The source uses natural counted-repetition wording with counts far beyond the small individually audited Core forms, including 125 and 127.
- Source examples: חמש ועשרים ומאה פעמים, שבע ועשרים ומאה, פעם אחר פעם
- Why Core repair is unsatisfactory: Named recursion can encode the computation, but replacing every ordinary N פעמים occurrence by explicit counters/recursion is non-local.
- Anti-imitation audit: The source already says N פעמים in Biblical Hebrew; this is not a request for a conventional for-loop.

## D-LANGUAGE-REQUEST-007 — Explicit external input binding for the two day values
- Computational need: The Megillah is parameterized by יום המעשה and היום אשר עליו תשאל, but a Core executable has no source-level external input association.
- Source examples: למלאכת הלוח קח שני ימים, לראשון קרא יום המעשה, לשני קרא היום אשר עליו תשאל
- Why Core repair is unsatisfactory: A fixed-query program can hard-code/initialize two places, but that is not the reusable two-input algorithm described by the source.
- Anti-imitation audit: No stdin/argv convention is assumed; the request is only an explicit language/host boundary for two source-described input values.

## Deliberately not requested
- A separate while/pre-check loop feature is not requested merely because the source says כל עוד. Current Core recursion/conditionals can express pre-gated repetition; D must first attempt a source repair.
- Multiplication/squaring is not requested as a primitive merely because the Megillah computes it; the source itself supplies algorithms for those operations.
- Positional multi-result tuples are not requested for the final five fields; explicit retained result referents should be tried first.
