#!/usr/bin/env python3
from __future__ import annotations
import random
UNITS={1:"אחד",2:"שנים",3:"שלשה",4:"ארבעה",5:"חמשה",6:"ששה",7:"שבעה",8:"שמנה",9:"תשעה"}
TEENS={10:"עשרה",11:"אחד עשר",12:"שנים עשר",13:"שלשה עשר",14:"ארבעה עשר",15:"חמשה עשר",16:"ששה עשר",17:"שבעה עשר",18:"שמנה עשר",19:"תשעה עשר"}
TENS={20:"עשרים",30:"שלשים",40:"ארבעים",50:"חמשים",60:"ששים",70:"שבעים",80:"שמנים",90:"תשעים"}
HUNDREDS={100:"מאה",200:"מאתים",300:"שלש מאות",400:"ארבע מאות",500:"חמש מאות",600:"שש מאות",700:"שבע מאות",800:"שמנה מאות",900:"תשע מאות"}
THOUSANDS={1000:"אלף",2000:"שני אלפים",3000:"שלשת אלפים",4000:"ארבעת אלפים",5000:"חמשת אלפים",6000:"ששת אלפים",7000:"שבעת אלפים",8000:"שמנת אלפים",9000:"תשעת אלפים"}
MILLION_2_10={2:"שני אלפי אלפים",3:"שלשת אלפי אלפים",4:"ארבעת אלפי אלפים",5:"חמשת אלפי אלפים",6:"ששת אלפי אלפים",7:"שבעת אלפי אלפים",8:"שמנת אלפי אלפים",9:"תשעת אלפי אלפים",10:"עשרת אלפי אלפים"}
def waw(s): return "ו"+s
def join(parts):
    parts=[p for p in parts if p]
    return "" if not parts else parts[0]+"".join(" "+waw(p) for p in parts[1:])
def small(n):
    if not 1<=n<=9999: raise ValueError(n)
    if n<10: return UNITS[n]
    if n<20: return TEENS[n]
    if n<100:
        q,r=divmod(n,10); return TENS[q*10] if r==0 else TENS[q*10]+" ו"+UNITS[r]
    if n<1000:
        h,r=divmod(n,100); return HUNDREDS[h*100] if r==0 else HUNDREDS[h*100]+" ו"+small(r)
    th,r=divmod(n,1000); head=THOUSANDS[th*1000]; return head if r==0 else head+" ו"+small(r)
def millions(m):
    if m==1: return "אלף אלפים"
    if 2<=m<=10: return MILLION_2_10[m]
    if 11<=m<=99: return small(m)+" אלף אלפים"
    raise ValueError(m)
def thousand_components(k):
    if not 0<=k<=999: raise ValueError(k)
    if k==0: return []
    if k==1: return ["אלף"]
    if 2<=k<=9: return [THOUSANDS[k*1000]]
    if k==10: return ["עשרת אלפים"]
    if 11<=k<=19: return [small(k)+" אלף"]
    out=[]; h,rest=divmod(k,100); t,u=divmod(rest,10)
    if h: out.append(HUNDREDS[h*100]+" אלף")
    if t: out.append("עשרת אלפים" if t==1 else TENS[t*10]+" אלף")
    if u: out.append(THOUSANDS[u*1000])
    return out
def format_natural(n):
    if not 1<=n<=99_999_999: raise ValueError("A14 direct numeral domain is 1..99,999,999")
    if n<=9999: return small(n)
    m,rem=divmod(n,1_000_000); k,lo=divmod(rem,1000); parts=[]
    if m: parts.append(millions(m))
    parts.extend(thousand_components(k))
    if lo: parts.append(small(lo))
    return join(parts)
F_UNITS={1:"אחת",2:"שתים",3:"שלש",4:"ארבע",5:"חמש",6:"שש",7:"שבע",8:"שמנה",9:"תשע"}
F_TEENS={10:"עשר",11:"אחת עשרה",12:"שתים עשרה",13:"שלש עשרה",14:"ארבע עשרה",15:"חמש עשרה",16:"שש עשרה",17:"שבע עשרה",18:"שמנה עשרה",19:"תשע עשרה"}
def feminine_small(n):
    if not 1<=n<=999: raise ValueError(n)
    if n<10: return F_UNITS[n]
    if n<20: return F_TEENS[n]
    if n<100:
        q,r=divmod(n,10); return TENS[q*10] if r==0 else TENS[q*10]+" ו"+F_UNITS[r]
    h,r=divmod(n,100); return HUNDREDS[h*100] if r==0 else HUNDREDS[h*100]+" ו"+feminine_small(r)
def format_repeat_count(n):
    if not 1<=n<=99_999_999: raise ValueError("A14 repeat-count domain is 1..99,999,999")
    if n==1: return "פעם אחת"
    if n==2: return "שתי פעמים"
    if n<1000: return feminine_small(n)+" פעמים"
    m,rem=divmod(n,1_000_000); k,lo=divmod(rem,1000); parts=[]
    if m: parts.append(millions(m))
    parts.extend(thousand_components(k))
    if lo: parts.append(feminine_small(lo))
    return join(parts)+" פעמים"
def selftest():
    examples={9999:"תשעת אלפים ותשע מאות ותשעים ותשעה",10000:"עשרת אלפים",14000:"ארבעה עשר אלף",14700:"ארבעה עשר אלף ושבע מאות",307500:"שלש מאות אלף ושבעת אלפים וחמש מאות",1000000:"אלף אלפים",14777149:"ארבעה עשר אלף אלפים ושבע מאות אלף ושבעים אלף ושבעת אלפים ומאה וארבעים ותשעה",99999999:"תשעים ותשעה אלף אלפים ותשע מאות אלף ותשעים אלף ותשעת אלפים ותשע מאות ותשעים ותשעה"}
    for n,s in examples.items(): assert format_natural(n)==s,(n,format_natural(n),s)
    seen={}
    for n in range(1,250001):
        s=format_natural(n)
        if s in seen: raise AssertionError((seen[s],n,s))
        seen[s]=n
    rnd=random.Random(14014); sampled={}
    for _ in range(50000):
        n=rnd.randint(250001,99999999); s=format_natural(n); prior=sampled.get(s)
        if prior is not None and prior!=n: raise AssertionError((prior,n,s))
        sampled[s]=n
    reps={1:"פעם אחת",2:"שתי פעמים",3:"שלש פעמים",10:"עשר פעמים",13:"שלש עשרה פעמים",125:"מאה ועשרים וחמש פעמים",197:"מאה ותשעים ושבע פעמים",3005:"שלשת אלפים וחמש פעמים"}
    for n,s in reps.items(): assert format_repeat_count(n)==s,(n,format_repeat_count(n),s)
    seen={}
    for n in range(1,250001):
        s=format_repeat_count(n)
        if s in seen: raise AssertionError((seen[s],n,s))
        seen[s]=n
    sampled={}
    for _ in range(50000):
        n=rnd.randint(250001,99999999); s=format_repeat_count(n); prior=sampled.get(s)
        if prior is not None and prior!=n: raise AssertionError((prior,n,s))
        sampled[s]=n
    return {"exhaustive":250000,"random":50000,"repeat_exhaustive":250000,"repeat_random":50000,"status":"PASS"}
if __name__=="__main__":
    import json; print(json.dumps(selftest(),ensure_ascii=False))
