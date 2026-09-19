import hashlib
import json
from pathlib import Path

from compiler.api import check, parse, run_source

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT / "megillah" / "original" / "Megilat_HaItim_Yehuda_FINAL_2026-09-18.md"
CANDIDATE = ROOT / "megillah" / "candidates" / "Megilat_HaItim_Marak_Candidate.md"
SPAN_MAP = ROOT / "megillah" / "analysis" / "D3_DOCUMENTARY_SPAN_MAP.json"

EXPECTED_ORIGINAL_SHA = "7b834f4a444e021bb65164282b851af960a6dbc0be3d458c2412181773b9db7b"
ZERO = "המספר הנחשב בגרע את המספר אשר הוא אחד מן המספר אשר הוא אחד"


def test_d3_original_is_immutable():
    assert hashlib.sha256(ORIGINAL.read_bytes()).hexdigest() == EXPECTED_ORIGINAL_SHA


def test_d3_named_act_introduction_repair():
    assert len(parse("יהי שם מעשה חיבור", start_lhs="NamedActIdentity").forest.alternatives) == 0
    assert len(parse("יהי מעשה ושמו חיבור", start_lhs="NamedActIdentity").forest.alternatives) == 1


def test_d3_addition_structural_pattern_runs_5_plus_6_as_11():
    source = """יהי מקום ושמו מענה ובמקום אשר שמו מענה יהי המספר אשר הוא אחד לבדו
יהי מעשה ושמו חיבור
יהי במעשה אשר שמו חיבור דבר ושמו ראשון ובעשות את המעשה אשר שמו חיבור יעמד מספר תחת הדבר אשר במעשה אשר שמו חיבור שמו ראשון
יהי במעשה אשר שמו חיבור דבר ושמו שני ובעשות את המעשה אשר שמו חיבור יעמד מספר תחת הדבר אשר במעשה אשר שמו חיבור שמו שני
זה דבר המעשה אשר שמו חיבור
הוצא מן המעשה הזה את המספר הנחשב בהוסיף את המספר אשר במעשה הזה עומד תחת הדבר אשר במעשה אשר שמו חיבור שמו ראשון על המספר אשר במעשה הזה עומד תחת הדבר אשר במעשה אשר שמו חיבור שמו שני
עד הנה דבר המעשה אשר שמו חיבור
ועתה עשה את המעשה אשר שמו חיבור בהיות המספר אשר הוא חמשה תחת הדבר אשר במעשה אשר שמו חיבור שמו ראשון ובהיות המספר אשר הוא ששה תחת הדבר אשר במעשה אשר שמו חיבור שמו שני ואחרי כן שים במקום אשר שמו מענה את המספר אשר יצא עתה מן המעשה אשר שמו חיבור תחת המספר אשר במקום אשר שמו מענה"""
    c = check(source)
    assert c.valid, [d.code for d in c.diagnostics]
    outcome = run_source(source, fuel=100).outcome
    assert outcome.facts == ((1, 11),)


def test_d3_recurrence_surface_repair_positive_and_negative():
    good = f"""יהי מקום ושמו גד ובמקום אשר שמו גד יהי המספר אשר הוא שנים לבדו
ועתה שים במקום אשר שמו גד את המספר הנחשב בגרע את המספר אשר הוא אחד מן המספר אשר במקום אשר שמו גד תחת המספר אשר במקום אשר שמו גד וכן תעשה עד אשר המספר אשר במקום אשר שמו גד הוא {ZERO}"""
    bad = good.replace("וכן תעשה", "וכן עשה")
    assert check(good).valid
    assert not check(bad).valid
    assert run_source(good, fuel=100).outcome.facts == ((1, 0),)


def test_d3_sequence_surface_repair_positive_and_negative():
    good = """יהי מקום ושמו גד ובמקום אשר שמו גד יהי המספר אשר הוא אחד לבדו
ועתה שים במקום אשר שמו גד את המספר הנחשב בהוסיף את המספר אשר הוא אחד על המספר אשר במקום אשר שמו גד תחת המספר אשר במקום אשר שמו גד ואחרי כן שים במקום אשר שמו גד את המספר הנחשב בהוסיף את המספר אשר הוא אחד על המספר אשר במקום אשר שמו גד תחת המספר אשר במקום אשר שמו גד"""
    bad = good.replace("ואחרי כן", "ואחר כן")
    assert check(good).valid
    assert not check(bad).valid
    assert run_source(good, fuel=100).outcome.facts == ((1, 3),)


def test_d3_candidate_contains_master_approved_5778_repair():
    text = CANDIDATE.read_text(encoding="utf-8")
    assert "ולא תקח שנה אם ירבו ימיה על חמשת אלפים ושבע מאות ושבעים ושמנה" in text


def test_d3_externalized_input_contract_is_retained_as_requirement():
    data = json.loads(SPAN_MAP.read_text(encoding="utf-8"))
    entry = next(x for x in data["spans"] if x["id"] == "D3-BLOCK-001")
    assert entry["classification"] == "INTERFACE_REQUIREMENT_BLOCKED"
    assert entry["retained_requirement"] == "D-LANGUAGE-REQUEST-007"
    assert "למלאכת הלוח קח שני ימים" in entry["original_text"]
