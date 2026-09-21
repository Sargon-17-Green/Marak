# A17 — Megillah Need Boundary

A17 does not edit the Megillah and does not certify conformance. This document only separates evidence from language proposal.

| Need | Megillah proves? | B13 semantic support | A17 surface | Boundary |
|---|---|---|---|---|
| external values that preserve day chronology | YES | BidirectionalIndex | generic `מעלה` Program Input head/reference | proposed |
| distinguished reference day | YES (`יום היסוד`) | ZeroIndex | `מעלת היתד` | proposed |
| positions before/after the reference | YES | BeforeZero/AfterZero | counted `מעלות לפני/אחרי` | proposed |
| chronological strict order | YES | strict total order | `A לפני B` | proposed |
| retain/replace coordinate state | needed for composition | A16/B15 typed place | `המעלה אשר במקום...` carrier | proposed |
| pass coordinate through named act | needed for composition | A16/B15 role flow | generic `מעלה` role carrier | proposed |
| produce/read result | needed for composition | A16/B15 output/provenance | generic immediate-result head | proposed |
| move one coordinate toward another | source algorithm needs traversal | total succ/pred | `המעלה אשר אחר/לפני I` | proposed |
| exact distance | source explicitly says to count days | B13 distance exists | **NO direct distance primitive** | left to source algorithm |
| equality | not independently demanded as primitive | semantic identity exists | **NO equality surface** | derive control from strict order/step discipline where needed |
| convert Natural day number to chronology | source explicitly says number alone is insufficient | explicit conversion boundary exists | **NO conversion surface** | not a repair |
| generic Index collection | not shown at D4 frontier | Collection<Index> exists semantically | **NO new generic book kind** | insufficient evidence |
| Day/Date object | NO | not present | NONE | forbidden overreach |

## Why succ/pred but not distance

The Megillah says to count how many days pass between a day and the foundation. Directly surfacing B13 `distance` would collapse that described algorithm into one primitive. Exposing the already-existing one-step relation instead supplies only the minimum mechanics needed to write the count as Marak acts/state/recurrence.

B16 must independently judge this anti-imitation boundary.

## Day is evidence, not language ontology

The selected head is `מעלה`, not `יום`. `יום` remains ordinary domain discourse in the Megillah. A17 does not create a Day type, day literal, calendar object, or host-time bridge.

## D4-LANG-001 disposition proposed by A17

`SURFACE_PROPOSAL_READY_FOR_B16/MASTER_REVIEW`

A17 does not claim the finding semantically or production-implementation closed.
