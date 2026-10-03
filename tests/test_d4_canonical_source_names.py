from __future__ import annotations

import json
import re
from pathlib import Path

from compiler.parse.a15_numerals import format_natural

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "megillah" / "candidates" / "Megilat_HaItim_Marak_Candidate.md"
INVENTORY = ROOT / "megillah" / "analysis" / "D4_CANONICAL_SOURCE_NAME_INVENTORY.json"


def _counted(payload: str) -> str:
    words = payload.split(" ")
    assert len(words) >= 2
    return (
        "שם אשר מספר המלים אשר בו הוא "
        f"{format_natural(len(words))} והמלים הן {' '.join(words)}"
    )


def _accepted_t18_prefix() -> str:
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    boundary = next(i for i, line in enumerate(lines) if line.startswith("# לוח חמשה עשר:"))
    return "\n".join(lines[:boundary])


def test_d4_canonical_source_name_inventory_has_no_uncertain_identity():
    data = json.loads(INVENTORY.read_text(encoding="utf-8"))
    assert data["summary"]["uncertain_identities"] == 0
    assert data["summary"]["artificially_welded_unique_spellings"] == len(
        data["verified_removed_spellings"]
    )
    assert set(data["verified_removed_spellings"]) == set(data["canonical_replacements"])


def test_d4_live_candidate_contains_none_of_the_verified_removed_welded_spellings():
    data = json.loads(INVENTORY.read_text(encoding="utf-8"))
    source = _accepted_t18_prefix()
    for welded in data["verified_removed_spellings"]:
        pattern = rf"(?<![א-ת]){re.escape(welded)}(?![א-ת])"
        assert re.search(pattern, source) is None, welded


def test_d4_all_verified_multiword_replacements_use_counted_source_name_surface():
    data = json.loads(INVENTORY.read_text(encoding="utf-8"))
    source = _accepted_t18_prefix()
    for payload in sorted(set(data["canonical_replacements"].values())):
        assert " " in payload
        assert _counted(payload) in source, payload


def test_d4_cleanup_keeps_luach_fifteen_as_next_unadmitted_source_boundary():
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    boundary = next(i for i, line in enumerate(lines) if line.startswith("# לוח חמשה עשר:"))
    assert boundary + 1 == 466
    assert lines[boundary] == "# לוח חמשה עשר: לשאול את הקערות"
