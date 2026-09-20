from __future__ import annotations
from dataclasses import dataclass

SUPPORTED_WITH_EXACT_SURFACE="SUPPORTED_WITH_EXACT_SURFACE"
SEMANTICALLY_SUPPORTED_BUT_NO_SURFACE="SEMANTICALLY_SUPPORTED_BUT_NO_SURFACE"

DOMAINS=("Natural","Symbol","BidirectionalIndex","Collection")
CONTEXTS=("value","equality","state","replacement","act_role","act_output","immediate_result","program_input","collection_element","observation")

SURFACE={
    "Natural": {k:SUPPORTED_WITH_EXACT_SURFACE for k in CONTEXTS},
    "Symbol": {},
    "BidirectionalIndex": {},
    "Collection": {},
}
for d in ("Symbol","BidirectionalIndex","Collection"):
    for k in CONTEXTS:
        SURFACE[d][k]=SEMANTICALLY_SUPPORTED_BUT_NO_SURFACE
    for k in ("value","program_input","collection_element"):
        SURFACE[d][k]=SUPPORTED_WITH_EXACT_SURFACE

GAPS=(
    "B14-A-SURFACE-GAP-001",
    "B14-A-SURFACE-GAP-002",
    "B14-A-SURFACE-GAP-003",
    "B14-A-SURFACE-GAP-004",
    "B14-A-SURFACE-GAP-005",
)

class OutputCardinalityError(Exception):
    pass

class SurfaceDomainError(Exception):
    pass

def typed_membership(collection,item):
    if not collection.element_domain.accepts(item):
        raise SurfaceDomainError("VALUE_DOMAIN_MISMATCH")
    return collection.contains(item)

@dataclass
class Occurrence:
    produced: object|None=None
    has_output: bool=False
    def produce(self,value):
        if self.has_output:
            raise OutputCardinalityError("ZERO_OR_ONE_OUTPUT_PER_OCCURRENCE")
        self.produced=value
        self.has_output=True
