# D2 Language Requests

These are requests for Master routing only. Workstream D does not implement language features.

## D-LANGUAGE-REQUEST-001 — Runtime symbolic/text labels for calendar names
- Source examples: שם הקציצה, שם החודש, 17 cutlet names, 47 month names
- Computational need: Canonical algorithm returns names; compile-time Marak names are not runtime data and Core strings are absent.
- Biblical-Hebrew evidence: The Megillah explicitly names and later returns selected names.
- Why Core repair is unsatisfactory: No satisfactory local numeric-only repair preserves the five-field calendar result naturally.
- Anti-imitation audit: Need is symbolic named data, not 'strings because other languages have strings'.

## D-LANGUAGE-REQUEST-002 — Signed year-number representation
- Source examples: אחר שנה אחת תבוא שנת אין, ולשנה אשר לפניה קרא אחת לפני אין, שים ... את אות החסר
- Computational need: The canonical year sequence crosses zero and continues to negative-numbered years; Core Values are naturals.
- Biblical-Hebrew evidence: The source explicitly describes years before zero and a written minus sign.
- Why Core repair is unsatisfactory: Sign+magnitude in two naturals is possible but materially rewrites the source/result contract.
- Anti-imitation audit: Need comes from the calendar domain, not from assuming an Integer type.

## D-LANGUAGE-REQUEST-003 — Finite ordered runtime collections or equivalent general data relation
- Source examples: ספר שמות, ספר ימי החודשים, ordered candidate years, permutations/weavings
- Computational need: The source manipulates runtime-sized ordered alternatives and selects/reorders them as data.
- Biblical-Hebrew evidence: Repeated ספר/מערכת/list-like discourse has order and membership semantics.
- Why Core repair is unsatisfactory: Encoding every collection into naturals would be a wholesale algorithm rewrite.
- Anti-imitation audit: Request is for ordered finite collection behavior, not specifically an array/list implementation.

## D-LANGUAGE-REQUEST-004 — General numeric ordering propositions / pre-gated recurrence evidence
- Source examples: אם רב המספר, אשר ימעט, פעם אחר פעם כל עוד
- Computational need: A13 Core freezes equality/zero and one post-action recurrence; source repeatedly relies on order and before-gated continuation.
- Biblical-Hebrew evidence: רב/מעט/כל עוד are explicit relational Hebrew, not symbolic operators.
- Why Core repair is unsatisfactory: Possible via Core constructions but non-local and repeatedly obscures the original algorithm.
- Anti-imitation audit: No > operator or while keyword is requested; only the source-expressed relation/capability.

## D-LANGUAGE-REQUEST-005 — Productive direct Biblical numeral grammar beyond 9999
- Source examples: large fixed constants throughout the sauce/calendar rules
- Computational need: A-NUM-001 explicitly calls >9999 a full-language/Megillah compatibility requirement.
- Biblical-Hebrew evidence: The original spells large numbers in Hebrew words.
- Why Core repair is unsatisfactory: They can be computed from smaller literals, but systematic replacement would be large and historically distortive.
- Anti-imitation audit: This extends Biblical numeral language, not machine integer syntax.
