# B13 Backward Compatibility

## Conservative-extension claim
For every valid A13/B12 program P that uses no B13-only construction:

`Observe_B13(P) = Observe_B12(P)`.

## Preserved semantics
- Natural remains exact and unbounded.
- Natural subtraction underflow remains `ARITHMETIC_DOMAIN_ERROR`.
- propositions remain non-Boolean semantic judgments.
- B12 act roles remain occurrence-specific immutable Natural associations.
- output remains nonterminal and zero/one per occurrence.
- no implicit dereference or runtime name search appears.
- Preparation/Principal and normal exhaustion remain unchanged.
- trace/internal identities remain unobservable.

## Domain extension, not reinterpretation
A B12 place/role/output is a Natural-specialized instance of the post-M2 declared-domain model. No Natural is automatically a BidirectionalIndex; no source name automatically becomes a Symbol; no B12 recurrence changes checkpoint or count behavior.

## Invocation
B12 programs declare zero Program Input Roles, so their required association set is empty and Preparation starts exactly as before.

## Verification requirement
Run `spec/semantics/run_all.py` unchanged together with B13 property/reference tests. B13 acceptance fails if the frozen B12 suite changes without an explicitly approved normative reason.
