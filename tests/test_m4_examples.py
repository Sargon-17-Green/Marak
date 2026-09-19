from __future__ import annotations

import json
import unittest
from pathlib import Path

from compiler.api import compile_source, run_source
from compiler.artifact.format import verify_artifact
from compiler.runtime.observables import backend_observable

ROOT = Path(__file__).resolve().parents[1]


class M4GeneralExampleTests(unittest.TestCase):
    def test_all_general_examples_compile_execute_and_match_committed_artifacts(self):
        rows = json.loads((ROOT / "examples/m4/EXPECTED_RESULTS.json").read_text(encoding="utf-8"))
        for row in rows:
            with self.subTest(source=row["source"]):
                source_path = ROOT / row["source"]
                artifact_path = ROOT / row["artifact"]
                text = source_path.read_text(encoding="utf-8")
                compiled = compile_source(text, file=row["source"])
                self.assertTrue(compiled.valid, [d.code for d in compiled.diagnostics])
                self.assertEqual(compiled.artifact, artifact_path.read_bytes())
                verify_artifact(compiled.artifact)
                outcome = run_source(text, file=row["source"], fuel=10000).outcome
                self.assertEqual(backend_observable(outcome), row["observable"])


if __name__ == "__main__":
    unittest.main()
