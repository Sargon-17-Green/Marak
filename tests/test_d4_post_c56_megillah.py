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
        place_nat("שם אשר מספר המלים אשר בו הוא שלשה והמלים הן חשב מספר היום", 1),
        "ועתה " + replace_nat("שם אשר מספר המלים אשר בו הוא שלשה והמלים הן חשב מספר היום", "המספר אשר הוא אחד"),
    ])
    _, observed = three(source)
    facts = dict(observed["facts"])
    assert facts["יסוד"] == {"index": "Zero"}
    assert facts["חשב מספר היום"] == 1


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
        "ועתה עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן חשב מספר היום "
        f"בהיות {general_index(z)} תחת הדבר אשר במעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן חשב מספר היום שמו יום"
    )


def test_d4_post_c56_day_number_algorithm_matches_historical_examples_and_three_runtimes():
    from tests.test_c5_6_general_index_surface import three
    expected = {-3: 6, -2: 4, -1: 2, 0: 1, 1: 3, 2: 5, 3: 7}
    for z, want in expected.items():
        source = _d4_day_number_preparation() + " " + _d4_day_number_call(z)
        _, observed = three(source)
        facts = dict(observed["facts"])
        assert facts["מספר היום המחושב"] == want


def test_d4_post_c56_day_number_algorithm_keeps_coordinate_and_number_domains_separate():
    from tests.test_c5_6_general_index_surface import three
    source = _d4_day_number_preparation() + " " + _d4_day_number_call(-2)
    _, observed = three(source)
    facts = dict(observed["facts"])
    assert facts["סמן"] == {"index": "Zero"}
    assert facts["מספר היום המחושב"] == 4
    assert isinstance(facts["מספר היום המחושב"], int)


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
    source = _d4_luach2_preparation() + " ועתה עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן חשב שמות המספרים"
    compiled = compile_source(source)
    assert compiled.valid, [d.to_dict() for d in compiled.diagnostics]
    a = input_id(compiled, "יום המעשה")
    b = input_id(compiled, "היום אשר עליו תשאל")
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
        assert facts["מספר המעשה"] == nca
        assert facts["מספר השאלה"] == nqu
        assert facts["מספר המרחק"] == dist
        assert facts["מספר החיבור"] == conn
        assert facts["מספר הדרך"] == way


def test_d4_post_c56_luach2_has_named_nonpositional_general_index_inputs():
    text = CANDIDATE.read_text(encoding="utf-8")
    assert "ובטרם תחל המלאכה הזאת תעמד מעלה תחת הדבר אשר למלאכה הזאת שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן יום המעשה" in text
    assert "ובטרם תחל המלאכה הזאת תעמד מעלה תחת הדבר אשר למלאכה הזאת שמו שם אשר מספר המלים אשר בו הוא ארבעה והמלים הן היום אשר עליו תשאל" in text
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
    assert "יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מספר המרחק" in text
    assert "יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מספר הדרך" in text


def _d4_repeat_add_preparation() -> str:
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מכפלה"))
    end = next(i for i, line in enumerate(lines) if line.startswith("יהי מעשה ושמו רבוע"))
    selected = lines[0:6] + lines[start:end]
    return " ".join(x for x in selected if x.strip() and x.strip() != "---")


def _d4_zero_natural() -> str:
    return "המספר הנחשב בגרע את המספר אשר הוא אחד מן המספר אשר הוא אחד"


def _d4_repeat_add_call(value: str, count: str) -> str:
    return (
        "ועתה עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן לקחת מספר פעמים "
        f"בהיות {value} תחת הדבר אשר במעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן לקחת מספר פעמים שמו מספר "
        f"ובהיות {count} תחת הדבר אשר במעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן לקחת מספר פעמים שמו מנין"
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
        assert obs["products"][-1] == ["לקחת מספר פעמים", want]
        assert dict(obs["facts"])["מכפלה"] == want


def test_d4_post_c56_luach3_uses_source_doubling_decomposition_not_linear_repeat_exactly():
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מכפלה"))
    end = next(i for i, line in enumerate(lines) if line.startswith("יהי מעשה ושמו רבוע"))
    text = " ".join(lines[start:end])
    assert "יהי מעשה ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן רד בכפל" in text
    assert "יהי מעשה ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן בחר בכפל" in text
    assert "עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן רד בכפל" in text
    assert "פעמים כמספר אשר במעשה הזה עומד" not in text
    assert "שלשה ושלשה ושלשה" not in text




def test_d4_post_c56_luach3_large_count_completes_with_logarithmic_doubling_path():
    from compiler.api import compile_source
    from compiler.backend.portable import execute_ir
    from compiler.runtime.ir_reference import execute_reference_ir
    from compiler.runtime.observables import backend_observable, ir_reference_observable, reference_observable
    from compiler.runtime.reference import execute_reference

    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    mul_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מכפלה"))
    square_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מעשה ושמו רבוע"))
    big_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן המספר הגדול"))
    rem_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן עבודת הנותר"))
    preparation = " ".join(
        line for line in lines[0:6] + lines[mul_start:square_start] + lines[big_start:rem_start]
        if line.strip() and line.strip() != "---"
    )
    source = (
        preparation
        + " ועתה עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן חשב המספר הגדול"
        + " ואחרי כן עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן לקחת מספר פעמים "
        + "בהיות המספר אשר הוא שלשה תחת הדבר אשר במעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן לקחת מספר פעמים שמו מספר "
        + "ובהיות המספר אשר במקום אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן המספר הגדול תחת הדבר אשר במעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן לקחת מספר פעמים שמו מנין"
    )
    compiled = compile_source(source)
    assert compiled.valid, [d.to_dict() for d in compiled.diagnostics]
    observed = [
        reference_observable(execute_reference(compiled.hast, fuel=20000)),
        ir_reference_observable(execute_reference_ir(compiled.ir, fuel=20000)),
        backend_observable(execute_ir(compiled.ir, fuel=20000)),
    ]
    assert observed[0] == observed[1] == observed[2]
    assert observed[0]["outcome"] == "Normal"
    assert observed[0]["products"][-1] == ["לקחת מספר פעמים", 3 * ((1 << 127) - 1)]


def _d4_square_preparation() -> str:
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מכפלה"))
    end = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן המספר הגדול"))
    selected = lines[0:6] + lines[start:end]
    return " ".join(x for x in selected if x.strip() and x.strip() != "---")


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
    start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן המספר הגדול"))
    end = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן עבודת הנותר"))
    selected = lines[0:6] + lines[start:end]
    return " ".join(x for x in selected if x.strip() and x.strip() != "---")


def test_d4_post_c56_luach5_big_number_exact_three_runtimes():
    from tests.test_c5_6_general_index_surface import three
    source = _d4_big_number_preparation() + " ועתה עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן חשב המספר הגדול"
    _, obs = three(source)
    want = (1 << 127) - 1
    assert obs["products"][-1] == ["חשב המספר הגדול", want]
    assert dict(obs["facts"])["המספר הגדול"] == want
    assert dict(obs["facts"])["עבודת המספר הגדול"] == (1 << 127)


def test_d4_post_c56_luach5_uses_exact_canonical_127_count_and_persistent_place():
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן המספר הגדול"))
    end = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן עבודת הנותר"))
    text = " ".join(lines[start:end])
    assert "מאה ועשרים ושבע פעמים עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן כפל המספר הגדול" in text
    assert "שש ועשרים ומאה פעמים" not in text
    assert "שמנה ועשרים ומאה פעמים" not in text
    assert "יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן המספר הגדול" in text

def _d4_luach6_preparation() -> str:
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    big_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן המספר הגדול"))
    next_section = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן עבודת האח"))
    fast_start = next(i for i, line in enumerate(lines) if line.startswith("זה דבר המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן הנותר בדרך הקצרה "))
    luach7 = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מספר הטיפה"))
    selected = lines[0:6] + lines[big_start:next_section] + lines[fast_start:luach7]
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
        assert dict(obs["facts"])["עבודת הנותר"] == want


def test_d4_post_c56_luach6_keep_maps_zero_remainder_to_big_number():
    from tests.test_c5_6_general_index_surface import three
    prep = _d4_luach6_preparation()
    source = (
        prep
        + " ועתה עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן חשב המספר הגדול"
        + " ואחרי כן "
        + _d4_keep_call("המספר אשר במקום אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן המספר הגדול")
    )
    _, obs = three(source)
    want = (1 << 127) - 1
    assert obs["products"][-1] == ["שמור", want]
    assert dict(obs["facts"])["עבודת שמור"] == want


def test_d4_post_c56_luach6_keep_preserves_nonzero_remainder():
    from tests.test_c5_6_general_index_surface import three
    prep = _d4_luach6_preparation()
    source = (
        prep
        + " ועתה עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן חשב המספר הגדול"
        + " ואחרי כן "
        + _d4_keep_call("המספר אשר הוא שבעה")
    )
    _, obs = three(source)
    assert obs["products"][-1] == ["שמור", 7]
    assert dict(obs["facts"])["עבודת שמור"] == 7


def test_d4_post_c56_luach6_uses_safe_post_action_remainder_not_underflow_control():
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן עבודת הנותר"))
    end = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן עבודת האח"))
    text = " ".join(lines[start:end])
    assert "וכן תעשה עד אשר המספר אשר במקום אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מחלק הנותר רב מן המספר אשר במקום אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן עבודת הנותר" in text
    assert "אם המספר אשר במקום אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מחלק הנותר רב מן המספר אשר במקום אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן עבודת הנותר" in text
    assert "יהי מעשה ושמו נותר" in text
    assert "יהי מעשה ושמו שמור" in text

def _d4_luach6_wrapped_subtraction_preparation() -> str:
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    big_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן המספר הגדול"))
    luach7 = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מספר הטיפה"))
    selected = lines[0:6] + lines[big_start:luach7]
    return " ".join(
        line for line in selected
        if line.strip() and line.strip() != "---" and not line.lstrip().startswith("#")
    )


def _d4_wrapped_subtraction_call(subtrahend: str, sibling: str) -> str:
    return (
        "עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן לקחת מספר מאחיו "
        f"בהיות {subtrahend} תחת הדבר אשר במעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן לקחת מספר מאחיו שמו מחסר "
        f"ובהיות {sibling} תחת הדבר אשר במעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן לקחת מספר מאחיו שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מספר האח"
    )


def test_d4_post_c56_luach6_wrapped_subtraction_direct_and_wrap_three_runtimes():
    from tests.test_c5_6_general_index_surface import three
    prep = _d4_luach6_wrapped_subtraction_preparation()
    cases = [
        ("המספר אשר הוא חמשה", "המספר אשר הוא שמנה", 3),
        ("המספר אשר הוא שמנה", "המספר אשר הוא חמשה", (1 << 127) - 4),
    ]
    for subtrahend, sibling, want in cases:
        source = (
            prep
            + " ועתה עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן חשב המספר הגדול"
            + " ואחרי כן "
            + _d4_wrapped_subtraction_call(subtrahend, sibling)
        )
        _, obs = three(source)
        assert obs["products"][-1] == ["לקחת מספר מאחיו", want]


def test_d4_post_c56_luach6_wrapped_subtraction_equal_maps_through_keep():
    from tests.test_c5_6_general_index_surface import three
    prep = _d4_luach6_wrapped_subtraction_preparation()
    source = (
        prep
        + " ועתה עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן חשב המספר הגדול"
        + " ואחרי כן "
        + _d4_wrapped_subtraction_call("המספר אשר הוא שבעה", "המספר אשר הוא שבעה")
    )
    _, obs = three(source)
    assert obs["products"][-1] == ["לקחת מספר מאחיו", (1 << 127) - 1]


def test_d4_post_c56_luach6_wrapped_subtraction_repeats_modulus_addition_as_needed():
    from tests.test_c5_6_general_index_surface import three
    prep = _d4_luach6_wrapped_subtraction_preparation()
    add_two_moduli = (
        "עשה את המעשה אשר שמו חיבור "
        "בהיות המספר אשר במקום אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן המספר הגדול תחת הדבר אשר במעשה אשר שמו חיבור שמו ראשון "
        "ובהיות המספר אשר במקום אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן המספר הגדול תחת הדבר אשר במעשה אשר שמו חיבור שמו שני"
    )
    source = (
        prep
        + " ועתה עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן חשב המספר הגדול"
        + " ואחרי כן "
        + add_two_moduli
        + " ואחרי כן "
        + _d4_wrapped_subtraction_call(
            "המספר אשר יצא עתה מן המעשה אשר שמו חיבור",
            "המספר אשר הוא אחד",
        )
    )
    _, obs = three(source)
    assert obs["products"][-1] == ["לקחת מספר מאחיו", 1]


def test_d4_post_c56_luach6_wrapped_subtraction_never_uses_underflow_as_control():
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן עבודת האח"))
    end = next(i for i, line in enumerate(lines) if line.startswith("זה דבר המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן הנותר בדרך הקצרה "))
    text = " ".join(lines[start:end])
    assert "שם אשר מספר המלים אשר בו הוא שנים והמלים הן מחסר האח רב מן המספר אשר במקום אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן עבודת האח" in text
    assert "עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן הוסף לאח" in text
    assert "המספר הנחשב בגרע את המספר אשר במקום אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מחסר האח מן המספר אשר במקום אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן עבודת האח" in text
    assert "עשה את המעשה אשר שמו שמור" in text

def _d4_fast_remainder_call(value: str, divisor: str) -> str:
    return (
        "עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן הנותר בדרך הקצרה "
        f"בהיות {value} תחת הדבר אשר במעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן הנותר בדרך הקצרה שמו מספר "
        f"ובהיות {divisor} תחת הדבר אשר במעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן הנותר בדרך הקצרה שמו מחלק"
    )


def test_d4_post_c56_luach6_fast_remainder_matches_long_way_three_runtimes():
    from tests.test_c5_6_general_index_surface import three
    prep = _d4_luach6_wrapped_subtraction_preparation()
    cases = [
        ("המספר אשר הוא עשרים ושלשה", "המספר אשר הוא שבעה", 2),
        ("המספר אשר הוא עשרים ואחד", "המספר אשר הוא שבעה", 0),
        ("המספר אשר הוא חמשה", "המספר אשר הוא שבעה", 5),
    ]
    for value, divisor, want in cases:
        source = prep + " ועתה " + _d4_fast_remainder_call(value, divisor)
        _, obs = three(source)
        assert obs["products"][-1] == ["הנותר בדרך הקצרה", want]


def test_d4_post_c56_luach6_fast_remainder_handles_large_natural_by_doubling():
    from compiler.parse.a15_numerals import format_natural
    from tests.test_c5_6_general_index_surface import three
    prep = _d4_luach6_wrapped_subtraction_preparation()
    value = f"המספר אשר הוא {format_natural(99_999_999)}"
    divisor = f"המספר אשר הוא {format_natural(97)}"
    source = prep + " ועתה " + _d4_fast_remainder_call(value, divisor)
    _, obs = three(source)
    assert obs["products"][-1] == ["הנותר בדרך הקצרה", 80]


def test_d4_post_c56_luach6_fast_remainder_is_recursive_doubling_greedy_not_linear_subtraction():
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("זה דבר המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן הנותר בדרך הקצרה "))
    end = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מספר הטיפה"))
    text = " ".join(lines[start:end])
    assert "עשה את המעשה אשר שמו חיבור" in text
    assert text.count("שמו מחלק תחת הדבר אשר במעשה אשר שמו חיבור") >= 2
    assert "עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן הנותר בדרך הקצרה" in text
    assert "המספר הנחשב בגרע" in text
    assert "עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן גרע לנותר" not in text


def test_d4_post_c56_luach6_keep_uses_fast_remainder_without_hidden_threshold():
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    keep = next(line for line in lines if line.startswith("זה דבר המעשה אשר שמו שמור "))
    assert "עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן הנותר בדרך הקצרה" in keep
    assert "עשה את המעשה אשר שמו נותר " not in keep

def _d4_luach7_preparation() -> str:
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מכפלה"))
    end = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן הנסתרת האחת"))
    selected = lines[0:6] + lines[start:end]
    return " ".join(
        line for line in selected
        if line.strip() and line.strip() != "---" and not line.lstrip().startswith("#")
    )


def test_d4_post_c56_luach7_first_transition_uses_only_old_stone_snapshot():
    from tests.test_c5_6_general_index_surface import three
    source = (
        _d4_luach7_preparation()
        + " ועתה עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן חשב המספר הגדול"
        + " ואחרי כן עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן הטיפה הבאה"
    )
    _, obs = three(source)
    facts = dict(obs["facts"])
    expected = [378, 1073, 2375, 6195, 10493]
    assert facts["מספר הטיפה"] == 2
    assert [facts[x] for x in ["חיטה ישנה","שעורה ישנה","מלח ישנה","מרה ישנה","אדומה ישנה"]] == expected
    assert [facts[x] for x in ["חיטה חדשה","שעורה חדשה","מלח חדשה","מרה חדשה","אדומה חדשה"]] == expected
    assert facts["אבני הטיפות"] == [[17,29,43,71,101], expected]


def test_d4_post_c56_luach7_builds_exact_46_drop_table_three_runtimes_with_fuel():
    from compiler.api import compile_source
    from compiler.backend.portable import execute_ir
    from compiler.runtime.ir_reference import execute_reference_ir
    from compiler.runtime.observables import backend_observable, ir_reference_observable, reference_observable
    from compiler.runtime.reference import execute_reference

    source = (
        _d4_luach7_preparation()
        + " ועתה עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן חשב המספר הגדול"
        + " ואחרי כן עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן בנה אבנים"
    )
    compiled = compile_source(source)
    assert compiled.valid, [d.to_dict() for d in compiled.diagnostics]
    observed = [
        reference_observable(execute_reference(compiled.hast, fuel=1_000_000)),
        ir_reference_observable(execute_reference_ir(compiled.ir, fuel=1_000_000)),
        backend_observable(execute_ir(compiled.ir, fuel=1_000_000)),
    ]
    assert observed[0] == observed[1] == observed[2]
    assert observed[0]["outcome"] == "Normal"
    facts = dict(observed[0]["facts"])
    table = facts["אבני הטיפות"]
    assert facts["מספר הטיפה"] == 46
    assert len(table) == 46
    assert table[0] == [17,29,43,71,101]
    assert table[1] == [378,1073,2375,6195,10493]
    assert table[-1] == [
        73799454308499791987382386781055001470,
        147925408106533232424672641008220632365,
        94499522601819303005579577099149028685,
        108473647672201258090947028490673028834,
        137131922036975206684616468948804344042,
    ]


def test_d4_post_c56_luach7_canonical_count_and_snapshot_copy_order():
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מספר הטיפה"))
    end = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן הנסתרת האחת"))
    text = " ".join(lines[start:end])
    assert "ארבעים וחמש פעמים עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן הטיפה הבאה" in text
    assert "שש וארבעים" not in text
    body = next(line for line in lines if line.startswith("זה דבר המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן הטיפה הבאה "))
    assert body.index("שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן אדומה חדשה") < body.index("שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן חיטה ישנה את המספר אשר במקום אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן חיטה חדשה")
    assert "ספר ספרי מספרים" in text

def _d4_luach8_preparation() -> str:
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    counters_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מספר המעשה"))
    counters_end = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן סמן המרחק"))
    core_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מכפלה"))
    luach9 = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן מספר הטיפה הגלויה"))
    selected = lines[0:6] + lines[counters_start:counters_end] + lines[core_start:luach9]
    return " ".join(
        line for line in selected
        if line.strip() and line.strip() != "---" and not line.lstrip().startswith("#")
    )


def _d4_set_luach8_counters() -> str:
    return " ואחרי כן ".join([
        "שים במקום אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מספר המעשה את המספר אשר הוא שנים תחת המספר אשר במקום אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מספר המעשה",
        "שים במקום אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מספר השאלה את המספר אשר הוא שלשה תחת המספר אשר במקום אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מספר השאלה",
        "שים במקום אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מספר המרחק את המספר אשר הוא ארבעה תחת המספר אשר במקום אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מספר המרחק",
        "שים במקום אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מספר החיבור את המספר אשר הוא חמשה תחת המספר אשר במקום אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מספר החיבור",
        "שים במקום אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מספר הדרך את המספר אשר הוא אחד תחת המספר אשר במקום אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מספר הדרך",
    ])


def test_d4_post_c56_luach8_seven_hidden_drops_exact_three_runtimes():
    from tests.test_c5_6_general_index_surface import three
    source = (
        _d4_luach8_preparation()
        + " ועתה "
        + _d4_set_luach8_counters()
        + " ואחרי כן עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן חשב המספר הגדול"
        + " ואחרי כן שש פעמים עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן הטיפה הבאה"
        + " ואחרי כן עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן בנה נסתרות"
    )
    _, obs = three(source)
    facts = dict(obs["facts"])
    expected = [
        11444032270830949316106214743872497511,
        28452868261542307484545760903286527681,
        112739049138818416587726524909828373299,
        152668047685990206548249493436880013083,
        150701631999741008562130578980114868144,
        70454981221026737591078108330515014309,
        119123926606937080003165916448677215346,
    ]
    names = ["הנסתרת האחת","הנסתרת השנית","הנסתרת השלישית","הנסתרת הרביעית","הנסתרת החמישית","הנסתרת הששית","הנסתרת השביעית"]
    assert [facts[x] for x in names] == expected
    assert facts["הטיפות הנסתרות"] == list(reversed(expected))
    assert obs["products"][-1] == ["בנה נסתרות", list(reversed(expected))]


def test_d4_post_c56_luach8_grind_stone_sequence_is_explicit_seven_steps():
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    body = next(line for line in lines if line.startswith("זה דבר המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן טחן נסתרת "))
    assert body.count("עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן טחן פעם") == 7
    positions = [
        "המספר אשר הוא אחד", "המספר אשר הוא שנים", "המספר אשר הוא שלשה",
        "המספר אשר הוא ארבעה", "המספר אשר הוא חמשה",
        "המספר אשר הוא אחד", "המספר אשר הוא שנים",
    ]
    cursor = -1
    for position in positions:
        cursor = body.index(position, cursor + 1)
    assert "שבעה פעמים עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן טחן פעם" not in body


def test_d4_post_c56_luach8_hidden_order_is_seven_to_one_for_predecessor_history():
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    body = next(line for line in lines if line.startswith("זה דבר המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן בנה נסתרות "))
    order = ["שם אשר מספר המלים אשר בו הוא שנים והמלים הן הנסתרת השביעית","שם אשר מספר המלים אשר בו הוא שנים והמלים הן הנסתרת הששית","שם אשר מספר המלים אשר בו הוא שנים והמלים הן הנסתרת החמישית","שם אשר מספר המלים אשר בו הוא שנים והמלים הן הנסתרת הרביעית","שם אשר מספר המלים אשר בו הוא שנים והמלים הן הנסתרת השלישית","שם אשר מספר המלים אשר בו הוא שנים והמלים הן הנסתרת השנית","שם אשר מספר המלים אשר בו הוא שנים והמלים הן הנסתרת האחת"]
    cursor = body.index("ספר מספרים אשר אין בו מספר")
    for name in order:
        cursor = body.index(f"המספר אשר במקום אשר שמו {name}", cursor + 1)

def _d4_luach9_preparation() -> str:
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    counters_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מספר המעשה"))
    counters_end = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן סמן המרחק"))
    core_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מכפלה"))
    luach10 = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן עבודת מלא הקערה"))
    selected = lines[0:6] + lines[counters_start:counters_end] + lines[core_start:luach10]
    return " ".join(
        line for line in selected
        if line.strip() and line.strip() != "---" and not line.lstrip().startswith("#")
    )


def test_d4_post_c56_luach9_builds_exact_46_visible_drops_three_runtimes():
    from tests.test_c5_6_general_index_surface import three
    source = (
        _d4_luach9_preparation()
        + " ועתה "
        + _d4_set_luach8_counters()
        + " ואחרי כן עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן חשב המספר הגדול"
        + " ואחרי כן עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן בנה אבנים"
        + " ואחרי כן עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן בנה נסתרות"
        + " ואחרי כן עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן בנה טיפות"
    )
    _, obs = three(source)
    facts = dict(obs["facts"])
    expected_first = [
        123334831551511603687649975447681761062,
        156673085926334718073075063360231111300,
        154047674952282304836724395515854998098,
        63342935234911242715034474012998539443,
    ]
    assert facts["מספר הטיפה הגלויה"] == 46
    assert len(facts["הטיפות הגלויות"]) == 46
    assert facts["הטיפות הגלויות"][:4] == expected_first
    assert facts["הטיפות הגלויות"][-1] == 45970703249572047980738520652128782598
    assert len(facts["כל הטיפות"]) == 53
    assert facts["כל הטיפות"][-46:] == facts["הטיפות הגלויות"]


def test_d4_post_c56_luach9_predecessor_offsets_and_eleven_rounds_are_explicit():
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    step = next(line for line in lines if line.startswith("זה דבר המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן עשה טיפה גלויה "))
    assert "המספר האחרון אשר בתוך הספר אשר במקום אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן כל הטיפות" in step
    assert "בגרע את המספר אשר הוא שנים מן מספר הדברים אשר בתוך הספר אשר במקום אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן כל הטיפות" in step
    assert "בגרע את המספר אשר הוא ששה מן מספר הדברים אשר בתוך הספר אשר במקום אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן כל הטיפות" in step
    grind = next(line for line in lines if line.startswith("זה דבר המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן טחן טיפה "))
    assert grind.count("עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן טחן טיפה פעם") == 11
    assert "ארבעים ושש פעמים עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן עשה טיפה גלויה" in next(
        line for line in lines if line.startswith("זה דבר המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן בנה טיפות ")
    )

def _d4_luach10_preparation() -> str:
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    counters_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מספר המעשה"))
    counters_end = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן סמן המרחק"))
    core_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מכפלה"))
    luach11 = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן עבודת החלוקה"))
    selected = lines[0:6] + lines[counters_start:counters_end] + lines[core_start:luach11]
    return " ".join(
        line for line in selected
        if line.strip() and line.strip() != "---" and not line.lstrip().startswith("#")
    )


def test_d4_post_c56_luach10_initial_six_bowl_fills_three_runtimes():
    from tests.test_c5_6_general_index_surface import three
    source = (
        _d4_luach10_preparation()
        + " ועתה "
        + _d4_set_luach8_counters()
        + " ואחרי כן עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן חשב המספר הגדול"
        + " ואחרי כן עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן אתחל קערות"
    )
    _, obs = three(source)
    facts = dict(obs["facts"])
    assert facts["מלא הקערות"] == [92417, 143643, 302503, 748229, 976149, 1957207]
    assert obs["products"][-1] == ["אתחל קערות", [92417, 143643, 302503, 748229, 976149, 1957207]]


def test_d4_post_c56_luach10_six_fixed_bowl_identities_and_primes_are_explicit():
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    body = next(line for line in lines if line.startswith("זה דבר המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן אתחל קערות "))
    for numeral in ["אחד","שנים","שלשה","ארבעה","חמשה","ששה"]:
        assert f"המספר אשר הוא {numeral}" in body
    for prime in ["שבעה עשר","תשעה עשר","עשרים ושלשה","עשרים ותשעה","שלשים ואחד","שלשים ושבעה"]:
        assert f"המספר אשר הוא {prime}" in body
    assert body.count("עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן חשב מלא הקערה") == 6

def _d4_luach11_preparation() -> str:
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    counters_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מספר המעשה"))
    counters_end = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן סמן המרחק"))
    core_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מכפלה"))
    luach12 = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן עבודת הציקה"))
    selected = lines[0:6] + lines[counters_start:counters_end] + lines[core_start:luach12]
    return " ".join(
        line for line in selected
        if line.strip() and line.strip() != "---" and not line.lstrip().startswith("#")
    )


def _d4_find_arrangement_call(n: int) -> str:
    from compiler.parse.a15_numerals import format_natural
    return (
        "עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן מצא את המערכה "
        f"בהיות המספר אשר הוא {format_natural(n)} תחת הדבר אשר במעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן מצא את המערכה שמו מספר"
    )


def test_d4_post_c56_luach11_factoradic_boundaries_and_middle_three_runtimes():
    from tests.test_c5_6_general_index_surface import three
    prep = _d4_luach11_preparation()
    cases = {
        1: [1,2,3,4,5,6],
        100: [1,6,2,4,5,3],
        720: [6,5,4,3,2,1],
    }
    for n, want in cases.items():
        _, obs = three(prep + " ועתה " + _d4_find_arrangement_call(n))
        assert obs["products"][-1] == ["מצא את המערכה", want]


def test_d4_post_c56_luach11_arrangement_number_wraps_721_to_one():
    from tests.test_c5_6_general_index_surface import three
    source = (
        _d4_luach11_preparation()
        + " ועתה עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן בחר מערכה "
        + "בהיות המספר אשר הוא שבע מאות ועשרים ואחד תחת הדבר אשר במעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן בחר מערכה שמו מספר"
    )
    _, obs = three(source)
    assert obs["products"][-1] == ["בחר מערכה", [1,2,3,4,5,6]]
    assert dict(obs["facts"])["המערכה הנוכחית"] == [1,2,3,4,5,6]


def test_d4_post_c56_luach11_bowl_position_is_distinct_from_identity():
    from tests.test_c5_6_general_index_surface import three
    source = (
        _d4_luach11_preparation()
        + " ועתה " + _d4_find_arrangement_call(100)
        + " ואחרי כן עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מקום הקערה "
        + "בהיות המספר אשר הוא ששה תחת הדבר אשר במעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מקום הקערה שמו קערה "
        + "ובהיות הספר אשר יצא עתה מן המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן מצא את המערכה תחת הדבר אשר במעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מקום הקערה שמו מערכה"
    )
    _, obs = three(source)
    assert obs["products"][-1] == ["מקום הקערה", 2]


def test_d4_post_c56_luach11_factor_blocks_are_exact_source_short_way():
    text = CANDIDATE.read_text(encoding="utf-8")
    for n in ["מאה ועשרים","עשרים וארבעה","ששה","שנים","אחד"]:
        assert f"בהיות המספר אשר הוא {n} תחת הדבר אשר במעשה אשר שמו חלק שמו מחלק" in text
    assert "שבע מאות ועשרים" in text

def _d4_luach12_preparation() -> str:
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    counters_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מספר המעשה"))
    counters_end = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן סמן המרחק"))
    core_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מכפלה"))
    end = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מלא ישן"))
    selected = lines[0:6] + lines[counters_start:counters_end] + lines[core_start:end]
    return " ".join(
        line for line in selected
        if line.strip() and line.strip() != "---" and not line.lstrip().startswith("#")
    )


def test_d4_post_c56_luach12_three_pours_follow_arrangement_positions():
    from tests.test_c5_6_general_index_surface import three
    source = (
        _d4_luach12_preparation()
        + " ועתה "
        + _d4_set_luach8_counters()
        + " ואחרי כן עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן חשב המספר הגדול"
        + " ואחרי כן עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן אתחל קערות"
        + " ואחרי כן עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן מצא את המערכה "
        + "בהיות המספר אשר הוא עשרה תחת הדבר אשר במעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן מצא את המערכה שמו מספר"
        + " ואחרי כן עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן צוק טיפה "
        + "בהיות המספר אשר הוא עשרה תחת הדבר אשר במעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן צוק טיפה שמו טיפה "
        + "ובהיות המספר אשר הוא אחד תחת הדבר אשר במעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן צוק טיפה שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מספר הטיפה "
        + "ובהיות ספר מספרים אשר בו כל אשר ב ספר מספרים אשר בו כל אשר ב ספר מספרים אשר בו כל אשר ב ספר מספרים אשר בו כל אשר ב ספר מספרים אשר בו כל אשר ב ספר מספרים אשר אין בו מספר כסדרו ואחר כלם המספר אשר הוא שבעה עשר כסדרו ואחר כלם המספר אשר הוא עשרים ותשעה כסדרו ואחר כלם המספר אשר הוא ארבעים ושלשה כסדרו ואחר כלם המספר אשר הוא שבעים ואחד כסדרו ואחר כלם המספר אשר הוא מאה ואחד תחת הדבר אשר במעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן צוק טיפה שמו אבנים "
        + "ובהיות הספר אשר יצא עתה מן המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן מצא את המערכה תחת הדבר אשר במעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן צוק טיפה שמו מערכה"
    )
    _, obs = three(source)
    assert obs["products"][-1] == ["צוק טיפה", [1571192, 4165752, 32173954]]


def test_d4_post_c56_luach12_only_first_three_positions_receive_pours():
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    body = next(line for line in lines if line.startswith("זה דבר המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן צוק טיפה "))
    assert body.count("עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן חשב ציקה") == 3
    assert "שמו מערכה הוא המספר אשר הוא ארבעה תחת הדבר אשר במעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן חשב ציקה שמו קערה" not in body
    assert "שמו מערכה הוא המספר אשר הוא חמשה תחת הדבר אשר במעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן חשב ציקה שמו קערה" not in body
    assert "שמו מערכה הוא המספר אשר הוא ששה תחת הדבר אשר במעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן חשב ציקה שמו קערה" not in body

def _d4_luach13_preparation() -> str:
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    counters_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מספר המעשה"))
    counters_end = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן סמן המרחק"))
    core_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מכפלה"))
    end = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו פעם ובמקום אשר שמו פעם"))
    selected = lines[0:6] + lines[counters_start:counters_end] + lines[core_start:end]
    return " ".join(
        line for line in selected
        if line.strip() and line.strip() != "---" and not line.lstrip().startswith("#")
    )


def test_d4_post_c56_luach13_one_synthetic_drop_snapshot_mix_three_runtimes():
    from tests.test_c5_6_general_index_surface import three
    stones = "ספר מספרים אשר בו כל אשר ב ספר מספרים אשר בו כל אשר ב ספר מספרים אשר בו כל אשר ב ספר מספרים אשר בו כל אשר ב ספר מספרים אשר בו כל אשר ב ספר מספרים אשר אין בו מספר כסדרו ואחר כלם המספר אשר הוא שבעה עשר כסדרו ואחר כלם המספר אשר הוא עשרים ותשעה כסדרו ואחר כלם המספר אשר הוא ארבעים ושלשה כסדרו ואחר כלם המספר אשר הוא שבעים ואחד כסדרו ואחר כלם המספר אשר הוא מאה ואחד"
    arrangement = "ספר מספרים אשר בו כל אשר ב ספר מספרים אשר בו כל אשר ב ספר מספרים אשר בו כל אשר ב ספר מספרים אשר בו כל אשר ב ספר מספרים אשר בו כל אשר ב ספר מספרים אשר בו כל אשר ב ספר מספרים אשר אין בו מספר כסדרו ואחר כלם המספר אשר הוא אחד כסדרו ואחר כלם המספר אשר הוא שנים כסדרו ואחר כלם המספר אשר הוא ארבעה כסדרו ואחר כלם המספר אשר הוא חמשה כסדרו ואחר כלם המספר אשר הוא ששה כסדרו ואחר כלם המספר אשר הוא שלשה"
    source = (
        _d4_luach13_preparation()
        + " ועתה "
        + _d4_set_luach8_counters()
        + " ואחרי כן עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן חשב המספר הגדול"
        + " ואחרי כן עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן אתחל קערות"
        + " ואחרי כן עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן צוק טיפה "
        + "בהיות המספר אשר הוא עשרה תחת הדבר אשר במעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן צוק טיפה שמו טיפה "
        + "ובהיות המספר אשר הוא אחד תחת הדבר אשר במעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן צוק טיפה שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מספר הטיפה "
        + f"ובהיות {stones} תחת הדבר אשר במעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן צוק טיפה שמו אבנים "
        + f"ובהיות {arrangement} תחת הדבר אשר במעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן צוק טיפה שמו מערכה"
        + " ואחרי כן עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן ערבב טיפה "
        + "בהיות המספר אשר הוא עשרה תחת הדבר אשר במעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן ערבב טיפה שמו טיפה "
        + "ובהיות המספר אשר הוא אחד תחת הדבר אשר במעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן ערבב טיפה שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מספר הטיפה "
        + f"ובהיות {stones} תחת הדבר אשר במעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן ערבב טיפה שמו אבנים "
        + f"ובהיות {arrangement} תחת הדבר אשר במעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן ערבב טיפה שמו מערכה "
        + "ובהיות הספר אשר יצא עתה מן המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן צוק טיפה תחת הדבר אשר במעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן ערבב טיפה שמו ציקות"
    )
    _, obs = three(source)
    assert obs["products"][-1] == ["ערבב טיפה", [
        7504945776187, 45759259889492, 21102184694626,
        1306653888298999, 76949687869500, 24681133270365,
    ]]


def test_d4_post_c56_luach13_snapshot_then_commit_and_exact_46_driver():
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    body = next(line for line in lines if line.startswith("זה דבר המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן ערבב טיפה "))
    assert body.index("שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מלא ישן את הספר אשר במקום אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מלא הקערות") < body.index("עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא ארבעה והמלים הן חשב קערה לאחר הטיפה")
    assert body.count("עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא ארבעה והמלים הן חשב קערה לאחר הטיפה") == 6
    assert body.rindex("שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מלא הקערות") > body.rindex("עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא ארבעה והמלים הן חשב קערה לאחר הטיפה")
    driver = next(line for line in lines if line.startswith("זה דבר המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן ערבב כל הטיפות "))
    assert "ארבעים ושש פעמים עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן קערות הטיפה הבאה" in driver
    step = next(line for line in lines if line.startswith("זה דבר המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן קערות הטיפה הבאה "))
    assert "שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן מערכת הטיפה האחרונה את הספר אשר במקום אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן המערכה הנוכחית" in step



def _d4_nat_book(values: list[int]) -> str:
    from compiler.parse.a15_numerals import format_natural
    book = "ספר מספרים אשר אין בו מספר"
    for value in values:
        book = (
            "ספר מספרים אשר בו כל אשר ב "
            + book
            + " כסדרו ואחר כלם המספר אשר הוא "
            + format_natural(value)
        )
    return book


def _d4_luach14_preparation() -> str:
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    counters_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מספר המעשה"))
    counters_end = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן סמן המרחק"))
    core_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מכפלה"))
    end = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו שם אשר מספר המלים אשר בו הוא חמשה והמלים הן חותם דרך בין שערי קציצה"))
    selected = lines[0:6] + lines[counters_start:counters_end] + lines[core_start:end]
    return " ".join(
        line for line in selected
        if line.strip() and line.strip() != "---" and not line.lstrip().startswith("#")
    )


def _d4_set_bowl_fills(values: list[int]) -> str:
    book = _d4_nat_book(values)
    return (
        "שים במקום אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מלא הקערות את "
        + book
        + " תחת הספר אשר במקום אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מלא הקערות"
    )


def test_d4_post_c56_luach14_one_postfinal_mix_three_runtimes():
    source = (
        _d4_luach14_preparation()
        + " ועתה עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן חשב המספר הגדול"
        + " ואחרי כן " + _d4_set_bowl_fills([1, 2, 3, 4, 5, 6])
        + " ואחרי כן עשה את המעשה אשר שמו בלול"
    )
    _, obs = three(source)
    facts = dict(obs["facts"])
    assert obs["products"][-1] == ["בלול", [3565, 3740, 5518, 1695, 8365, 7674]]
    assert facts["פעם"] == 1
    assert facts["מספר שש הקערות"] == 21
    assert facts["המערכה הנוכחית"] == [2, 4, 1, 3, 6, 5]
    assert facts["מלא הקערות"] == [3565, 3740, 5518, 1695, 8365, 7674]


def _d4_luach14_oracle_mix(fills: list[int], round_number: int) -> list[int]:
    from itertools import permutations

    modulus = (1 << 127) - 1

    def keep(value: int) -> int:
        residue = value % modulus
        return residue if residue else modulus

    snapshot = list(fills)
    bowl_sum = sum(snapshot)
    arrangement_number = keep(149 * round_number + bowl_sum)
    arrangement = list(permutations((1, 2, 3, 4, 5, 6)))[
        (arrangement_number - 1) % 720
    ]
    next_by_identity: dict[int, int] = {}
    for position, bowl_identity in enumerate(arrangement, start=1):
        predecessor = arrangement[(position - 2) % 6]
        successor = arrangement[position % 6]
        before = snapshot[bowl_identity - 1]
        before_predecessor = snapshot[predecessor - 1]
        before_successor = snapshot[successor - 1]
        mixed = (
            before
            + 3 * before_predecessor
            + 5 * before_successor
            + bowl_sum
            + round_number
            + position * position
        )
        next_by_identity[bowl_identity] = keep(
            mixed * mixed + 7 * before_predecessor * before_successor
        )
    return [next_by_identity[i] for i in range(1, 7)]


def test_d4_post_c56_luach14_exact_twelve_oracle_receipt():
    fills = [1, 2, 3, 4, 5, 6]
    for round_number in range(1, 13):
        fills = _d4_luach14_oracle_mix(fills, round_number)

    assert fills == [
        36108001607085984155684996137766958104,
        148814309144118602128584347831122254145,
        146577346212655508303902655220312506515,
        113571227321377053045622633394311758065,
        156703568566579726750728213438464676042,
        87934172320087745809620382672045550969,
    ]


def test_d4_post_c56_luach14_snapshot_commit_identity_and_exact_twelve_structure():
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    mix = next(line for line in lines if line.startswith("זה דבר המעשה אשר שמו בלול "))
    assert mix.index("שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מלא ישן את הספר אשר במקום אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מלא הקערות") < mix.index(
        "עשה את המעשה אשר שמו חשב בהיות"
    )
    assert mix.count("עשה את המעשה אשר שמו חשב בהיות") == 6
    assert mix.rindex("שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן מלא הקערות") > mix.rindex("עשה את המעשה אשר שמו חשב בהיות")
    assert "שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן זוגות מסודרים את הספר הערוך" in mix
    assert "שמו פעם את המספר הנחשב בהוסיף את המספר אשר הוא אחד על המספר אשר במקום אשר שמו פעם" in mix
    driver = next(line for line in lines if line.startswith("זה דבר המעשה אשר שמו גמר "))
    assert driver.index("שמו פעם את המספר הנחשב בגרע") < driver.index(
        "שתים עשרה פעמים עשה את המעשה אשר שמו בלול"
    )
    assert "שתים עשרה פעמים עשה את המעשה אשר שמו בלול" in driver
    assert "שם אשר מספר המלים אשר בו הוא שלשה והמלים הן מערכת הטיפה האחרונה" not in mix
    assert "שם אשר מספר המלים אשר בו הוא שלשה והמלים הן מערכת הטיפה האחרונה" not in driver


def test_d4_post_c56_luach14_uses_counted_source_name_without_welded_alias():
    text = CANDIDATE.read_text(encoding="utf-8")
    counted = "שם אשר מספר המלים אשר בו הוא שלשה והמלים הן מספר שש הקערות"
    assert f"יהי מקום ושמו {counted}" in text
    assert f"המספר אשר במקום אשר שמו {counted}" in text
    assert "מספרששהקערות" not in text


def test_d4_post_c56_luach14_exact_twelve_successive_mixes_three_runtimes():
    source = (
        _d4_luach14_preparation()
        + " ועתה עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן חשב המספר הגדול"
        + " ואחרי כן " + _d4_set_bowl_fills([1, 2, 3, 4, 5, 6])
        + " ואחרי כן עשה את המעשה אשר שמו גמר"
    )
    _, obs = three(source)
    facts = dict(obs["facts"])
    expected = [
        36108001607085984155684996137766958104,
        148814309144118602128584347831122254145,
        146577346212655508303902655220312506515,
        113571227321377053045622633394311758065,
        156703568566579726750728213438464676042,
        87934172320087745809620382672045550969,
    ]
    assert obs["products"][-1] == ["גמר", expected]
    assert facts["פעם"] == 12
    assert facts["מלא הקערות"] == expected


def test_d4_post_c56_luach14_uses_source_authorized_fast_mod_720():
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    mix = next(line for line in lines if line.startswith("זה דבר המעשה אשר שמו בלול "))
    assert "עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן הנותר בדרך הקצרה" in mix
    assert (
        "בהיות המספר אשר הוא שבע מאות ועשרים "
        "תחת הדבר אשר במעשה אשר שמו שם אשר מספר המלים אשר בו הוא שלשה והמלים הן הנותר בדרך הקצרה שמו מחלק"
    ) in mix
    assert "עשה את המעשה אשר שמו שם אשר מספר המלים אשר בו הוא שנים והמלים הן בחר מערכה" not in mix
