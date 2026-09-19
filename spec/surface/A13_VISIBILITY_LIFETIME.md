# A13_VISIBILITY_LIFETIME.md

Status: NORMATIVE Core v0.1 integration closure

Core visibility is discourse introduction-before-use.

- Place: visible after complete initialized introduction through program completion; no self-reference
  from its own initializer.
- Act: visible after `יהי מעשה ושמו X`; exactly one body later, before `ועתה`.
- Role: owner act must already exist; declaration precedes owner's body; identity remains available.
- Associated role number: exists only during the corresponding performance occurrence.
- Result provenance: retains A12's immediate post-performance lifetime.

No hoisting or implicit forward declaration exists.

Direct self-reference is legal because the act identity is introduced before its body. Mutual
recursion is legal when all participating identities are introduced before bodies that refer to them.

Invalid: duplicate place name, duplicate act name, duplicate role within one owner, duplicate body.
Same spelling across explicitly typed kinds can remain legal when complete references stay unique.

Frozen Core bodies do not introduce new places/acts/roles, so A13 creates no generic nested block-scope
system.
