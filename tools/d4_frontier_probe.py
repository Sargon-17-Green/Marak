from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import asdict
from pathlib import Path

from compiler.api import compile_source
from compiler.normalize.code import normalize_code

if hasattr(sys.stdout, "reconfigure"):\n    sys.stdout.reconfigure(encoding="utf-8")\n\nROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "megillah" / "candidates" / "Megilat_HaItim_Marak_Candidate.md"
ORIGINAL = ROOT / "megillah" / "original" / "Megilat_HaItim_Yehuda_FINAL_2026-09-18.md"

text = CANDIDATE.read_text(encoding="utf-8")
normalized = normalize_code(text, file=str(CANDIDATE))
compiled = compile_source(text, file=str(CANDIDATE))

furthest = -1
frontier = None
for diagnostic in compiled.diagnostics:
    value = diagnostic.metadata.get("furthest_token") if diagnostic.metadata else None
    if isinstance(value, int) and value > furthest:
        furthest = value
        frontier = diagnostic

obj = {
    "candidate_sha256": hashlib.sha256(CANDIDATE.read_bytes()).hexdigest(),
    "original_sha256": hashlib.sha256(ORIGINAL.read_bytes()).hexdigest(),
    "normalized_tokens": len(normalized.text.split()),
    "valid": compiled.valid,
    "hast_reached": compiled.hast is not None,
    "ir_reached": compiled.ir is not None,
    "artifact_reached": getattr(compiled, "artifact", None) is not None,
    "furthest_normalized_token": furthest,
    "frontier": None if frontier is None else {
        "code": frontier.code,
        "phase": frontier.phase,
        "message_en": frontier.message_en,
        "source_span": None if frontier.source_span is None else asdict(frontier.source_span),
        "normalized_span": frontier.normalized_span,
        "metadata": frontier.metadata,
    },
    "diagnostic_codes": [d.code for d in compiled.diagnostics],
}
print(json.dumps(obj, ensure_ascii=False, indent=2, default=str))
