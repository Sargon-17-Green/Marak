# C5.2 Productive Direct Naturals

The production numeral recognizer now admits the accepted A15 direct-literal edition family from 1 through 99,999,999. This is a source-family frontier only; runtime Naturals remain exact and unbounded. No direct zero literal or Arabic-digit literal was added.

The recognizer is an exact inverse of the accepted A15 canonical formatter. It uses the frozen A13 reverse table as authority through 9,999, then exact million/thousand/low component indexes for the productive range. Canonical descending magnitude order, one-use magnitude slots, and accepted waw placement are enforced by accepting a phrase only when recomputation yields the identical canonical spelling. There is no heuristic, closest reading, or fuzzy decomposition.

Independent evidence covers all 9,999 frozen A13 forms, the 14,777,149 Megillah constant, magnitude boundaries, 500 production-parser random large samples, and the broader A15 reference suite (335,280 case checks including 75,000 random large samples). Malformed reordered, duplicated, illegal-coefficient, malformed-waw, ambiguous, zero, Arabic-digit, and out-of-edition forms are rejected.
