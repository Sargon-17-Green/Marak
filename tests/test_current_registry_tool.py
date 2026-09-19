import json
from pathlib import Path
import subprocess
import sys
import unittest

from compiler.parse.a3_registry import A3_REGISTRY
from compiler.parse.a8_registry import A8_REGISTRY
from compiler.parse.a9_registry import A9_REGISTRY
from compiler.parse.a10_registry import A10_REGISTRY
from compiler.parse.a11_registry import A11_REGISTRY
from compiler.parse.a12_registry import A12_REGISTRY
from compiler.parse.current_registry import CURRENT_REGISTRY

ROOT = Path(__file__).resolve().parents[1]


class CurrentRegistryToolTests(unittest.TestCase):
    def test_dump_current_registry_targets_current_file_and_preserves_a3_snapshot(self):
        historical = {
            "A3_CONSTRUCTION_REGISTRY.json": A3_REGISTRY,
            "A8_CONSTRUCTION_REGISTRY.json": A8_REGISTRY,
            "A9_CONSTRUCTION_REGISTRY.json": A9_REGISTRY,
            "A10_CONSTRUCTION_REGISTRY.json": A10_REGISTRY,
            "A11_CONSTRUCTION_REGISTRY.json": A11_REGISTRY,
            "A12_CONSTRUCTION_REGISTRY.json": A12_REGISTRY,
        }
        before = {name: (ROOT / "spec" / name).read_bytes() for name in historical}
        cp = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "dump_current_registry.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertTrue(cp.stdout.strip().endswith("spec/CURRENT_CONSTRUCTION_REGISTRY.json"))
        for name, registry in historical.items():
            path = ROOT / "spec" / name
            self.assertEqual(path.read_bytes(), before[name])
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), registry.to_dict())
        current = json.loads((ROOT / "spec" / "CURRENT_CONSTRUCTION_REGISTRY.json").read_text(encoding="utf-8"))
        self.assertEqual(current, CURRENT_REGISTRY.to_dict())


if __name__ == "__main__":
    unittest.main()
