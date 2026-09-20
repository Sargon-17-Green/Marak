from __future__ import annotations

import hashlib
from pathlib import Path

from compiler.api import compile_source
from tests.test_c5_2_surface_pipeline import (
    index_flow_source,
    large_numeral_source,
    symbol_flow_source,
)


ROOT=Path(__file__).resolve().parents[1]

EXPECTED={
    "symbol":"20467465dd6498bff8b99386e7653302eed66219910a9e000cd7e328939746d1",
    "index":"d598b9e95a170c54040f3e9f17e059ccbd18eea79e68f02cc55c7cbc7e1e817b",
    "large":"2968266401d094ef44ac5833ba935eda106fd06b1da8dac6b2beb22fc8066d36",
    "registry":"9e1c9aae709697b3a10f3b49f97cd38fa9374712cc6c2a26f95b1b41f237ff45",
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def test_c52_artifact_bytes_are_cross_host_canonical():
    cases={
        "symbol":symbol_flow_source(),
        "index":index_flow_source(),
        "large":large_numeral_source([10_000,999_999,1_000_000,14_777_149,99_999_999]),
    }
    actual={}
    for name,source in cases.items():
        c=compile_source(source)
        assert c.valid
        actual[name]=digest(c.artifact)
    assert actual=={name:EXPECTED[name] for name in cases}


def test_current_registry_bytes_are_cross_host_canonical_lf():
    data=(ROOT/"spec"/"CURRENT_CONSTRUCTION_REGISTRY.json").read_bytes()
    assert b"\r\n" not in data
    assert data.endswith(b"\n")
    assert digest(data)==EXPECTED["registry"]
