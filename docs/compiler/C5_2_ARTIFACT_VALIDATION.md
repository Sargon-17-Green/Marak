# C5.2 Artifact Validation

C5.2 advances HAST, IR, and artifact schemas to `core-*-0.3-candidate-1`. The 0.3 verifier cleanly rejects 0.2 artifacts; no migration reader is provided.

The artifact trust boundary does not trust numeric identity serials or embedded labels by themselves. Every serialized Symbol Value must reference a declared domain and a member belonging to that domain, and its external label must exactly equal the canonical label in the member declaration metadata. A payload cannot pair a legitimate member identity with a forged display label.

Canonical IR validation independently verifies Symbol domain/member ownership, duplicate identity rejection, typed place/role/output contracts, same-domain Symbol equality, Index operation operand domains, Natural GT operand domains, and complete Symbol-order chains. Invalid payloads are rejected before execution.

Adversarial tests recompute a valid payload digest before calling the verifier, proving rejection occurs in semantic verification rather than by accidental hash failure. Covered attacks include forged labels, unknown members, cross-domain equality, malformed Index state, Natural-as-Index operand, Index-as-Natural-GT operand, unknown/self order edges, duplicate Symbol identities, and prior-schema artifacts.
