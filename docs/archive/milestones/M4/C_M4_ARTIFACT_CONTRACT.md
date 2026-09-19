# C M4 — Artifact Contract

Version: `core-artifact-0.1-candidate-1`.

The artifact is canonical UTF-8 JSON with explicit tags. It contains:

- artifact version;
- IR version;
- compatible language edition;
- SHA-256 of the canonical program payload;
- full canonical IR including source spans.

Serialization uses sorted keys and compact deterministic JSON. It contains no timestamp, random UUID, pickle or executable Python representation.

The verifier rejects unknown versions/tags, incompatible language edition, digest mismatch, wrong fields, duplicate/nonpositive identity serials, invalid semantic kinds, invalid role ownership/profile, unresolved Place/Act/Role references, negative Natural values, malformed sequence/conditional/recurrence nodes and subtraction operations lacking the defined domain-error code.

Because control is represented structurally rather than by raw jump targets, malformed branch-target checks are replaced by semantic-kind/tree-structure verification at this artifact level.
