from __future__ import annotations

import pytest

from compiler.api import compile_source, parse
from compiler.models.values import NaturalValue
from compiler.runtime.invocation import InputBinding
from tests.test_c5_2_surface_pipeline import (
    member, num, place_nat, place_typed, replace_nat, symbol_domain,
)
from tests.test_c5_5_program_inputs import input_nat, input_nat_ref
from tests.test_c5_5_typed_inputs import input_symbol, input_symbol_ref


def test_role_name_mismatch_and_duplicate_declaration_are_static_errors():
    mismatch=(
        "יהי למלאכה הזאת דבר ושמו קלט ובטרם תחל המלאכה הזאת יעמד מספר "
        "תחת הדבר אשר למלאכה הזאת שמו אחר "
        "ועתה שים במקום אשר שמו יעד את המספר אשר הוא אחד תחת המספר אשר במקום אשר שמו יעד"
    )
    # Add a valid place so failure is specifically declaration resolution rather than use.
    mismatch=place_nat("יעד",1)+" "+mismatch
    c=compile_source(mismatch)
    assert not c.valid
    assert "REF0502" in [d.code for d in c.diagnostics]

    dup=" ".join([
        input_nat("קלט"),input_nat("קלט"),place_nat("יעד",1),
        "ועתה "+replace_nat("יעד",num(2)),
    ])
    c=compile_source(dup)
    assert not c.valid
    assert "REF0502" in [d.code for d in c.diagnostics]


def test_program_input_reference_obeys_introduced_before_use_and_no_hoisting():
    before=" ".join([
        f"יהי מקום ושמו יעד ובמקום אשר שמו יעד יהי {input_nat_ref('קלט')} לבדו",
        input_nat("קלט"),
        "ועתה "+replace_nat("יעד",num(1)),
    ])
    c=compile_source(before)
    assert not c.valid
    assert "REF0501" in [d.code for d in c.diagnostics]

    undeclared=" ".join([
        place_nat("יעד",1),
        "ועתה "+replace_nat("יעד",input_nat_ref("קלט")),
    ])
    c=compile_source(undeclared)
    assert not c.valid
    assert "REF0501" in [d.code for d in c.diagnostics]


def test_wrong_typed_head_and_wrong_symbol_domain_are_static_errors():
    d1,d2="צבעים","חיות"
    natural_as_symbol=" ".join([
        symbol_domain(d1),member(d1,"אדום",1,"אדום"),
        input_nat("קלט"),
        place_typed("יעד",input_symbol_ref("קלט",d1)),
        "ועתה "+replace_nat("דגל",num(1)),
    ])
    # Give the principal a valid target; resolver must fail on the input head first.
    natural_as_symbol=place_nat("דגל",1)+" "+natural_as_symbol
    c=compile_source(natural_as_symbol)
    assert not c.valid
    assert "REF0503" in [d.code for d in c.diagnostics]

    wrong_symbol_domain=" ".join([
        symbol_domain(d1),member(d1,"אדום",1,"אדום"),
        symbol_domain(d2),member(d2,"חתול",1,"חתול"),
        input_symbol("קלט",d1),
        place_typed("יעד",input_symbol_ref("קלט",d2)),
        "ועתה "+replace_nat("דגל",num(1)),
    ])
    wrong_symbol_domain=place_nat("דגל",1)+" "+wrong_symbol_domain
    c=compile_source(wrong_symbol_domain)
    assert not c.valid
    assert "REF0503" in [d.code for d in c.diagnostics]


def test_program_input_declaration_is_preparation_only_and_not_mutable_or_transport():
    action=replace_nat("יעד",num(2))
    bad=[
        # after principal
        place_nat("יעד",1)+" ועתה "+action+" "+input_nat("קלט"),
        # inside act/body-like material is not a preparatory slot
        f"יהי מעשה ושמו עובד זה דבר המעשה אשר שמו עובד {input_nat('קלט')} עד הנה דבר המעשה אשר שמו עובד ועתה עשה את המעשה אשר שמו עובד",
        # positional / transport / default / generic type / main / mutable input inventions
        "יהי למלאכה הזאת הארגומנט הראשון מספר ועתה "+action,
        "יהי למלאכה הזאת המספר הראשון אשר ניתן קלט ועתה "+action,
        "קרא מן הקלט מספר ועתה "+action,
        "יהי למלאכה הזאת דבר ושמו קלט מסוג Natural ועתה "+action,
        "יהי main ושמו ראשי ועתה "+action,
        "יהי למלאכה הזאת דבר ושמו קלט ואם לא ניתן יהיה אחד ועתה "+action,
        "שים תחת הדבר אשר למלאכה הזאת שמו קלט את המספר אשר הוא אחד ועתה "+action,
    ]
    for source in bad:
        assert not compile_source(source).valid


def test_raw_role_spelling_is_not_an_invocation_binding_identity():
    with pytest.raises(TypeError,match="resolved ProgramInputId"):
        InputBinding("קלט",NaturalValue(1))  # type: ignore[arg-type]


def test_charter_invariance_preserves_program_input_contract_identity():
    base=" ".join([
        input_nat("קלט"),place_nat("יעד",1),
        "ועתה "+replace_nat("יעד",input_nat_ref("קלט")),
    ])
    c=compile_source(base); assert c.valid
    owner=c.ir.program_input_domains[0].input_id.program_contract
    variants=[
        base.replace(" ","\n"),
        base.replace(" ",", "),
        "123 Latin "+base,
        base.replace("קלט","קֶלֶט"),
        base.replace("מספר","**מספר**"),
    ]
    for source in variants:
        x=compile_source(source)
        assert x.valid,[d.to_dict() for d in x.diagnostics]
        assert x.ir.program_input_domains[0].input_id.program_contract==owner
