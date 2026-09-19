#!/usr/bin/env python3
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tools'))
from a13_contract_model import validate,ContractError
HEBREW=set('אבגדהוזחטיכךלמםנןסעפףצץקרשת')
CPS=list(range(0x0009,0x000E))+[0x20,0x85,0xA0,0x1680]+list(range(0x2000,0x200B))+[0x2028,0x2029,0x202F,0x205F,0x3000]
WS={chr(c) for c in CPS}
def norm(s):
    out=[]; pending=False
    for ch in s:
        if ch in HEBREW:
            if pending:
                out.append(' ')
                pending=False
            out.append(ch)
        elif ch in WS:
            pending=True
        else:
            # transparent deletion does not end or create a whitespace run
            pass
    if pending:
        out.append(' ')
    return ''.join(out)
checks=0; groups={}
def ck(g,x,msg=''):
    global checks
    if not x: raise AssertionError(msg or g)
    checks+=1; groups[g]=groups.get(g,0)+1
w=json.loads((ROOT/'fixtures'/'a13_whitespace_equivalence.json').read_text(encoding='utf-8'))
ck('meta',len(CPS)==25); ck('meta',len(HEBREW)==27)
for x in w['all_codepoint_boundary_cases']: ck('ws_all',norm(x['source'])==x['expected_normalized'],x['codepoint'])
for x in w['required_equivalence_corpus']: ck('ws_required',norm(x['source'])==x['expected_normalized'],x['id'])
for x in w['u200b_cases']: ck('u200b',norm(x['source'])==x['expected_normalized'])
for ch in HEBREW: ck('letters27',norm(ch)==ch,ch)
for ch in ['#','*','`',',',';',':','(',')','[',']','{','}','1','9','A','z','!','?','־','׃','\u200B']:
    ck('transparent',norm('אב'+ch+'גד')=='אבגד',repr(ch))
p=json.loads((ROOT/'fixtures'/'a13_program_conformance.json').read_text(encoding='utf-8'))
for f in p['positive']:
    ck('program_positive',validate(f['units']) is True,f['id'])
    ck('one_entry',norm(f['source']).count('ועתה')==1,f['id'])
    ck('no_halt_positive','חדל' not in norm(f['source']),f['id'])
for f in p['negative']:
    try: validate(f['units'])
    except ContractError as e: ck('program_negative',str(e)==f['expect'],(f['id'],str(e),f['expect']))
    else: raise AssertionError('negative accepted '+f['id'])
s=json.loads((ROOT/'fixtures'/'a13_subtraction_domain.json').read_text(encoding='utf-8'))
for c in s['cases']:
    A,B=c['A'],c['B']
    if A<=B:
        ck('subtraction',c['status']=='VALUE' and c['value']==B-A,str(c))
        ck('subtraction_nonnegative',c['value']>=0,str(c))
    else:
        ck('subtraction',c['status']=='DOMAIN_FAILURE' and c['value'] is None,str(c))

ck('ws_boundary',norm('\tיהי')==' יהי')
ck('ws_boundary',norm('יהי\u3000')=='יהי ')
ck('ws_boundary',norm('\u00A0#\u200Bיהי')==' יהי')
ck('ws_boundary',norm('יהי \u200B  מקום')=='יהי מקום')
print(json.dumps({'status':'PASS','checks':checks,'groups':groups},ensure_ascii=False,sort_keys=True))
