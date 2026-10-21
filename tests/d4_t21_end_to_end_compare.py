from __future__ import annotations

import json
from pathlib import Path


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


root = Path("evidence")
for side in ("after", "before"):
    obs = {
        runtime: load(root / f"evidence-{side}-{runtime}.json")
        for runtime in ("hast", "ir", "portable")
    }
    assert obs["hast"] == obs["ir"] == obs["portable"], side

    expected_gap = 377 if side == "after" else 762
    gaps = [v for act, v in obs["portable"]["products"] if act == "חשב רווח שער"]
    assert gaps == [expected_gap]

print("PASS: exact HAST/IR/portable observable agreement for after and before")
