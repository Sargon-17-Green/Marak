from __future__ import annotations

from compiler.parse.current_registry import CURRENT_REGISTRY
from tests.test_c5_2_surface_pipeline import place_nat, place_typed, replace_nat
from tests.test_c5_6_general_index_surface import (
    general_index,
    general_place,
    general_succ,
    replace_general,
    three,
)
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "megillah" / "candidates" / "Megilat_HaItim_Marak_Candidate.md"


def test_d4_post_c56_foundation_repair_maps_named_referent_to_zero_index():
    source = " ".join([
        place_typed("יסוד", general_index(0)),
        place_typed("סמן", general_index(-1)),
        "ועתה " + replace_general("סמן", general_succ(general_place("סמן"))),
    ])
    _, observed = three(source)
    facts = dict(observed["facts"])
    assert facts["יסוד"] == {"index": "Zero"}
    assert facts["סמן"] == {"index": "Zero"}


def test_d4_post_c56_candidate_contains_foundation_repair_and_not_historical_sentence():
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    assert lines[10] == "יהי מקום ושמו יסוד ובמקום אשר שמו יסוד יהי מעלת היתד לבדו"
    assert "ותבחר מפלצת הספגטי המעופפת יום אחד ותקרא את שמו יום היסוד." not in lines
    assert "לא נאמר כי לא היו ימים טרם יום היסוד" not in lines


def test_d4_post_c56_day_coordinate_and_natural_day_number_are_distinct_values():
    source = " ".join([
        place_typed("יסוד", general_index(0)),
        place_nat("מספריום", 1),
        "ועתה " + replace_nat("מספריום", "המספר אשר הוא אחד"),
    ])
    _, observed = three(source)
    facts = dict(observed["facts"])
    assert facts["יסוד"] == {"index": "Zero"}
    assert facts["מספריום"] == 1


def test_d4_post_c56_no_day_domain_or_direct_distance_or_index_equality_is_added():
    ids = " ".join(p.production_id for p in CURRENT_REGISTRY.productions).upper()
    for forbidden in ("DAY", "DATE", "TIMESTAMP", "INDEX_DISTANCE", "INDEX_EQUAL"):
        assert forbidden not in ids


def test_d4_post_c56_addition_precedent_remains_explicit_named_act():
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "יהי מעשה ושמו חיבור"
    assert lines[3] == "זה דבר המעשה אשר שמו חיבור"
    assert "הוצא מן המעשה הזה את המספר הנחשב בהוסיף את" in lines[4]
    assert lines[5] == "עד הנה דבר המעשה אשר שמו חיבור"


def test_d4_post_c56_tablets_offset_is_externalized_as_unused_historical_proof():
    text = CANDIDATE.read_text(encoding="utf-8")
    assert "יום הינתן הלוחות אחרי יום היסוד" not in text
    assert "ארבעה עשר אלף אלפים ימים" not in text
    import json
    p = ROOT / "megillah" / "analysis" / "D4_SOURCE_PROVENANCE.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    by_id = {x["id"]: x for x in data["externalized_spans"]}
    assert by_id["D4-DOC-002"]["classification"] == "EXAMPLE_OR_PROOF"
    assert by_id["D4-DOC-003"]["classification"] == "EXAMPLE_OR_PROOF"
    assert by_id["D4-DOC-004"]["classification"] == "DOCUMENTARY_EXTERNALIZATION"
