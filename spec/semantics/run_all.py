#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys

ROOT=Path(__file__).resolve().parent
FIX=ROOT/"fixtures"
B11=ROOT/"regression"/"b11_original"

jobs=[
    ("B11_ORIGINAL", [sys.executable,"test_b11_integrated_suite.py"], B11),
    ("B11_INTENT_UNDER_B12", [sys.executable,"test_b11_regression_under_b12.py"], FIX),
    ("B12_SEMANTICS", [sys.executable,"test_b12_semantics.py"], FIX),
    ("B12_RM", [sys.executable,"test_b12_rm_witness.py"], FIX),
]
for name,cmd,cwd in jobs:
    p=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True)
    print(f"=== {name} ===")
    print(p.stdout,end="")
    if p.stderr:
        print(p.stderr,file=sys.stderr,end="")
    if p.returncode:
        raise SystemExit(p.returncode)
print("B12 RUN_ALL: PASS")
