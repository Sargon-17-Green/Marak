#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]

jobs = [
    [sys.executable, "-m", "pytest", "-q", str(HERE / "test_b17_semantics.py")],
    [sys.executable, "-m", "pytest", "-q", str(HERE / "test_b17_production_compatibility.py")],
]

for command in jobs:
    proc = subprocess.run(command, cwd=ROOT, text=True)
    if proc.returncode:
        raise SystemExit(proc.returncode)

print("B17 REFERENCE TESTS: PASS")
