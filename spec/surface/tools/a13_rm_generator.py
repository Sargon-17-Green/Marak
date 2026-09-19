#!/usr/bin/env python3
import json,sys
from pathlib import Path
ZERO='המספר הנחשב בגרע את המספר אשר הוא אחד מן המספר אשר הוא אחד'
ONE='המספר אשר הוא אחד'
WORDS={0:ZERO,1:'המספר אשר הוא אחד',2:'המספר אשר הוא שנים',3:'המספר אשר הוא שלשה',4:'המספר אשר הוא ארבעה',5:'המספר אשר הוא חמשה',6:'המספר אשר הוא ששה',7:'המספר אשר הוא שבעה',8:'המספר אשר הוא שמנה',9:'המספר אשר הוא תשעה'}
def read(p): return f'המספר אשר במקום אשר שמו {p}'
def repl(p,v): return f'שים במקום אשר שמו {p} את {v} תחת {read(p)}'
def inc(p): return repl(p,f'המספר הנחשב בהוסיף את {ONE} על {read(p)}')
def dec(p): return repl(p,f'המספר הנחשב בגרע את {ONE} מן {read(p)}')
def call(a): return f'עשה את המעשה אשר שמו {a}'
def body(a,c): return f'זה דבר המעשה אשר שמו {a} {c} עד הנה דבר המעשה אשר שמו {a}'
def gen(m):
    rn=m['surface_names']['registers']; ln=m['surface_names']['labels']; hn=m['surface_names'].get('helpers',{}); sink=m['surface_names']['sink']; out=[]
    for r,n in m['registers'].items(): out.append(f'יהי מקום ושמו {rn[r]} ובמקום אשר שמו {rn[r]} יהי {WORDS[n]} לבדו')
    out.append(f'יהי מקום ושמו {sink} ובמקום אשר שמו {sink} יהי {ZERO} לבדו')
    acts=[ln[x] for x in m['instructions']]
    for l,i in m['instructions'].items():
        if i['op']=='DECJZ': acts.append(hn[l])
    for a in acts: out.append(f'יהי מעשה ושמו {a}')
    for l,i in m['instructions'].items():
        a=ln[l]
        if i['op']=='INC': c=inc(rn[i['register']])+' ואחרי כן '+call(ln[i['next']])
        elif i['op']=='DECJZ':
            p=rn[i['register']]; c=f"אם {read(p)} הוא {ZERO} {call(ln[i['zero']])} ואם לא {call(hn[l])}"
        elif i['op']=='HALT': c=repl(sink,read(sink))
        out.append(body(a,c))
    for l,i in m['instructions'].items():
        if i['op']=='DECJZ': out.append(body(hn[l],dec(rn[i['register']])+' ואחרי כן '+call(ln[i['nonzero']])) )
    out.append('ועתה '+call(ln[m['entry']]))
    src=' '.join(out); assert 'חדל' not in src and src.count('ועתה')==1; return src
def sim(m,limit=1000):
    regs=dict(m['registers']); pc=m['entry']
    for n in range(limit+1):
        i=m['instructions'][pc]
        if i['op']=='HALT': return {'halted':True,'steps':n,'registers':regs}
        if i['op']=='INC': regs[i['register']]+=1; pc=i['next']
        else:
            r=i['register']
            if regs[r]==0: pc=i['zero']
            else: regs[r]-=1; pc=i['nonzero']
    return {'halted':False,'steps':limit,'registers':regs}
if __name__=='__main__':
    m=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8')); print(gen(m)); print(json.dumps(sim(m),ensure_ascii=False),file=sys.stderr)
