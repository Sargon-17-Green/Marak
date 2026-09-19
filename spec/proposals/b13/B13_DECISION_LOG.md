# B13 Decision Log

All entries are **PROPOSED** pending A/B integration review.

- `B-SYM-001` finite declared Symbol domains; equality by domain/member identity; no dynamic minting.
- `B-SYM-002` canonical label is observable rendering metadata, not source-name identity and not general Text.
- `B-IDX-001` BidirectionalIndex = BeforeZero/Zero/AfterZero, distinct from Natural.
- `B-IDX-002` Natural↔Index conversion is explicit; B12 Natural subtraction is unchanged.
- `B-COLL-001` immutable finite ordered homogeneous collections, recursively nestable.
- `B-COLL-002` positions are positive Naturals 1..count; otherwise `COLLECTION_POSITION_ERROR`.
- `B-COLL-003` ordering consumes an admitted strict total relation; nested collection order is lexicographic.
- `B-ORD-001` Natural LT/GT propositions with derived LE/GE; no Boolean value.
- `B-LIT-001` admitted direct numeral denotes exact unbounded Natural; no semantic ceiling.
- `B-REP-R06` exact counted recurrence fixes a Natural count once and repeats one admitted action.
- `B-INVOKE-001` named immutable Program Input Roles are bound by identity per invocation before Preparation.
- `B-VAL-POST-001` post-M2 state-bearing referents, roles, inputs, and zero/one outputs may declare semantic domains; B12 Natural behavior is preserved.
- `B-ERR-POST-001` B13 operations use stable semantic errors, never host exceptions as definitions.
- `B-OBS-002` Symbol, BidirectionalIndex, and Collection observations are representation-independent.
- `B-COMPAT-001` B13 is a conservative extension of B12.
