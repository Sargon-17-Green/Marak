#!/usr/bin/env python3
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[4]
SOURCE=ROOT/"megillah/original/Megilat_HaItim_Yehuda_FINAL_2026-09-18.md"
OUT=Path(__file__).resolve().parents[1]/"corpora"
HEBREW=set("אבגדהוזחטיכךלמםנןסעפףצץקרשת")
WS=set(chr(cp) for cp in list(range(0x9,0xE))+[0x20,0x85,0xA0,0x1680]+list(range(0x2000,0x200B))+[0x2028,0x2029,0x202F,0x205F,0x3000])
BASE={"אחד":1,"אחת":1,"שנים":2,"שניים":2,"שני":2,"שתים":2,"שתיים":2,"שתי":2,"שלשה":3,"שלושה":3,"שלש":3,"שלוש":3,"שלשת":3,"ארבעה":4,"ארבע":4,"ארבעת":4,"חמשה":5,"חמש":5,"חמשת":5,"ששה":6,"שש":6,"ששת":6,"שבעה":7,"שבע":7,"שבעת":7,"שמנה":8,"שמונה":8,"שמנת":8,"תשעה":9,"תשע":9,"תשעת":9,"עשרה":10,"עשר":10,"עשרת":10,"עשרים":20,"שלשים":30,"שלושים":30,"ארבעים":40,"חמשים":50,"חמישים":50,"ששים":60,"שישים":60,"שבעים":70,"שמנים":80,"שמונים":80,"תשעים":90,"מאה":100,"מאתים":200,"מאתיים":200}
SCALES={"מאות","אלף","אלפים","רבבה","רבבות"}; NUMWORDS=set(BASE)|SCALES
def normalize(s):
    out=[]; pending=False
    for c in s:
        if c in HEBREW:
            if pending and out: out.append(" ")
            pending=False; out.append(c)
        elif c in WS: pending=True
    return re.sub(r" +"," ","".join(out)).strip()
def de_waw(w):
    if w in NUMWORDS:return w
    if w.startswith("ו") and w[1:] in NUMWORDS:return w[1:]
def parse_simple(words):
    current=total=0;i=0
    while i<len(words):
        w=de_waw(words[i])
        if w is None:return None
        if w in BASE: current+=BASE[w];i+=1;continue
        if w=="מאות":
            if current<=0:return None
            current*=100;i+=1;continue
        if w in {"אלף","אלפים"}:
            if current==0:current=1
            current*=1000
            if i+1<len(words) and de_waw(words[i+1]) in {"אלף","אלפים"}:current*=1000;i+=1
            total+=current;current=0;i+=1;continue
        if w in {"רבבה","רבבות"}:
            if current==0:current=1
            total+=current*10000;current=0;i+=1;continue
    return total+current
lines=SOURCE.read_text(encoding="utf-8").splitlines(); numeral_rows=[];times_rows=[]
for lineno,raw in enumerate(lines,1):
    norm=normalize(raw);words=norm.split();spans=[];i=0
    while i<len(words):
        if de_waw(words[i]) is None:i+=1;continue
        j=i
        while j<len(words) and de_waw(words[j]) is not None:j+=1
        span=words[i:j];spans.append({"raw_normalized":" ".join(span),"research_value":parse_simple(span)});i=j
    if spans:numeral_rows.append({"line":lineno,"raw":raw,"normalized":norm,"numeral_spans":spans})
    if "פעמים" in words:
        occ=[]
        for idx,w in enumerate(words):
            if w!="פעמים":continue
            following=" ".join(words[idx:idx+4])
            if idx+1<len(words) and (words[idx+1].startswith("כמספר") or words[idx+1].startswith("כמלא") or words[idx+1]=="כמספר"):kind="runtime_count";best=None
            else:
                best=None
                for width in range(1,min(8,idx)+1):
                    cand=words[idx-width:idx]
                    if all(de_waw(x) is not None for x in cand):best=(cand,parse_simple(cand))
                    else:break
                kind="literal_count" if best else "other_times_usage"
            item={"token_index":idx,"kind":kind,"following":following}
            if best:item.update(count_phrase=" ".join(best[0]),research_count=best[1])
            occ.append(item)
        times_rows.append({"line":lineno,"raw":raw,"normalized":norm,"occurrences":occ})
for row in numeral_rows:
    if row["line"]==41: row["manual_large_analysis"]=[{"phrase":"תשעה וארבעים ומאה","value":149},{"phrase":"שבעה ושבעים ושבע מאות אלף","value":777000},{"phrase":"ארבעה עשר אלף אלפים","value":14000000},{"sum":14777149}]
    if row["line"]==43: row["manual_large_analysis"]=[{"value":14777149,"decomposition":[149,7000,70000,700000,4000000,10000000]}]
OUT.mkdir(parents=True,exist_ok=True)
(OUT/"A14_MEGILLAH_NUMERAL_CENSUS.json").write_text(json.dumps({"source":str(SOURCE.relative_to(ROOT)).replace("\\","/"),"line_count":len(numeral_rows),"rows":numeral_rows},ensure_ascii=False,indent=2),encoding="utf-8")
(OUT/"A14_MEGILLAH_TIMES_CENSUS.json").write_text(json.dumps({"source":str(SOURCE.relative_to(ROOT)).replace("\\","/"),"token_times_count":sum(len(r["occurrences"]) for r in times_rows),"line_count":len(times_rows),"rows":times_rows},ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"numeral_lines":len(numeral_rows),"times_tokens":sum(len(r["occurrences"]) for r in times_rows),"times_lines":len(times_rows)},ensure_ascii=False))
