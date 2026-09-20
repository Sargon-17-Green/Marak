# B15 Typed Role Semantics

A role declaration fixes `RoleDomain(a,r)=D` statically. It is independent of first performance,
caller state, associated value, or expected use.

For each performance occurrence o of act a, the source supplies named associations. Validation requires
every associated expression to have the exact declared role domain before the occurrence begins.

Execution establishes:
`Associated(o,r,v)` where `v in D`.

Properties inherited and preserved:
- association is immutable for o;
- association is named, never positional;
- no alias to caller state;
- no mutable parameter cell;
- RoleId belongs to ActId;
- same role spelling in a different act is a different semantic identity;
- current-role lookup uses the current occurrence plus statically resolved ActId/RoleId;
- no runtime spelling/name search.

## Recursive/nested occurrence

When an act recursively performs itself, the inner occurrence has a distinct association relation.
Inside the inner body, `המעשה הזה` denotes the inner occurrence. After inner completion, the outer
body resumes with its original association unchanged. Host stack identity is unobservable.

Wrong-domain association is rejected before performance starts; no partial occurrence is created.
