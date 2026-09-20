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
    "symbol":"bc9552106e17955b0f67d1187b3c83468ac78a2e283f3ffa5b20ca52c24a69f7",
    "index":"949721f698e5b491da4af1ae69ea309cd026aab27fbdb013e951e5978ef0c8d8",
    "large":"3dd3831f417f6404a909851fd330086e629f9b0286670ad6b98ef55ddbbc5426",
    "registry":"2e1d5a8d685ca0f52c9a657cfd20a0594465c4cc5fa344bf55693a169c9a0483",
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def test_c52_artifact_bytes_are_cross_host_canonical():
    cases={
        "symbol":symbol_flow_source(),
        "index":index_flow_source(),
        "large":large_numeral_source([10_000,999_999,1_000_000,14_777_149,99_999_999]),
    }
    for name,source in cases.items():
        c=compile_source(source)
        assert c.valid
        assert digest(c.artifact)==EXPECTED[name]


def test_current_registry_bytes_are_cross_host_canonical_lf():
    data=(ROOT/"spec"/"CURRENT_CONSTRUCTION_REGISTRY.json").read_bytes()
    assert b"\r\n" not in data
    assert data.endswith(b"\n")
    assert digest(data)==EXPECTED["registry"]
