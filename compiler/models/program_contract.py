"""Canonical reusable-program identity for Program Input ownership.

The fingerprint is derived from source-independent IR semantics. Source spans
and the ProgramInputId.program_contract field itself are excluded, avoiding
both charter sensitivity and circular self-hashing.
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
from dataclasses import fields

from compiler.models.domains import ProgramInputId
from compiler.source.source_map import OriginalSpan

PREFIX = "marak-ir-contract-sha256:"


def _semantic_obj(value):
    if isinstance(value, ProgramInputId):
        return {"tag":"ProgramInputId","serial":value.serial,"spelling":value.spelling}
    if isinstance(value, tuple):
        return [_semantic_obj(x) for x in value]
    if dataclasses.is_dataclass(value):
        out={"tag":type(value).__name__}
        for field in fields(value):
            if field.name=="source_span":
                continue
            item=getattr(value,field.name)
            if isinstance(item,OriginalSpan):
                continue
            out[field.name]=_semantic_obj(item)
        return out
    if value is None or isinstance(value,(str,int,bool)):
        return value
    raise TypeError(f"unsupported program-contract material {type(value).__name__}")


def ir_program_contract_id(program) -> str:
    data=json.dumps(_semantic_obj(program),ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False).encode("utf-8")
    return PREFIX+hashlib.sha256(data).hexdigest()


def reowner_program_inputs(value, owner: str):
    if isinstance(value, ProgramInputId):
        return ProgramInputId(value.serial,value.spelling,owner)
    if isinstance(value, tuple):
        return tuple(reowner_program_inputs(x,owner) for x in value)
    if dataclasses.is_dataclass(value):
        changes={}
        for field in fields(value):
            item=getattr(value,field.name)
            if isinstance(item,OriginalSpan):
                continue
            new=reowner_program_inputs(item,owner)
            if new is not item and new!=item:
                changes[field.name]=new
        return dataclasses.replace(value,**changes) if changes else value
    return value


__all__=["PREFIX","ir_program_contract_id","reowner_program_inputs"]
