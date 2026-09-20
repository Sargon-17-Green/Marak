from __future__ import annotations

from compiler.api import compile_source, explain
from compiler.backend.portable import execute_ir
from compiler.runtime.ir_reference import execute_reference_ir
from compiler.runtime.observables import backend_observable, ir_reference_observable, reference_observable
from compiler.runtime.reference import execute_reference
from compiler.parse.a15_numerals import format_natural


def sym(d,m): return f"השם אשר במשפחת השמות אשר שמה {d} שמו {m}"
def sym_place(d,p): return f"השם אשר במשפחת השמות אשר שמה {d} ואשר במקום אשר שמו {p}"
def sym_role(d,a,r): return f"השם אשר במשפחת השמות אשר שמה {d} ואשר במעשה הזה עומד תחת הדבר אשר במעשה אשר שמו {a} שמו {r}"
def sym_recent(d,a): return f"השם אשר במשפחת השמות אשר שמה {d} ואשר יצא עתה מן המעשה אשר שמו {a}"
def idx_place(p): return f"מספר השנה אשר במקום אשר שמו {p}"
def idx_role(a,r): return f"מספר השנה אשר במעשה הזה עומד תחת הדבר אשר במעשה אשר שמו {a} שמו {r}"
def idx_recent(a): return f"מספר השנה אשר יצא עתה מן המעשה אשר שמו {a}"
def succ(v): return f"מספר השנה אשר אחר {v}"
def pred(v): return f"מספר השנה אשר לפני {v}"
def num(n): return f"המספר אשר הוא {format_natural(n)}"
def current(p): return f"המספר אשר במקום אשר שמו {p}"
def place_nat(p,n): return f"יהי מקום ושמו {p} ובמקום אשר שמו {p} יהי {num(n)} לבדו"
def replace_nat(p,v): return f"שים במקום אשר שמו {p} את {v} תחת {current(p)}"
def place_typed(p,v): return f"יהי מקום ושמו {p} ובמקום אשר שמו {p} יהי {v} לבדו"
def act(a): return f"יהי מעשה ושמו {a}"
def body(a,x): return f"זה דבר המעשה אשר שמו {a} {x} עד הנה דבר המעשה אשר שמו {a}"
def output(v): return f"הוצא מן המעשה הזה את {v}"
def perform(a): return f"עשה את המעשה אשר שמו {a}"
def perform_one(a,r,v): return f"עשה את המעשה אשר שמו {a} בהיות {v} תחת הדבר אשר במעשה אשר שמו {a} שמו {r}"
def role_sym(a,r,d): return f"יהי במעשה אשר שמו {a} דבר ושמו {r} ובעשות את המעשה אשר שמו {a} יעמד שם ממשפחת השמות אשר שמה {d} תחת הדבר אשר במעשה אשר שמו {a} שמו {r}"
def role_idx(a,r): return f"יהי במעשה אשר שמו {a} דבר ושמו {r} ובעשות את המעשה אשר שמו {a} יעמד מספר שנה תחת הדבר אשר במעשה אשר שמו {a} שמו {r}"
def replace_sym(p,d,v): return f"שים במקום אשר שמו {p} את {v} תחת {sym_place(d,p)}"
def replace_idx(p,v): return f"שים במקום אשר שמו {p} את {v} תחת {idx_place(p)}"
def symbol_domain(d): return f"תהי משפחת שמות ושמה {d}"
def member(d,m,count,label): return f"יהי במשפחת השמות אשר שמה {d} שם ושמו {m} ולשם אשר במשפחת השמות אשר שמה {d} שמו {m} מספר המלים אשר בשמו הנראה יהיה {format_natural(count)} והמלים הן {label}"
def order(d,a,b): return f"במשפט משפחת השמות אשר שמה {d} יהיה {sym(d,a)} מיד לפני {sym(d,b)}"


def three(source: str):
    c=compile_source(source)
    assert c.valid, [d.to_dict() for d in c.diagnostics]
    h=reference_observable(execute_reference(c.hast))
    i=ir_reference_observable(execute_reference_ir(c.ir))
    b=backend_observable(execute_ir(c.ir))
    assert h==i==b
    return c,b


def symbol_flow_source(*, d="צבעים", red="אדום", blue="כחול"):
    keep="שמור"; side="צד"; flag="דגל"; a="מחליף"; r="קלט"
    cond=f"אם {sym_role(d,a,r)} הוא {sym(d,blue)} {replace_nat(flag,num(1))} ואם לא {replace_nat(flag,num(2))}"
    b=body(a,cond+" ואחרי כן "+output(sym_role(d,a,r))+" ואחרי כן "+replace_sym(side,d,sym_role(d,a,r)))
    principal=" ואחרי כן ".join([
        replace_sym(keep,d,sym(d,blue)),
        perform_one(a,r,sym_place(d,keep)),
        replace_sym(keep,d,sym_recent(d,a)),
    ])
    return " ".join([
        symbol_domain(d),member(d,red,2,"צבע אדום"),member(d,blue,2,"צבע כחול"),order(d,red,blue),
        place_typed(keep,sym(d,red)),place_typed(side,sym(d,red)),place_nat(flag,2),act(a),role_sym(a,r,d),b,
        "ועתה "+principal,
    ])


def index_flow_source():
    p="שנה"; side="שנהצד"; a="מעביר"; r="קלט"
    b=body(a,output(idx_role(a,r))+" ואחרי כן "+replace_idx(side,succ(idx_role(a,r))))
    principal=" ואחרי כן ".join([
        replace_idx(p,pred(idx_place(p))),
        replace_idx(p,pred(idx_place(p))),
        perform_one(a,r,idx_place(p)),
        replace_idx(p,idx_recent(a)),
        replace_idx(p,succ(idx_place(p))),
        replace_idx(p,succ(idx_place(p))),
    ])
    return " ".join([
        place_typed(p,"שנה אחת אחרי שנת אין"),place_typed(side,"שנת אין"),
        act(a),role_idx(a,r),b,"ועתה "+principal,
    ])


def gt_source():
    p="דגל"
    cond=f"אם {num(7)} רב מן {num(3)} {replace_nat(p,num(1))} ואם לא {replace_nat(p,num(2))}"
    return " ".join([place_nat(p,1),"ועתה "+cond])


def same_label_source():
    d="גוונים"; a="ראשון"; b="שני"; flag="דגל"
    cond=f"אם {sym(d,a)} הוא {sym(d,b)} {replace_nat(flag,num(1))} ואם לא {replace_nat(flag,num(2))}"
    return " ".join([symbol_domain(d),member(d,a,1,"צבע"),member(d,b,1,"צבע"),place_nat(flag,1),"ועתה "+cond])


def recursive_symbol_role_source():
    d="מצבים"; stop="עצור"; go="המשך"; p="שמור"; A="ראשון"; B="שני"; C="שלישי"; ra="מצב"; rb="מצב"
    A_body=body(A,f"אם {sym_role(d,A,ra)} הוא {sym(d,stop)} {perform(C)} ואם לא {perform_one(B,rb,sym_role(d,A,ra))}")
    B_body=body(B,perform_one(A,ra,sym(d,stop))+" ואחרי כן "+replace_sym(p,d,sym_role(d,B,rb)))
    C_body=body(C,replace_sym(p,d,sym(d,stop)))
    return " ".join([
        symbol_domain(d),member(d,stop,1,"עצור"),member(d,go,1,"המשך"),
        place_typed(p,sym(d,stop)),act(A),act(B),act(C),role_sym(A,ra,d),role_sym(B,rb,d),
        A_body,B_body,C_body,"ועתה "+perform_one(A,ra,sym(d,go)),
    ])


def order_program(edges):
    d="דרגות"; members=["ראשון","שני","שלישי"]
    prep=[symbol_domain(d)]+[member(d,m,1,m) for m in members]+[order(d,a,b) for a,b in edges]+[place_nat("דגל",1)]
    return " ".join(prep+["ועתה "+replace_nat("דגל",num(1))])


def large_numeral_source(values):
    names=["אלף","בית","גמל","דלת","הא"]
    pre=[place_nat(name,n) for name,n in zip(names,values)]
    return " ".join(pre+["ועתה "+replace_nat(names[0],current(names[0]))])


def test_symbol_actual_source_end_to_end():
    c,obs=three(symbol_flow_source())
    facts=dict(obs["facts"])
    assert facts["שמור"]=="צבע כחול"
    assert facts["צד"]=="צבע כחול"  # proves action after הוצא executed
    assert facts["דגל"]==1          # proves same-member Symbol equality held
    assert obs["products"][-1][1]=="צבע כחול"
    assert c.ir.symbol_domains and len(c.ir.symbol_members)==2 and len(c.ir.symbol_order_edges)==1


def test_index_actual_source_end_to_end_crosses_zero_and_returns_after_one():
    _,obs=three(index_flow_source())
    assert dict(obs["facts"])["שנה"]=={"index":"AfterZero","magnitude":1}


def test_natural_gt_actual_source_end_to_end():
    _,obs=three(gt_source())
    assert dict(obs["facts"])["דגל"]==1


def test_same_visible_label_members_remain_unequal_from_source():
    c,obs=three(same_label_source())
    assert dict(obs["facts"])["דגל"]==2
    assert len(c.ir.symbol_members)==2
    assert c.ir.symbol_members[0].external_label==c.ir.symbol_members[1].external_label=="צבע"
    assert c.ir.symbol_members[0].member_id!=c.ir.symbol_members[1].member_id


def test_cross_domain_symbol_equality_is_static_invalid():
    d1,d2="צבעים","טעמים"
    src=" ".join([
        symbol_domain(d1),member(d1,"אדום",1,"אחד"),
        symbol_domain(d2),member(d2,"מתוק",1,"אחד"),
        place_nat("דגל",1),
        "ועתה "+f"אם {sym(d1,'אדום')} הוא {sym(d2,'מתוק')} {replace_nat('דגל',num(1))} ואם לא {replace_nat('דגל',num(2))}",
    ])
    c=compile_source(src)
    assert not c.valid
    assert any(d.code=="SEM0301" or d.metadata.get("semantic_code")=="DOMAIN_SYMBOL_EQUALITY" for d in c.diagnostics)


def test_recursive_symbol_role_occurrences_are_isolated():
    _,obs=three(recursive_symbol_role_source())
    assert dict(obs["facts"])["שמור"]=="המשך"


def test_symbol_order_three_member_complete_chain_preserved():
    c,_=three(order_program([("ראשון","שני"),("שני","שלישי")]))
    assert len(c.ir.symbol_order_edges)==2
    assert [(x.before_member_id.spelling,x.after_member_id.spelling) for x in c.ir.symbol_order_edges]==[("ראשון","שני"),("שני","שלישי")]


def test_symbol_order_incomplete_cycle_and_fork_rejected():
    cases=[
        [("ראשון","שני")],
        [("ראשון","שני"),("שני","ראשון")],
        [("ראשון","שני"),("ראשון","שלישי")],
    ]
    for edges in cases:
        c=compile_source(order_program(edges))
        assert not c.valid
        assert any(d.metadata.get("semantic_code")=="DOMAIN_SYMBOL_ORDER" for d in c.diagnostics)


def test_multword_symbol_label_boundary_uses_declared_count_only():
    d="כינויים"
    src=" ".join([
        symbol_domain(d),
        member(d,"אחד",1,"אור"),
        member(d,"שנים",2,"אור גדול"),
        member(d,"שלשה",3,"אור גדול מאד"),
        place_nat("דגל",1),
        "ועתה "+replace_nat("דגל",num(1)),
    ])
    c,_=three(src)
    assert [x.external_label for x in c.ir.symbol_members]==["אור","אור גדול","אור גדול מאד"]


def test_index_farther_magnitudes_source_succ_pred_inverse():
    p="שנה"
    src=" ".join([
        place_typed(p,"שלש שנים אחרי שנת אין"),
        "ועתה "+replace_idx(p,pred(idx_place(p)))+" ואחרי כן "+replace_idx(p,succ(idx_place(p))),
    ])
    _,obs=three(src)
    assert dict(obs["facts"])[p]=={"index":"AfterZero","magnitude":3}


def test_large_direct_naturals_actual_source_exact():
    values=[10_000,999_999,1_000_000,14_777_149,99_999_999]
    _,obs=three(large_numeral_source(values))
    facts=dict(obs["facts"])
    assert [facts[x] for x in ["אלף","בית","גמל","דלת","הא"]]==values


def test_explain_surfaces_c52_resolved_metadata_without_changing_observation():
    obj=explain(symbol_flow_source(),level="resolve")
    assert obj["identities"]["symbol_domains_debug"]
    assert len(obj["identities"]["symbol_members_debug"])==2
    assert obj["symbol_order_debug"][0]["relation"]=="adjacent-before"
    assert all(x["debug_only_internal_identity"] for x in obj["identities"]["symbol_members_debug"])
    assert any(x["typed"] for x in obj["immediate_result_provenance"])



def test_index_crossing_laws_total_helpers():
    from compiler.models.values import BidirectionalIndexValue,index_predecessor,index_successor
    zero=BidirectionalIndexValue("zero",0)
    before1=BidirectionalIndexValue("before",1)
    after1=BidirectionalIndexValue("after",1)
    assert index_predecessor(after1)==zero
    assert index_predecessor(zero)==before1
    assert index_successor(before1)==zero
    assert index_successor(zero)==after1
    assert index_predecessor(BidirectionalIndexValue("before",9))==BidirectionalIndexValue("before",10)
    assert index_successor(BidirectionalIndexValue("after",9))==BidirectionalIndexValue("after",10)


def test_symbol_label_count_and_reference_negative_forms():
    from compiler.api import parse
    from compiler.parse.c5_2_registry import C5_2_REGISTRY
    d="צבעים"; m="אדום"
    bad=[
        f"יהי במשפחת השמות אשר שמה {d} שם ושמו {m} ולשם אשר במשפחת השמות אשר שמה {d} שמו {m} מספר המלים אשר בשמו הנראה יהיה אפס והמלים הן צבע",
        f"יהי במשפחת השמות אשר שמה {d} שם ושמו {m} ולשם אשר במשפחת השמות אשר שמה {d} שמו {m} מספר המלים אשר בשמו הנראה יהיה שנים והמלים הן צבע",
        f"יהי במשפחת השמות אשר שמה {d} שם ושמו {m} ולשם אשר במשפחת השמות אשר שמה {d} שמו {m} מספר המלים אשר בשמו הנראה יהיה והמלים הן צבע",
    ]
    for src in bad:
        assert not parse(src,registry=C5_2_REGISTRY,start_lhs="SymbolMemberDeclaration").forest.alternatives
    for src in (m,f"שם {m}","צבע אדום"):
        assert not parse(src,registry=C5_2_REGISTRY,start_lhs="SymbolValue").forest.alternatives


def test_index_no_natural_conversion_and_historical_alias_excluded():
    from compiler.api import parse
    from compiler.parse.c5_2_registry import C5_2_REGISTRY
    for src in (num(5),"שנת חמשת אלפים",f"מספר השנה אשר אחר {num(5)}"):
        assert not parse(src,registry=C5_2_REGISTRY,start_lhs="IndexValue").forest.alternatives


def test_wrong_domain_symbol_place_replacement_is_static_invalid():
    d1,d2="צבעים","טעמים"; p="שמור"
    src=" ".join([
        symbol_domain(d1),member(d1,"אדום",1,"אדום"),
        symbol_domain(d2),member(d2,"מתוק",1,"מתוק"),
        place_typed(p,sym(d1,"אדום")),
        "ועתה "+replace_sym(p,d1,sym(d2,"מתוק")),
    ])
    c=compile_source(src)
    assert not c.valid
    assert any(d.phase in {"resolve","semantic"} for d in c.diagnostics)


def test_mixed_symbol_output_domains_are_static_invalid():
    d1,d2="צבעים","טעמים"; a="מפיק"
    src=" ".join([
        symbol_domain(d1),member(d1,"אדום",1,"אדום"),
        symbol_domain(d2),member(d2,"מתוק",1,"מתוק"),act(a),
        body(a,output(sym(d1,"אדום"))+" ואחרי כן "+output(sym(d2,"מתוק"))),
        "ועתה "+perform(a),
    ])
    c=compile_source(src)
    assert not c.valid
    assert any(d.code=="SEM0306" or d.metadata.get("semantic_code")=="MIXED_OUTPUT_DOMAINS" for d in c.diagnostics)



def test_symbol_domain_and_member_source_rename_invariance():
    _,a=three(symbol_flow_source())
    _,b=three(symbol_flow_source(d="גוונים",red="ראשון",blue="שני"))
    assert a==b
