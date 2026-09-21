from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

HERE=Path(__file__).resolve()
A17=HERE.parents[1]
RUNNER=A17/"reference"/"run_a17_surface_tests.py"
RESULT=A17/"A17_TEST_RESULTS.json"

def test_a17_reference_suite_passes():
    p=subprocess.run([sys.executable,str(RUNNER)],capture_output=True,text=True)
    assert p.returncode==0, p.stdout+"\n"+p.stderr
    data=json.loads(RESULT.read_text(encoding="utf-8"))
    assert data["status"]=="PASS"
    assert data["checks"]["total"]==4415
    assert data["checks"]["negative"]==27
    assert data["failures"]==[]

def test_a17_scope_and_domain_guard():
    data=json.loads(RESULT.read_text(encoding="utf-8"))
    assert data["new_semantic_domains"]==[]
    assert data["production_files_changed"]==[]
    assert data["megillah_changed"] is False
    assert data["selected_profile"]=="מעלה / מעלת היתד"

def test_a17_baseline_is_exact():
    data=json.loads(RESULT.read_text(encoding="utf-8"))
    assert data["baseline"]=="e8f766889676b219f0abf5c9e4f08fad3034fa5b"
