# C M4.1 — Artifact Semantic Verifier

Artifact integrity is not canonical-IR validity. M4.1 adds a shared source-independent `validate_canonical_ir(program)` pass used both before artifact emission and after artifact decoding.

The pass validates preparation visibility/order, initializer contexts, role ownership, performance context, output path cardinality, recent-result context, static checked-Natural underflow and semantic kinds/control contexts.

It rejects all eight E-FIND-024 constructions: output outside performance, self initializer, two outputs on one path, recent result in initializer, static constant underflow, repeated output, forward initializer read and wrong-owner role read.

The verifier never invokes the source parser/resolver and remains an explicit tagged-data trust boundary; no pickle/eval is used.
