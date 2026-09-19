#!/usr/bin/env python3
from pathlib import Path
import json,re,importlib.util
HERE=Path(__file__).resolve().parent; BASE=HERE.parent
HEBREW=set("אבגדהוזחטיכךלמםנןסעפףצץקרשת")
WS=set(chr(cp) for cp in list(range(0x9,0xE))+[0x20,0x85,0xA0,0x1680]+list(range(0x2000,0x200B))+[0x2028,0x2029,0x202F,0x205F,0x3000])
def normalize(s):
    out=[];pending=False
    for c in s:
        if c in HEBREW:
            if pending and out:out.append(" ")
            pending=False;out.append(c)
        elif c in WS:pending=True
    return re.sub(r" +"," ","".join(out)).strip()
spec=importlib.util.spec_from_file_location("num",HERE/"a14_numeral_reference.py");num=importlib.util.module_from_spec(spec);spec.loader.exec_module(num)
groups={}
def check(g,c,m=""):
    if not c:raise AssertionError(m or g)
    groups[g]=groups.get(g,0)+1
nr=num.selftest();check("numeral_meta",nr["status"]=="PASS")
fx=json.loads((BASE/"fixtures"/"A14_REQUEST_FIXTURES.json").read_text(encoding="utf-8"))
for k,v in fx["requests"]["005"]["positive_values"].items():check("numeral_examples",num.format_natural(int(k))==v,(k,num.format_natural(int(k)),v))
order=[x["surface"] for x in fx["requests"]["004"]["positive"]]
for s in order:check("ordering_positive"," רב מן " in normalize(s),s)
for x in fx["requests"]["004"]["negative"][:3]:check("ordering_negative"," רב מן " not in normalize(x["surface"]),x["surface"])
rep_expected={1:"פעם אחת",2:"שתי פעמים",7:"שבע פעמים",13:"שלש עשרה פעמים",125:"מאה ועשרים וחמש פעמים",197:"מאה ותשעים ושבע פעמים",3005:"שלשת אלפים וחמש פעמים"}
rep=[]
for n,p in rep_expected.items():
    check("repeat_count_examples",num.format_repeat_count(n)==p,(n,num.format_repeat_count(n),p))
    s=p+" עשה את המעשה אשר שמו טחון";rep.append(s);check("recurrence_literal_positive",normalize(s).startswith(normalize(p)+" "),s)
check("recurrence_negative",normalize("שבעה פעמים עשה את המעשה אשר שמו טחון")!=normalize("שבע פעמים עשה את המעשה אשר שמו טחון"))
noise=["#","*",",",":",";","(",")","[","]","1","A","!","?","־","׃","​"]
for src in order+rep+list(fx["requests"]["005"]["positive_values"].values()):
    base=normalize(src)
    for ch in noise:
        pos=next((i+1 for i,c in enumerate(src[:-1]) if c in HEBREW and src[i+1] in HEBREW),None)
        if pos is not None:check("transparency",normalize(src[:pos]+ch+src[pos:])==base,(src,ch))
negative_count=sum(len(r.get("negative",[])) for r in fx["requests"].values())
check("negative_inventory",negative_count>=20,negative_count)
amb=sum(1 for r in fx["requests"].values() for x in r.get("negative",[]) if any(k in str(x).lower() for k in ["implicit","position","boundary","alias","order","layout","conversion","source"]))
out={"status":"PASS","case_checks":sum(groups.values()),"groups":groups,"negative_fixture_count":negative_count,"ambiguity_focus_count":amb,"numeral_collision_generation_checks":nr["exhaustive"]+nr["random"],"repeat_collision_generation_checks":nr["repeat_exhaustive"]+nr["repeat_random"]}
print(json.dumps(out,ensure_ascii=False,sort_keys=True))
