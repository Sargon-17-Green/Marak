import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

from compiler.cli.main import main


class CliTests(unittest.TestCase):
    def test_version_is_separate_dimensions(self):
        out = io.StringIO()
        with redirect_stdout(out):
            rc = main(["version"])
        self.assertEqual(rc, 0)
        obj = json.loads(out.getvalue())
        self.assertIn("compiler_version", obj)
        self.assertIn("language_edition", obj)
        self.assertIn("ir_version", obj)
        self.assertIn("artifact_format_version", obj)
        self.assertIn("construction_registry_version", obj)
        self.assertEqual(obj["construction_registry_version"], "a13-b12.1")

    def test_check_rejects_source_that_cannot_complete_current_normative_shell(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "x.md"
            p.write_text("עשה דבר", encoding="utf-8")
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                rc = main(["check", str(p)])
            self.assertEqual(rc, 1)
            self.assertIn("PARSE0002", err.getvalue())


    def test_superseded_mitzvah_action_surface_is_not_admitted(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "x.md"
            p.write_text("עשה את המצוה אשר שמה ראובן", encoding="utf-8")
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                rc = main(["check", str(p)])
            self.assertEqual(rc, 1)
            self.assertIn("PARSE0002", err.getvalue())
            self.assertNotIn("SEM0001", err.getvalue())

    def test_explain_shows_normalized_tokens_without_confidence_scores(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "x.md"
            p.write_text("**אב** 😀 גד", encoding="utf-8")
            out = io.StringIO()
            with redirect_stdout(out):
                rc = main(["explain", str(p)])
            self.assertEqual(rc, 1)
            obj = json.loads(out.getvalue())
            self.assertEqual(obj["normalized_source"], "אב גד")
            self.assertNotIn("confidence", json.dumps(obj, ensure_ascii=False))

    def test_explain_parse_level_shows_registry_and_parser_metrics(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "x.md"
            p.write_text("עשה דבר", encoding="utf-8")
            out = io.StringIO()
            with redirect_stdout(out):
                rc = main(["explain", "--parse", str(p)])
            self.assertEqual(rc, 1)
            obj = json.loads(out.getvalue())
            self.assertIn("registry", obj)
            self.assertIn("parse", obj)
            self.assertTrue(obj["parse"]["grammar_available"])
            self.assertEqual(obj["parse"]["metrics"]["alternatives"], 0)


if __name__ == "__main__":
    unittest.main()
