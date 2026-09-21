#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]

def run(path):
    p=subprocess.run([sys.executable,str(ROOT/path)],cwd=ROOT,capture_output=True,text=True)
    assert p.returncode==0, p.stdout+"\n"+p.stderr
    return p.stdout,p.stderr

def test_b13_reference_suite():
    out,err=run("spec/proposals/b13/reference/run_reference_tests.py")
    assert "B13 REFERENCE TESTS: PASS (28 tests)" in out+err

def test_b15_reference_suite():
    out,err=run("spec/proposals/b15/reference/run_b15_tests.py")
    assert "Ran 29 tests" in out+err
    assert "OK" in out+err

def test_a16_reference_suite():
    out,err=run("spec/proposals/a16/reference/run_a16_surface_tests.py")
    data=json.loads(out)
    assert data["status"]=="PASS"
    assert data["checks"]["total"]==2548
    assert data["checks"]["positive"]==2518
    assert data["checks"]["negative"]==30

def test_a17_proposal_suite():
    out,err=run("spec/proposals/a17/reference/run_a17_surface_tests.py")
    data=json.loads(out)
    assert data["status"]=="PASS"
    assert data["checks"]["total"]==4415
    assert data["checks"]["positive"]==4388
    assert data["checks"]["negative"]==27
