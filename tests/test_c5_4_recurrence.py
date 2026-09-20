from __future__ import annotations

from compiler.api import check, compile_source, parse
from compiler.backend.portable import execute_ir
from compiler.parse.a15_numerals import format_feminine_count
from compiler.runtime.ir_reference import execute_reference_ir
from compiler.runtime.observables import backend_observable, ir_reference_observable, reference_observable
from compiler.runtime.reference import execute_reference
from compiler.models.hast import HastRepeatExactly
from compiler.parse.a13_b12_registry import A13_B12_REGISTRY
from compiler.validate.ir_canonical import validate_canonical_ir
from compiler.models.ir import IRAddNatural, IRNatural, IRReadCurrentFact, IRRepeatExactly
from tests.test_c5_2_surface_pipeline import (
    act, body, current, idx_role, member, num, output, perform, perform_one,
    place_nat, replace_nat, role_idx, role_sym, sym, sym_role, symbol_domain,
)
from tests.test_c5_3_collections import (
    append_nat, book_place, count, empty_nat, nat_book, nth_nat, place_book, replace_book,
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


def test_direct_morphology_frontier_compiles_without_becoming_semantic_ceiling():
    n=99_999_999
    src=" ".join([place_nat("מונה",1),"ועתה "+repeat_literal(n,increment("מונה"))])
    c=compile_source(src)
    assert c.valid,[d.to_dict() for d in c.diagnostics]
    assert isinstance(c.ir.principal,IRRepeatExactly)
    assert isinstance(c.ir.principal.count,IRNatural)
    assert c.ir.principal.count.value==n


def test_dynamic_count_can_exceed_direct_morphology_frontier_without_semantic_cap():
    count_expr=add(num(99_999_999),num(1))
    src=" ".join([place_nat("מונה",1),"ועתה "+repeat_dynamic(count_expr,increment("מונה"))])
    c=compile_source(src)
    assert c.valid,[d.to_dict() for d in c.diagnostics]
    assert isinstance(c.ir.principal,IRRepeatExactly)
    assert isinstance(c.ir.principal.count,IRAddNatural)


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
    assert isinstance(c.ir.principal.count,IRReadCurrentFact)


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
    body_place="יעד"; flag="דגל"; amount="גורע"; source="מקור"
    # Dynamic current-place reads make the underflow a runtime count-evaluation
    # failure rather than a statically provable constant error.
    failing_count=subtract(current(amount),current(source))
    principal=" ואחרי כן ".join([
        replace_nat(flag,num(2)),
        repeat_dynamic(failing_count,increment(body_place)),
        replace_nat(flag,num(3)),
    ])
    src=" ".join([
        place_nat(body_place,7),place_nat(flag,1),place_nat(amount,3),place_nat(source,2),
        "ועתה "+principal,
    ])
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
        place_nat(tick,1),place_nat(target,9),place_book(book,nat_book(11,22)),
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


def test_repeated_symbol_carrying_act_keeps_typed_role_and_output_contract():
    domain,worker,role,red="צבעים","צבעמעביר","צבע","אדום"
    src=" ".join([
        symbol_domain(domain),member(domain,red,1,"אדום"),
        act(worker),role_sym(worker,role,domain),
        body(worker,output(sym_role(domain,worker,role))),
        "ועתה "+repeat_literal(2,perform_one(worker,role,sym(domain,red))),
    ])
    _,obs=three(src)
    assert obs["products"]==[[worker,"אדום"],[worker,"אדום"]]


def test_recurrence_does_not_create_immediate_result_provenance_of_last_iteration():
    worker="פולט"
    recent=f"המספר אשר יצא עתה מן המעשה אשר שמו {worker}"
    src=" ".join([
        place_nat("יעד",1),act(worker),body(worker,output(num(7))),
        "ועתה "+repeat_literal(2,perform(worker))+" ואחרי כן "+replace_nat("יעד",recent),
    ])
    c=compile_source(src)
    assert not c.valid
    assert "REF0112" in [d.code for d in c.diagnostics]


def test_failure_after_output_keeps_completed_output_event_and_stops_recurrence():
    worker="פולט"
    failing=nth_nat(book_place("ספר"),num(2))
    src=" ".join([
        place_book("ספר",nat_book(11)),place_nat("יעד",9),
        act(worker),body(worker,output(num(7))+" ואחרי כן "+replace_nat("יעד",failing)),
        "ועתה "+repeat_literal(3,perform(worker)),
    ])
    c=compile_source(src)
    assert c.valid,[d.to_dict() for d in c.diagnostics]
    observed=[
        reference_observable(execute_reference(c.hast)),
        ir_reference_observable(execute_reference_ir(c.ir)),
        backend_observable(execute_ir(c.ir)),
    ]
    assert observed[0]==observed[1]==observed[2]
    obs=observed[0]
    assert obs["outcome"]=="Error"
    assert obs["error"]["code"]=="COLLECTION_POSITION_ERROR"
    assert obs["products"]==[[worker,7]]
    assert dict(obs["facts"])["יעד"]==9


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
        f"פעמים כמספר השנה אשר במקום אשר שמו שנה {action}",
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


# C5.4-MR-001: recurrence entry is a provenance boundary for the body.
def test_repeat_exactly_body_rejects_incoming_immediate_result_from_preceding_performance():
    producer="פולט"; target="יעד"
    recent=f"המספר אשר יצא עתה מן המעשה אשר שמו {producer}"
    src=" ".join([
        place_nat(target,1),act(producer),body(producer,output(num(3))),
        "ועתה "+perform(producer)+" ואחרי כן "+
        repeat_literal(3,replace_nat(target,recent)),
    ])
    c=compile_source(src)
    assert not c.valid
    assert "REF0112" in [d.code for d in c.diagnostics]


def test_dynamic_count_may_observe_incoming_result_once_but_repeat_body_starts_without_it():
    producer="פולט"; target="מונה"
    recent=f"המספר אשר יצא עתה מן המעשה אשר שמו {producer}"
    src=" ".join([
        place_nat(target,10),act(producer),body(producer,output(num(3))),
        "ועתה "+perform(producer)+" ואחרי כן "+
        repeat_dynamic(recent,increment(target)),
    ])
    _,obs=three(src)
    assert dict(obs["facts"])[target]==13
    assert obs["products"]==[[producer,3]]


def test_first_iteration_cannot_reuse_provenance_that_was_valid_for_dynamic_count():
    producer="פולט"; target="יעד"
    recent=f"המספר אשר יצא עתה מן המעשה אשר שמו {producer}"
    src=" ".join([
        place_nat(target,1),act(producer),body(producer,output(num(3))),
        "ועתה "+perform(producer)+" ואחרי כן "+
        repeat_dynamic(recent,replace_nat(target,recent)),
    ])
    c=compile_source(src)
    assert not c.valid
    assert "REF0112" in [d.code for d in c.diagnostics]


def test_historical_fixed_recurrence_body_also_starts_without_incoming_provenance():
    producer="פולט"; target="יעד"
    recent=f"המספר אשר יצא עתה מן המעשה אשר שמו {producer}"
    src=" ".join([
        place_nat(target,1),act(producer),body(producer,output(num(3))),
        "ועתה "+perform(producer)+" ואחרי כן שלש פעמים "+
        replace_nat(target,recent),
    ])
    c=compile_source(src,registry=A13_B12_REGISTRY)
    assert not c.valid
    assert "REF0112" in [d.code for d in c.diagnostics]


def test_post_action_recurrence_drops_incoming_provenance_but_proposition_sees_own_perform():
    prior="קודם"; worker="מודד"; target="יעד"
    prior_recent=f"המספר אשר יצא עתה מן המעשה אשר שמו {prior}"
    worker_recent=f"המספר אשר יצא עתה מן המעשה אשר שמו {worker}"

    bad=" ".join([
        place_nat(target,1),
        act(prior),body(prior,output(num(7))),
        "ועתה "+perform(prior)+" ואחרי כן "+
        replace_nat(target,prior_recent)+" וכן תעשה עד אשר "+
        current(target)+" הוא "+num(7),
    ])
    rejected=compile_source(bad)
    assert not rejected.valid
    assert "REF0112" in [d.code for d in rejected.diagnostics]

    good=" ".join([
        place_nat(target,1),
        act(prior),body(prior,output(num(7))),
        act(worker),body(worker,output(num(1))),
        "ועתה "+perform(prior)+" ואחרי כן "+
        perform(worker)+" וכן תעשה עד אשר "+
        worker_recent+" הוא "+num(1),
    ])
    _,obs=three(good)
    assert obs["products"]==[[prior,7],[worker,1]]


def test_source_resolution_and_canonical_ir_validation_agree_at_recurrence_boundary():
    producer="פולט"; target="מונה"
    recent=f"המספר אשר יצא עתה מן המעשה אשר שמו {producer}"

    bad=" ".join([
        place_nat(target,1),act(producer),body(producer,output(num(2))),
        "ועתה "+perform(producer)+" ואחרי כן "+
        repeat_literal(2,replace_nat(target,recent)),
    ])
    checked=check(bad)
    assert not checked.valid
    assert "REF0112" in [d.code for d in checked.diagnostics]

    good=" ".join([
        place_nat(target,10),act(producer),body(producer,output(num(2))),
        "ועתה "+perform(producer)+" ואחרי כן "+
        repeat_dynamic(recent,increment(target)),
    ])
    compiled=compile_source(good)
    assert compiled.valid,[d.to_dict() for d in compiled.diagnostics]
    assert compiled.ir is not None
    validate_canonical_ir(compiled.ir)
