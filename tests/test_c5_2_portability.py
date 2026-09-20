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
    "symbol":"7862d3b43bcff13bf7f7fbd4c9390b38c8b8a3806a8bc785f0bbbd0c62d5249b",
    "index":"1f301398973e84ed327a48b31557d9eaaf62ed5ceb9dc4465abc44d412580e65",
    "large":"b4ddf822987986a044c0bb997c8b5e93af9d844d5ded21e230cfca617c781f19",
    "registry":"924bf2e4047bea13fadc42e4161018c5b15171773fc93ff7f8b6224f77f2f665",
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
