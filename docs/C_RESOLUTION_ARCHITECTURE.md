# C Resolution Architecture

Status: current through A13/B12.

Resolution consumes one unambiguous whole-program parse and produces canonical HAST with stable typed identities: `PlaceId`, `ActId`, `RoleId` (owned by an `ActId`). Runtime string lookup is forbidden.

A13 visibility is source-discourse introduced-before-use:

- a Place is visible only after its initialized introduction completes;
- an Act is visible after its introduction, allowing self-recursion in its later body;
- a Role is visible after declaration and belongs to one Act;
- no implicit forward reference/hoisting exists;
- mutual recursion is legal only through already introduced Act identities.

Same spelling across kinds is legal because namespaces preserve kind. Same-kind duplicates, duplicate bodies, duplicate roles within an Act, self-initializers and future references are rejected statically.

Role association resolves by explicit owner/name relation and then RoleId, never source position. Immediate result references are structurally tied to the directly preceding compatible performance; stale/wrong-act uses are rejected before execution.
