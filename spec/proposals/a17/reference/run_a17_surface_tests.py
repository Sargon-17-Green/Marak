#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from collections import Counter
import json, re, sys

HERE=Path(__file__).resolve()
ROOT=HERE.parents[1]
FIX=ROOT/"fixtures"/"A17_SURFACE_FIXTURES.json"
RESULT=ROOT/"A17_TEST_RESULTS.json"
fx=json.loads(FIX.read_text(encoding="utf-8"))

HEBREW=set("אבגדהוזחטיכךלמםנןסעפףצץקרשת")
WS=set(chr(cp) for cp in list(range(0x9,0xE))+[0x20,0x85,0xA0,0x1680]+list(range(0x2000,0x200B))+[0x2028,0x2029,0x202F,0x205F,0x3000])

def normalize(s:str)->str:
    out=[]; pending=False
    for ch in s:
        if ch in HEBREW:
            if pending and out: out.append(" ")
            pending=False; out.append(ch)
        elif ch in WS:
            pending=True
        else:
            continue
    return re.sub(r" +"," ","".join(out)).strip()

@dataclass(frozen=True)
class Index:
    z:int
    @property
    def side(self): return "ZERO" if self.z==0 else ("AFTER" if self.z>0 else "BEFORE")
    @property
    def magnitude(self): return abs(self.z)

COUNT_WORDS={"שלש":3,"ארבע":4,"חמש":5,"שש":6,"שבע":7,"שמנה":8,"תשע":9}
REV_COUNT={v:k for k,v in COUNT_WORDS.items()}

def parse_generic_literal(s:str)->Index|None:
    n=normalize(s)
    if n=="מעלת היתד": return Index(0)
    m=re.fullmatch(r"מעלה אחת (לפני|אחרי) מעלת היתד",n)
    if m: return Index(-1 if m.group(1)=="לפני" else 1)
    m=re.fullmatch(r"שתי מעלות (לפני|אחרי) מעלת היתד",n)
    if m: return Index(-2 if m.group(1)=="לפני" else 2)
    m=re.fullmatch(r"(שלש|ארבע|חמש|שש|שבע|שמנה|תשע) מעלות (לפני|אחרי) מעלת היתד",n)
    if m:
        k=COUNT_WORDS[m.group(1)]
        return Index(-k if m.group(2)=="לפני" else k)
    return None

def render_generic(i:Index)->str:
    z=i.z
    if z==0: return "מעלת היתד"
    direction="אחרי" if z>0 else "לפני"
    k=abs(z)
    if k==1: return f"מעלה אחת {direction} מעלת היתד"
    if k==2: return f"שתי מעלות {direction} מעלת היתד"
    if k in REV_COUNT: return f"{REV_COUNT[k]} מעלות {direction} מעלת היתד"
    raise ValueError("reference renderer only covers fixture count atoms 1..9")

def succ(i:Index)->Index: return Index(i.z+1)
def pred(i:Index)->Index: return Index(i.z-1)
def lt(a:Index,b:Index)->bool: return a.z<b.z

def parse_strict_order(s:str):
    toks=normalize(s).split()
    matches=[]
    for j,t in enumerate(toks):
        if t!="לפני": continue
        a=parse_generic_literal(" ".join(toks[:j]))
        b=parse_generic_literal(" ".join(toks[j+1:]))
        if a is not None and b is not None:
            matches.append((a,b))
    return matches

counts=Counter(); failures=[]
def check(group, cond, detail="", polarity="positive"):
    counts["total"]+=1; counts[polarity]+=1; counts["group:"+group]+=1
    if not cond: failures.append(f"{group}: {detail}")

check("baseline",fx["baseline"]=="e8f766889676b219f0abf5c9e4f08fad3034fa5b")
check("semantic_domain",fx["semantic_domain"]=="BidirectionalIndex")
check("no_new_domains",set(fx["forbidden_new_semantic_domains"]).isdisjoint({fx["semantic_domain"]}))

expected={"zero":0,"before_one":-1,"before_two":-2,"before_three":-3,"before_seven":-7,"after_one":1,"after_two":2,"after_three":3,"after_seven":7}
for key,z in expected.items():
    got=parse_generic_literal(fx["generic_literals"][key])
    check("literal_mapping",got==Index(z),f"{key}: {got} != {z}")
for z in range(-9,10):
    src=render_generic(Index(z))
    check("literal_roundtrip",parse_generic_literal(src)==Index(z),src)
for z in range(-500,501):
    i=Index(z)
    check("succ",succ(i)==Index(z+1),str(z)); check("pred",pred(i)==Index(z-1),str(z))
    check("inverse_pred_succ",pred(succ(i))==i,str(z)); check("inverse_succ_pred",succ(pred(i))==i,str(z))
order=fx["carrier_forms"]["strict_order"]
matches=parse_strict_order(order)
check("strict_order_unique_parse",len(matches)==1,repr(matches))
if matches: check("strict_order_semantics",lt(*matches[0]) is True,repr(matches[0]))
a,b=Index(-2),Index(3); check("after_by_reversal",(a.z>b.z)==lt(b,a))
positives=list(fx["generic_literals"].values())+list(fx["carrier_forms"].values())
ws_variants=["\t","\n","\r\n","\u00a0","\u1680","\u2003","\u2028","\u2029","\u202f","\u205f","\u3000"]
for src in positives:
    canon=normalize(src); check("normalized_nonempty",bool(canon),src)
    for ws in ws_variants: check("whitespace_invariance",normalize(ws.join(src.split(" ")))==canon,repr(src))
    decorated="**"+src.replace(" "," , ")+"**"; check("punctuation_markdown_transparency",normalize(decorated)==canon,repr(src))
    idx=next((i for i,c in enumerate(src) if c in HEBREW),None)
    if idx is not None:
        with_niqqud=src[:idx+1]+"\u05b0"+src[idx+1:]; check("niqqud_transparency",normalize(with_niqqud)==canon,repr(src))
for src in fx["negative"]: check("negative_literal_rejection",parse_generic_literal(src) is None,src,"negative")
for src in fx["negative_order"]: check("negative_order_rejection",len(parse_strict_order(src))==0,src,"negative")
generic_norm={normalize(x) for x in fx["generic_literals"].values()}
for src in fx["year_controls"]:
    check("year_unchanged_disjoint",normalize(src) not in generic_norm,src); check("generic_parser_rejects_year",parse_generic_literal(src) is None,src)
for src in fx["natural_controls"]:
    check("natural_unchanged_disjoint",normalize(src) not in generic_norm,src); check("generic_parser_rejects_natural",parse_generic_literal(src) is None,src)
current=set(fx["current_exact_word_terminals"]); new=set(fx["new_exact_word_terminals"])
check("current_word_inventory_count",len(current)==115,str(len(current))); check("new_word_inventory_count",len(new)==8,str(len(new)))
check("no_existing_word_terminal_collision",current.isdisjoint(new),repr(current & new))
for src in fx["identifier_collision_controls"]: check("identifier_name_freedom_witness",any(w in normalize(src).split() for w in new),src)
c=fx["carrier_forms"]
check("input_feminine_declaration","תעמד מעלה" in normalize(c["program_input_declaration"])); check("input_feminine_reference","המעלה אשר עומדת" in normalize(c["program_input_reference"]))
check("role_feminine_declaration","תעמד מעלה" in normalize(c["role_declaration"])); check("role_feminine_current","המעלה אשר במעשה הזה עומדת" in normalize(c["role_current"]))
check("result_feminine","המעלה אשר יצאה עתה" in normalize(c["immediate_result"])); check("place_generic_head",normalize(c["place_current"]).startswith("המעלה אשר במקום"))
check("output_reuses_existing_verb",normalize(c["output"]).startswith("הוצא מן המעשה הזה את"))
for forbidden in ("מספר יום","מספר היום","מינוס","אפס"): check("no_forbidden_canonical_form",all(forbidden not in normalize(x) for x in positives),forbidden)
check("no_generic_index_collection_kind",all("ספר מעלות" not in normalize(x) for x in positives)); check("no_index_equality_surface",all(" הוא " not in (" "+normalize(x)+" ") for x in positives)); check("no_direct_distance_surface",all("מרחק" not in normalize(x) for x in positives))
status="PASS" if not failures else "FAIL"
result={"schema":"marak-a17-proposal-test-results-v1","baseline":fx["baseline"],"status":status,"checks":{"total":counts["total"],"positive":counts["positive"],"negative":counts["negative"],"groups":{k[6:]:v for k,v in sorted(counts.items()) if k.startswith("group:")}},"selected_profile":"מעלה / מעלת היתד","current_registry_word_terminals":115,"new_exact_construction_local_word_terminals":8,"new_semantic_domains":[],"production_files_changed":[],"megillah_changed":False,"failures":failures}
RESULT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(result,ensure_ascii=False,indent=2)); raise SystemExit(0 if status=="PASS" else 1)
