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
    "symbol":"01105e78babda15784fee8da618e56aa0aa1972e3428785b6ae0c01ff983efa8",
    "index":"3ff09c6d0c05ed43607b031f54a517206a9137c032ab507a375872bba53b9ef2",
    "large":"8a8d30bbe7c25356871663a55c5e8dc614469d9d95529605e18ab90a5d7b2cf7",
    "registry":"cef84d06ff6f3f1a9212e812ceb3a8326c3687f75d0c7da093ed782febdb28af",
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
