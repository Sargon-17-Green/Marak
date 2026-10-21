# D4 Post-C5.6 — Luach Two Audit / Repair Contract

Status: analysis-only; no candidate source change in this document.

## Source span

Canonical original lines 77–117, candidate lines 53–93 before repair.

## Executable requirements

### Two day inputs

Original lines 79–87 require two independently supplied days:

- first day -> `יום המעשה`;
- second day -> `היום אשר עליו תשאל`.

Post-C5.6 mapping:

- Program Input role `יוםמעשה` : general `BidirectionalIndex`;
- Program Input role `יוםשאלה` : general `BidirectionalIndex`.

This uses the existing C5.6 general `מעלה` profile. No Day/Date domain is introduced.

### Natural day numbers

`מספר המעשה` and `מספר השאלה` are not Index values. They are Naturals computed by the already-repaired named act `מספריום`.

This preserves the original law that chronological order is not inferred from the Natural day-number values.

### Inclusive distance

Original lines 91–103 define:

`distance = |question_index - calculation_index| + 1`.

The source requires counting days, including both endpoints, with same-day -> 1.

Repair boundary:

- no direct Index distance surface;
- no Index equality surface;
- classify direction using strict Index order twice;
- same-position is the trichotomy remainder;
- step with successor/predecessor one position at a time;
- Natural counter begins at one and increments once per step until the target coordinate is reached.

This is the same semantic boundary proven adequate by B16, but the source-level repair must remain its own Megillah algorithm rather than importing a distance primitive.

### Connection number

Original line 105:

`מספר החיבור = מספר המעשה + מספר השאלה`.

Repair must invoke the existing named act `חיבור`; no duplicate arithmetic abstraction is introduced.

### Way number

Original lines 107–115 define:

- question before calculation -> 1;
- same coordinate -> 2;
- question after calculation -> 3.

Repair uses only strict Index order and the binary alternative:

1. if QUESTION < CALC -> 1;
2. else if CALC < QUESTION -> 3;
3. else -> 2.

No first-class Boolean or Index equality value is introduced.

## Documentary/example material

- headings are organizational and may be externalized with provenance;
- lines 97–101 are worked examples validating inclusive distance and should become regression cases;
- line 117 is a semantic invariant explaining that distance and way are distinct Naturals with different meanings. Preserve it in documentation/tests, not as a runtime action.

## Anti-imitation check

- no positional arguments: Program Inputs and act roles remain explicitly named;
- no hidden `abs`, `while`, integer conversion, tuple, Date, or enum;
- no source order as execution order where observable order matters;
- no equality primitive invented for same-position;
- no direct distance primitive despite B13/B16 mathematical reference operation.

Classification: `COMPUTATION-DERIVED + LANGUAGE-DERIVED`.

## Gate to candidate repair

Candidate mutation for this tranche is permitted only after T03 focused verification proves that `מספריום` compiles and matches the historical -3..+3 examples in HAST/IR/backend execution.

