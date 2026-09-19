# C M4 — Runtime Error Mapping

Core execution outcomes are `Normal`, `Error` or `Divergence`. Fuel exhaustion is a test-harness representation of divergence and is not a language error.

Defined runtime semantic errors currently include:

| Code | Meaning | Effect boundary |
|---|---|---|
| `ARITHMETIC_DOMAIN_ERROR` | dynamic Natural subtraction would require a negative result | RHS fails before destination commit; previous completed effects remain; later sequence actions do not run |
| `RESULT_PROVENANCE_ERROR` | structurally valid immediate result reference observes a completed occurrence that produced no output | no invented default/global last result |
| `ROLE_VALUE_OUTSIDE_PERFORMANCE` | defensive runtime fallback for malformed IR/context | valid source is rejected earlier |
| `CORE_OUTPUT_CARDINALITY_ERROR` | defensive runtime fallback for more than one output production | valid source is rejected statically |

Host exceptions are not Core semantics. Public source execution passes through validation/artifact verification and maps execution failures into the defined outcome records. Debug/internal causes remain tooling metadata only.
