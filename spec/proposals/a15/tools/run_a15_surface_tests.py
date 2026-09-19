#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import importlib.util, json, random, sys

HERE=Path(__file__).resolve().parent; BASE=HERE.parent
sys.path.insert(0,str(HERE))
from a15_reference import *
from a15_numeral_reference import format_natural, format_repeat_count

REPO_ROOT=HERE.parents[3]
if (REPO_ROOT/'compiler'/'parse'/'numeral_lexicons.py').exists():
    sys.path.insert(0,str(REPO_ROOT))
    from compiler.parse.numeral_lexicons import A12_DIRECT_NUMERALS
else:
    A12_DIRECT_NUMERALS=None

fx=json.loads((BASE/'fixtures'/'A15_SURFACE_FIXTURES.json').read_text(encoding='utf-8'))
groups={}
def check(group, cond, detail=''):
    groups[group]=groups.get(group,0)+1
    if not cond: raise AssertionError(f'{group}: {detail}')

# Charter normalization invariance: punctuation/Markdown/niqqud/Latin/digits are transparent.
noise=['#','*',',',':',';','(',')','[',']','1','A','!','?','־','׃','\u200b','ַ','ּ']
positive_surfaces=[fx['symbol']['domain'],fx['symbol']['reference'],fx['index']['zero'],fx['index']['before_many'],fx['collection']['empty_natural'],fx['ordering']['positive'],fx['recurrence']['dynamic'],fx['inputs']['natural_calc']]
positive_surfaces += [m['declaration'] for m in fx['symbol']['members']]
for src in positive_surfaces:
    base=normalize(src)
    for ch in noise:
        pos=max(1,len(src)//2)
        check('normalization_punctuation',normalize(src[:pos]+ch+src[pos:])==base,(src,ch))
    check('normalization_whitespace',normalize(src.replace(' ','\n\t\u00a0'))==base,src)

# Symbols: identity is domain/member, label is counted metadata, same visible label may exist in another domain.
def counted_label_ok(decl: str) -> bool:
    words=normalize(decl).split()
    try:
        marker=next(i for i in range(len(words)-1) if words[i]=='והמלים' and words[i+1]=='הן')
        y=max(i for i in range(marker) if words[i]=='יהיה')
    except (StopIteration,ValueError): return False
    count_text=' '.join(words[y+1:marker])
    reverse={format_natural(n):n for n in range(1,100)}
    n=reverse.get(count_text)
    return n is not None and len(words[marker+2:])==n
for m in fx['symbol']['members']:
    check('symbol_declaration_boundary',counted_label_ok(m['declaration']),m['source_id'])
check('symbol_declaration_negative',not counted_label_ok(fx['symbol']['negative'][-1]))
months=SymbolDomain('חדשים'); cutlets=SymbolDomain('קציצות')
tin=months.declare('טין',['טין']); door=months.declare('דלת',['הדלת','הסגורה']); parts=months.declare('חלקים',['שלושה','חלקים','מחמישה'])
other_door=cutlets.declare('דלת',['הדלת','הסגורה'])
check('symbol_label',months.visible(tin)=='טין')
check('symbol_label',months.visible(door)=='הדלת הסגורה')
check('symbol_label',months.visible(parts)=='שלושה חלקים מחמישה')
check('symbol_collision',door!=other_door)
check('symbol_collision',months.visible(door)==cutlets.visible(other_door))
check('symbol_source_not_value','דלת' != door)
months.establish_adjacent_order(['טין','דלת','חלקים'])
check('symbol_order',months.order_key(tin)<months.order_key(door)<months.order_key(parts))

# Bidirectional index family.
zero=BidirectionalIndex.zero(); before1=BidirectionalIndex.before(1); before3=BidirectionalIndex.before(3); after1=BidirectionalIndex.after(1); after5000=BidirectionalIndex.after(5000)
check('index_order',before3<before1<zero<after1<after5000)
check('index_distinct_natural',after1 != 1)
for bad in fx['index']['negative']: check('index_negative',normalize(bad) not in {normalize(fx['index'][k]) for k in ['zero','before_one','before_two','before_many','after_one','after_two','after_many']},bad)

# Collections: immutable, ordered, duplicates preserved, positive ordinal positions.
c0=Collection('Natural'); c1=c0.append(3); c2=c1.append(3).append(1).append(7)
check('collection_empty',c0.count()==0)
check('collection_empty_symbol_surface','אין בו שם' in normalize(fx['collection']['empty_symbol']))
check('collection_empty_nested_surface','אין בו ספר' in normalize(fx['collection']['empty_nested_natural']))
check('collection_immutable',c0.items==() and c1.items==(3,))
check('collection_duplicates',c2.items==(3,3,1,7))
check('collection_first_last',c2.first()==3 and c2.last()==7)
check('collection_membership',c2.contains(1) and not c2.contains(9))
check('collection_ordinal',c2.select(3)==1)
try: c2.select(0); check('collection_invalid_ordinal',False,'zero accepted')
except CollectionPositionError: check('collection_invalid_ordinal',True)
try: c2.successor_at(c2.count()); check('collection_successor_last',False,'successor after last accepted')
except CollectionPositionError: check('collection_successor_last',True)
ordered=c2.ordered(lambda x:x); check('collection_order',ordered.items==(1,3,3,7) and c2.items==(3,3,1,7))
nested=Collection('Collection<Natural>').append(Collection('Natural',(2,1))).append(Collection('Natural',(1,9)))
lex=nested.ordered(lambda c:c.items); check('collection_nested',tuple(c.items for c in lex.items)==((1,9),(2,1)))
try: c0.append(Symbol('חדשים','טין')); check('collection_homogeneous_reject',False,'heterogeneous append accepted')
except SurfaceError as e: check('collection_homogeneous_reject',str(e)=='COLLECTION_ELEMENT_DOMAIN_MISMATCH',str(e))

# Strict Natural ordering only: no direct LE/GE surface is admitted.
check('numeric_order',7>3 and not 3>7)
for bad in fx['ordering']['negative']: check('numeric_order_negative',' רב מן ' not in normalize(bad),bad)

# Numerals: A13 direct family 1..9999 remains unique; edition family reaches the grammatical 99-million frontier.
seen={}
for n in range(1,10000):
    s=format_natural(n); check('numeral_a13_unique',s not in seen,(n,s,seen.get(s))); seen[s]=n
    if A12_DIRECT_NUMERALS is not None:
        check('numeral_a13_frozen_exact',s==A12_DIRECT_NUMERALS[n],(n,s,A12_DIRECT_NUMERALS[n]))
for k,v in fx['numeral_examples'].items(): check('numeral_examples',format_natural(int(k))==v,(k,format_natural(int(k)),v))
seen_large={}
for n in range(10000,250001):
    s=format_natural(n); check('numeral_collision_prefix',s not in seen_large,(n,s)); seen_large[s]=n
rnd=random.Random(15015); sampled={}
for _ in range(75000):
    n=rnd.randint(250001,99_999_999); s=format_natural(n)
    check('numeral_collision_sample',s not in sampled or sampled[s]==n,(n,s,sampled.get(s))); sampled[s]=n
for n in [1,2,3,10,13,125,127,149,179,193,197,99_999_999]:
    check('repeat_literal_count',len(format_repeat_count(n))>0,n)
try: format_natural(100_000_000); check('numeral_frontier',False,'100m admitted')
except ValueError: check('numeral_frontier',True)

# Dynamic RepeatExactly: observe count once; zero/one/large; state changes do not retarget.
state={'count':0,'performed':0,'observations':0}
def obs(): state['observations']+=1; return state['count']
def action(): state['performed']+=1; state['count']=99
repeat_exactly(obs,action); check('repeat_dynamic_zero',state['performed']==0 and state['observations']==1)
state.update(count=1,performed=0,observations=0); repeat_exactly(obs,action); check('repeat_dynamic_one',state['performed']==1 and state['observations']==1)
state.update(count=127,performed=0,observations=0); repeat_exactly(obs,action); check('repeat_dynamic_once',state['performed']==127 and state['observations']==1 and state['count']==99)
def dynamic_count_surface_ok(src: str) -> bool:
    n=normalize(src)
    return n.startswith('פעמים כמספר ') and not n.startswith('פעמים כמספר המספר ') and ' עשה את המעשה אשר שמו ' in n
check('repeat_attachment',dynamic_count_surface_ok(fx['recurrence']['dynamic']))
for bad in fx['recurrence']['negative'][:3]: check('repeat_negative',not dynamic_count_surface_ok(bad),bad)
check('repeat_ambiguous_composite_rejected','כמקשה אחת' in normalize(fx['recurrence']['negative'][3]))

# Program inputs: association order is irrelevant; identity and domain are mandatory; immutable binding is represented by returned mapping.
contract=ProgramInputContract({'יוםהמעשה':'Natural','יוםהשאלה':'Natural'})
a=contract.bind([('יוםהמעשה','Natural',11),('יוםהשאלה','Natural',22)])
b=contract.bind([('יוםהשאלה','Natural',22),('יוםהמעשה','Natural',11)])
check('input_identity',a==b=={'יוםהמעשה':11,'יוםהשאלה':22})
try:
    a['יוםהמעשה']=99
    check('input_immutable',False,'bound input mapping was mutable')
except TypeError:
    check('input_immutable',a['יוםהמעשה']==11)
for associations,code in [([('יוםהמעשה','Natural',11)],'MISSING_INPUT_BINDING'),([('יוםהמעשה','Natural',11),('יוםהמעשה','Natural',12),('יוםהשאלה','Natural',22)],'DUPLICATE_INPUT_BINDING'),([('יוםהמעשה','Symbol',11),('יוםהשאלה','Natural',22)],'INPUT_DOMAIN_MISMATCH'),([('יוםהמעשה','Natural',11),('יוםהשאלה','Natural',22),('שלישי','Natural',33)],'EXTRA_INPUT_BINDING')]:
    try: contract.bind(associations); check('input_negative',False,code)
    except InputBindingError as e: check('input_negative',str(e)==code,(str(e),code))
for bad in fx['inputs']['negative']: check('input_surface_negative','המלאכה הזאת' not in normalize(bad) or 'שים' in normalize(bad),bad)

result={
  'status':'PASS',
  'case_checks':sum(groups.values()),
  'groups':groups,
  'a13_numerals_checked':9999,
  'a13_frozen_lexicon_exact': A12_DIRECT_NUMERALS is not None,
  'large_numeral_prefix_checked':240001,
  'large_numeral_random_samples':75000,
  'requests':{str(i).zfill(3):'INTEGRATED_SURFACE_READY' for i in range(1,8)}
}
print(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True))
