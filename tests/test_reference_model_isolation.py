from pathlib import Path
import ast
import unittest

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_DIRS = (
    ROOT / "compiler" / "models",
    ROOT / "compiler" / "parse",
    ROOT / "compiler" / "resolve",
    ROOT / "compiler" / "validate",
    ROOT / "compiler" / "optimize",
    ROOT / "compiler" / "backend",
    ROOT / "compiler" / "artifact",
    ROOT / "compiler" / "runtime",
)
CANONICAL_FILES = (ROOT / "compiler" / "api.py",)


def imports_reference_models(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    hits = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("compiler.reference_models"):
                    hits.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module.startswith("compiler.reference_models"):
                hits.append(module)
    return hits


class ReferenceModelIsolationTests(unittest.TestCase):
    def test_canonical_compiler_layers_do_not_import_reference_models(self):
        offenders = {}
        files = list(CANONICAL_FILES)
        for directory in CANONICAL_DIRS:
            files.extend(directory.rglob("*.py"))
        for path in files:
            hits = imports_reference_models(path)
            if hits:
                offenders[str(path.relative_to(ROOT))] = hits
        self.assertEqual(offenders, {})

    def test_reference_package_is_not_reexported_from_compiler_root(self):
        text = (ROOT / "compiler" / "__init__.py").read_text(encoding="utf-8")
        self.assertNotIn("reference_models", text)


    def test_new_canonical_hast_and_semantic_core_do_not_import_reference_models(self):
        root = Path(__file__).resolve().parents[1] / "compiler"
        for relative in ("hast", "semantic_core"):
            for path in (root / relative).rglob("*.py"):
                tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
                imported = []
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        imported.extend(alias.name for alias in node.names)
                    elif isinstance(node, ast.ImportFrom) and node.module:
                        imported.append(node.module)
                self.assertFalse(
                    any(name.startswith("compiler.reference_models") for name in imported),
                    f"{path} imports reference model",
                )


if __name__ == "__main__":
    unittest.main()
