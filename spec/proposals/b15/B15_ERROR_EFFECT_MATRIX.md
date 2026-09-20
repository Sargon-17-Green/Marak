# B15 Error and Effect Matrix

| Situation | Classification | Effect |
|---|---|---|
| unresolved/ambiguous initializer domain | InvalidProgram | no execution |
| structurally inconsistent/wrong place initialization domain | InvalidProgram | no place established |
| initializer runtime error | RuntimeError propagated from expression | no place established by that unit; prior completed Preparation effects remain |
| initializer divergence | Divergence | no completed place establishment |
| replacement domain mismatch | InvalidProgram | RHS need not execute; destination unchanged |
| replacement RHS runtime error | RuntimeError propagated | destination unchanged; prior effects retained; later continuation absent |
| role association domain mismatch | InvalidProgram | occurrence does not begin |
| wrong ActId/RoleId association | InvalidProgram | occurrence does not begin |
| mixed output-site domains | InvalidProgram(`MIXED_OUTPUT_DOMAINS`) | no execution |
| unresolved output-site domain | InvalidProgram | no execution |
| second reached output in one occurrence | existing output-cardinality RuntimeError / invalid occurrence | first completed output effect retained according to B12; later continuation stops on fatal error |
| wrong immediate-result typed head | InvalidProgram | no execution |
| structurally stale immediate reference | InvalidProgram | no historical lookup |
| immediate reference after runtime no-output path | RuntimeError `RESULT_PROVENANCE_ERROR` | prior completed effects retained |
| stale/invalid artifact runtime fallback | RuntimeError `RESULT_PROVENANCE_ERROR` | no stale value supplied |
| succ/pred operand not BidirectionalIndex | InvalidProgram | no evaluation as Index step |
| cross-domain Symbol equality | InvalidProgram | proposition not evaluated |
| implementation cannot realize exact value | `RESOURCE_EXHAUSTION` | never substitute/truncate |

Statically known domain mismatches are rejected statically. New domain computations are pure unless an
explicit state replacement commits. No new transaction or rollback model is introduced.
