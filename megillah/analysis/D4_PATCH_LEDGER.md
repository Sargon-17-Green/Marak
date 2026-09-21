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

## D4-PATCH-012 — Luach Seven / five stones

Original lines 269–319 define a deterministic table of 46 visible drops, each with five Natural stones. Drop 1 is `[17,29,43,71,101]`. Every later row is computed from a complete snapshot of the preceding five stones; no newly computed stone may feed another stone in the same row.

The candidate retains five old-state places, five new-state places, the current drop number, and `אבניטיפות` as a nested Natural Collection. Generic `חשבאבן` implements the common formula `שמור(square(base) + count*weighted + extra)`. `טיפההבאה` computes all five new places before any old place is replaced, appends one five-element book, then commits the new snapshot. `בנהאבנים` performs exactly 45 transitions after the initial row, reaching visible drop 46.

The source's permission to precompute the table once is retained as a lifecycle/documentation invariant; no day-dependent input is used in this table.

## D4-PATCH-013 — Luach Eight / seven hidden drops

Original lines 323–461 define seven hidden drops before visible drop 1. Each hidden drop has its own four coefficients over the question/distance/connection/way counters, also receives the action counter and all five stones from the visible drop with the same ordinal, then passes through `שמור`.

Each hidden drop is then ground exactly seven times. Every round uses the pre-square value, its square, three copies of the pre-square value, one stone, the round number, and `שמור`. The stone sequence is explicitly retained as wheat, barley, salt, bitter, red, wheat, barley.

The repair stores the seven final values both in named places and in `טיפותנסתרות`, ordered hidden7 through hidden1 so later predecessor selection can append visible drops and count backward without an inverted convention.

## D4-PATCH-014 — Luach Nine / 46 visible drops

The source defines one chronological predecessor chain containing hidden7..hidden1 followed by visible drops 1..46. For each visible drop, the first, third and seventh predecessors are taken without skipping, exactly as illustrated for drops 1–4.

`ראשיתטיפה` retains the five stone×counter contributions, predecessor weights 1/3/5, visible-drop number and final `שמור`. `טחןטיפה` spells all eleven coefficient tuples and their stone sequence explicitly. `עשהטיפהגלויה` selects predecessor positions from the retained history, and `בנהטיפות` performs exactly 46 complete drops, appending a drop only after all eleven rounds finish.

## D4-PATCH-015 — Luach Ten / six bowls and initial fills

The six bowl identities are retained by their source-assigned Natural numbers 1..6. Their current fills are stored in `מלאקערות` in bowl-identity order; later arrangements can reorder identities without changing the fills attached to those identities.

`חשבמלאקערה` implements the shared initial-fill formula. `אתחלקערות` supplies the exact six bowl-number/prime pairs 1/17, 2/19, 3/23, 4/29, 5/31 and 6/37 and builds the six-element fill book.

## D4-PATCH-016 — Luach Eleven / 720 bowl arrangements

The source's lexicographic order over the six permanent bowl numbers is exactly the block decomposition 120, 24, 6, 2, 1. The candidate implements this directly rather than materializing 720 books.

`חלק` supplies safe Natural quotient/remainder, `בחרקערה` selects the ordinal unused bowl, and `מצאמערכה` applies the five source block sizes then appends the remaining bowl. `מספרמערכה` implements `((n-1) mod 720)+1`. `מקוםקערה` returns arrangement position separately from permanent bowl identity.

## D4-PATCH-017 — Luach Twelve / pour the drop

Only arrangement positions 1–3 receive the three pour values. Bowl fill is looked up by the permanent bowl identity currently occupying that position, not by position index itself. The candidate returns the pours as a three-Natural book ordered by arrangement position.

## D4-PATCH-018 — Luach Thirteen / mix six bowls after each drop

`מלאישן` freezes all six identity-keyed fills before any new value is calculated. Six calculations walk the selected arrangement circularly; every one reads only that snapshot. Temporary `[bowl identity, new fill]` books are sorted by permanent identity and only then committed to `מלאקערות` together.

The 46-drop driver also retains `מערכתטיפהאחרונה` separately. This is required by Luach Fifteen: the successor bowl for later questions comes from the arrangement chosen by visible drop 46, not from an arrangement used by the twelve post-drop blends.
