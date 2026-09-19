# B14 — A15 Semantic Integration Review

Status: **B14 INTEGRATION BLOCKED — A16 SURFACE REMEDIATION REQUIRED**

Baseline main: `621a656c25b7667640cc61a1d1a6ddef95db474d`
Reviewed B13: `3c47a57debd381c2b4e41d00d12c792ae43debe8`
Reviewed A15: `2ae820803250b0753834eff7275c9409426bd0ad`

## Review method

B14 did not trust A15's mapping table as proof. Each exact A15 construction was checked for a unique
semantic target, complete outcome/error behavior, and compositional use with frozen B12/A13 machinery.
A second audit tested cross-domain flow through places, replacement, act roles, act output,
immediate-result provenance, Program Input Roles, collection elements, equality, and observation.

## Result

The isolated A15 constructions map cleanly to B13+B12: no semantic mismatch was found. Integration is
nevertheless incomplete because A15 does not surface several B13 cross-domain capabilities needed by D.

Blocking A16 items:
- `B14-A-SURFACE-GAP-001` typed state-bearing places/replacement for Symbol, BidirectionalIndex, Collection;
- `B14-A-SURFACE-GAP-002` typed named-act roles for those domains;
- `B14-A-SURFACE-GAP-003` typed act output plus typed immediate-result reference;
- `B14-A-SURFACE-GAP-004` runtime BidirectionalIndex successor/predecessor;
- `B14-A-SURFACE-GAP-005` Symbol equality proposition.

Both Master candidate gaps are therefore real.

A13 freezes numeric-only `מקום`, named-act role, output, and immediate-result forms. A15 explicitly
generalizes Program Input Roles and Collection value forms, but does not add exact typed variants of
the other carriers. A15 itself defers mutable working state to "whatever integrated state-bearing
surface B14 accepts"; no such surface exists.

A15 also exposes year-profile Index literals/references while explicitly declining spellings for
B13 `succ`/`pred`. The Megillah's year-numbering section requires dynamic progression across
`שנת אין`, so literal constants are insufficient.

B14 rejects silent genericization by analogy. A numeric place does not become a polymorphic variable,
numeric output does not become a generic return, and year values do not become signed integers.

Do not hand this integration candidate to C. A16 must remediate the surface and return to B review.
