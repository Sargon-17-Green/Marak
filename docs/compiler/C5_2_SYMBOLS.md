# C5.2 Symbols

C5.2 implements the accepted A15/A16 finite Symbol surface in the production compiler. The source pipeline now declares Symbol domains and members, records counted canonical external labels, resolves exact domain-qualified Symbol values, and carries Symbol domains through places, named act roles, outputs, immediate results, and equality propositions.

## Identity and observation

Runtime Symbol identity is the pair `SymbolDomainId + SymbolMemberId`. Source spelling, declaration order, intern serials, and the visible label are not semantic identity. Different members may therefore have identical visible labels. Normal observation exposes only the canonical external label; implementation/source identities are available only through explicitly debug-marked `marak explain` fields.

Counted labels are declaration metadata, not Text values. `CountedLabelTerminal` consumes one admitted positive direct Natural count, the fixed label marker, and exactly that many normalized Hebrew words. It does not use punctuation, Markdown, line boundaries, quotation marks, or maqaf semantics as a boundary.

## Typed carriers

Symbol places, named roles, result production, and immediate result reads carry one exact `Symbol(D)` domain. Wrong-domain replacements, role associations, typed heads, output sites, or equality operands are invalid before execution whenever source resolution makes the mismatch knowable. Occurrence-local role storage remains the existing B12 model; recursive/nested performances have independent role bindings.

`output` remains nonterminal: the reference evaluator, IR evaluator, and portable backend all continue with later body actions after the output event. Immediate-result provenance remains structural and retains the B12 runtime `RESULT_PROVENANCE_ERROR` fallback for dynamically legal no-output paths.

## Equality and order

Symbol equality is a separately typed proposition. It compares validated member identity inside one declared domain and never compares external labels. Cross-domain Symbol equality is static invalid, not false.

Explicit adjacent-order declarations are preparatory metadata. If a domain has an order profile, validation requires exactly one complete chain over every member: no cycle, fork, merge, missing member, duplicate edge, disconnected component, self-edge, or inferred declaration/spelling/label order. C5.2 stores the adjacency metadata and validates the induced total order but introduces no comparator value/action and no Collection operation.
