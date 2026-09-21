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
    "symbol":"e0cda7fc10d49186261002834cd418942e0ee1a76baca983625a90b61281874a",
    "index":"12faf39bcb597b69ebe4d88a29d3f2367f07d01d46f670ae07894a61db23be5e",
    "large":"9e109fa49b6f4cbf9f93d51252ed6fe9897880fc6b648c7c6dc6dac999bfefe9",
    "registry":"ea1174516e0f3955b697fe15db3f2436ea0fcc0795e083899df8fe7c8e5ac1d8",
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
