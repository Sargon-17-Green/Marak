# C M4.1 — E v0.8 Adversarial Remediation

Baseline: C M4 + A13 + B12.  No A13/B12 rule was changed.

M4.1 fixes E-FIND-021 through E-FIND-025:

- public semantic observations erase implementation serials and use source-semantic identity;
- root-marker diagnostics derive top-level `ועתה` positions from grammar context rather than raw token counts;
- language act recursion uses explicit implementation continuations in all three execution layers;
- decoded artifacts pass a shared, source-independent canonical-IR semantic validator;
- role-association target ownership is read only from target descriptor fields, never recursively from the NumberValue expression.

The language remains Marak Core v0.1 candidate.  Explicit continuation stacks, allocation serials and VM machinery are implementation details, not language ontology.
