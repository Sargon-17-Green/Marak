# B16 Error / Effect Matrix

| Situation | Classification | Effect |
|---|---|---|
| malformed/mixed year-general literal phrase | InvalidProgram | no execution |
| bare/incomplete general head expected to be Index | InvalidProgram | no expected-type rescue |
| order operand not independently BidirectionalIndex | InvalidProgram where source-resolved; B13 mismatch fallback otherwise | pure; no write |
| succ/pred operand not BidirectionalIndex | InvalidProgram where source-resolved | pure; no write |
| generic Program Input receives non-Index | InvalidInvocation `INPUT_DOMAIN_MISMATCH` | Preparation does not start |
| cross-profile Index input/carrier | valid | same semantic Value |
| cross-profile place/role/output/result | valid | same B15 effects/provenance |
| runtime profile mismatch | **does not exist** | no profile tag/domain exists |
| Natural subtraction below zero | existing `ARITHMETIC_DOMAIN_ERROR` | never creates BeforeZero |
| explicit B13 conversion of BeforeZero to Natural | existing `INDEX_TO_NATURAL_DOMAIN_ERROR` where conversion exists semantically | A17 adds no source form |
| resource failure on exact Value | `RESOURCE_EXHAUSTION` | no substitution/truncation |

There is no new transaction, rollback, profile-conversion, or unit-coercion effect.
