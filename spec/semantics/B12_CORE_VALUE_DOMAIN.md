# B12 Core Value Domain

## Normative Core numeric value

\[
Value_{numeric}^{Core}=\mathbb N=\{0,1,2,\ldots\}.
\]

Core v0.1 has:
- no negative literal;
- no automatic promotion to integers;
- no negative subtraction result;
- no host-width bound.

Natural values are semantically unbounded.

Implementation inability to represent a required Natural is `RESOURCE_EXHAUSTION`, never overflow
semantics.

## Propositions are not values

The existence of `אם` and exact equality does not add a Boolean member to the Core value universe.

\[
S\models P
\]

is a semantic judgment used by control.

## Names and identities are not values

Source names resolve to typed semantic identities:
- PlaceId;
- ActId;
- RoleId owned by ActId.

They are not runtime strings.

## Occurrences are not values

A performance occurrence is a semantic event/context used to interpret the current performance and
role associations.

It is not a stack-frame value visible to the program.

## Post-Core research

Signed integers and negative integer syntax are:

**OPEN_AFTER_M2 / POST_CORE_RESEARCH**

Earlier B2/B11 integer arithmetic can be retained only as research material outside normative
B-Core v0.1.
