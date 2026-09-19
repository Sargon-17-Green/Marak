# C M4 — Visibility and Resolution

Resolution is static and produces stable typed identities:

- `PlaceId`
- `ActId`
- `RoleId(owner=ActId)`

Names are never looked up by runtime strings after resolution. Place and Act may share spelling because namespaces preserve semantic kind.

## Visibility

- Place becomes visible only after its initialized introduction completes.
- Act becomes visible at its act introduction, so self-recursion in a later body is legal.
- Role becomes visible after its declaration and belongs to one Act.
- No implicit forward reference or hoisting is admitted.
- Mutual recursion is legal only when both Act identities were introduced before the referring bodies.

## Static rejections

The resolver rejects references before introduction, duplicate Place/Act identity, duplicate Role within one Act, duplicate body, self-initializer, role-owner errors, role use outside owning occurrence, incomplete/duplicate role association profiles, stale recent-result references and wrong-act recent-result references.

Body opener/closer co-reference remains exact; there is no nearest-body heuristic.
