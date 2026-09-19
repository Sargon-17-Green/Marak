# C Validation Contract

Status: current through A13/B12.

Validation runs only after parse ambiguity has been eliminated and references have been resolved to typed identities.

Current Core checks include:

- Natural-only numeric domain;
- statically provable subtraction underflow => `SEM0201` with semantic code `ARITHMETIC_DOMAIN_ERROR`;
- zero-or-one output production per allowed performance path => `SEM0012`;
- semantic-kind preservation for propositions/actions/numbers;
- complete exact role-association profile;
- output only in a current performance;
- A13 whole-program structural constraints and source visibility constraints (handled at parser/resolver boundary with stable diagnostics).

Dynamic subtraction underflow remains a checked runtime error rather than being converted to a signed value, wrapped result or clipped zero.
