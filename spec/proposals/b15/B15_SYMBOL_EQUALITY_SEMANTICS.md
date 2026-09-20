# B15 Symbol Equality Semantics

A16 admits `SYMBOL_A הוא SYMBOL_B` only when both operands independently resolve to the same declared
Symbol domain D.

The proposition holds iff the B13 Symbol identities have equal DomainId and MemberId.
Within one D, this is MemberId identity.

Not compared:
- visible label words;
- source identifier spelling;
- declaration order;
- object identity;
- intern index;
- serialized representation.

Two different members may have the same visible label and are still unequal.

Cross-domain Symbol equality is statically invalid rather than a runtime false proposition. B13 can
mathematically distinguish/compare identities across domains, but rejecting an unrelated-domain source
comparison is an **acceptable surface narrowing** because no current Megillah need requires it.

The result is a proposition consumed directly by admitted control. It is not a Boolean runtime Value.
A16 does not create generic equality for Collection, Index, Text, or arbitrary Value.
