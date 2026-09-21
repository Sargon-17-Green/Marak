#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from spec.proposals.b16.reference.test_b16_semantics import B16SemanticTests

FROZEN_IDENTITY_RECEIPTS = {
    "test_01_registry_identity",
    "test_02_compiler_identity",
}
EXPECTED_SEMANTIC_TESTS = {
    name
    for name in dir(B16SemanticTests)
    if name.startswith("test_")
} - FROZEN_IDENTITY_RECEIPTS


def main() -> int:
    all_tests = {name for name in dir(B16SemanticTests) if name.startswith("test_")}
    if len(all_tests) != 30:
        raise SystemExit(f"unexpected B16 test inventory: {sorted(all_tests)}")
    if FROZEN_IDENTITY_RECEIPTS - all_tests:
        raise SystemExit("B16 frozen identity receipt inventory changed")
    if len(EXPECTED_SEMANTIC_TESTS) != 28:
        raise SystemExit("expected exactly 28 B16 semantic regressions")

    suite = unittest.TestSuite(
        B16SemanticTests(name)
        for name in sorted(EXPECTED_SEMANTIC_TESTS)
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1
    print("C5.6 B16 SEMANTIC REGRESSIONS: PASS (28 tests; 2 frozen identity receipts excluded)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
