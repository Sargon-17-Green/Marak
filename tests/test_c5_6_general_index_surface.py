from __future__ import annotations

from compiler.api import compile_source
from compiler.backend.portable import execute_ir
from compiler.models.values import BidirectionalIndexValue
from compiler.parse.a15_numerals import format_feminine_count
from compiler.runtime.invocation import InputBinding
from compiler.runtime.ir_reference import execute_reference_ir
from compiler.runtime.observables import (
    backend_observable,
    ir_reference_observable,
    reference_observable,
)
from compiler.runtime.reference import execute_reference
from tests.test_c5_2_surface_pipeline import (
    act,
    body,
    current,
    idx_place,
    idx_recent,
    idx_role,
    num,
    output,
    perform,
    perform_one,
    place_nat,
    place_typed,
    replace_idx,
    replace_nat,
    role_idx,
)


def general_index(z: int) -> str:
    if z == 0:
        return "מעלת היתד"
    before = z < 0
    n = abs(z)
    rel = "לפני" if before else "אחרי"
    if n == 1:
        return f"מעלה אחת {rel} מעלת היתד"
    if n == 2:
        return f"שתי מעלות {rel} מעלת היתד"
    return f"{format_feminine_count(n)} מעלות {rel} מעלת היתד"


def year_index(z: int) -> str:
    if z == 0:
        return "שנת אין"
    before = z < 0
    n = abs(z)
    rel = "לפני" if before else "אחרי"
    if n == 1:
        return f"שנה אחת {rel} שנת אין"
    if n == 2:
        return f"שתי שנים {rel} שנת אין"
    return f"{format_feminine_count(n)} שנים {rel} שנת אין"


def general_place(place: str) -> str:
    return f"המעלה אשר במקום אשר שמו {place}"


def replace_general(place: str, value: str) -> str:
    return (
        f"שים במקום אשר שמו {place} את {value} "
        f"תחת המעלה אשר במקום אשר שמו {place}"
    )


def general_role_decl(act_name: str, role: str) -> str:
    return (
        f"יהי במעשה אשר שמו {act_name} דבר ושמו {role} "
        f"ובעשות את המעשה אשר שמו {act_name} תעמד מעלה "
        f"תחת הדבר אשר במעשה אשר שמו {act_name} שמו {role}"
    )


def general_role(act_name: str, role: str) -> str:
    return (
        f"המעלה אשר במעשה הזה עומדת תחת הדבר אשר במעשה "
        f"אשר שמו {act_name} שמו {role}"
    )


def general_recent(act_name: str) -> str:
    return f"המעלה אשר יצאה עתה מן המעשה אשר שמו {act_name}"


def general_succ(value: str) -> str:
    return f"המעלה אשר אחר {value}"


def general_pred(value: str) -> str:
    return f"המעלה אשר לפני {value}"


def index_lt(left: str, right: str) -> str:
    return f"{left} לפני {right}"


def input_year(role: str) -> str:
    return (
        f"יהי למלאכה הזאת דבר ושמו {role} ובטרם תחל המלאכה הזאת "
        f"יעמד מספר שנה תחת הדבר אשר למלאכה הזאת שמו {role}"
    )


def input_general(role: str) -> str:
    return (
        f"יהי למלאכה הזאת דבר ושמו {role} ובטרם תחל המלאכה הזאת "
        f"תעמד מעלה תחת הדבר אשר למלאכה הזאת שמו {role}"
    )


def input_year_ref(role: str) -> str:
    return f"מספר השנה אשר עומד תחת הדבר אשר למלאכה הזאת שמו {role}"


def input_general_ref(role: str) -> str:
    return f"המעלה אשר עומדת תחת הדבר אשר למלאכה הזאת שמו {role}"


def input_id(compiled, spelling: str):
    return next(
        x.input_id for x in compiled.ir.program_input_domains
        if x.input_id.spelling == spelling
    )


def three(source: str, bindings=()):
    compiled = compile_source(source)
    assert compiled.valid, [d.to_dict() for d in compiled.diagnostics]
    h = reference_observable(execute_reference(compiled.hast, bindings=bindings))
    i = ir_reference_observable(execute_reference_ir(compiled.ir, bindings=bindings))
    b = backend_observable(execute_ir(compiled.ir, bindings=bindings))
    assert h == i == b
    return compiled, b


def test_year_and_general_literals_are_same_semantic_index_values():
    for z in (-17, -2, -1, 0, 1, 2, 17):
        ysrc = " ".join([
            place_typed("מקום", year_index(z)),
            "ועתה " + replace_idx("מקום", idx_place("מקום")),
        ])
        gsrc = " ".join([
            place_typed("מקום", general_index(z)),
            "ועתה " + replace_general("מקום", general_place("מקום")),
        ])
        _, y = three(ysrc)
        _, g = three(gsrc)
        assert y["facts"] == g["facts"]


def test_cross_profile_place_current_and_replacement_are_admitted():
    src1 = " ".join([
        place_typed("מקום", year_index(-3)),
        "ועתה " + replace_general("מקום", general_place("מקום")),
    ])
    src2 = " ".join([
        place_typed("מקום", general_index(4)),
        "ועתה " + replace_idx("מקום", idx_place("מקום")),
    ])
    _, a = three(src1)
    _, b = three(src2)
    assert dict(a["facts"])["מקום"] == {"index": "BeforeZero", "magnitude": 3}
    assert dict(b["facts"])["מקום"] == {"index": "AfterZero", "magnitude": 4}


def test_cross_profile_role_flow_in_both_directions():
    act_name, role, target = "מעביר", "ערך", "יעד"
    generic_decl = " ".join([
        place_typed(target, general_index(0)),
        act(act_name),
        general_role_decl(act_name, role),
        body(act_name, output(idx_role(act_name, role))),
        "ועתה " + perform_one(act_name, role, year_index(-2)) +
        " ואחרי כן " + replace_general(target, general_recent(act_name)),
    ])
    year_decl = " ".join([
        place_typed(target, year_index(0)),
        act(act_name),
        role_idx(act_name, role),
        body(act_name, output(general_role(act_name, role))),
        "ועתה " + perform_one(act_name, role, general_index(3)) +
        " ואחרי כן " + replace_idx(target, idx_recent(act_name)),
    ])
    _, a = three(generic_decl)
    _, b = three(year_decl)
    assert dict(a["facts"])[target] == {"index": "BeforeZero", "magnitude": 2}
    assert dict(b["facts"])[target] == {"index": "AfterZero", "magnitude": 3}


def test_cross_profile_program_input_declaration_and_read():
    role, target = "קלט", "יעד"
    for declaration, reference, value in (
        (input_general(role), input_year_ref(role), BidirectionalIndexValue("before", 5)),
        (input_year(role), input_general_ref(role), BidirectionalIndexValue("after", 6)),
    ):
        src = " ".join([
            declaration,
            place_typed(target, reference),
            "ועתה " + replace_idx(target, idx_place(target)),
        ])
        compiled = compile_source(src)
        assert compiled.valid, [d.to_dict() for d in compiled.diagnostics]
        binding = (InputBinding(input_id(compiled, role), value),)
        h = reference_observable(execute_reference(compiled.hast, bindings=binding))
        i = ir_reference_observable(execute_reference_ir(compiled.ir, bindings=binding))
        b = backend_observable(execute_ir(compiled.ir, bindings=binding))
        assert h == i == b
        assert b["outcome"] == "Normal"


def test_cross_profile_output_and_immediate_result_both_directions():
    act_name, target = "פולט", "יעד"
    general_to_year = " ".join([
        place_typed(target, year_index(0)),
        act(act_name), body(act_name, output(general_index(-4))),
        "ועתה " + perform(act_name) + " ואחרי כן " +
        replace_idx(target, idx_recent(act_name)),
    ])
    year_to_general = " ".join([
        place_typed(target, general_index(0)),
        act(act_name), body(act_name, output(year_index(4))),
        "ועתה " + perform(act_name) + " ואחרי כן " +
        replace_general(target, general_recent(act_name)),
    ])
    _, a = three(general_to_year)
    _, b = three(year_to_general)
    assert dict(a["facts"])[target] == {"index": "BeforeZero", "magnitude": 4}
    assert dict(b["facts"])[target] == {"index": "AfterZero", "magnitude": 4}


def test_generic_succ_pred_cross_zero_and_accept_mixed_profile_operands():
    target = "יעד"
    src = " ".join([
        place_typed(target, general_index(-1)),
        "ועתה " + replace_general(target, general_succ(year_index(-1))) +
        " ואחרי כן " + replace_idx(target, general_succ(general_index(0))) +
        " ואחרי כן " + replace_general(target, general_pred(year_index(1))),
    ])
    _, obs = three(src)
    assert dict(obs["facts"])[target] == {"index": "Zero"}


def test_strict_index_order_grid_matches_b13_total_order():
    for a, b in (
        (-9, -3), (-3, -9), (-1, 0), (-1, 7),
        (0, -1), (0, 0), (0, 1), (8, 3), (3, 8), (5, 5),
    ):
        flag = "דגל"
        src = " ".join([
            place_nat(flag, 2),
            "ועתה אם " + index_lt(general_index(a), year_index(b)) +
            " " + replace_nat(flag, num(1)) +
            " ואם לא " + replace_nat(flag, num(2)),
        ])
        _, obs = three(src)
        assert dict(obs["facts"])[flag] == (1 if a < b else 2)


def test_same_position_classification_uses_two_strict_order_tests_and_named_act():
    def source(a: int, b: int) -> str:
        left, right, flag = "א", "ב", "דגל"
        before, after, same, decide = "קודם", "אחר", "זהה", "הכרע"
        decide_body = (
            "אם " + index_lt(general_place(right), idx_place(left)) +
            " " + perform(after) + " ואם לא " + perform(same)
        )
        top = (
            "אם " + index_lt(idx_place(left), general_place(right)) +
            " " + perform(before) + " ואם לא " + perform(decide)
        )
        return " ".join([
            place_typed(left, general_index(a)),
            place_typed(right, year_index(b)),
            place_nat(flag, 9),
            act(before), body(before, replace_nat(flag, num(1))),
            act(after), body(after, replace_nat(flag, num(2))),
            act(same), body(same, replace_nat(flag, num(3))),
            act(decide), body(decide, decide_body),
            "ועתה " + top,
        ])
    for a, b, expected in [(-2, 5, 1), (5, -2, 2), (4, 4, 3)]:
        _, obs = three(source(a, b))
        assert dict(obs["facts"])["דגל"] == expected


def test_existing_year_oriented_index_collection_accepts_general_index_value_items():
    from tests.test_c5_3_collections import append_idx, empty_idx, place_book
    src = " ".join([
        place_book("ספר", append_idx(empty_idx(), general_index(6))),
        "ועתה " + replace_nat("דגל", num(1)),
    ])
    # Add an ordinary Natural place only so Principal has a visible harmless action.
    src = place_nat("דגל", 0 + 1) + " " + src
    _, obs = three(src)
    assert dict(obs["facts"])["ספר"] == [{"index": "AfterZero", "magnitude": 6}]


def _zero_natural() -> str:
    return f"המספר הנחשב בגרע את {num(1)} מן {num(1)}"


def _increment_natural(place: str) -> str:
    return (
        f"המספר הנחשב בהוסיף את {num(1)} על {current(place)}"
    )


def distance_source(start: int, target_value: int) -> str:
    cursor, target, counter = "סמן", "יעד", "מונה"
    decide, decide_back = "הכרע", "הכרעאחור"
    forward, backward = "קדימה", "אחורה"
    forward_step, backward_step, done = "צעדקדימה", "צעדאחורה", "סיום"

    forward_test = index_lt(general_place(cursor), idx_place(target))
    backward_test = index_lt(idx_place(target), general_place(cursor))

    decide_body = (
        f"אם {forward_test} {perform(forward)} ואם לא {perform(decide_back)}"
    )
    decide_back_body = (
        f"אם {backward_test} {perform(backward)} ואם לא {perform(done)}"
    )
    forward_body = (
        f"אם {forward_test} {perform(forward_step)} ואם לא {perform(done)}"
    )
    backward_body = (
        f"אם {backward_test} {perform(backward_step)} ואם לא {perform(done)}"
    )
    forward_step_body = " ואחרי כן ".join([
        replace_general(cursor, general_succ(general_place(cursor))),
        replace_nat(counter, _increment_natural(counter)),
        perform(forward),
    ])
    backward_step_body = " ואחרי כן ".join([
        replace_idx(cursor, general_pred(idx_place(cursor))),
        replace_nat(counter, _increment_natural(counter)),
        perform(backward),
    ])

    counter_intro = (
        f"יהי מקום ושמו {counter} ובמקום אשר שמו {counter} "
        f"יהי {_zero_natural()} לבדו"
    )
    return " ".join([
        place_typed(cursor, general_index(start)),
        place_typed(target, year_index(target_value)),
        counter_intro,
        act(decide), act(decide_back), act(forward), act(backward),
        act(forward_step), act(backward_step), act(done),
        body(decide, decide_body),
        body(decide_back, decide_back_body),
        body(forward, forward_body),
        body(backward, backward_body),
        body(forward_step, forward_step_body),
        body(backward_step, backward_step_body),
        body(done, replace_nat(counter, current(counter))),
        "ועתה " + perform(decide),
    ])


def test_constructive_distance_is_composed_without_distance_or_index_equality_surface():
    for start, target, expected in [(-2, 2, 4), (2, -2, 4), (3, 3, 0)]:
        _, obs = three(distance_source(start, target))
        assert dict(obs["facts"])["מונה"] == expected
