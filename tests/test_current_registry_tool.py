import json
from pathlib import Path
import subprocess
import sys
import unittest

from compiler.parse.a0_registry import A0_REGISTRY
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
        current_path = ROOT / "spec" / "CURRENT_CONSTRUCTION_REGISTRY.json"
        current_before = current_path.read_bytes()
        cp = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "dump_current_registry.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        reported_path = Path(cp.stdout.strip())
        self.assertEqual(reported_path.resolve(), current_path.resolve())
        for name, registry in historical.items():
            path = ROOT / "spec" / name
            self.assertEqual(path.read_bytes(), before[name])
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), registry.to_dict())
        current_bytes = current_path.read_bytes()
        self.assertEqual(current_bytes, current_before)
        self.assertNotIn(b"\r\n", current_bytes)
        self.assertTrue(current_bytes.endswith(b"\n"))
        self.assertEqual(json.loads(current_bytes.decode("utf-8")), CURRENT_REGISTRY.to_dict())

    def test_dump_a0_registry_is_byte_stable_utf8_lf(self):
        registry_path = ROOT / "spec" / "A0_CONSTRUCTION_REGISTRY.json"
        before = registry_path.read_bytes()
        cp = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "dump_construction_registry.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        reported_path = Path(cp.stdout.strip())
        self.assertEqual(reported_path.resolve(), registry_path.resolve())
        after = registry_path.read_bytes()
        self.assertEqual(after, before)
        self.assertNotIn(b"\r\n", after)
        self.assertTrue(after.endswith(b"\n"))
        self.assertEqual(json.loads(after.decode("utf-8")), A0_REGISTRY.to_dict())


if __name__ == "__main__":
    unittest.main()
