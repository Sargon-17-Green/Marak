from __future__ import annotations

"""Productive A15 direct-Natural and feminine-count numeral recognition.

This module intentionally implements the accepted canonical A15 edition family
without importing proposal/reference code into the production compiler.
It is an exact recognizer: a phrase is admitted iff it is the canonical
formatter output for exactly one value in the edition frontier.
"""

from compiler.parse.numeral_lexicons import A12_VALUE_BY_TEXT

A15_DIRECT_NUMERAL_LEXICON_ID = "a15-direct-1-99999999"
A15_FEMININE_COUNT_LEXICON_ID = "a15-feminine-count-3-99999999"
MAX_A15_NUMERAL_WORDS = 24

UNITS={1:'אחד',2:'שנים',3:'שלשה',4:'ארבעה',5:'חמשה',6:'ששה',7:'שבעה',8:'שמנה',9:'תשעה'}
TEENS={10:'עשרה',11:'אחד עשר',12:'שנים עשר',13:'שלשה עשר',14:'ארבעה עשר',15:'חמשה עשר',16:'ששה עשר',17:'שבעה עשר',18:'שמנה עשר',19:'תשעה עשר'}
TENS={20:'עשרים',30:'שלשים',40:'ארבעים',50:'חמשים',60:'ששים',70:'שבעים',80:'שמנים',90:'תשעים'}
HUNDREDS={100:'מאה',200:'מאתים',300:'שלש מאות',400:'ארבע מאות',500:'חמש מאות',600:'שש מאות',700:'שבע מאות',800:'שמנה מאות',900:'תשע מאות'}
THOUSANDS={1000:'אלף',2000:'שני אלפים',3000:'שלשת אלפים',4000:'ארבעת אלפים',5000:'חמשת אלפים',6000:'ששת אלפים',7000:'שבעת אלפים',8000:'שמנת אלפים',9000:'תשעת אלפים'}
MILLION_2_10={2:'שני אלפי אלפים',3:'שלשת אלפי אלפים',4:'ארבעת אלפי אלפים',5:'חמשת אלפי אלפים',6:'ששת אלפי אלפים',7:'שבעת אלפי אלפים',8:'שמנת אלפי אלפים',9:'תשעת אלפי אלפים',10:'עשרת אלפי אלפים'}
F_UNITS={1:'אחת',2:'שתים',3:'שלש',4:'ארבע',5:'חמש',6:'שש',7:'שבע',8:'שמנה',9:'תשע'}
F_TEENS={10:'עשר',11:'אחת עשרה',12:'שתים עשרה',13:'שלש עשרה',14:'ארבע עשרה',15:'חמש עשרה',16:'שש עשרה',17:'שבע עשרה',18:'שמנה עשרה',19:'תשע עשרה'}

def _waw(s: str) -> str:
    return "ו" + s

def _join(parts: list[str]) -> str:
    parts=[p for p in parts if p]
    return "" if not parts else parts[0] + "".join(" " + _waw(p) for p in parts[1:])

def _small(n: int) -> str:
    if not 1 <= n <= 9999: raise ValueError(n)
    if n < 10: return UNITS[n]
    if n < 20: return TEENS[n]
    if n < 100:
        q,r=divmod(n,10); return TENS[q*10] if r==0 else TENS[q*10]+" ו"+UNITS[r]
    if n < 1000:
        h,r=divmod(n,100); return HUNDREDS[h*100] if r==0 else HUNDREDS[h*100]+" ו"+_small(r)
    th,r=divmod(n,1000); head=THOUSANDS[th*1000]; return head if r==0 else head+" ו"+_small(r)

def _feminine_small(n: int) -> str:
    if not 1 <= n <= 999: raise ValueError(n)
    if n < 10: return F_UNITS[n]
    if n < 20: return F_TEENS[n]
    if n < 100:
        q,r=divmod(n,10); return TENS[q*10] if r==0 else TENS[q*10]+" ו"+F_UNITS[r]
    h,r=divmod(n,100); return HUNDREDS[h*100] if r==0 else HUNDREDS[h*100]+" ו"+_feminine_small(r)

def _millions(m: int) -> str:
    if m==1: return "אלף אלפים"
    if 2 <= m <= 10: return MILLION_2_10[m]
    if 11 <= m <= 99: return _small(m)+" אלף אלפים"
    raise ValueError(m)

def _thousand_components(k: int) -> list[str]:
    if not 0 <= k <= 999: raise ValueError(k)
    if k==0: return []
    if k==1: return ["אלף"]
    if 2 <= k <= 9: return [THOUSANDS[k*1000]]
    if k==10: return ["עשרת אלפים"]
    if 11 <= k <= 19: return [_small(k)+" אלף"]
    out=[]; h,rest=divmod(k,100); t,u=divmod(rest,10)
    if h: out.append(HUNDREDS[h*100]+" אלף")
    if t: out.append("עשרת אלפים" if t==1 else TENS[t*10]+" אלף")
    if u: out.append(THOUSANDS[u*1000])
    return out

def format_natural(n: int) -> str:
    if not 1 <= n <= 99_999_999:
        raise ValueError(n)
    if n <= 9999:
        return _small(n)
    m,rem=divmod(n,1_000_000); k,lo=divmod(rem,1000); parts=[]
    if m: parts.append(_millions(m))
    parts.extend(_thousand_components(k))
    if lo: parts.append(_small(lo))
    return _join(parts)

def format_feminine_count(n: int) -> str:
    if not 1 <= n <= 99_999_999: raise ValueError(n)
    if n < 1000: return _feminine_small(n)
    m,rem=divmod(n,1_000_000); k,lo=divmod(rem,1000); parts=[]
    if m: parts.append(_millions(m))
    parts.extend(_thousand_components(k))
    if lo: parts.append(_feminine_small(lo))
    return _join(parts)

def _tokens(s: str) -> tuple[str, ...]:
    return tuple(s.split())

def _prefixed_first(parts: tuple[str, ...]) -> tuple[str, ...]:
    if not parts: return parts
    return ("ו"+parts[0],)+parts[1:]

_MILLION = {_tokens(_millions(m)):m*1_000_000 for m in range(1,100)}
_THOUSAND = {_tokens(_join(_thousand_components(k))):k*1000 for k in range(1,1000)}
_LOW = {_tokens(_small(n)):n for n in range(1,1000)}
_F_LOW = {_tokens(_feminine_small(n)):n for n in range(1,1000)}
_F_LOW_BY_TEXT = {_feminine_small(n):n for n in range(1,1000)}

def _by_len(table: dict[tuple[str,...],int], *, prefixed: bool=False):
    out={}
    for phrase,value in table.items():
        key=_prefixed_first(phrase) if prefixed else phrase
        out.setdefault(len(key),{})[key]=value
    return out

_INDEX={
    ("million",False):_by_len(_MILLION),
    ("million",True):_by_len(_MILLION,prefixed=True),
    ("thousand",False):_by_len(_THOUSAND),
    ("thousand",True):_by_len(_THOUSAND,prefixed=True),
    ("low",False):_by_len(_LOW),
    ("low",True):_by_len(_LOW,prefixed=True),
    ("flow",False):_by_len(_F_LOW),
    ("flow",True):_by_len(_F_LOW,prefixed=True),
}

def _prefix_matches(kind: str, words: tuple[str,...], pos: int, prefixed: bool):
    out=[]
    for length,table in _INDEX[(kind,prefixed)].items():
        end=pos+length
        if end>len(words):
            continue
        candidate=words[pos:end]
        value=table.get(candidate)
        if value is not None:
            out.append((end,value))
    return out

def _parse_composite(words: tuple[str,...], *, feminine_low: bool) -> int | None:
    if not words:
        return None
    # A13's exact family remains authoritative through 9999.
    text=" ".join(words)
    if not feminine_low:
        a12=A12_VALUE_BY_TEXT.get(text)
        if a12 is not None:
            return a12
    elif len(words) <= 6:
        # Exact feminine forms below 1000 are handled by the same canonical
        # formatter used by the A15 reference evidence.
        direct=_F_LOW_BY_TEXT.get(text)
        if direct is not None:
            return direct

    mchoices=[(0,0)]+_prefix_matches("million",words,0,False)
    answers=set()
    for mpos,mval in mchoices:
        tchoices=[(mpos,0)]+_prefix_matches("thousand",words,mpos,mval>0)
        for tpos,tval in tchoices:
            low_kind="flow" if feminine_low else "low"
            lchoices=[(tpos,0)]+_prefix_matches(low_kind,words,tpos,(mval>0 or tval>0))
            for end,lval in lchoices:
                if end != len(words):
                    continue
                value=mval+tval+lval
                if 1 <= value <= 99_999_999:
                    canonical=format_feminine_count(value) if feminine_low else format_natural(value)
                    if canonical==text:
                        answers.add(value)
    if len(answers)==1:
        return next(iter(answers))
    return None

def match_a15_numeral(lexicon_id: str, words: tuple[str,...], start: int):
    if lexicon_id not in {A15_DIRECT_NUMERAL_LEXICON_ID,A15_FEMININE_COUNT_LEXICON_ID}:
        raise KeyError(lexicon_id)
    feminine=lexicon_id==A15_FEMININE_COUNT_LEXICON_ID
    out=[]
    stop=min(len(words),start+MAX_A15_NUMERAL_WORDS)
    for end in range(start+1,stop+1):
        phrase=words[start:end]
        value=_parse_composite(phrase,feminine_low=feminine)
        if value is None:
            continue
        if feminine and value < 3:
            continue
        out.append((end,value," ".join(phrase)))
    return tuple(out)

__all__=[
    "A15_DIRECT_NUMERAL_LEXICON_ID","A15_FEMININE_COUNT_LEXICON_ID",
    "MAX_A15_NUMERAL_WORDS","format_natural","format_feminine_count",
    "match_a15_numeral",
]
