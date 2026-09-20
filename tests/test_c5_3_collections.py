from __future__ import annotations

from compiler.api import compile_source, parse
from compiler.backend.portable import execute_ir
from compiler.parse.a15_numerals import format_natural
from compiler.runtime.ir_reference import execute_reference_ir
from compiler.runtime.observables import backend_observable, ir_reference_observable, reference_observable
from compiler.runtime.reference import ErrorOutcome, execute_reference
from tests.test_c5_2_surface_pipeline import (
    act, body, member, num, order, perform_one, place_nat, replace_nat,
    sym, symbol_domain,
)


def empty_nat(): return "ספר מספרים אשר אין בו מספר"
def empty_idx(): return "ספר מספרי שנים אשר אין בו מספר שנה"
def empty_sym(d): return f"ספר שמות ממשפחת השמות אשר שמה {d} אשר אין בו שם"
def empty_books_nat(): return "ספר ספרי מספרים אשר אין בו ספר"
def empty_books_sym(d): return f"ספר ספרי שמות ממשפחת השמות אשר שמה {d} אשר אין בו ספר"
def append_nat(book,v): return f"ספר מספרים אשר בו כל אשר ב {book} כסדרו ואחר כלם {v}"
def append_idx(book,v): return f"ספר מספרי שנים אשר בו כל אשר ב {book} כסדרו ואחר כלם {v}"
def append_sym(d,book,v): return f"ספר שמות ממשפחת השמות אשר שמה {d} אשר בו כל אשר ב {book} כסדרו ואחר כלם {v}"
def append_books_nat(book,v): return f"ספר ספרי מספרים אשר בו כל אשר ב {book} כסדרו ואחר כלם {v}"
def append_books_sym(d,book,v): return f"ספר ספרי שמות ממשפחת השמות אשר שמה {d} אשר בו כל אשר ב {book} כסדרו ואחר כלם {v}"
def book_place(p): return f"הספר אשר במקום אשר שמו {p}"
def book_role(a,r): return f"הספר אשר במעשה הזה עומד תחת הדבר אשר במעשה אשר שמו {a} שמו {r}"
def book_recent(a): return f"הספר אשר יצא עתה מן המעשה אשר שמו {a}"
def place_book(p,v): return f"יהי מקום ושמו {p} ובמקום אשר שמו {p} יהי {v} לבדו"
def replace_book(p,v): return f"שים במקום אשר שמו {p} את {v} תחת {book_place(p)}"
def role_book(a,r,kind="ספר מספרים"): return f"יהי במעשה אשר שמו {a} דבר ושמו {r} ובעשות את המעשה אשר שמו {a} יעמד {kind} תחת הדבר אשר במעשה אשר שמו {a} שמו {r}"
def output(v): return f"הוצא מן המעשה הזה את {v}"
def count(v): return f"מספר הדברים אשר בתוך {v}"
def first_nat(v): return f"המספר אשר בראש {v}"
def last_nat(v): return f"המספר האחרון אשר בתוך {v}"
def nth_nat(v,k): return f"המספר אשר מספרו בסדר {v} הוא {k}"
def nth_book(v,k): return f"הספר אשר מספרו בסדר {v} הוא {k}"
def sort_nat(v): return f"הספר הערוך מן {v} מן המעט אל הרב"
def sort_sym(d,v): return f"הספר הערוך מן {v} כמשפט משפחת השמות אשר שמה {d}"
def sort_lex_nat(v): return f"הספר הערוך מן {v} מראש כל ספר ועד אחריתו מן המעט אל הרב"
def sort_lex_sym(d,v): return f"הספר הערוך מן {v} מראש כל ספר ועד אחריתו כמשפט משפחת השמות אשר שמה {d}"


def three(source: str):
    c=compile_source(source)
    assert c.valid, [d.to_dict() for d in c.diagnostics]
    h=reference_observable(execute_reference(c.hast))
    i=ir_reference_observable(execute_reference_ir(c.ir))
    b=backend_observable(execute_ir(c.ir))
    assert h==i==b
    return c,b


def nat_book(*values):
    out=empty_nat()
    for n in values:
        out=append_nat(out,num(n))
    return out


def symbol_book(d,*members):
    out=empty_sym(d)
    for m in members:
        out=append_sym(d,out,sym(d,m))
    return out


def test_empty_append_count_and_observation_end_to_end():
    b=nat_book(3,1,3)
    src=" ".join([place_book("ספר",b),place_nat("מנה",9),"ועתה "+replace_nat("מנה",count(book_place("ספר")))])
    _,obs=three(src)
    facts=dict(obs["facts"])
    assert facts["ספר"]==[3,1,3]
    assert facts["מנה"]==3


def test_membership_hit_miss_uses_semantic_element_equality():
    b=nat_book(3,1,3)
    hit=f"אם {num(1)} כתוב בתוך {book_place('ספר')} {replace_nat('דגל',num(1))} ואם לא {replace_nat('דגל',num(2))}"
    miss=f"אם {num(8)} כתוב בתוך {book_place('ספר')} {replace_nat('דגל',num(3))} ואם לא {replace_nat('דגל',num(4))}"
    src=" ".join([place_book("ספר",b),place_nat("דגל",9),"ועתה "+hit+" ואחרי כן "+miss])
    _,obs=three(src)
    assert dict(obs["facts"])["דגל"]==4


def test_first_last_and_positive_ordinal_selection():
    b=nat_book(7,2,9)
    actions=[
        replace_nat("א",first_nat(book_place("ספר"))),
        replace_nat("ב",last_nat(book_place("ספר"))),
        replace_nat("ג",nth_nat(book_place("ספר"),num(2))),
    ]
    src=" ".join([place_book("ספר",b),place_nat("א",1),place_nat("ב",1),place_nat("ג",1),"ועתה "+" ואחרי כן ".join(actions)])
    _,obs=three(src)
    facts=dict(obs["facts"])
    assert (facts["א"],facts["ב"],facts["ג"])==(7,9,2)


def test_zero_and_out_of_range_positions_are_collection_position_errors():
    b=nat_book(5)
    empty=empty_nat()
    positions=[count(empty),num(2)]
    for pos in positions:
        src=" ".join([place_book("ספר",b),place_nat("יעד",1),"ועתה "+replace_nat("יעד",nth_nat(book_place("ספר"),pos))])
        c=compile_source(src)
        assert c.valid,[d.to_dict() for d in c.diagnostics]
        h=execute_reference(c.hast)
        i=execute_reference_ir(c.ir)
        p=execute_ir(c.ir)
        assert isinstance(h,ErrorOutcome)
        assert h.error.code=="COLLECTION_POSITION_ERROR"
        assert i.error.code=="COLLECTION_POSITION_ERROR"
        assert p.error.code=="COLLECTION_POSITION_ERROR"


def test_natural_sort_is_numeric_and_preserves_duplicates():
    b=nat_book(10,2,10,1)
    src=" ".join([place_book("ספר",b),"ועתה "+replace_book("ספר",sort_nat(book_place("ספר")))])
    _,obs=three(src)
    assert dict(obs["facts"])["ספר"]==[1,2,10,10]


def test_symbol_sort_uses_explicit_non_declaration_order_only():
    d="צבעים"; members=["אדום","כחול","ירוק"]
    b=symbol_book(d,"כחול","ירוק","אדום")
    src=" ".join([
        symbol_domain(d),
        member(d,members[0],1,"אדום"),
        member(d,members[1],1,"כחול"),
        member(d,members[2],1,"ירוק"),
        order(d,"ירוק","אדום"),order(d,"אדום","כחול"),
        place_book("ספר",b),
        "ועתה "+replace_book("ספר",sort_sym(d,book_place("ספר"))),
    ])
    _,obs=three(src)
    assert dict(obs["facts"])["ספר"]==["ירוק","אדום","כחול"]


def test_same_label_distinct_symbol_members_do_not_match_membership():
    d="גוונים"
    b=symbol_book(d,"ראשון")
    cond=f"אם {sym(d,'שני')} כתוב בתוך {book_place('ספר')} {replace_nat('דגל',num(1))} ואם לא {replace_nat('דגל',num(2))}"
    src=" ".join([
        symbol_domain(d),member(d,"ראשון",1,"צבע"),member(d,"שני",1,"צבע"),
        place_book("ספר",b),place_nat("דגל",1),"ועתה "+cond,
    ])
    _,obs=three(src)
    assert dict(obs["facts"])["דגל"]==2


def test_index_collection_construct_count_select_and_membership():
    b=append_idx(append_idx(empty_idx(),"שנה אחת לפני שנת אין"),"שנת אין")
    cond=f"אם שנת אין כתוב בתוך {book_place('ספר')} {replace_nat('דגל',num(1))} ואם לא {replace_nat('דגל',num(2))}"
    src=" ".join([place_book("ספר",b),place_nat("דגל",2),"ועתה "+cond])
    _,obs=three(src)
    assert dict(obs["facts"])["ספר"]==[
        {"index":"BeforeZero","magnitude":1},{"index":"Zero"}
    ]
    assert dict(obs["facts"])["דגל"]==1


def test_nested_natural_lex_order_strict_prefix_and_equal_ties():
    a=nat_book(1)
    b=nat_book(1,2)
    outer=append_books_nat(append_books_nat(append_books_nat(empty_books_nat(),b),a),a)
    src=" ".join([place_book("ספרים",outer),"ועתה "+replace_book("ספרים",sort_lex_nat(book_place("ספרים")))])
    _,obs=three(src)
    assert dict(obs["facts"])["ספרים"]==[[1],[1],[1,2]]


def test_collection_place_role_output_and_immediate_result_roundtrip():
    b=nat_book(4,6)
    a="מחזיר"; r="קלט"
    src=" ".join([
        place_book("מקור",b),place_book("יעד",empty_nat()),
        act(a),role_book(a,r),body(a,output(book_role(a,r))),
        "ועתה "+perform_one(a,r,book_place("מקור"))+" ואחרי כן "+replace_book("יעד",book_recent(a)),
    ])
    _,obs=three(src)
    facts=dict(obs["facts"])
    assert facts["מקור"]==[4,6]
    assert facts["יעד"]==[4,6]


def test_untyped_empty_and_deeper_source_nesting_are_not_admitted():
    for src in [
        "ספר שאין בו דבר",
        "ספר ספרי ספרי מספרים אשר אין בו ספר",
        "ספר מספרים אשר בו כל אשר ב ספר מספרים אשר אין בו מספר כסדרו ואחר כלם שנת אין",
    ]:
        assert not parse(src,start_lhs="CollectionValue").forest.alternatives
