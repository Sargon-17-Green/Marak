# C M4.1 — Anti-Imitation Delta

| Component | Classification | Reason |
|---|---|---|
| explicit continuation/work stack | IMPLEMENTATION-ONLY | removes host recursion dependence; not user-visible stack-frame semantics |
| target role descriptor vs NumberValue | LANGUAGE/SEMANTICS-DERIVED | preserves A13 named correspondence and B12 caller-context evaluation |
| semantic observation quotient | SEMANTICS-DERIVED | B12 excludes allocation IDs/counters from observation |
| canonical-IR semantic verifier | SEMANTICS-DERIVED implementation boundary | enforces already-fixed A13/B12 invariants; does not invent VM-language rules |
| root diagnostic grammar analysis | LANGUAGE-DERIVED | `ועתה` meaning depends on its A13 grammatical role, not token spelling alone |

No Function/Parameter/Return/While/BooleanValue language ontology was introduced. `הוצא` remains nonterminating product production, propositions remain non-values, and roles remain identity-based rather than positional.
