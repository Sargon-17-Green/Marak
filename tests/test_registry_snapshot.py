import json
import unittest
from pathlib import Path

from compiler.parse.a0_registry import A0_REGISTRY
from compiler.parse.grammar import ConstructionKind, SpecStatus


ROOT = Path(__file__).resolve().parents[1]


class A0RegistrySnapshotTests(unittest.TestCase):
    def test_no_positive_normative_construction_is_silently_created(self):
        self.assertEqual(A0_REGISTRY.admitted_root_productions, ())
        positives = [d for d in A0_REGISTRY.declarations if d.kind is ConstructionKind.POSITIVE]
        self.assertTrue(positives)
        self.assertTrue(all(d.status is SpecStatus.PROPOSED for d in positives))

    def test_normative_negative_rules_are_inspectable_not_executable_productions(self):
        obj = A0_REGISTRY.to_dict()
        ids = {d["construction_id"]: d for d in obj["declarations"]}
        self.assertEqual(ids["A0.BARE_WAW_NOT_SEQUENCE"]["status"], "normative")
        self.assertEqual(ids["A0.BARE_WAW_NOT_SEQUENCE"]["kind"], "negative")
        self.assertEqual(obj["productions"], [])

    def test_committed_registry_snapshot_matches_code_exactly(self):
        disk = json.loads((ROOT / "spec" / "A0_CONSTRUCTION_REGISTRY.json").read_text(encoding="utf-8"))
        self.assertEqual(disk, A0_REGISTRY.to_dict())


if __name__ == "__main__":
    unittest.main()

class A3RegistrySnapshotTests(unittest.TestCase):
    def test_current_a3_registry_snapshot_matches_code_exactly(self):
        from compiler.parse.a3_registry import A3_REGISTRY
        disk = json.loads((ROOT / "spec" / "A3_CONSTRUCTION_REGISTRY.json").read_text(encoding="utf-8"))
        self.assertEqual(disk, A3_REGISTRY.to_dict())
