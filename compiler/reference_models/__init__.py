"""Non-normative executable reference calculi.

Nothing in this package is part of the canonical language model.  These modules
exist so C can differentially test historical/spec-candidate semantics without
letting their implementation ontology constrain A/B or canonical HAST/IR.
"""

from .b4_candidate import REFERENCE_MODEL_STATUS, ReferenceRuntime

__all__ = ["REFERENCE_MODEL_STATUS", "ReferenceRuntime"]
