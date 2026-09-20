from itertools import permutations
from b13_reference_model import *

def sf(code,fn):
    try: fn()
    except SemanticFailure as e: assert e.code==code; return
    raise AssertionError(code)
def inv(code,fn):
    try: fn()
    except InvalidInvocation as e: assert e.code==code; return
    raise AssertionError(code)

def test_symbol_identity():
    a=SymbolDomain(1,'a'); b=SymbolDomain(2,'b')
    x=SymbolMember(a,1,'נר'); y=SymbolMember(a,1,'נר'); z=SymbolMember(b,1,'נר'); q=SymbolMember(a,2,'נר')
    assert symbol_equal(x,y) and not symbol_equal(x,z) and not symbol_equal(x,q)

def test_symbol_domain_collection_guard():
    a=SymbolDomain(1,'a'); b=SymbolDomain(2,'b'); c=FiniteOrderedCollection(symbol_domain(a),(SymbolMember(a,1,'x'),))
    sf(COLLECTION_ELEMENT_DOMAIN_ERROR,lambda:c.append(SymbolMember(b,1,'x')))

def test_index_zero_crossings():
    z=from_math_index(0); assert z.pred()==from_math_index(-1) and z.succ()==from_math_index(1)
    assert from_math_index(-1).succ()==z and from_math_index(1).pred()==z

def test_index_inverse_grid():
    for n in range(-300,301):
        x=from_math_index(n); assert x.succ().pred()==x and x.pred().succ()==x

def test_index_order_distance_grid():
    for a in range(-50,51):
        for b in range(-50,51):
            x,y=from_math_index(a),from_math_index(b)
            assert index_lt(x,y)==(a<b) and x.distance(y)==Natural(abs(a-b))

def test_index_conversion():
    assert index_from_natural(Natural(0))==from_math_index(0)
    assert index_from_natural(Natural(8))==from_math_index(8)
    assert from_math_index(8).to_natural()==Natural(8)
    sf(INDEX_TO_NATURAL_DOMAIN_ERROR,lambda:from_math_index(-1).to_natural())

def test_collection_append_immutable():
    c=FiniteOrderedCollection(NAT_DOMAIN,()); d=c.append(Natural(4)).append(Natural(9))
    assert c.items==() and d.items==(Natural(4),Natural(9)) and d.count()==Natural(2)

def test_collection_one_based_positions():
    c=FiniteOrderedCollection(NAT_DOMAIN,(Natural(10),Natural(20),Natural(30)))
    assert c.select(Natural(1))==Natural(10) and c.select(Natural(3))==Natural(30)
    sf(COLLECTION_POSITION_ERROR,lambda:c.select(Natural(0))); sf(COLLECTION_POSITION_ERROR,lambda:c.select(Natural(4)))

def test_collection_membership():
    c=FiniteOrderedCollection(NAT_DOMAIN,(Natural(1),Natural(2),Natural(2)))
    assert c.contains(Natural(2)) and not c.contains(Natural(3))

def test_collection_order():
    c=FiniteOrderedCollection(NAT_DOMAIN,tuple(Natural(x) for x in [5,1,3,1,9])); o=order_collection(c,nat_lt)
    assert [x.n for x in o.items]==[1,1,3,5,9] and [x.n for x in c.items]==[5,1,3,1,9]

def test_collection_order_permutations():
    target=(Natural(1),Natural(2),Natural(3))
    for p in permutations(target): assert order_collection(FiniteOrderedCollection(NAT_DOMAIN,p),nat_lt).items==target

def test_nested_lex_order():
    books=[FiniteOrderedCollection(NAT_DOMAIN,tuple(Natural(x) for x in xs)) for xs in ([2,1],[1,9],[1,2],[1,2,0])]
    outer=FiniteOrderedCollection(collection_domain(NAT_DOMAIN),tuple(books)); lt=lambda a,b:lex_lt(NAT_DOMAIN,nat_lt,a,b)
    got=order_collection(outer,lt).items
    assert [[x.n for x in b.items] for b in got]==[[1,2],[1,2,0],[1,9],[2,1]]

def test_invalid_order_relation():
    c=FiniteOrderedCollection(NAT_DOMAIN,(Natural(1),Natural(2))); sf(ORDER_RELATION_ERROR,lambda:order_collection(c,lambda a,b:a!=b))

def test_natural_order_trichotomy_huge():
    vals=[0,1,2,10**100,10**1000,10**2000+17]
    for av in vals:
        for bv in vals:
            a,b=Natural(av),Natural(bv); assert sum((nat_lt(a,b),a==b,nat_gt(a,b)))==1
            assert nat_le(a,b)==(av<=bv) and nat_ge(a,b)==(av>=bv)

def test_repeat_zero():
    calls=[]; r=repeat_exactly(lambda:Natural(0),lambda s,i:(calls.append(i) or StepNormal(s+1)),5)
    assert r==StepNormal(5,()) and calls==[]

def test_repeat_one(): assert repeat_exactly(lambda:Natural(1),lambda s,i:StepNormal(s+2),3)==StepNormal(5,())
def test_repeat_large(): assert repeat_exactly(lambda:Natural(10000),lambda s,i:StepNormal(s+1),0).state==10000

def test_count_evaluated_once():
    calls={'n':0}
    def count(): calls['n']+=1; return Natural(7)
    r=repeat_exactly(count,lambda s,i:StepNormal(s+1),0); assert calls['n']==1 and r.state==7

def test_repeat_error_boundary():
    def action(s,i): return StepError(s,'BOOM') if i==4 else StepNormal(s+1)
    assert repeat_exactly(lambda:Natural(10),action,0)==StepError(3,'BOOM',())

def test_repeat_outputs_not_collection():
    r=repeat_exactly(lambda:Natural(3),lambda s,i:StepNormal(s,(Natural(i),)),0)
    assert r.outputs==(Natural(1),Natural(2),Natural(3)) and not isinstance(r.outputs,FiniteOrderedCollection)

def test_repeat_wrong_count_domain():
    r=repeat_exactly(lambda:from_math_index(3),lambda s,i:StepNormal(s+1),0)
    assert isinstance(r,StepError) and r.code==RECURRENCE_COUNT_DOMAIN_ERROR and r.state==0

def pair(): return ProgramInputId(1,'calculation_day',NAT_DOMAIN),ProgramInputId(2,'target_day',NAT_DOMAIN)
def test_inputs_named_order_independent():
    a,b=pair(); c=ProgramContract((a,b)); x=bind_invocation(c,[(a,Natural(10)),(b,Natural(20))]); y=bind_invocation(c,[(b,Natural(20)),(a,Natural(10))])
    assert x.get(a)==y.get(a)==Natural(10) and x.get(b)==y.get(b)==Natural(20)
def test_input_missing():
    a,b=pair(); inv(MISSING_INPUT_BINDING,lambda:bind_invocation(ProgramContract((a,b)),[(a,Natural(1))]))
def test_input_extra():
    a,b=pair(); e=ProgramInputId(3,'extra',NAT_DOMAIN); inv(EXTRA_INPUT_BINDING,lambda:bind_invocation(ProgramContract((a,b)),[(a,Natural(1)),(b,Natural(2)),(e,Natural(3))]))
def test_input_duplicate():
    a,b=pair(); inv(DUPLICATE_INPUT_BINDING,lambda:bind_invocation(ProgramContract((a,b)),[(a,Natural(1)),(a,Natural(2)),(b,Natural(3))]))
def test_input_domain_mismatch():
    a,b=pair(); inv(INPUT_DOMAIN_MISMATCH,lambda:bind_invocation(ProgramContract((a,b)),[(a,from_math_index(1)),(b,Natural(2))]))
def test_input_binding_immutable_value():
    a,b=pair(); x=bind_invocation(ProgramContract((a,b)),[(a,Natural(1)),(b,Natural(2))]); assert x.values==((a,Natural(1)),(b,Natural(2)))

def test_large_natural_no_ceiling():
    expected=10**5000+123; n=Natural(expected); assert n.n==expected and n.n>9999

TESTS=[v for k,v in sorted(globals().items()) if k.startswith('test_') and callable(v)]
if __name__=='__main__':
    for t in TESTS: t(); print('PASS',t.__name__)
    print(f'B13 REFERENCE TESTS: PASS ({len(TESTS)} tests)')
