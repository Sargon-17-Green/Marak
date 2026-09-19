# B12 Visibility, Identity, Lifetime, and Occurrence

## Static source identity

Runtime does not search names.

After C resolution, a reference is already a typed identity such as:

\[
PlaceRef(p),\quad ActRef(a),\quad RoleRef(\rho).
\]

The spelling that introduced the identity is not a runtime string value.

## Introduced-before-use

### Place
Becomes available only after its complete initialized introduction.

Lifetime for Core source reference:
from completed introduction through program completion.

### Act
Becomes available after its act introduction.

Its body may refer to itself because the ActId already exists.

Exactly one body is defined later before Principal.

### Role identity
Owned by one ActId.

Available after role declaration; declaration must follow owner introduction and precede owner body.

Role identity persists through the program discourse.

### Role-associated number
For performance occurrence \(o\):

\[
Associated(o,\rho,n).
\]

This relation exists only for that occurrence and remains fixed for as long as that occurrence is active.

After normal completion or fatal error, it is no longer available to later source evaluation. If the occurrence diverges, there is no later continuation in which expiration could be observed.

The RoleId itself remains the same identity throughout the program discourse.

## Mutual recursion

No hoisting is needed.

Valid conceptual order:

1. introduce Act A;
2. introduce Act B;
3. define body A referring to B;
4. define body B referring to A.

Invalid:
body A refers to B before B is introduced.

## Same spelling across kinds

Identity is not a global string key.

A PlaceId named X and ActId named X can coexist if A13's typed linguistic references keep them unique.

Duplicate same-kind introduction is invalid.

Role duplicate identity is checked within its owning act.

## Performance occurrence

Occurrence may be modeled abstractly as:

\[
o=(ActId,RoleAssociation,\text{output slot},\ldots)
\]

where the ellipsis is non-observable runtime support.

It is not automatically:
- a stack frame;
- a heap object;
- a user-visible identity.

Nested recursive occurrences of one ActId may simultaneously satisfy:

\[
Associated(o_1,\rho,5)
\]

and:

\[
Associated(o_2,\rho,3).
\]

The RoleId \(\rho\) is one identity; the associations are occurrence-specific.

## No Core local mutable state

A13 does not admit performance-owned mutable places in Core.

Any activation storage needed by stack/trampoline/CPS implementation is implementation-only.
