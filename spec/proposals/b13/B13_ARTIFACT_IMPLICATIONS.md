# B13 Canonical Artifact Implications

B13 defines only the semantic information that a canonical artifact must preserve. It does not choose a binary layout, text encoding, object representation, or ABI.

## Symbol
An artifact must preserve:
- Symbol-domain identity;
- member identity within that domain;
- canonical external label metadata;
- any explicitly admitted strict order/rank for the domain.

The external label alone is not a lossless serialization key because two separately declared members may have the same spelling. If a future public serialization format is standardized, it must preserve semantic domain/member identity or an equivalent unambiguous canonical identifier.

## BidirectionalIndex
An artifact must preserve exactly one of:
- BeforeZero with positive unbounded magnitude;
- Zero;
- AfterZero with positive unbounded magnitude.

Host sign bit, word size, and sign/magnitude implementation are not semantic.

## Finite ordered collection
An artifact must preserve:
- declared element domain;
- finite count;
- element order;
- each element's canonical semantic representation recursively.

Capacity, node/array layout, sharing, and allocation identity must not affect the artifact meaning.

## Ordering propositions
An artifact needs to preserve the resolved proposition/relation identity and operands sufficiently to recover the same satisfaction judgment. It need not store a Boolean result unless a particular execution artifact separately records outcomes.

## Counted recurrence
An executable artifact must preserve:
- the count description;
- the fact that it is determined once at recurrence entry;
- the identity/boundary of the single repeated admitted action;
- ordinary B12 error/divergence propagation.

No iterator/index object is required.

## Program Input Roles
A program artifact must preserve:
- ProgramInputId identity;
- owning program contract;
- declared value domain;
- required-binding status.

Invocation values are per-run data, not part of the reusable program artifact.

## Large Natural literals
An artifact must preserve the exact mathematical Natural denotation with no machine-word ceiling. Concrete digit/base encoding is a C/artifact-format decision so long as it is lossless and canonical under that format.

## Backward compatibility
Existing B12 artifact concepts remain valid Natural-specialized cases. B13 does not require rewriting B12 frozen source semantics.
