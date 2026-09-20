# C5.1 Typed Domain Infrastructure

Status: implementation tranche for the accepted Post-M2 A16/B15 domain flow; M2 Core semantics remain frozen.

## Domain model
The production compiler now represents four explicit semantic domains: `Natural`, `Symbol(SymbolDomainId)`, `BidirectionalIndex`, and recursive `Collection<ElementDomain>`. This is a small closed domain contract system, not a general-purpose inferred type system. There is no subtyping, implicit conversion, union, generic inference solver, or expected-type rescue.

The production HAST records explicit contracts for `PlaceId -> Domain`, `RoleId -> Domain`, `ActId -> None | Domain`, and `ProgramInputId -> Domain`. The validated IR carries the same contracts. A13/B12 resolution explicitly emits `Natural` contracts for all existing Core places, roles, and result-producing acts; no legacy construct relies on a consumer to infer Natural.

## Values and carriers
`NaturalValue`, `SymbolValue`, `BidirectionalIndexValue`, and immutable `CollectionValue` provide runtime-neutral value representations for post-M2 carrier tests. Natural arithmetic remains exact and unbounded. Symbol equality identity is domain/member based; visible labels are metadata. BidirectionalIndex is not a generic Integer. Collections are finite ordered homogeneous values and carry an explicit element domain.

Place initialization/replacement, named role association, act output, and immediate-result provenance now accept typed Value carriers while preserving the existing B12 commit/provenance rules. Runtime role associations remain occurrence-local and identity-based, never positional or aliasing caller state.

## Program Inputs
`ProgramInputId -> Domain` is represented in HAST/IR now. `validate_invocation()` validates missing, extra, duplicate, and wrong-domain bindings before Preparation. It deliberately defines no stdin/argv/HTTP/environment transport semantics.

## Surface scope
C5.1 does not land the complete A15/A16 grammar. Non-Natural end-to-end coverage uses canonical production HAST fixtures that enter the same lowering, IR, artifact verifier, reference execution, and portable backend as parsed programs. This proves production carrier architecture without inventing new surface syntax.
