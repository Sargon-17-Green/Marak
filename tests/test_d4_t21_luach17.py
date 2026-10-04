from __future__ import annotations

from functools import lru_cache
from itertools import permutations
from pathlib import Path

from compiler.api import compile_source
from compiler.backend.portable import execute_ir
from compiler.parse.a15_numerals import format_natural
from compiler.runtime.observables import backend_observable
from tests.test_c5_6_general_index_surface import three

ROOT=Path(__file__).resolve().parents[1]
CANDIDATE=ROOT/"megillah"/"candidates"/"Megilat_HaItim_Marak_Candidate.md"
ORIGINAL=ROOT/"megillah"/"original"/"Megilat_HaItim_Yehuda_FINAL_2026-09-18.md"

M=(1<<127)-1
PRIMES=[17,19,23,29,31,37]
HIDDEN_COEFFS=[
    (3,4,6,8),(5,7,10,12),(7,10,14,16),(9,13,18,20),
    (11,16,22,24),(13,19,26,28),(15,22,30,32),
]
VISIBLE_ROUNDS=[
    (3,5,7,11,0),(5,7,11,13,1),(7,11,13,17,2),
    (11,13,17,19,3),(13,17,19,23,4),(17,19,23,29,0),
    (19,23,29,31,1),(23,29,31,37,2),(29,31,37,41,3),
    (31,37,41,43,4),(37,41,43,47,0),
]
POSITION_STONE=[0,1,2,3,4,0]
PERMS=list(permutations(range(1,7)))

def _counted(payload:str)->str:
    words=payload.split()
    forms={2:"שנים",3:"שלשה",4:"ארבעה",5:"חמשה",6:"ששה"}
    assert len(words) in forms
    return f"שם אשר מספר המלים אשר בו הוא {forms[len(words)]} והמלים הן {payload}"

def _nat(n:int)->str:
    if n==0:
        return "המספר הנחשב בגרע את המספר אשר הוא אחד מן המספר אשר הוא אחד"
    return "המספר אשר הוא "+format_natural(n)

def _act(name:str)->str:
    return _counted(name) if " " in name else name

def _call(name:str,pairs=()):
    a=_act(name)
    out=f"עשה את המעשה אשר שמו {a}"
    for i,(role,value) in enumerate(pairs):
        out+=(" בהיות " if i==0 else " ובהיות ")+value+f" תחת הדבר אשר במעשה אשר שמו {a} שמו {role}"
    return out

def _place_index(payload:str)->str:
    return f"המעלה אשר במקום אשר שמו {_counted(payload)}"

def _probe_query_decl()->str:
    name="צלם"
    return " ".join([
        f"יהי מעשה ושמו {name}",
        f"זה דבר המעשה אשר שמו {name}",
        f"הוצא מן המעשה הזה את {_place_index('יום שאלת השער')}",
        f"עד הנה דבר המעשה אשר שמו {name}",
    ])

def _probe_gate_decl()->str:
    name="ראי"
    return " ".join([
        f"יהי מעשה ושמו {name}",
        f"זה דבר המעשה אשר שמו {name}",
        f"הוצא מן המעשה הזה את {_place_index('השער הנוכחי')}",
        f"עד הנה דבר המעשה אשר שמו {name}",
    ])

def _reset_gate_to_middle()->str:
    return (
        "שים במקום אשר שמו "+_counted("השער הנוכחי")+" "
        "את "+_place_index("השער התיכון")+" "
        "תחת "+_place_index("השער הנוכחי")
    )

def _t21_bounds(lines:list[str])->tuple[int,int]:
    start=next(i for i,line in enumerate(lines) if line.startswith("יהי מקום ושמו "+_counted("השער התיכון")))
    end=next(i for i,line in enumerate(lines) if line.startswith("# לוח שמונה עשר: שנת חמשת אלפים"))
    return start,end

def _preparation(extra:str="")->str:
    lines=CANDIDATE.read_text(encoding="utf-8").splitlines()
    input_start=next(i for i,line in enumerate(lines) if line.startswith("יהי למלאכה הזאת דבר ושמו "))
    counters_start=next(i for i,line in enumerate(lines) if line.startswith("יהי מקום ושמו "+_counted("מספר המעשה")))
    _,end=_t21_bounds(lines)
    selected=lines[:input_start]+lines[counters_start:end]
    excluded_acts={"חשב שמות המספרים","הכרעת הדרך"}
    excluded_prefixes=[]
    for act_name in excluded_acts:
        a=_counted(act_name)
        excluded_prefixes.extend([
            "יהי מעשה ושמו "+a,
            "זה דבר המעשה אשר שמו "+a+" ",
        ])
    prep=" ".join(
        line for line in selected
        if line.strip()
        and line.strip()!="---"
        and not line.lstrip().startswith("#")
        and not any(line.startswith(prefix) for prefix in excluded_prefixes)
    )
    return prep+((" "+extra) if extra else "")

def _keep(x:int)->int:
    r=x%M
    return r if r else M

@lru_cache(maxsize=1)
def _stones():
    rows=[[17,29,43,71,101]]
    for drop in range(2,47):
        old=rows[-1]
        rows.append([
            _keep(old[0]**2+3*old[1]+drop),
            _keep(old[1]**2+5*old[2]+old[0]),
            _keep(old[2]**2+7*old[3]+old[1]),
            _keep(old[3]**2+11*old[4]+old[2]),
            _keep(old[4]**2+13*old[0]+old[3]),
        ])
    return tuple(tuple(r) for r in rows)

def _hidden(counters):
    action,question,distance,connection,way=counters
    rows=_stones()
    seq=[0,1,2,3,4,0,1]
    out=[]
    for idx,(cq,cd,cc,cw) in enumerate(HIDDEN_COEFFS,start=1):
        row=rows[idx-1]
        x=_keep(action+cq*question+cd*distance+cc*connection+cw*way+sum(row))
        for rnd,stone_idx in enumerate(seq,start=1):
            old=x
            x=_keep(old*old+3*old+row[stone_idx]+rnd)
        out.append(x)
    return out

def _visible(counters):
    action,question,distance,connection,way=counters
    rows=_stones()
    history=list(reversed(_hidden(counters)))
    out=[]
    for drop_number in range(1,47):
        p1,p3,p7=history[-1],history[-3],history[-7]
        row=rows[drop_number-1]
        x=_keep(
            row[0]*action+row[1]*question+row[2]*distance+
            row[3]*connection+row[4]*way+p1+3*p3+5*p7+drop_number
        )
        for a,b,c,d,stone_idx in VISIBLE_ROUNDS:
            old=x
            x=_keep(old*old+a*old+b*p1+c*p3+d*p7+row[stone_idx])
        out.append(x)
        history.append(x)
    return out

def _initial_bowls(counters):
    action,question,distance,connection,way=counters
    out=[]
    for bowl,prime in enumerate(PRIMES,start=1):
        x=action+question*bowl+distance+connection+way+prime*prime
        out.append(_keep(x*x+bowl))
    return out

def _arrangement(number:int):
    return PERMS[(number-1)%720]

def _visible_bowl_work(counters):
    rows=_stones()
    drops=_visible(counters)
    fills=_initial_bowls(counters)
    last_arr=None
    for drop_number,drop in enumerate(drops,start=1):
        arr=_arrangement(drop)
        last_arr=arr
        old=list(fills)
        row=rows[drop_number-1]
        pours=[
            _keep(drop*drop+row[0]*old[arr[0]-1]+3*drop_number),
            _keep(drop*drop+row[1]*old[arr[1]-1]+5*drop_number),
            _keep(drop*drop+row[2]*old[arr[2]-1]+7*drop_number),
        ]
        new=[None]*6
        for position,bowl in enumerate(arr,start=1):
            predecessor=arr[(position-2)%6]
            successor=arr[position%6]
            mixed=old[bowl-1]+2*old[predecessor-1]+3*old[successor-1]
            if position<=3:
                mixed+=pours[position-1]
            mixed+=drop+row[POSITION_STONE[position-1]]
            value=mixed*mixed+5*old[predecessor-1]*old[successor-1]+drop_number*position
            new[bowl-1]=_keep(value)
        fills=new
    assert last_arr is not None
    return fills,last_arr

def _postdrop(counters):
    fills,last_arr=_visible_bowl_work(counters)
    fills=list(fills)
    for round_number in range(1,13):
        old=list(fills)
        bowl_sum=sum(old)
        arrangement_number=_keep(149*round_number+bowl_sum)
        arr=_arrangement(arrangement_number)
        new=[None]*6
        for position,bowl in enumerate(arr,start=1):
            predecessor=arr[(position-2)%6]
            successor=arr[position%6]
            mixed=(
                old[bowl-1]+3*old[predecessor-1]+5*old[successor-1]+
                bowl_sum+round_number+position*position
            )
            new[bowl-1]=_keep(
                mixed*mixed+7*old[predecessor-1]*old[successor-1]
            )
        fills=new
    return fills,last_arr

def _counters(side:str,n:int):
    assert n>=1
    if side=="after":
        return (1,2*n+1,n+1,2*n+2,3)
    return (1,2*n,n+1,2*n+1,1)

def _oracle(side:str,n:int):
    counters=_counters(side,n)
    fills,last_arr=_postdrop(counters)
    pos=last_arr.index(1)
    successor=last_arr[(pos+1)%6]
    first=_keep((fills[0]+1+181)**2+179*fills[successor-1]+1)
    probe=_keep((first+1+1+193)**2+193*first+197*fills[5])
    direction=probe%2
    limit=(M//922)*922
    accepted=first
    while accepted>limit:
        accepted=(1 if accepted==M else accepted+1) if direction==1 else (M if accepted==1 else accepted-1)
    selected=((accepted-1)%922)+1
    gap=selected+41
    return {
        "counters":counters,
        "fills":fills,
        "last_arr":list(last_arr),
        "first":first,
        "direction":direction,
        "selected":selected,
        "gap":gap,
    }

def _index(side:str,magnitude:int):
    if magnitude==0:
        return {"index":"Zero"}
    return {"index":"AfterZero" if side=="after" else "BeforeZero","magnitude":magnitude}

def _run_three_one_each_side():
    extra=_probe_query_decl()
    principal=" ואחרי כן ".join([
        _call("חשב המספר הגדול"),
        _call("אתחל שערים"),
        _call("בנה שערים אחרי",[("מנין",_nat(1))]),
        "עשה את המעשה אשר שמו צלם",
        _call("בנה שערים לפני",[("מנין",_nat(1))]),
        "עשה את המעשה אשר שמו צלם",
    ])
    return three(_preparation(extra)+" ועתה "+principal)[1]

def _run_three_cumulative_steps(a1:int,a2:int,b1:int,b2:int):
    extra=_probe_gate_decl()
    middle=_counted("השער התיכון")
    set_middle=(
        f"שים במקום אשר שמו {middle} את המעלה אשר במקום אשר שמו יסוד "
        f"תחת המעלה אשר במקום אשר שמו {middle}"
    )
    step_after="עשה את המעשה אשר שמו "+_counted("צעד שער אחרי")
    step_before="עשה את המעשה אשר שמו "+_counted("צעד שער לפני")
    principal=" ואחרי כן ".join([
        set_middle,
        _reset_gate_to_middle(),
        format_natural(a1)+" פעמים "+step_after,
        "עשה את המעשה אשר שמו ראי",
        format_natural(a2)+" פעמים "+step_after,
        "עשה את המעשה אשר שמו ראי",
        _reset_gate_to_middle(),
        format_natural(b1)+" פעמים "+step_before,
        "עשה את המעשה אשר שמו ראי",
        format_natural(b2)+" פעמים "+step_before,
        "עשה את המעשה אשר שמו ראי",
    ])
    return three(_preparation(extra)+" ועתה "+principal)[1]

def test_d4_t21_authorized_span_names_reuse_and_constructive_shape():
    lines=CANDIDATE.read_text(encoding="utf-8").splitlines()
    start,end=_t21_bounds(lines)
    block="\n".join(lines[start:end])
    assert start+1==559
    assert "# לוח שמונה עשר" not in block

    names=[
        "השער התיכון","יום שאלת השער","השער הנוכחי","תוצאת השער",
        "רווח השער","מענה השער","כיוון השער","בחירת השער","מונה השערים",
        "צעד יום אחרי","צעד יום לפני","צעד שער אחרי","צעד שער לפני",
        "חשב מוני שער","אתחל שערים","אתחל שאלת שער","חשב רווח שער",
        "השער הבא אחרי","השער הבא לפני","בנה שערים אחרי","בנה שערים לפני",
    ]
    for name in names:
        assert _counted(name) in block
        assert name.replace(" ","") not in block

    assert _counted("השער התיכון") in block
    assert "השערהתיכון" not in block
    for reused in [
        "בנה אבנים","בנה נסתרות","בנה טיפות","אתחל קערות",
        "ערבב כל הטיפות","חשב מענה ראשון","חשב כיוון המענה",
    ]:
        assert "עשה את המעשה אשר שמו "+_counted(reused) in block
    assert "עשה את המעשה אשר שמו גמר" in block
    assert "עשה את המעשה אשר שמו בחירה" in block
    assert _counted("חותם דרך בין שערי קציצה") in block
    assert "המספר אשר הוא תשע מאות ועשרים ושנים" in block
    assert "המספר אשר הוא ארבעים ואחד" in block
    assert "מצא את המערכה" not in block
    init_gates=next(line for line in lines if line.startswith("זה דבר המעשה אשר שמו "+_counted("אתחל שערים")+" "))
    gap_body=next(line for line in lines if line.startswith("זה דבר המעשה אשר שמו "+_counted("חשב רווח שער")+" "))
    assert "עשה את המעשה אשר שמו "+_counted("בנה אבנים") in init_gates
    assert "שים במקום אשר שמו "+_counted("השער התיכון") in init_gates
    assert "המעלה אשר במקום אשר שמו יסוד" in init_gates
    assert _counted("בנה אבנים") not in gap_body

    after=next(line for line in lines if line.startswith("זה דבר המעשה אשר שמו "+_counted("השער הבא אחרי")+" "))
    assert after.index(_counted("צעד יום אחרי")) < after.index(_counted("חשב מוני שער"))
    assert after.index(_counted("חשב מוני שער")) < after.index(_counted("חשב רווח שער"))
    assert "פעמים כמספר אשר במקום אשר שמו "+_counted("רווח השער") in after
    assert _counted("צעד שער אחרי") in after

    before=next(line for line in lines if line.startswith("זה דבר המעשה אשר שמו "+_counted("השער הבא לפני")+" "))
    assert _counted("צעד יום לפני") in before
    assert _counted("צעד שער לפני") in before

    build_after=next(line for line in lines if line.startswith("זה דבר המעשה אשר שמו "+_counted("בנה שערים אחרי")+" "))
    build_before=next(line for line in lines if line.startswith("זה דבר המעשה אשר שמו "+_counted("בנה שערים לפני")+" "))
    assert _place_index("השער התיכון") in build_after
    assert _place_index("השער התיכון") in build_before
    assert "פעמים כמספר אשר במעשה הזה עומד" in build_after
    assert "פעמים כמספר אשר במעשה הזה עומד" in build_before
    assert "ארבעים ושש פעמים" not in block  # T21 itself has no finite gate table.

def test_d4_t21_source_numeral_922_is_normalized_without_value_change():
    original=ORIGINAL.read_text(encoding="utf-8")
    assert "מאחד ועד שנים ועשרים ותשע מאות" in original
    assert format_natural(922)=="תשע מאות ועשרים ושנים"
    src=(
        "יהי מקום ושמו בחן ובמקום אשר שמו בחן יהי המספר אשר הוא "
        +format_natural(922)+
        " לבדו ועתה שים במקום אשר שמו בחן את המספר אשר במקום אשר שמו בחן "
        "תחת המספר אשר במקום אשר שמו בחן"
    )
    c=compile_source(src)
    assert c.valid,[d.to_dict() for d in c.diagnostics]
    obs=backend_observable(execute_ir(c.ir))
    assert dict(obs["facts"])["בחן"]==922

def test_d4_t21_independent_oracle_receipts_bounds_monotonicity_and_asymmetry():
    assert _stones()[1]==(378,1073,2375,6195,10493)
    assert _stones()[-1]==(
        73799454308499791987382386781055001470,
        147925408106533232424672641008220632365,
        94499522601819303005579577099149028685,
        108473647672201258090947028490673028834,
        137131922036975206684616468948804344042,
    )
    assert _hidden((2,3,4,5,1))==[
        11444032270830949316106214743872497511,
        28452868261542307484545760903286527681,
        112739049138818416587726524909828373299,
        152668047685990206548249493436880013083,
        150701631999741008562130578980114868144,
        70454981221026737591078108330515014309,
        119123926606937080003165916448677215346,
    ]
    after=[_oracle("after",n) for n in range(1,5)]
    before=[_oracle("before",n) for n in range(1,5)]
    assert [x["gap"] for x in after]==[377,740,885,200]
    assert [x["gap"] for x in before]==[762,513,584,808]
    assert all(42<=x["gap"]<=963 for x in after+before)
    after_positions=[]
    pos=0
    for x in after:
        pos+=x["gap"]; after_positions.append(pos)
    before_positions=[]
    pos=0
    for x in before:
        pos-=x["gap"]; before_positions.append(pos)
    assert after_positions==[377,1117,2002,2202]
    assert before_positions==[-762,-1275,-1859,-2667]
    assert all(a<b for a,b in zip(after_positions,after_positions[1:]))
    assert all(a>b for a,b in zip(before_positions,before_positions[1:]))
    assert after[0]["gap"]!=before[0]["gap"]

def test_d4_t21_representative_positive_negative_three_runtimes_matches_oracle():
    a1=_oracle("after",1)
    b1=_oracle("before",1)
    obs=_run_three_one_each_side()
    assert obs["outcome"]=="Normal"

    gaps=[v for act,v in obs["products"] if act=="חשב רווח שער"]
    assert gaps==[a1["gap"],b1["gap"]]
    assert all(42<=g<=963 for g in gaps)

    selections=[v for act,v in obs["products"] if act=="בחירה"]
    assert selections[-2:]==[a1["selected"],b1["selected"]]
    firsts=[v for act,v in obs["products"] if act=="חשב מענה ראשון"]
    assert firsts[-2:]==[a1["first"],b1["first"]]
    directions=[v for act,v in obs["products"] if act=="חשב כיוון המענה"]
    assert directions[-2:]==[a1["direction"],b1["direction"]]

    after_steps=[v for act,v in obs["products"] if act=="השער הבא אחרי"]
    before_steps=[v for act,v in obs["products"] if act=="השער הבא לפני"]
    assert after_steps==[_index("after",a1["gap"])]
    assert before_steps==[_index("before",b1["gap"])]

    query_snapshots=[v for act,v in obs["products"] if act=="צלם"]
    assert query_snapshots==[_index("after",1),_index("before",1)]
    assert a1["gap"]!=1
    assert b1["gap"]!=1

    facts=dict(obs["facts"])
    assert facts["השער התיכון"]==_index("after",0)
    assert facts["יום שאלת השער"]==_index("before",1)
    assert facts["השער הנוכחי"]==_index("before",b1["gap"])
    assert facts["מספר המעשה"]==1
    assert facts["מספר השאלה"]==2
    assert facts["מספר המרחק"]==2
    assert facts["מספר החיבור"]==3
    assert facts["מספר הדרך"]==1
    assert facts["מונה השערים"]==1
    assert facts["מלא הקערות"]==b1["fills"]
    assert facts["מערכת הטיפה האחרונה"]==b1["last_arr"]

def test_d4_t21_cumulative_prefix_stepping_three_runtimes():
    a1,a2=_oracle("after",1),_oracle("after",2)
    b1,b2=_oracle("before",1),_oracle("before",2)
    obs=_run_three_cumulative_steps(a1["gap"],a2["gap"],b1["gap"],b2["gap"])
    assert obs["outcome"]=="Normal"
    snapshots=[v for act,v in obs["products"] if act=="ראי"]
    assert snapshots==[
        _index("after",a1["gap"]),
        _index("after",a1["gap"]+a2["gap"]),
        _index("before",b1["gap"]),
        _index("before",b1["gap"]+b2["gap"]),
    ]

def test_d4_t21_query_day_and_gate_day_are_separate_recurrences():
    lines=CANDIDATE.read_text(encoding="utf-8").splitlines()
    after=next(line for line in lines if line.startswith("זה דבר המעשה אשר שמו "+_counted("השער הבא אחרי")+" "))
    before=next(line for line in lines if line.startswith("זה דבר המעשה אשר שמו "+_counted("השער הבא לפני")+" "))
    build_after=next(line for line in lines if line.startswith("זה דבר המעשה אשר שמו "+_counted("בנה שערים אחרי")+" "))
    build_before=next(line for line in lines if line.startswith("זה דבר המעשה אשר שמו "+_counted("בנה שערים לפני")+" "))

    assert after.count("עשה את המעשה אשר שמו "+_counted("צעד יום אחרי"))==1
    assert before.count("עשה את המעשה אשר שמו "+_counted("צעד יום לפני"))==1
    assert after.index(_counted("צעד יום אחרי")) < after.index(_counted("חשב מוני שער"))
    assert before.index(_counted("צעד יום לפני")) < before.index(_counted("חשב מוני שער"))
    assert "פעמים כמספר אשר במקום אשר שמו "+_counted("רווח השער") in after
    assert "פעמים כמספר אשר במקום אשר שמו "+_counted("רווח השער") in before
    assert _counted("צעד שער אחרי") in after
    assert _counted("צעד שער לפני") in before
    assert "פעמים כמספר אשר במעשה הזה עומד" in build_after
    assert "פעמים כמספר אשר במעשה הזה עומד" in build_before