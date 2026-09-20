from __future__ import annotations

from compiler.api import compile_source
from compiler.backend.portable import execute_ir
from compiler.models.domains import NATURAL, CollectionDomain
from compiler.models.values import BidirectionalIndexValue, CollectionValue, NaturalValue, SymbolValue
from compiler.runtime.invocation import InputBinding
from compiler.runtime.ir_reference import execute_reference_ir
from compiler.runtime.observables import backend_observable, ir_reference_observable, reference_observable
from compiler.runtime.reference import execute_reference
from tests.test_c5_2_surface_pipeline import (
    act, body, member, num, output, perform_one, place_nat, place_typed,
    replace_idx, replace_nat, replace_sym, role_sym, succ, sym_recent,
    sym_role, symbol_domain,
)
from tests.test_c5_3_collections import append_nat, count, first_book, first_nat, place_book, replace_book


def input_symbol(role,d):
    return f"יהי למלאכה הזאת דבר ושמו {role} ובטרם תחל המלאכה הזאת יעמד שם ממשפחת השמות אשר שמה {d} תחת הדבר אשר למלאכה הזאת שמו {role}"
def input_symbol_ref(role,d):
    return f"השם אשר במשפחת השמות אשר שמה {d} עומד תחת הדבר אשר למלאכה הזאת שמו {role}"
def input_index(role):
    return f"יהי למלאכה הזאת דבר ושמו {role} ובטרם תחל המלאכה הזאת יעמד מספר שנה תחת הדבר אשר למלאכה הזאת שמו {role}"
def input_index_ref(role):
    return f"מספר השנה אשר עומד תחת הדבר אשר למלאכה הזאת שמו {role}"
def input_collection(role,kind):
    return f"יהי למלאכה הזאת דבר ושמו {role} ובטרם תחל המלאכה הזאת יעמד {kind} תחת הדבר אשר למלאכה הזאת שמו {role}"
def input_collection_ref(role):
    return f"הספר אשר עומד תחת הדבר אשר למלאכה הזאת שמו {role}"
def input_id(c,name):
    return next(x.input_id for x in c.ir.program_input_domains if x.input_id.spelling==name)
def three(c,bindings):
    h=reference_observable(execute_reference(c.hast,bindings=bindings))
    i=ir_reference_observable(execute_reference_ir(c.ir,bindings=bindings))
    b=backend_observable(execute_ir(c.ir,bindings=bindings))
    assert h==i==b
    return b


def test_symbol_input_flows_through_place_role_output_and_immediate_result():
    d,red,inp,worker,role,place="צבעים","אדום","צבעקלט","מעביר","צבע","יעד"
    src=" ".join([
        symbol_domain(d),member(d,red,1,"אדום"),input_symbol(inp,d),
        place_typed(place,input_symbol_ref(inp,d)),act(worker),role_sym(worker,role,d),
        body(worker,output(sym_role(d,worker,role))),
        "ועתה "+perform_one(worker,role,input_symbol_ref(inp,d))+
        " ואחרי כן "+replace_sym(place,d,sym_recent(d,worker)),
    ])
    c=compile_source(src); assert c.valid,[x.to_dict() for x in c.diagnostics]
    pid=input_id(c,inp); dom=c.ir.symbol_domains[0].domain_id; mem=c.ir.symbol_members[0].member_id
    obs=three(c,(InputBinding(pid,SymbolValue(dom,mem,"אדום")),))
    assert dict(obs["facts"])[place]=="אדום"
    assert obs["products"]==[[worker,"אדום"]]


def test_index_input_flows_through_typed_state_and_stays_immutable():
    inp,place="שנהקלט","שנה"
    src=" ".join([
        input_index(inp),place_typed(place,input_index_ref(inp)),
        "ועתה "+replace_idx(place,succ(input_index_ref(inp)))+
        " ואחרי כן "+replace_idx(place,input_index_ref(inp)),
    ])
    c=compile_source(src); assert c.valid,[x.to_dict() for x in c.diagnostics]
    obs=three(c,(InputBinding(input_id(c,inp),BidirectionalIndexValue("after",3)),))
    assert dict(obs["facts"])[place]=={"index":"AfterZero","magnitude":3}


def test_collection_input_uses_existing_count_select_append_without_mutating_input():
    inp,work,total,first="ספרקלט","עבודה","מנה","ראש"; ref=input_collection_ref(inp)
    src=" ".join([
        input_collection(inp,"ספר מספרים"),place_book(work,ref),place_nat(total,1),place_nat(first,1),
        "ועתה "+replace_book(work,append_nat(ref,num(9)))+
        " ואחרי כן "+replace_nat(total,count(ref))+
        " ואחרי כן "+replace_nat(first,first_nat(ref)),
    ])
    c=compile_source(src); assert c.valid,[x.to_dict() for x in c.diagnostics]
    value=CollectionValue(NATURAL,(NaturalValue(4),NaturalValue(7)))
    obs=three(c,(InputBinding(input_id(c,inp),value),)); facts=dict(obs["facts"])
    assert facts[work]==[4,7,9] and facts[total]==2 and facts[first]==4


def test_nested_collection_input_preserves_recursive_domain():
    inp,work,total="ספריםקלט","עבודה","מנה"; ref=input_collection_ref(inp)
    src=" ".join([
        input_collection(inp,"ספר ספרי מספרים"),place_book(work,ref),place_nat(total,1),
        "ועתה "+replace_nat(total,count(first_book(ref))),
    ])
    c=compile_source(src); assert c.valid,[x.to_dict() for x in c.diagnostics]
    a=CollectionValue(NATURAL,(NaturalValue(2),NaturalValue(3)))
    b=CollectionValue(NATURAL,(NaturalValue(8),))
    value=CollectionValue(CollectionDomain(NATURAL),(a,b))
    obs=three(c,(InputBinding(input_id(c,inp),value),)); facts=dict(obs["facts"])
    assert facts[work]==[[2,3],[8]] and facts[total]==2
