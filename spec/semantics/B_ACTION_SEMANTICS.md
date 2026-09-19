# B-Core v0.1 Act / Occurrence Semantics — A13

## Act
A described reusable computation identified by resolved ActId.

## Occurrence
Each performance creates a distinct semantic occurrence.

This distinction is required by `המעשה הזה` and occurrence-specific role values, not by a stack-frame
convention.

## Role identity
RoleId belongs to ActId and persists as source identity after declaration.

## Role association
During occurrence \(o\):

\[
Associated(o,\rho,n),\quad n\in\mathbb N.
\]

Each required role gets exactly one number by explicit named association.

No position and no mutable parameter cell.

Association values are pure and fixed for the occurrence.

## Nested/recursive performance
A nested occurrence may coexist with its caller occurrence.

Implementations may use stack/trampoline/CPS; none is observable language ontology.

## Output
One occurrence may produce zero or one Natural.

Production is nonterminal.

## Completion
Body exhaustion normally completes the occurrence.

Successful completion enables immediate result provenance for a direct performed act.

Error/divergence does not produce successful completion provenance.
