# C M4.1 — Observation Quotient

M4 exposed allocator serials through functions labelled as B12 observables. M4.1 separates two interfaces.

Public/reference semantic observation uses source-semantic identity:

- facts: Place spelling + Natural value;
- products: Act spelling + Natural product;
- language Error/Divergence as defined by B12.

Allocation serials and occurrence counters are erased. Therefore alpha-renumbering caused by an unused earlier introduction does not change semantic observation.

White-box functions `*_debug_internal_state` retain serials for implementation tests. They are explicitly not language observations.

E v0.8 contains one stale ordinary assertion that calls `backend_observable` and expects occurrence serial renumbering to change it, despite that test's own title/comment and E-FIND-021 stating the opposite. C follows A13/B12 and the finding's normative expectation; E was not edited.
