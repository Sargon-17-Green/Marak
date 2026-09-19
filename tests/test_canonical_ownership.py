import ast
import pathlib
import unittest

from compiler.models.hast import HastNode, HastProgram
from compiler.models.ir import IRNode, IRProgram


class CanonicalOwnershipTests(unittest.TestCase):
    def test_canonical_models_have_single_import_identity(self):
        from compiler.models import HastNode as H2, IRNode as I2
        self.assertIs(HastNode, H2)
        self.assertIs(IRNode, I2)

    def test_no_dynamic_source_file_imports_in_compiler(self):
        root = pathlib.Path(__file__).resolve().parents[1] / "compiler"
        offenders = []
        for path in root.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            if "spec_from_file_location" in text or "SourceFileLoader" in text:
                offenders.append(str(path.relative_to(root)))
        self.assertEqual(offenders, [])

    def test_hast_ir_classes_are_defined_only_in_models(self):
        root = pathlib.Path(__file__).resolve().parents[1] / "compiler"
        bad = []
        protected = {"HastNode", "HastProgram", "IRNode", "IRProgram"}
        for path in root.rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in tree.body:
                if isinstance(node, ast.ClassDef) and node.name in protected:
                    rel = path.relative_to(root).as_posix()
                    if rel not in {"models/hast.py", "models/ir.py"}:
                        bad.append((rel, node.name))
        self.assertEqual(bad, [])


if __name__ == "__main__":
    unittest.main()
