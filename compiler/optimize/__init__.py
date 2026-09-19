"""Semantics-preserving optimizer boundary for Core v0.1.

M4 deliberately enables only an identity pass.  This is a real pass contract, not
an absent optimizer: it records that error timing, occurrence provenance,
source-defined sequencing and divergence must not be changed without a later
proved transformation.
"""
from __future__ import annotations

from dataclasses import dataclass
from compiler.models.ir import IRProgram

OPTIMIZER_VERSION = "core-optimizer-identity-0.1"

@dataclass(frozen=True, slots=True)
class OptimizationReport:
    optimizer_version: str
    passes: tuple[str, ...]


def optimize(program: IRProgram) -> tuple[IRProgram, OptimizationReport]:
    return program, OptimizationReport(OPTIMIZER_VERSION, ("identity-preserve-observables",))

__all__ = ["OPTIMIZER_VERSION", "OptimizationReport", "optimize"]
