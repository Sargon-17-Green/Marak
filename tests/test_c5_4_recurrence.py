from __future__ import annotations

from compiler.api import compile_source, parse
from compiler.backend.portable import execute_ir
from compiler.parse.a15_numerals import format_feminine_count
from compiler.runtime.ir_reference import execute_reference_ir
from compiler.runtime.observables import backend_observable, ir_reference_observable, reference_observable
from compiler.runtime.reference import execute_reference
from compiler.models.hast import HastRepeatExactly
from compiler.models.ir import IRRepeatExactly
from tests.test_c5_2_surface_pipeline import (
    act, body, current, idx_role, num, output, perform, place_nat, replace_nat,
    role_idx,
)
from tests.test_c5_3_collections import (
    append_nat, book_place, count, empty_nat, nat_book, place_book, replace_book,
)


def add(a: str, b: str) -> str:
    return f"המספר הנחשב בהוסיף את {a} על {b}"


def subtract(amount: str, source: str) -> str:
    return f"המספר הנחשב בגרע את {amount} מן {source}"


def as_count(number_value: str) -> str:
    if number_value.startswith("המספר"):
        return "כמספר" + number_value[len("המספר"):]
    if number_value.startswith("מספר"):
        return "כמספר" + number_value[len("מספר"):]
    raise AssertionError(number_value)


def repeat_dynamic(number_value: str, action: str) -> str:
    return f"פעמים {as_count(number_value)} {action}"


def repeat_literal(n: int, action: str) -> str:
    if n == 1:
        return f"פעם אחת {action}"
    if n == 2:
        return f"שתי פעמים {action}"
    return f"{format_feminine_count(n)} פעמים {action}"


def increment(place: str, amount: int = 1) -> str:
    return replace_nat(place, add(num(amount), current(place)))


def zero() -> str:
    return subtract(num(1), num(1))


def three(source: str, *, fuel: int | None = None):
    c=compile_source(source)
    assert c.valid,[d.to_dict() for d in c.diagnostics]
    assert c.hast is not None and c.ir is not None
    h=reference_observable(execute_reference(c.hast,fuel=fuel))
    i=ir_reference_observable(execute_reference_ir(c.ir,fuel=fuel))
    b=backend_observable(execute_ir(c.ir,fuel=fuel))
    assert h==i==b
    return c,b


def test_literal_one_two_many_and_large_admitted_counts_source_first():
    for n in (1,2,3,7,10,1000):
        src=" ".join([place_nat("מונה",1),"ועתה "+repeat_literal(n,increment("מונה"))])
        c,obs=three(src)
        assert dict(obs["facts"])["מונה"]==1+n
        assert isinstance(c.hast.principal,HastRepeatExactly)
        assert isinstance(c.ir.principal,IRRepeatExactly)


def test_dynamic_current_place_count_is_evaluated_once_while_body_mutates_that_place():
    # Entry count is 3. Re-evaluating after each iteration would never terminate,
    # because the body increments the very place that supplied the count.
    src=" ".join([
        place_nat("מנין",3),
        "ועתה "+repeat_dynamic(current("מנין"),increment("מנין")),
    ])
    c,obs=three(src)
    assert dict(obs["facts"])["מנין"]==6
    assert isinstance(c.ir.principal,IRRepeatExactly)


def test_computed_dynamic_count_is_evaluated_once_over_two_mutable_places():
    a,b="אלף","בית"
    worker="משנה"
    work=increment(a)+" ואחרי כן "+increment(b)
    src=" ".join([
        place_nat(a,2),place_nat(b,1),act(worker),body(worker,work),
        "ועתה "+repeat_dynamic(add(current(a),current(b)),perform(worker)),
    ])
    _,obs=three(src)
    facts=dict(obs["facts"])
    assert facts[a]==5 and facts[b]==4


def test_dynamic_collection_count_uses_existing_natural_domain_path():
    book=nat_book(4,5,6)
    src=" ".join([
        place_book("ספר",book),place_nat("מונה",1),
        "ועתה "+repeat_dynamic(count(book_place("ספר")),increment("מונה")),
    ])
    _,obs=three(src)
    assert dict(obs["facts"])["מונה"]==4


def test_computed_zero_executes_body_zero_times_and_dynamic_one_once():
    src0=" ".join([
        place_nat("מונה",5),
        "ועתה "+repeat_dynamic(zero(),increment("מונה")),
    ])
    _,obs0=three(src0)
    assert dict(obs0["facts"])["מונה"]==5

    src1=" ".join([
        place_nat("מונה",5),
        "ועתה "+repeat_dynamic(subtract(num(2),num(3)),increment("מונה")),
    ])
    _,obs1=three(src1)
    assert dict(obs1["facts"])["מונה"]==6


def test_error_determining_count_happens_before_first_iteration_and_stops_later_continuation():
    body_place="יעד"; flag="דגל"
    failing_count=subtract(num(3),num(2))
    principal=" ואחרי כן ".join([
        replace_nat(flag,num(2)),
        repeat_dynamic(failing_count,increment(body_place)),
        replace_nat(flag,num(3)),
    ])
    src=" ".join([place_nat(body_place,7),place_nat(flag,1),"ועתה "+principal])
    c=compile_source(src)
    assert c.valid,[d.to_dict() for d in c.diagnostics]
    observed=[
        reference_observable(execute_reference(c.hast)),
        ir_reference_observable(execute_reference_ir(c.ir)),
        backend_observable(execute_ir(c.ir)),
    ]
    assert observed[0]==observed[1]==observed[2]
    obs=observed[0]
    assert obs["outcome"]=="Error" and obs["error"]["code"]=="ARITHMETIC_DOMAIN_ERROR"
    facts=dict(obs["facts"])
    assert facts[body_place]==7
    assert facts[flag]==2


def test_failure_on_iteration_k_preserves_prior_and_failing_iteration_commits_and_stops_later_iterations():
    tick,target,book="מונה","יעד","ספר"
    worker="עובד"
    select=f"המספר אשר מספרו בסדר {book_place(book)} הוא {current(tick)}"
    work=increment(tick)+" ואחרי כן "+replace_nat(target,select)
    src=" ".join([
        place_nat(tick,zero()),place_nat(target,9),place_book(book,nat_book(11,22)),
        act(worker),body(worker,work),
        "ועתה "+repeat_literal(5,perform(worker)),
    ])
    c=compile_source(src)
    assert c.valid,[d.to_dict() for d in c.diagnostics]
    obs=[
        reference_observable(execute_reference(c.hast)),
        ir_reference_observable(execute_reference_ir(c.ir)),
        backend_observable(execute_ir(c.ir)),
    ]
    assert obs[0]==obs[1]==obs[2]
    assert obs[0]["outcome"]=="Error"
    assert obs[0]["error"]["code"]=="COLLECTION_POSITION_ERROR"
    facts=dict(obs[0]["facts"])
    assert facts[tick]==3
    assert facts[target]==22


def test_repeated_collection_operation_is_ordinary_committed_effect_each_iteration():
    src=" ".join([
        place_book("ספר",nat_book(1)),
        "ועתה "+repeat_literal(3,replace_book("ספר",append_nat(book_place("ספר"),num(2)))),
    ])
    _,obs=three(src)
    assert dict(obs["facts"])["ספר"]==[1,2,2,2]


def test_repeated_performances_produce_one_output_per_occurrence_in_order():
    worker="פולט"
    src=" ".join([
        act(worker),body(worker,output(num(7))),
        "ועתה "+repeat_literal(3,perform(worker)),
    ])
    _,obs=three(src)
    assert obs["products"]==[[worker,7],[worker,7],[worker,7]]


def test_repeated_no_output_occurrences_do_not_create_implicit_results():
    worker="שקט"
    src=" ".join([
        place_nat("מונה",1),act(worker),body(worker,increment("מונה")),
        "ועתה "+repeat_literal(3,perform(worker)),
    ])
    _,obs=three(src)
    assert dict(obs["facts"])["מונה"]==4
    assert obs["products"]==[]


def test_repeated_index_carrying_act_keeps_typed_role_and_output_contract():
    worker,role="שנהמעביר","שנה"
    src=" ".join([
        act(worker),role_idx(worker,role),
        body(worker,output(idx_role(worker,role))),
        "ועתה "+repeat_literal(2,f"עשה את המעשה אשר שמו {worker} בהיות שנת אין תחת הדבר אשר במעשה אשר שמו {worker} שמו {role}"),
    ])
    _,obs=three(src)
    assert len(obs["products"])==2
    assert all(x[1]=={"index":"Zero"} for x in obs["products"])


def test_divergent_repeated_action_never_advances_to_later_iteration_under_fuel_harness():
    worker="נצחי"
    src=" ".join([
        act(worker),body(worker,perform(worker)),
        "ועתה "+repeat_literal(3,perform(worker)),
    ])
    _,obs=three(src,fuel=12)
    assert obs["outcome"]=="Divergence"


def test_surrounding_and_after_then_is_outside_recurrence():
    principal=repeat_literal(3,increment("מונה"))+" ואחרי כן "+increment("דגל")
    src=" ".join([place_nat("מונה",1),place_nat("דגל",1),"ועתה "+principal])
    _,obs=three(src)
    facts=dict(obs["facts"])
    assert facts["מונה"]==4
    assert facts["דגל"]==2


def test_attachment_and_negative_surface_forms_are_rejected_without_heuristics():
    action=increment("מונה")
    bad=[
        f"פעמים {action}",
        f"שבעה פעמים {action}",
        f"{action} פעמים {as_count(current('מונה'))}",
        f"פעמים כמספר המספר אשר במקום אשר שמו מונה {action}",
        f"אפס פעמים {action}",
        f"repeat {action}",
        f"for {action}",
        f"while {action}",
        f"7 פעמים {action}",
        f"שלש פעמים {action} {increment('דגל')}",
    ]
    for fragment in bad:
        assert not parse(fragment,start_lhs="CountedConsequence").forest.alternatives


def test_charter_transparency_does_not_change_recurrence_semantics_or_scope():
    base=" ".join([
        place_nat("מונה",1),place_nat("דגל",1),
        "ועתה "+repeat_literal(3,increment("מונה"))+" ואחרי כן "+increment("דגל"),
    ])
    _,expected=three(base)
    variants=[
        base.replace(" ","\n"),
        base.replace(" ",", "),
        "123 Latin "+base,
        base.replace("מונה","מוֹנה"),
        base.replace("פעמים","**פעמים**"),
        base.replace("פעמים","״פעמים״"),
    ]
    for source in variants:
        _,actual=three(source)
        assert actual==expected
