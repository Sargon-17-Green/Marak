from __future__ import annotations
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

from compiler.artifact.format import verify_artifact
from compiler.cli.main import main
from compiler.version import ARTIFACT_FORMAT_VERSION, HAST_VERSION, IR_REFERENCE_VERSION, IR_VERSION, RUNTIME_BACKEND_VERSION
from tests.m4_support import tiny_source


class M4CliEndToEndTests(unittest.TestCase):
    def _source_file(self,td):
        p=Path(td)/"tiny.he.txt"; p.write_text(tiny_source(),encoding="utf-8"); return p

    def test_version_reports_all_dimensions(self):
        out=io.StringIO()
        with redirect_stdout(out): rc=main(["version"])
        self.assertEqual(rc,0); obj=json.loads(out.getvalue())
        self.assertEqual(obj["construction_registry_version"],"c5.5-a15-b13.1")
        self.assertEqual(obj["hast_contract_version"],HAST_VERSION)
        self.assertEqual(obj["ir_version"],IR_VERSION)
        self.assertEqual(obj["ir_reference_version"],IR_REFERENCE_VERSION)
        self.assertEqual(obj["artifact_format_version"],ARTIFACT_FORMAT_VERSION)
        self.assertEqual(obj["runtime_backend_version"],RUNTIME_BACKEND_VERSION)

    def test_check_tiny_rm(self):
        with tempfile.TemporaryDirectory() as td:
            p=self._source_file(td); out,err=io.StringIO(),io.StringIO()
            with redirect_stdout(out),redirect_stderr(err): rc=main(["check",str(p),"--json"])
            self.assertEqual(rc,0,err.getvalue()); self.assertEqual(json.loads(out.getvalue()),{"valid":True})

    def test_compile_tiny_rm_writes_verified_artifact(self):
        with tempfile.TemporaryDirectory() as td:
            p=self._source_file(td); a=Path(td)/"program.cbh-artifact.json"; out=io.StringIO(); err=io.StringIO()
            with redirect_stdout(out),redirect_stderr(err): rc=main(["compile",str(p),"-o",str(a)])
            self.assertEqual(rc,0,err.getvalue()); self.assertTrue(a.is_file())
            verify_artifact(a.read_bytes())
            meta=json.loads(out.getvalue()); self.assertEqual(Path(meta["artifact"]),a)

    def test_run_tiny_rm_reports_language_outcome_not_stdout_semantics(self):
        with tempfile.TemporaryDirectory() as td:
            p=self._source_file(td); out=io.StringIO(); err=io.StringIO()
            with redirect_stdout(out),redirect_stderr(err): rc=main(["run",str(p),"--json"])
            self.assertEqual(rc,0,err.getvalue()); obj=json.loads(out.getvalue())
            self.assertEqual(obj["outcome"],"Normal"); self.assertEqual(obj["facts"],[["גד",0],["עזר",0]])
            self.assertNotIn("stdout",obj)

    def test_explain_tiny_rm_exposes_program_ids_hast_ir_without_confidence(self):
        with tempfile.TemporaryDirectory() as td:
            p=self._source_file(td); out=io.StringIO()
            with redirect_stdout(out): rc=main(["explain","--all",str(p)])
            self.assertEqual(rc,0); obj=json.loads(out.getvalue())
            self.assertIn("registry",obj); self.assertIn("hast",obj); self.assertIn("validated_ir",obj)
            blob=json.dumps(obj,ensure_ascii=False)
            self.assertNotIn("confidence",blob.lower())
            self.assertIn("HastCoreProgram",blob); self.assertIn("IRProgram",blob)

if __name__ == '__main__': unittest.main()
