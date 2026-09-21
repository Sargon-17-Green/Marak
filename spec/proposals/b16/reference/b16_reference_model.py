#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from spec.proposals.b13.reference.b13_reference_model import (
    BidirectionalIndex, Natural, INDEX_DOMAIN, ProgramContract, ProgramInputId,
    bind_invocation, from_math_index, index_lt,
)

INDEX_DOMAIN_KEY = "BidirectionalIndex"

class SourceProfile(Enum):
    YEAR="year"
    GENERAL="general"

@dataclass(frozen=True)
class ResolvedIndexSource:
    profile:SourceProfile
    value:BidirectionalIndex

def resolve_index(profile:SourceProfile,z:int)->ResolvedIndexSource:
    return ResolvedIndexSource(profile,from_math_index(z))

def lower_index(src:ResolvedIndexSource)->BidirectionalIndex:
    return src.value

def semantic_fingerprint(value:BidirectionalIndex):
    return (INDEX_DOMAIN_KEY,value.side.value,value.magnitude)

def synthesize_source(value:BidirectionalIndex,target_profile:Optional[SourceProfile]):
    if target_profile is None:
        raise ValueError("TARGET_PROFILE_REQUIRED")
    return ResolvedIndexSource(target_profile,value)

def classify_by_order(a:BidirectionalIndex,b:BidirectionalIndex)->str:
    # Models two nested proposition observations, not a first-class Boolean language Value.
    if index_lt(a,b):
        return "before"
    if index_lt(b,a):
        return "after"
    return "same"

def distance_by_language_primitives(a:BidirectionalIndex,b:BidirectionalIndex)->Natural:
    # Constructive witness for the A12 post-action recurrence boundary.
    current=a
    count=0
    if index_lt(a,b):
        while True:
            current=current.succ()
            count+=1
            # Positive stop proposition after the step. It becomes true exactly at target.
            if index_lt(b,current.succ()):
                return Natural(count)
    if index_lt(b,a):
        while True:
            current=current.pred()
            count+=1
            # Positive stop proposition after the step. It becomes true exactly at target.
            if index_lt(current.pred(),b):
                return Natural(count)
    return Natural(0)

LANGUAGE_LEVEL_INDEX_SURFACE=frozenset({
    "general_literal","origin","strict_order","succ","pred",
    "program_input_carrier","place_carrier","role_carrier","output_result_carrier",
})

DELIBERATELY_ABSENT_INDEX_SURFACE=frozenset({
    "distance","equality","natural_to_index","index_to_natural",
    "signed_add","signed_subtract","unary_minus","generic_index_collection","arbitrary_profile_noun",
})
