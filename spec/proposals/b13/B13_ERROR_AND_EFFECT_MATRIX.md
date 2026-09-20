# B13 Error and Effect Matrix

| Situation | Classification | Effect rule |
|---|---|---|
| B12 Natural subtraction underflow | static InvalidProgram if proved; else RuntimeError `ARITHMETIC_DOMAIN_ERROR` | unchanged B12 rule |
| ordering proposition wrong domain | `VALUE_DOMAIN_MISMATCH` if not statically rejected | pure; no write |
| undeclared/dynamically minted Symbol | InvalidProgram / invalid artifact | no execution |
| Symbol from wrong domain | `VALUE_DOMAIN_MISMATCH` | pure; no write |
| BeforeZero Index converted to Natural | `INDEX_TO_NATURAL_DOMAIN_ERROR` | pure; no write |
| collection element wrong domain | `COLLECTION_ELEMENT_DOMAIN_ERROR` | immutable construction fails; no partial value |
| collection position outside 1..count | `COLLECTION_POSITION_ERROR` | pure; no write |
| ordering relation not admitted as strict total | static rejection where provable; else `ORDER_RELATION_ERROR` | no ordered replacement value produced |
| counted recurrence count non-Natural | `RECURRENCE_COUNT_DOMAIN_ERROR` | no iteration begins |
| counted recurrence body errors at k | propagated RuntimeError | prior completed iterations remain; later ones absent |
| counted recurrence body diverges | Divergence | no later iteration |
| missing program input | InvalidInvocation `MISSING_INPUT_BINDING` | Preparation does not start |
| extra program input | InvalidInvocation `EXTRA_INPUT_BINDING` | Preparation does not start |
| duplicate program input | InvalidInvocation `DUPLICATE_INPUT_BINDING` | Preparation does not start |
| input wrong domain | InvalidInvocation `INPUT_DOMAIN_MISMATCH` | Preparation does not start |
| exact value/collection exceeds implementation resources | `RESOURCE_EXHAUSTION` | never substitute an incorrect value |

## Shared effect law
Every new pure B13 value computation completes before a surrounding state replacement commits. If it fails, that replacement does not happen; effects of already completed actions are retained; later explicit continuation is not entered. No new implicit transaction is introduced.

## Host failures
Python/C/JS exceptions, container bounds faults, encoding exceptions, or allocator details are not semantic definitions. Implementations must map to a defined category or are defective.
