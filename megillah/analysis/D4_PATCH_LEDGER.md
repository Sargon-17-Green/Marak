# D4 Patch Ledger

D4 post-C5.6 preserves every accepted D3 repair and now resumes candidate repair.

| ID | State | Classification | Preservation |
|---|---|---|---|
| D-PATCH-0001 | PRESERVED_FROM_D3 / Master-approved | SOURCE_PROGRAMMING_BUG | ALGORITHM_CHANGE |
| D-PATCH-0002 | PRESERVED_FROM_D3 | SOURCE_AMBIGUITY | DISAMBIGUATION_ONLY |
| D-PATCH-0003 | PRESERVED_FROM_D3 | SOURCE_AMBIGUITY | DISAMBIGUATION_ONLY |
| D-PATCH-0004 | PRESERVED_FROM_D3 | SOURCE_AMBIGUITY | SEMANTIC_EQUIVALENT |
| D3-STRUCT-0001 | PRESERVED_FROM_D3 | STRUCTURAL_EXPLICITNESS | SEMANTIC_EQUIVALENT |
| D4-PATCH-001 | APPLIED_TO_CANDIDATE_POST_C56 | STRUCTURAL_EXPLICITNESS | SEMANTIC_EQUIVALENT |

## D4-PATCH-001 — Foundation referent

Original lines 35–37 introduce and explain `יום היסוד` as the distinguished day coordinate from which days on both sides are measured.

Candidate replacement:

`יהי מקום ושמו יסוד ובמקום אשר שמו יסוד יהי מעלת היתד לבדו`

This uses the A17/B16/C5.6 general profile of the existing `BidirectionalIndex` domain. It does not create a Day domain, profile tag, Natural conversion, direct distance, or equality primitive.

The explanatory remainder of original line 37 is externalized as `D4-DOC-001` with provenance; the semantic origin requirement remains executable.


## D4-PATCH-002 — Tablets historical proof externalization

Original lines 39–45 contain the one-off Tablets/Foundation relation, a worked derivation of the large offset, and the next section heading.

Occurrence audit finds no later computational reference to `יום הינתן הלוחות` or `מספר כל הימים`. D4 therefore classifies the relation and arithmetic as `EXAMPLE_OR_PROOF`, and the heading as documentary organization. They are removed from executable candidate text but retained in the provenance map. No Tablets primitive or precomputed runtime constant is introduced.


## D4-PATCH-003 — day-coordinate to Natural day-number algorithm

Original lines 47–59 define the executable mapping; lines 61–69 are worked examples; lines 71–73 state invariants.

The candidate now defines `מספריום` over a general BidirectionalIndex role. It:
- copies the input coordinate to an Index cursor;
- resets a retained Natural counter;
- classifies BEFORE/SAME/AFTER with two strict Index-order tests;
- walks with successor/predecessor one position at a time;
- increments the Natural counter for each step;
- invokes the existing D3 `חיבור` act to double the count and, on the after side, add one;
- returns one for the Foundation coordinate.

No direct Index distance, equality, Natural↔Index conversion, signed arithmetic, or Day domain is introduced.


## D4-PATCH-004 — Luach Two / Program Input and derived numbers

Original lines 77–117 are converted to two named immutable general-BidirectionalIndex Program Inputs plus retained Natural places for `מספרמעשה`, `מספרשאלה`, `מספרמרחק`, `מספרחיבור`, and `מספרדרך`.

`שמותמספרים` invokes the repaired `מספריום` twice, counts inclusive distance by one-step Index traversal starting from one, invokes the existing `חיבור` act for the connection number, and classifies way using two strict Index-order tests. No direct distance, equality, Date/Day, positional input, or transport syntax is introduced.


## D4-PATCH-005 — Luach Three exact repeated addition

Original lines 121–141 define the reusable operation “take a number N times,” with examples and a historical doubling/decomposition acceleration.

The candidate now defines `לקחתפעמים` with Natural roles `מספר` and `מנין`. It clears a Natural accumulator and uses C5.4 dynamic `RepeatExactly` to perform one atomic helper act exactly `מנין` times, adding `מספר` on each iteration, then returns the accumulator.

The 3×7 example and 13-count decomposition are retained as evidence. The historical doubling workaround is not kept as production emulation because general exact counted recurrence now exists.


## D4-PATCH-006 — Luach Four square

Original lines 145–163 define `רבוע`: take the supplied number exactly that many times and add the copies. A later square consumes the prior square result rather than returning to the first input.

The repaired candidate defines one Natural role and invokes `לקחתפעמים` with the same Natural as both value and count. No hidden accumulator or remembered “original” number is added to `רבוע`; repeated squaring is ordinary explicit composition.


## D4-PATCH-007 — Luach Five / המספר הגדול

Original lines 167–193 construct a retained constant by starting at one, doubling exactly 127 times, and subtracting one.

The candidate now has persistent Naturals `גדולעבודה` and `מספרגדול`, an atomic doubling act `כפלגדול`, and initializer `חשבגדול`. The initializer resets the work value to one, performs `כפלגדול` exactly `מאה ועשרים ושבע פעמים`, stores `2^127-1`, and returns it.

The source's “write once / do not remake every time” rule is represented without hidden setup: final principal assembly must invoke `חשבגדול` once before any dependent operation.

## D4-PATCH-008 — Luach Six / remainder and kept remainder

Original lines 197–227 define two deliberately distinct reductions. `נותר` is ordinary Natural remainder: repeated subtraction of the divisor, with “אין” meaning zero remainder. `שמור` reduces by `מספרגדול` but represents the zero residue by `מספרגדול`, so its result lies in 1..`מספרגדול`.

The repaired candidate defines Natural work places and named acts `נותר`, `נותרגרע`, `נותרלולאה`, and `שמור`. Before entering the post-action subtraction recurrence, `נותר` checks whether the divisor is already greater than the dividend; therefore B12 Natural underflow is never used as loop control. Exact multiples safely subtract to zero and terminate on the next proposition check.

`שמור` calls `נותר` with `מספרגדול` as divisor, then maps only zero to `מספרגדול`. The two operations remain semantically distinct exactly as required by the source.

## D4-PATCH-009 — Luach Six / wrapped sibling subtraction

Original lines 229–241 define subtraction in the cyclic `מספרגדול` space: subtract directly when possible; otherwise add `מספרגדול` to the sibling as many times as needed, then subtract and apply `שמור`.

The repair introduces `לקחתמאחיו` with Natural roles `מחסר` and `אחמספר`, plus explicit work state and two helper acts. `אחבדוק` asks exactly whether the subtrahend is still greater than the current work value; only then does `אחהוסף` add `מספרגדול` and recurse. Therefore the eventual B12 subtraction is always in-domain.

Equality needs no invented third arithmetic case: subtraction is already defined when the values are equal, yields Natural zero, and the source-mandated final `שמור` maps that residue to `מספרגדול`.

## D4-PATCH-010 — Luach Six / fast repeated subtraction

Original lines 243–263 prescribe the short route for large repeated subtraction: double the divisor until passing the dividend, then traverse those doublings from largest to smallest and subtract each value that still fits. The source explicitly states that the short route yields the same number as the long route.

The repaired candidate defines `נותרמהר` and `מהיררד`. Recursive performance occurrences retain the successive doubled divisors as explicit role values; unwind is therefore the source's descending greedy pass. Every subtraction is guarded by strict Natural order and remains within the B12 domain.

No numeric threshold is invented for the documentary word “מאד”. Because the source itself declares exact result equivalence, `שמור` uses the short act directly for its modulo-`מספרגדול` reduction. The separate linear `נותר` operation remains available and unchanged.

## D4-PATCH-011 — Luach Three fast multiplication remediation

Luach Seven supplies new concrete evidence against the earlier D4-PATCH-005 implementation strategy. The original Luach Three explicitly instructs powers-of-two doubling/decomposition when the repetition count is large and states that the shorter route gives the same number.

The previous repair used C5.4 RepeatExactly for every count. Production RepeatExactly executes one occurrence per count. By visible drop 5, a Luach Seven stone reaches `147018724953112136513405003837173`; squaring through the previous route would therefore require on the order of 10^32 performances.

The repaired `לקחתפעמים` restores the source algorithm. `כפלרד` builds doubled value/count pairs recursively and unwind visits them largest-to-smallest; `כפלבחר`/`כפלהוסף` greedily consume the remaining count. The public act contract and Luach Four `רבוע` remain unchanged. This is a D4 source-repair correction, not a compiler/language change.
