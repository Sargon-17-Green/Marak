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


def _d4_day_number_preparation() -> str:
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    selected = lines[0:6] + [lines[10]] + lines[22:44]
    return " ".join(x for x in selected if x.strip())


def _d4_day_number_call(z: int) -> str:
    from tests.test_c5_6_general_index_surface import general_index
    return (
        "ועתה עשה את המעשה אשר שמו מספריום "
        f"בהיות {general_index(z)} תחת הדבר אשר במעשה אשר שמו מספריום שמו יום"
    )


def test_d4_post_c56_day_number_algorithm_matches_historical_examples_and_three_runtimes():
    from tests.test_c5_6_general_index_surface import three
    expected = {-3: 6, -2: 4, -1: 2, 0: 1, 1: 3, 2: 5, 3: 7}
    for z, want in expected.items():
        source = _d4_day_number_preparation() + " " + _d4_day_number_call(z)
        _, observed = three(source)
        facts = dict(observed["facts"])
        assert facts["מענהיום"] == want


def test_d4_post_c56_day_number_algorithm_keeps_coordinate_and_number_domains_separate():
    from tests.test_c5_6_general_index_surface import three
    source = _d4_day_number_preparation() + " " + _d4_day_number_call(-2)
    _, observed = three(source)
    facts = dict(observed["facts"])
    assert facts["סמן"] == {"index": "Zero"}
    assert facts["מענהיום"] == 4
    assert isinstance(facts["מענהיום"], int)


def test_d4_post_c56_day_number_repair_uses_index_order_steps_and_existing_addition_act():
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()[22:44]
    source = " ".join(lines)
    assert "עשה את המעשה אשר שמו חיבור" in source
    assert "המעלה אשר אחר" in source
    assert "המעלה אשר לפני" in source
    assert "מרחק" not in source
    assert "רב מן" not in source


def _d4_luach2_preparation() -> str:
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    selected = lines[0:6] + [lines[10]] + lines[22:44] + lines[52:81]
    return " ".join(x for x in selected if x.strip())


def _d4_index_value(z: int):
    from compiler.models.values import BidirectionalIndexValue
    if z < 0:
        return BidirectionalIndexValue("before", abs(z))
    if z == 0:
        return BidirectionalIndexValue("zero", 0)
    return BidirectionalIndexValue("after", z)


def test_d4_post_c56_luach2_two_inputs_and_derived_numbers_three_runtimes():
    from compiler.api import compile_source
    from compiler.runtime.invocation import InputBinding
    from tests.test_c5_6_general_index_surface import input_id, three
    source = _d4_luach2_preparation() + " ועתה עשה את המעשה אשר שמו שמותמספרים"
    compiled = compile_source(source)
    assert compiled.valid, [d.to_dict() for d in compiled.diagnostics]
    a = input_id(compiled, "יוםמעשה")
    b = input_id(compiled, "יוםשאלה")
    cases = [
        (-2, -2, 4, 4, 1, 8, 2),
        (-2, -1, 4, 2, 2, 6, 3),
        (3, -4, 7, 8, 8, 15, 1),
    ]
    for ca, qu, nca, nqu, dist, conn, way in cases:
        _, obs = three(source, (
            InputBinding(a, _d4_index_value(ca)),
            InputBinding(b, _d4_index_value(qu)),
        ))
        facts = dict(obs["facts"])
        assert facts["מספרמעשה"] == nca
        assert facts["מספרשאלה"] == nqu
        assert facts["מספרמרחק"] == dist
        assert facts["מספרחיבור"] == conn
        assert facts["מספרדרך"] == way


def test_d4_post_c56_luach2_has_named_nonpositional_general_index_inputs():
    text = CANDIDATE.read_text(encoding="utf-8")
    assert "ובטרם תחל המלאכה הזאת תעמד מעלה תחת הדבר אשר למלאכה הזאת שמו יוםמעשה" in text
    assert "ובטרם תחל המלאכה הזאת תעמד מעלה תחת הדבר אשר למלאכה הזאת שמו יוםשאלה" in text
    assert "stdin" not in text.lower()
    assert "argv" not in text.lower()


def test_d4_post_c56_luach2_distance_examples_and_referent_distinction():
    import json
    p = ROOT / "megillah" / "analysis" / "D4_SOURCE_PROVENANCE.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    by_id = {x["id"]: x for x in data["externalized_spans"]}
    assert by_id["D4-DOC-008"]["classification"] == "EXAMPLE_OR_PROOF"
    assert "same=1" in by_id["D4-DOC-008"]["retained_requirement"]
    assert by_id["D4-DOC-009"]["classification"] == "DOCUMENTATION"
    text = CANDIDATE.read_text(encoding="utf-8")
    assert "יהי מקום ושמו מספרמרחק" in text
    assert "יהי מקום ושמו מספרדרך" in text


def _d4_repeat_add_preparation() -> str:
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    selected = lines[96:104]
    return " ".join(x for x in selected if x.strip())


def _d4_zero_natural() -> str:
    return "המספר הנחשב בגרע את המספר אשר הוא אחד מן המספר אשר הוא אחד"


def _d4_repeat_add_call(value: str, count: str) -> str:
    return (
        "ועתה עשה את המעשה אשר שמו לקחתפעמים "
        f"בהיות {value} תחת הדבר אשר במעשה אשר שמו לקחתפעמים שמו מספר "
        f"ובהיות {count} תחת הדבר אשר במעשה אשר שמו לקחתפעמים שמו מנין"
    )


def test_d4_post_c56_luach3_exact_repeated_addition_three_runtimes():
    from tests.test_c5_6_general_index_surface import three
    cases = [
        ("המספר אשר הוא שלשה", "המספר אשר הוא שבעה", 21),
        ("המספר אשר הוא חמשה", "המספר אשר הוא שלשה עשר", 65),
        ("המספר אשר הוא תשעה", _d4_zero_natural(), 0),
    ]
    for value, count, want in cases:
        source = _d4_repeat_add_preparation() + " " + _d4_repeat_add_call(value, count)
        _, obs = three(source)
        assert obs["products"][-1] == ["לקחתפעמים", want]
        assert dict(obs["facts"])["מכפלה"] == want


def test_d4_post_c56_luach3_uses_repeat_exactly_not_manual_expansion():
    text = " ".join(CANDIDATE.read_text(encoding="utf-8").splitlines()[96:104])
    assert "פעמים כמספר אשר במעשה הזה עומד" in text
    assert "עשה את המעשה אשר שמו הוסףלקיחה" in text
    assert "שלשה ושלשה ושלשה" not in text
    assert "שמונה פעמים" not in text


def _d4_square_preparation() -> str:
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    selected = lines[96:104] + lines[120:123]
    return " ".join(x for x in selected if x.strip())


def _d4_square_call(value: str) -> str:
    return (
        "עשה את המעשה אשר שמו רבוע "
        f"בהיות {value} תחת הדבר אשר במעשה אשר שמו רבוע שמו מספר"
    )


def test_d4_post_c56_luach4_square_three_runtimes():
    from tests.test_c5_6_general_index_surface import three
    source = _d4_square_preparation() + " ועתה " + _d4_square_call("המספר אשר הוא שבעה")
    _, obs = three(source)
    assert obs["products"][-1] == ["רבוע", 49]


def test_d4_post_c56_luach4_repeated_square_uses_previous_result_explicitly():
    from tests.test_c5_6_general_index_surface import three
    first = _d4_square_call("המספר אשר הוא שבעה")
    second = _d4_square_call("המספר אשר יצא עתה מן המעשה אשר שמו רבוע")
    source = _d4_square_preparation() + " ועתה " + first + " ואחרי כן " + second
    _, obs = three(source)
    assert obs["products"][-1] == ["רבוע", 2401]


def _d4_big_number_preparation() -> str:
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    selected = lines[0:6] + lines[142:148]
    return " ".join(x for x in selected if x.strip())


def test_d4_post_c56_luach5_big_number_exact_three_runtimes():
    from tests.test_c5_6_general_index_surface import three
    source = _d4_big_number_preparation() + " ועתה עשה את המעשה אשר שמו חשבגדול"
    _, obs = three(source)
    want = (1 << 127) - 1
    assert obs["products"][-1] == ["חשבגדול", want]
    assert dict(obs["facts"])["מספרגדול"] == want
    assert dict(obs["facts"])["גדולעבודה"] == (1 << 127)


def test_d4_post_c56_luach5_uses_exact_canonical_127_count_and_persistent_place():
    text = " ".join(CANDIDATE.read_text(encoding="utf-8").splitlines()[142:148])
    assert "מאה ועשרים ושבע פעמים עשה את המעשה אשר שמו כפלגדול" in text
    assert "שש ועשרים ומאה פעמים" not in text
    assert "שמנה ועשרים ומאה פעמים" not in text
    assert "יהי מקום ושמו מספרגדול" in text

def _d4_luach6_preparation() -> str:
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    big_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מספרגדול"))
    next_heading = next(i for i, line in enumerate(lines) if line.startswith("## לקחת מספר מאחיו"))
    selected = lines[0:6] + lines[big_start:next_heading]
    return " ".join(
        line for line in selected
        if line.strip() and line.strip() != "---" and not line.lstrip().startswith("#")
    )


def _d4_remainder_call(value: str, divisor: str) -> str:
    return (
        "עשה את המעשה אשר שמו נותר "
        f"בהיות {value} תחת הדבר אשר במעשה אשר שמו נותר שמו מספר "
        f"ובהיות {divisor} תחת הדבר אשר במעשה אשר שמו נותר שמו מחלק"
    )


def _d4_keep_call(value: str) -> str:
    return (
        "עשה את המעשה אשר שמו שמור "
        f"בהיות {value} תחת הדבר אשר במעשה אשר שמו שמור שמו מספר"
    )


def test_d4_post_c56_luach6_plain_remainder_three_runtimes():
    from tests.test_c5_6_general_index_surface import three
    cases = [
        ("המספר אשר הוא עשרים ושלשה", "המספר אשר הוא שבעה", 2),
        ("המספר אשר הוא עשרים ואחד", "המספר אשר הוא שבעה", 0),
        ("המספר אשר הוא חמשה", "המספר אשר הוא שבעה", 5),
    ]
    prep = _d4_luach6_preparation()
    for value, divisor, want in cases:
        source = prep + " ועתה " + _d4_remainder_call(value, divisor)
        _, obs = three(source)
        assert obs["products"][-1] == ["נותר", want]
        assert dict(obs["facts"])["נותרעבודה"] == want


def test_d4_post_c56_luach6_keep_maps_zero_remainder_to_big_number():
    from tests.test_c5_6_general_index_surface import three
    prep = _d4_luach6_preparation()
    source = (
        prep
        + " ועתה עשה את המעשה אשר שמו חשבגדול"
        + " ואחרי כן "
        + _d4_keep_call("המספר אשר במקום אשר שמו מספרגדול")
    )
    _, obs = three(source)
    want = (1 << 127) - 1
    assert obs["products"][-1] == ["שמור", want]
    assert dict(obs["facts"])["שמורעבודה"] == want


def test_d4_post_c56_luach6_keep_preserves_nonzero_remainder():
    from tests.test_c5_6_general_index_surface import three
    prep = _d4_luach6_preparation()
    source = (
        prep
        + " ועתה עשה את המעשה אשר שמו חשבגדול"
        + " ואחרי כן "
        + _d4_keep_call("המספר אשר הוא שבעה")
    )
    _, obs = three(source)
    assert obs["products"][-1] == ["שמור", 7]
    assert dict(obs["facts"])["שמורעבודה"] == 7


def test_d4_post_c56_luach6_uses_safe_post_action_remainder_not_underflow_control():
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו נותרעבודה"))
    end = next(i for i, line in enumerate(lines) if line.startswith("## לקחת מספר מאחיו"))
    text = " ".join(lines[start:end])
    assert "וכן תעשה עד אשר המספר אשר במקום אשר שמו נותרמחלק רב מן המספר אשר במקום אשר שמו נותרעבודה" in text
    assert "אם המספר אשר במקום אשר שמו נותרמחלק רב מן המספר אשר במקום אשר שמו נותרעבודה" in text
    assert "יהי מעשה ושמו נותר" in text
    assert "יהי מעשה ושמו שמור" in text

