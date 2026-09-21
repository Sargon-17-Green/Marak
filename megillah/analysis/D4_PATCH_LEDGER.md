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
