"""Emit fingerprints for human review. Never update the trust list automatically."""
from __future__ import annotations

from pathlib import Path
import hashlib
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from compiler.api import compile_source
from compiler.runtime.constructive_fingerprint_guard import structural_program_sha256
from tests.d4_t21_end_to_end_evidence import _production_source

CANDIDATE = ROOT / "megillah/candidates/Megilat_HaItim_Marak_Candidate.md"
CANDIDATE_SHA = "6fda03c4ca953898b471da666c048d81020f9bea4fcd240b94aab7bb3f091881"


def main() -> None:
    actual = hashlib.sha256(CANDIDATE.read_bytes()).hexdigest()
    if actual != CANDIDATE_SHA:
        raise AssertionError(f"refuse fingerprint: candidate SHA {actual}")
    for side in ("after", "before"):
        source = _production_source(side)
        c = compile_source(source)
        assert c.valid, [d.to_dict() for d in c.diagnostics]
        for kind, program in (("hast", c.hast), ("ir", c.ir)):
            print(f"CANONICAL_FINGERPRINT_V1 side={side} kind={kind} sha256={structural_program_sha256(program)} source_chars={len(source)}", flush=True)


if __name__ == "__main__":
    main()
