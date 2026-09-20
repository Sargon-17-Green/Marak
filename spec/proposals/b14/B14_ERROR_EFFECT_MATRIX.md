# B14 Integrated Error / Effect Matrix

| Category | Case | Result/effect |
|---|---|---|
| InvalidProgram | malformed/zero/short Symbol label declaration | reject before execution |
| InvalidProgram | duplicate Symbol member identity | reject before execution |
| InvalidProgram | incomplete/cyclic/forked Symbol order used as order | reject before execution |
| InvalidProgram | malformed/nonpositive Index literal | reject before execution |
| InvalidProgram | statically known collection domain mismatch | reject before execution |
| InvalidProgram | malformed numeral or recurrence attachment | reject before execution |
| InvalidProgram | duplicate Program Input Role declaration | reject program |
| InvalidInvocation | missing input | MISSING_INPUT_BINDING; no Preparation |
| InvalidInvocation | extra input | EXTRA_INPUT_BINDING; no Preparation |
| InvalidInvocation | duplicate supplied input | DUPLICATE_INPUT_BINDING; no Preparation |
| InvalidInvocation | wrong input domain | INPUT_DOMAIN_MISMATCH; no Preparation |
| RuntimeError | Natural subtraction underflow | ARITHMETIC_DOMAIN_ERROR; frozen B12 boundary |
| RuntimeError | collection position outside 1..count | COLLECTION_POSITION_ERROR |
| RuntimeError | dynamic collection/domain mismatch surviving validation | COLLECTION_ELEMENT_DOMAIN_ERROR / VALUE_DOMAIN_MISMATCH |
| RuntimeError | invalid surviving order relation | ORDER_RELATION_ERROR |
| RuntimeError | recurrence count non-Natural | RECURRENCE_COUNT_DOMAIN_ERROR; no iteration |
| RuntimeError | BeforeZero Index→Natural | INDEX_TO_NATURAL_DOMAIN_ERROR |
| RuntimeError | second direct output in one occurrence | existing zero/one output failure |
| Divergence | repeated/named action diverges | no later iteration/continuation |
| Resource | implementation cannot realize exact value | RESOURCE_EXHAUSTION; never wrong value |

Pure B13 value computation completes before surrounding replacement commits. On failure, that
replacement does not commit; earlier completed effects remain. No whole-program rollback or host
exception semantics are introduced.
