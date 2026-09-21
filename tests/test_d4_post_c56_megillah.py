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
    start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מכפלה"))
    end = next(i for i, line in enumerate(lines) if line.startswith("יהי מעשה ושמו רבוע"))
    selected = lines[0:6] + lines[start:end]
    return " ".join(x for x in selected if x.strip() and x.strip() != "---")


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


def test_d4_post_c56_luach3_uses_source_doubling_decomposition_not_linear_repeat_exactly():
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מכפלה"))
    end = next(i for i, line in enumerate(lines) if line.startswith("יהי מעשה ושמו רבוע"))
    text = " ".join(lines[start:end])
    assert "יהי מעשה ושמו כפלרד" in text
    assert "יהי מעשה ושמו כפלבחר" in text
    assert "עשה את המעשה אשר שמו כפלרד" in text
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
    big_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מספרגדול"))
    rem_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו נותרעבודה"))
    preparation = " ".join(
        line for line in lines[0:6] + lines[mul_start:square_start] + lines[big_start:rem_start]
        if line.strip() and line.strip() != "---"
    )
    source = (
        preparation
        + " ועתה עשה את המעשה אשר שמו חשבגדול"
        + " ואחרי כן עשה את המעשה אשר שמו לקחתפעמים "
        + "בהיות המספר אשר הוא שלשה תחת הדבר אשר במעשה אשר שמו לקחתפעמים שמו מספר "
        + "ובהיות המספר אשר במקום אשר שמו מספרגדול תחת הדבר אשר במעשה אשר שמו לקחתפעמים שמו מנין"
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
    assert observed[0]["products"][-1] == ["לקחתפעמים", 3 * ((1 << 127) - 1)]


def _d4_square_preparation() -> str:
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מכפלה"))
    end = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מספרגדול"))
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
    start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מספרגדול"))
    end = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו נותרעבודה"))
    selected = lines[0:6] + lines[start:end]
    return " ".join(x for x in selected if x.strip() and x.strip() != "---")


def test_d4_post_c56_luach5_big_number_exact_three_runtimes():
    from tests.test_c5_6_general_index_surface import three
    source = _d4_big_number_preparation() + " ועתה עשה את המעשה אשר שמו חשבגדול"
    _, obs = three(source)
    want = (1 << 127) - 1
    assert obs["products"][-1] == ["חשבגדול", want]
    assert dict(obs["facts"])["מספרגדול"] == want
    assert dict(obs["facts"])["גדולעבודה"] == (1 << 127)


def test_d4_post_c56_luach5_uses_exact_canonical_127_count_and_persistent_place():
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מספרגדול"))
    end = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו נותרעבודה"))
    text = " ".join(lines[start:end])
    assert "מאה ועשרים ושבע פעמים עשה את המעשה אשר שמו כפלגדול" in text
    assert "שש ועשרים ומאה פעמים" not in text
    assert "שמנה ועשרים ומאה פעמים" not in text
    assert "יהי מקום ושמו מספרגדול" in text

def _d4_luach6_preparation() -> str:
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    big_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מספרגדול"))
    next_section = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו אחעבודה"))
    fast_start = next(i for i, line in enumerate(lines) if line.startswith("זה דבר המעשה אשר שמו נותרמהר "))
    luach7 = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מספרטיפה"))
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
    end = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו אחעבודה"))
    text = " ".join(lines[start:end])
    assert "וכן תעשה עד אשר המספר אשר במקום אשר שמו נותרמחלק רב מן המספר אשר במקום אשר שמו נותרעבודה" in text
    assert "אם המספר אשר במקום אשר שמו נותרמחלק רב מן המספר אשר במקום אשר שמו נותרעבודה" in text
    assert "יהי מעשה ושמו נותר" in text
    assert "יהי מעשה ושמו שמור" in text

def _d4_luach6_wrapped_subtraction_preparation() -> str:
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    big_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מספרגדול"))
    luach7 = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מספרטיפה"))
    selected = lines[0:6] + lines[big_start:luach7]
    return " ".join(
        line for line in selected
        if line.strip() and line.strip() != "---" and not line.lstrip().startswith("#")
    )


def _d4_wrapped_subtraction_call(subtrahend: str, sibling: str) -> str:
    return (
        "עשה את המעשה אשר שמו לקחתמאחיו "
        f"בהיות {subtrahend} תחת הדבר אשר במעשה אשר שמו לקחתמאחיו שמו מחסר "
        f"ובהיות {sibling} תחת הדבר אשר במעשה אשר שמו לקחתמאחיו שמו אחמספר"
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
            + " ועתה עשה את המעשה אשר שמו חשבגדול"
            + " ואחרי כן "
            + _d4_wrapped_subtraction_call(subtrahend, sibling)
        )
        _, obs = three(source)
        assert obs["products"][-1] == ["לקחתמאחיו", want]


def test_d4_post_c56_luach6_wrapped_subtraction_equal_maps_through_keep():
    from tests.test_c5_6_general_index_surface import three
    prep = _d4_luach6_wrapped_subtraction_preparation()
    source = (
        prep
        + " ועתה עשה את המעשה אשר שמו חשבגדול"
        + " ואחרי כן "
        + _d4_wrapped_subtraction_call("המספר אשר הוא שבעה", "המספר אשר הוא שבעה")
    )
    _, obs = three(source)
    assert obs["products"][-1] == ["לקחתמאחיו", (1 << 127) - 1]


def test_d4_post_c56_luach6_wrapped_subtraction_repeats_modulus_addition_as_needed():
    from tests.test_c5_6_general_index_surface import three
    prep = _d4_luach6_wrapped_subtraction_preparation()
    add_two_moduli = (
        "עשה את המעשה אשר שמו חיבור "
        "בהיות המספר אשר במקום אשר שמו מספרגדול תחת הדבר אשר במעשה אשר שמו חיבור שמו ראשון "
        "ובהיות המספר אשר במקום אשר שמו מספרגדול תחת הדבר אשר במעשה אשר שמו חיבור שמו שני"
    )
    source = (
        prep
        + " ועתה עשה את המעשה אשר שמו חשבגדול"
        + " ואחרי כן "
        + add_two_moduli
        + " ואחרי כן "
        + _d4_wrapped_subtraction_call(
            "המספר אשר יצא עתה מן המעשה אשר שמו חיבור",
            "המספר אשר הוא אחד",
        )
    )
    _, obs = three(source)
    assert obs["products"][-1] == ["לקחתמאחיו", 1]


def test_d4_post_c56_luach6_wrapped_subtraction_never_uses_underflow_as_control():
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו אחעבודה"))
    end = next(i for i, line in enumerate(lines) if line.startswith("זה דבר המעשה אשר שמו נותרמהר "))
    text = " ".join(lines[start:end])
    assert "אחמחסר רב מן המספר אשר במקום אשר שמו אחעבודה" in text
    assert "עשה את המעשה אשר שמו אחהוסף" in text
    assert "המספר הנחשב בגרע את המספר אשר במקום אשר שמו אחמחסר מן המספר אשר במקום אשר שמו אחעבודה" in text
    assert "עשה את המעשה אשר שמו שמור" in text

def _d4_fast_remainder_call(value: str, divisor: str) -> str:
    return (
        "עשה את המעשה אשר שמו נותרמהר "
        f"בהיות {value} תחת הדבר אשר במעשה אשר שמו נותרמהר שמו מספר "
        f"ובהיות {divisor} תחת הדבר אשר במעשה אשר שמו נותרמהר שמו מחלק"
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
        assert obs["products"][-1] == ["נותרמהר", want]


def test_d4_post_c56_luach6_fast_remainder_handles_large_natural_by_doubling():
    from compiler.parse.a15_numerals import format_natural
    from tests.test_c5_6_general_index_surface import three
    prep = _d4_luach6_wrapped_subtraction_preparation()
    value = f"המספר אשר הוא {format_natural(99_999_999)}"
    divisor = f"המספר אשר הוא {format_natural(97)}"
    source = prep + " ועתה " + _d4_fast_remainder_call(value, divisor)
    _, obs = three(source)
    assert obs["products"][-1] == ["נותרמהר", 80]


def test_d4_post_c56_luach6_fast_remainder_is_recursive_doubling_greedy_not_linear_subtraction():
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("זה דבר המעשה אשר שמו נותרמהר "))
    end = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מספרטיפה"))
    text = " ".join(lines[start:end])
    assert "עשה את המעשה אשר שמו חיבור" in text
    assert text.count("שמו מחלק תחת הדבר אשר במעשה אשר שמו חיבור") >= 2
    assert "עשה את המעשה אשר שמו נותרמהר" in text
    assert "המספר הנחשב בגרע" in text
    assert "עשה את המעשה אשר שמו נותרגרע" not in text


def test_d4_post_c56_luach6_keep_uses_fast_remainder_without_hidden_threshold():
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    keep = next(line for line in lines if line.startswith("זה דבר המעשה אשר שמו שמור "))
    assert "עשה את המעשה אשר שמו נותרמהר" in keep
    assert "עשה את המעשה אשר שמו נותר " not in keep

def _d4_luach7_preparation() -> str:
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מכפלה"))
    end = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו נסתרתאחת"))
    selected = lines[0:6] + lines[start:end]
    return " ".join(
        line for line in selected
        if line.strip() and line.strip() != "---" and not line.lstrip().startswith("#")
    )


def test_d4_post_c56_luach7_first_transition_uses_only_old_stone_snapshot():
    from tests.test_c5_6_general_index_surface import three
    source = (
        _d4_luach7_preparation()
        + " ועתה עשה את המעשה אשר שמו חשבגדול"
        + " ואחרי כן עשה את המעשה אשר שמו טיפההבאה"
    )
    _, obs = three(source)
    facts = dict(obs["facts"])
    expected = [378, 1073, 2375, 6195, 10493]
    assert facts["מספרטיפה"] == 2
    assert [facts[x] for x in ["חיטהישנה","שעורהישנה","מלחישנה","מרהישנה","אדומהישנה"]] == expected
    assert [facts[x] for x in ["חיטהחדשה","שעורהחדשה","מלחחדשה","מרהחדשה","אדומהחדשה"]] == expected
    assert facts["אבניטיפות"] == [[17,29,43,71,101], expected]


def test_d4_post_c56_luach7_builds_exact_46_drop_table_three_runtimes_with_fuel():
    from compiler.api import compile_source
    from compiler.backend.portable import execute_ir
    from compiler.runtime.ir_reference import execute_reference_ir
    from compiler.runtime.observables import backend_observable, ir_reference_observable, reference_observable
    from compiler.runtime.reference import execute_reference

    source = (
        _d4_luach7_preparation()
        + " ועתה עשה את המעשה אשר שמו חשבגדול"
        + " ואחרי כן עשה את המעשה אשר שמו בנהאבנים"
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
    table = facts["אבניטיפות"]
    assert facts["מספרטיפה"] == 46
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
    start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מספרטיפה"))
    end = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו נסתרתאחת"))
    text = " ".join(lines[start:end])
    assert "ארבעים וחמש פעמים עשה את המעשה אשר שמו טיפההבאה" in text
    assert "שש וארבעים" not in text
    body = next(line for line in lines if line.startswith("זה דבר המעשה אשר שמו טיפההבאה "))
    assert body.index("שמו אדומהחדשה") < body.index("שמו חיטהישנה את המספר אשר במקום אשר שמו חיטהחדשה")
    assert "ספר ספרי מספרים" in text

def _d4_luach8_preparation() -> str:
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    counters_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מספרמעשה"))
    counters_end = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מרחקסמן"))
    core_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מכפלה"))
    luach9 = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מספרטיפהגלויה"))
    selected = lines[0:6] + lines[counters_start:counters_end] + lines[core_start:luach9]
    return " ".join(
        line for line in selected
        if line.strip() and line.strip() != "---" and not line.lstrip().startswith("#")
    )


def _d4_set_luach8_counters() -> str:
    return " ואחרי כן ".join([
        "שים במקום אשר שמו מספרמעשה את המספר אשר הוא שנים תחת המספר אשר במקום אשר שמו מספרמעשה",
        "שים במקום אשר שמו מספרשאלה את המספר אשר הוא שלשה תחת המספר אשר במקום אשר שמו מספרשאלה",
        "שים במקום אשר שמו מספרמרחק את המספר אשר הוא ארבעה תחת המספר אשר במקום אשר שמו מספרמרחק",
        "שים במקום אשר שמו מספרחיבור את המספר אשר הוא חמשה תחת המספר אשר במקום אשר שמו מספרחיבור",
        "שים במקום אשר שמו מספרדרך את המספר אשר הוא אחד תחת המספר אשר במקום אשר שמו מספרדרך",
    ])


def test_d4_post_c56_luach8_seven_hidden_drops_exact_three_runtimes():
    from tests.test_c5_6_general_index_surface import three
    source = (
        _d4_luach8_preparation()
        + " ועתה "
        + _d4_set_luach8_counters()
        + " ואחרי כן עשה את המעשה אשר שמו חשבגדול"
        + " ואחרי כן שש פעמים עשה את המעשה אשר שמו טיפההבאה"
        + " ואחרי כן עשה את המעשה אשר שמו בנהנסתרות"
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
    names = ["נסתרתאחת","נסתרתשנית","נסתרתשלישית","נסתרתרביעית","נסתרתחמישית","נסתרתששית","נסתרתשביעית"]
    assert [facts[x] for x in names] == expected
    assert facts["טיפותנסתרות"] == list(reversed(expected))
    assert obs["products"][-1] == ["בנהנסתרות", list(reversed(expected))]


def test_d4_post_c56_luach8_grind_stone_sequence_is_explicit_seven_steps():
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    body = next(line for line in lines if line.startswith("זה דבר המעשה אשר שמו טחןנסתרת "))
    assert body.count("עשה את המעשה אשר שמו טחןפעם") == 7
    positions = [
        "המספר אשר הוא אחד", "המספר אשר הוא שנים", "המספר אשר הוא שלשה",
        "המספר אשר הוא ארבעה", "המספר אשר הוא חמשה",
        "המספר אשר הוא אחד", "המספר אשר הוא שנים",
    ]
    cursor = -1
    for position in positions:
        cursor = body.index(position, cursor + 1)
    assert "שבעה פעמים עשה את המעשה אשר שמו טחןפעם" not in body


def test_d4_post_c56_luach8_hidden_order_is_seven_to_one_for_predecessor_history():
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    body = next(line for line in lines if line.startswith("זה דבר המעשה אשר שמו בנהנסתרות "))
    order = ["נסתרתשביעית","נסתרתששית","נסתרתחמישית","נסתרתרביעית","נסתרתשלישית","נסתרתשנית","נסתרתאחת"]
    cursor = body.index("ספר מספרים אשר אין בו מספר")
    for name in order:
        cursor = body.index(f"המספר אשר במקום אשר שמו {name}", cursor + 1)

def _d4_luach9_preparation() -> str:
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    counters_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מספרמעשה"))
    counters_end = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מרחקסמן"))
    core_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מכפלה"))
    luach10 = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מלאעבודה"))
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
        + " ואחרי כן עשה את המעשה אשר שמו חשבגדול"
        + " ואחרי כן עשה את המעשה אשר שמו בנהאבנים"
        + " ואחרי כן עשה את המעשה אשר שמו בנהנסתרות"
        + " ואחרי כן עשה את המעשה אשר שמו בנהטיפות"
    )
    _, obs = three(source)
    facts = dict(obs["facts"])
    expected_first = [
        123334831551511603687649975447681761062,
        156673085926334718073075063360231111300,
        154047674952282304836724395515854998098,
        63342935234911242715034474012998539443,
    ]
    assert facts["מספרטיפהגלויה"] == 46
    assert len(facts["טיפותגלויות"]) == 46
    assert facts["טיפותגלויות"][:4] == expected_first
    assert facts["טיפותגלויות"][-1] == 45970703249572047980738520652128782598
    assert len(facts["כלטיפות"]) == 53
    assert facts["כלטיפות"][-46:] == facts["טיפותגלויות"]


def test_d4_post_c56_luach9_predecessor_offsets_and_eleven_rounds_are_explicit():
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    step = next(line for line in lines if line.startswith("זה דבר המעשה אשר שמו עשהטיפהגלויה "))
    assert "המספר האחרון אשר בתוך הספר אשר במקום אשר שמו כלטיפות" in step
    assert "בגרע את המספר אשר הוא שנים מן מספר הדברים אשר בתוך הספר אשר במקום אשר שמו כלטיפות" in step
    assert "בגרע את המספר אשר הוא ששה מן מספר הדברים אשר בתוך הספר אשר במקום אשר שמו כלטיפות" in step
    grind = next(line for line in lines if line.startswith("זה דבר המעשה אשר שמו טחןטיפה "))
    assert grind.count("עשה את המעשה אשר שמו טחןטיפהפעם") == 11
    assert "ארבעים ושש פעמים עשה את המעשה אשר שמו עשהטיפהגלויה" in next(
        line for line in lines if line.startswith("זה דבר המעשה אשר שמו בנהטיפות ")
    )

def _d4_luach10_preparation() -> str:
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    counters_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מספרמעשה"))
    counters_end = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מרחקסמן"))
    core_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מכפלה"))
    luach11 = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו חלקעבודה"))
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
        + " ואחרי כן עשה את המעשה אשר שמו חשבגדול"
        + " ואחרי כן עשה את המעשה אשר שמו אתחלקערות"
    )
    _, obs = three(source)
    facts = dict(obs["facts"])
    assert facts["מלאקערות"] == [92417, 143643, 302503, 748229, 976149, 1957207]
    assert obs["products"][-1] == ["אתחלקערות", [92417, 143643, 302503, 748229, 976149, 1957207]]


def test_d4_post_c56_luach10_six_fixed_bowl_identities_and_primes_are_explicit():
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    body = next(line for line in lines if line.startswith("זה דבר המעשה אשר שמו אתחלקערות "))
    for numeral in ["אחד","שנים","שלשה","ארבעה","חמשה","ששה"]:
        assert f"המספר אשר הוא {numeral}" in body
    for prime in ["שבעה עשר","תשעה עשר","עשרים ושלשה","עשרים ותשעה","שלשים ואחד","שלשים ושבעה"]:
        assert f"המספר אשר הוא {prime}" in body
    assert body.count("עשה את המעשה אשר שמו חשבמלאקערה") == 6

def _d4_luach11_preparation() -> str:
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    counters_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מספרמעשה"))
    counters_end = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מרחקסמן"))
    core_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מכפלה"))
    luach12 = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו ציקהעבודה"))
    selected = lines[0:6] + lines[counters_start:counters_end] + lines[core_start:luach12]
    return " ".join(
        line for line in selected
        if line.strip() and line.strip() != "---" and not line.lstrip().startswith("#")
    )


def _d4_find_arrangement_call(n: int) -> str:
    from compiler.parse.a15_numerals import format_natural
    return (
        "עשה את המעשה אשר שמו מצאמערכה "
        f"בהיות המספר אשר הוא {format_natural(n)} תחת הדבר אשר במעשה אשר שמו מצאמערכה שמו מספר"
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
        assert obs["products"][-1] == ["מצאמערכה", want]


def test_d4_post_c56_luach11_arrangement_number_wraps_721_to_one():
    from tests.test_c5_6_general_index_surface import three
    source = (
        _d4_luach11_preparation()
        + " ועתה עשה את המעשה אשר שמו בחרמערכה "
        + "בהיות המספר אשר הוא שבע מאות ועשרים ואחד תחת הדבר אשר במעשה אשר שמו בחרמערכה שמו מספר"
    )
    _, obs = three(source)
    assert obs["products"][-1] == ["בחרמערכה", [1,2,3,4,5,6]]
    assert dict(obs["facts"])["מערכהנוכחית"] == [1,2,3,4,5,6]


def test_d4_post_c56_luach11_bowl_position_is_distinct_from_identity():
    from tests.test_c5_6_general_index_surface import three
    source = (
        _d4_luach11_preparation()
        + " ועתה " + _d4_find_arrangement_call(100)
        + " ואחרי כן עשה את המעשה אשר שמו מקוםקערה "
        + "בהיות המספר אשר הוא ששה תחת הדבר אשר במעשה אשר שמו מקוםקערה שמו קערה "
        + "ובהיות הספר אשר יצא עתה מן המעשה אשר שמו מצאמערכה תחת הדבר אשר במעשה אשר שמו מקוםקערה שמו מערכה"
    )
    _, obs = three(source)
    assert obs["products"][-1] == ["מקוםקערה", 2]


def test_d4_post_c56_luach11_factor_blocks_are_exact_source_short_way():
    text = CANDIDATE.read_text(encoding="utf-8")
    for n in ["מאה ועשרים","עשרים וארבעה","ששה","שנים","אחד"]:
        assert f"בהיות המספר אשר הוא {n} תחת הדבר אשר במעשה אשר שמו חלק שמו מחלק" in text
    assert "שבע מאות ועשרים" in text

def _d4_luach12_preparation() -> str:
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    counters_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מספרמעשה"))
    counters_end = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מרחקסמן"))
    core_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מכפלה"))
    end = next(i for i, line in enumerate(lines) if line.startswith("# לוח שלשה עשר: לבלול את שש הקערות אחר הטיפה"))
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
        + " ואחרי כן עשה את המעשה אשר שמו חשבגדול"
        + " ואחרי כן עשה את המעשה אשר שמו אתחלקערות"
        + " ואחרי כן עשה את המעשה אשר שמו מצאמערכה "
        + "בהיות המספר אשר הוא עשרה תחת הדבר אשר במעשה אשר שמו מצאמערכה שמו מספר"
        + " ואחרי כן עשה את המעשה אשר שמו צוקטיפה "
        + "בהיות המספר אשר הוא עשרה תחת הדבר אשר במעשה אשר שמו צוקטיפה שמו טיפה "
        + "ובהיות המספר אשר הוא אחד תחת הדבר אשר במעשה אשר שמו צוקטיפה שמו מספרטיפה "
        + "ובהיות ספר מספרים אשר בו כל אשר ב ספר מספרים אשר בו כל אשר ב ספר מספרים אשר בו כל אשר ב ספר מספרים אשר בו כל אשר ב ספר מספרים אשר בו כל אשר ב ספר מספרים אשר אין בו מספר כסדרו ואחר כלם המספר אשר הוא שבעה עשר כסדרו ואחר כלם המספר אשר הוא עשרים ותשעה כסדרו ואחר כלם המספר אשר הוא ארבעים ושלשה כסדרו ואחר כלם המספר אשר הוא שבעים ואחד כסדרו ואחר כלם המספר אשר הוא מאה ואחד תחת הדבר אשר במעשה אשר שמו צוקטיפה שמו אבנים "
        + "ובהיות הספר אשר יצא עתה מן המעשה אשר שמו מצאמערכה תחת הדבר אשר במעשה אשר שמו צוקטיפה שמו מערכה"
    )
    _, obs = three(source)
    assert obs["products"][-1] == ["צוקטיפה", [1571192, 4165752, 32173954]]


def test_d4_post_c56_luach12_only_first_three_positions_receive_pours():
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    body = next(line for line in lines if line.startswith("זה דבר המעשה אשר שמו צוקטיפה "))
    assert body.count("עשה את המעשה אשר שמו חשבציקה") == 3
    assert "המספר אשר הוא ארבעה" not in body
    assert "המספר אשר הוא חמשה" not in body
    assert "המספר אשר הוא ששה" not in body

