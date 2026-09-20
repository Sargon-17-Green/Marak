#!/usr/bin/env python3
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT))

from spec.proposals.a15.tools.a15_reference import SymbolDomain, BidirectionalIndex, Collection, normalize
from spec.proposals.a16.reference.a16_reference import (
    A16Error, Place, Role, value_domain, initialize_place, current_place_value, replace_place,
    bind_roles, current_role_value, resolve_output_domain, Occurrence, invalidate_immediate,
    read_immediate, index_successor, index_predecessor, symbol_equal_proposition,
    PLACE_DOMAIN_MISMATCH, ROLE_DOMAIN_MISMATCH, MIXED_OUTPUT_DOMAINS, SECOND_OUTPUT,
    STALE_IMMEDIATE_RESULT, IMMEDIATE_RESULT_HEAD_MISMATCH, INDEX_OPERAND_DOMAIN_MISMATCH,
    SYMBOL_EQUALITY_DOMAIN_MISMATCH
)

FX_PATH=ROOT/'spec/proposals/a16/fixtures/A16_SURFACE_FIXTURES.json'
RESULT_PATH=ROOT/'spec/proposals/a16/A16_TEST_RESULTS.json'
fx=json.loads(FX_PATH.read_text(encoding='utf-8'))

counts=Counter()
failures=[]

def check(group, condition, detail='', polarity='positive'):
    counts['total']+=1
    counts[polarity]+=1
    counts['group:'+group]+=1
    if not condition:
        failures.append(f'{group}: {detail}')

def expect_error(group, code, fn, detail=''):
    try:
        fn()
    except A16Error as exc:
        check(group, exc.args and exc.args[0]==code, f'{detail} got={exc}', 'negative')
    except Exception as exc:
        check(group, False, f'{detail} unexpected={type(exc).__name__}:{exc}', 'negative')
    else:
        check(group, False, f'{detail} did not fail', 'negative')

def idx(z):
    if z==0: return BidirectionalIndex.zero()
    return BidirectionalIndex.after(z) if z>0 else BidirectionalIndex.before(-z)

def whitespace_variant(s, ws):
    return ws.join(s.split(' '))

# Charter normalization for every new canonical construction.
for name,source in fx['canonical'].items():
    canonical=normalize(source)
    check('surface_canonical_nonempty', bool(canonical), name)
    for ws in ['\t','\n','\r\n','\u00a0','\u2003','\u202f','\u3000']:
        check('surface_whitespace', normalize(whitespace_variant(source,ws))==canonical, name)
    decorated='**'+source.replace(' ',' , ')+'**'
    check('surface_punctuation_transparency', normalize(decorated)==canonical, name)

# Full compositional sources: one principal execution and expected carrier phrases.
for name,source in fx['programs'].items():
    n=normalize(source)
    check('program_one_principal_execution', n.split().count('ועתה')==1, name)
    check('program_nontrivial', len(n.split())>150, name)
check('program_A_symbol_equality', normalize(fx['canonical']['symbol_equality']) in normalize(fx['programs']['A_symbol_flow']))
check('program_B_pred', 'מספר השנה אשר לפני' in normalize(fx['programs']['B_index_flow']))
check('program_B_succ', 'מספר השנה אשר אחר' in normalize(fx['programs']['B_index_flow']))
check('program_C_count', 'מספר הדברים אשר בתוך' in normalize(fx['programs']['C_collection_flow']))
check('program_C_select', 'מספרו בסדר' in normalize(fx['programs']['C_collection_flow']))

# Symbol model and same-label identity.
colors=SymbolDomain('צבעים')
red=colors.declare('אדום',['אדום'])
blue=colors.declare('כחול',['כחול'])
red_alias=colors.declare('ארגמן',['אדום'])
months=SymbolDomain('חדשים')
tin=months.declare('טין',['אדום'])
check('symbol_equal_same', symbol_equal_proposition(red,red) is True)
check('symbol_equal_different_member', symbol_equal_proposition(red,blue) is False)
check('symbol_equal_same_label_different_member', symbol_equal_proposition(red,red_alias) is False)
expect_error('symbol_equal_cross_domain',SYMBOL_EQUALITY_DOMAIN_MISMATCH,lambda:symbol_equal_proposition(red,tin))
expect_error('symbol_equal_source_identifier','SYMBOL_EQUALITY_OPERAND_DOMAIN_MISMATCH',lambda:symbol_equal_proposition('אדום','אדום'))

# Program A semantic carrier flow.
sp,sstate=initialize_place('שמור',red)
check('A_symbol_place_domain',sp.domain=='Symbol:צבעים')
check('A_symbol_place_read',current_place_value(sstate,sp,'Symbol:צבעים')==red)
srole=Role('העבר','קלט','Symbol:צבעים')
sbindings=bind_roles([srole],[(srole,current_place_value(sstate,sp))])
sarg=current_role_value(sbindings,srole,'Symbol:צבעים')
check('A_symbol_role_read',sarg==red)
check('A_symbol_conditional',symbol_equal_proposition(sarg,red) is True)
sout=resolve_output_domain(['Symbol:צבעים','Symbol:צבעים'])
occ=Occurrence('העבר',sout)
occ.emit(sarg)
occ.later_action()
check('output_not_termination',occ.later_actions==1 and occ.output==red)
sres=occ.complete()
sstate=replace_place(sstate,sp,lambda:read_immediate(sres,'העבר','Symbol:צבעים'),'Symbol:צבעים')
check('A_symbol_final_retained',current_place_value(sstate,sp)==red)

# Typed state failures and atomic commit boundary.
ip,istate=initialize_place('שנה',BidirectionalIndex.after(1))
cp,cstate=initialize_place('ספרון',Collection('Natural'))
expect_error('state_wrong_domain_symbol_into_index',PLACE_DOMAIN_MISMATCH,lambda:replace_place(istate,ip,lambda:red,'BidirectionalIndex'))
expect_error('state_wrong_domain_collection_into_symbol',PLACE_DOMAIN_MISMATCH,lambda:replace_place(sstate,sp,lambda:Collection('Natural'),'Symbol:צבעים'))
expect_error('implicit_place_dereference','VALUE_DOMAIN_MISMATCH',lambda:value_domain(sp))
before=istate
def failing_rhs():
    raise A16Error('RHS_FAILURE')
expect_error('state_failed_rhs_no_commit','RHS_FAILURE',lambda:replace_place(istate,ip,failing_rhs,'BidirectionalIndex'))
check('state_failed_rhs_original_unchanged',before==istate)

# Program B exact zero crossing and role/output flow.
istate=replace_place(istate,ip,lambda:index_predecessor(current_place_value(istate,ip)),'BidirectionalIndex')
check('B_pred_after1_zero',current_place_value(istate,ip).key()==0)
istate=replace_place(istate,ip,lambda:index_predecessor(current_place_value(istate,ip)),'BidirectionalIndex')
check('B_pred_zero_before1',current_place_value(istate,ip).key()==-1)
istate=replace_place(istate,ip,lambda:index_successor(current_place_value(istate,ip)),'BidirectionalIndex')
check('B_succ_before1_zero',current_place_value(istate,ip).key()==0)
istate=replace_place(istate,ip,lambda:index_successor(current_place_value(istate,ip)),'BidirectionalIndex')
check('B_succ_zero_after1',current_place_value(istate,ip).key()==1)
irole=Role('הקדם','קלט','BidirectionalIndex')
ib=bind_roles([irole],[(irole,current_place_value(istate,ip))])
iarg=current_role_value(ib,irole,'BidirectionalIndex')
iocc=Occurrence('הקדם',resolve_output_domain(['BidirectionalIndex']))
iocc.emit(index_predecessor(iarg))
ires=iocc.complete()
istate=replace_place(istate,ip,lambda:read_immediate(ires,'הקדם','BidirectionalIndex'),'BidirectionalIndex')
check('B_index_final_zero',current_place_value(istate,ip).key()==0)

# Index totality/inverses over a broad exact grid.
for z in range(-300,301):
    v=idx(z)
    check('index_succ_key',index_successor(v).key()==z+1,str(z))
    check('index_pred_key',index_predecessor(v).key()==z-1,str(z))
    check('index_pred_succ_inverse',index_predecessor(index_successor(v))==v,str(z))
    check('index_succ_pred_inverse',index_successor(index_predecessor(v))==v,str(z))
expect_error('index_succ_natural',INDEX_OPERAND_DOMAIN_MISMATCH,lambda:index_successor(1))
expect_error('index_pred_natural',INDEX_OPERAND_DOMAIN_MISMATCH,lambda:index_predecessor(0))

# Program C: pure collection accumulation, retained replacement, role, count/select, output.
empty=Collection('Natural')
bp,bstate=initialize_place('ספרון',empty)
c0=current_place_value(bstate,bp,'Collection<Natural>')
c1=c0.append(1)
check('C_append_pure_old_empty',c0.items==())
check('C_append_new_one',c1.items==(1,))
bstate=replace_place(bstate,bp,lambda:c1,'Collection<Natural>')
c2=current_place_value(bstate,bp).append(2)
check('C_append_second_pure_prior',current_place_value(bstate,bp).items==(1,))
bstate=replace_place(bstate,bp,lambda:c2,'Collection<Natural>')
brole=Role('החזרספר','קלט','Collection<Natural>')
bb=bind_roles([brole],[(brole,current_place_value(bstate,bp))])
book=current_role_value(bb,brole,'Collection<Natural>')
check('C_count',book.count()==2)
check('C_select_first',book.select(1)==1)
bocc=Occurrence('החזרספר',resolve_output_domain(['Collection<Natural>']))
bocc.emit(book)
bres=bocc.complete()
bstate=replace_place(bstate,bp,lambda:read_immediate(bres,'החזרספר','Collection<Natural>'),'Collection<Natural>')
check('C_collection_final_retained',current_place_value(bstate,bp).items==(1,2))

# Role, output, and immediate-result negative boundaries.
expect_error('role_wrong_domain',ROLE_DOMAIN_MISMATCH,lambda:bind_roles([srole],[(srole,Collection('Natural'))]))
expect_error('role_identity_not_value','VALUE_DOMAIN_MISMATCH',lambda:value_domain(srole))
expect_error('mixed_output_sites',MIXED_OUTPUT_DOMAINS,lambda:resolve_output_domain(['Symbol:צבעים','BidirectionalIndex']))
second=Occurrence('העבר','Symbol:צבעים')
second.emit(red)
expect_error('second_output',SECOND_OUTPUT,lambda:second.emit(blue))
stale=invalidate_immediate(sres)
expect_error('stale_immediate',STALE_IMMEDIATE_RESULT,lambda:read_immediate(stale,'העבר','Symbol:צבעים'))
expect_error('wrong_immediate_head',IMMEDIATE_RESULT_HEAD_MISMATCH,lambda:read_immediate(sres,'העבר','Natural'))

# Every required negative surface witness is present and nonempty; semantic counterparts above own rejection.
required_negative={
'untyped_non_natural_place','symbol_into_index_place','collection_into_symbol_role','role_identity_as_value',
'natural_head_for_symbol_result','stale_symbol_immediate','second_output','natural_underflow_to_index',
'standalone_none','label_equality','source_identifier_equality','implicit_place_deref','implicit_result_deref',
'succ_on_natural','cross_domain_symbol_equality'
}
seen={x['id'] for x in fx['negative_surface']}
check('negative_fixture_coverage',seen==required_negative,repr(seen))
neg={x['id']:normalize(x['source']) for x in fx['negative_surface']}
validated=set()
if 'השם אשר במשפחת השמות' not in neg['untyped_non_natural_place']: validated.add('untyped_non_natural_place')
validated.update({'symbol_into_index_place','collection_into_symbol_role','role_identity_as_value','natural_head_for_symbol_result','stale_symbol_immediate','second_output'})
if 'המספר הנחשב בגרע' in neg['natural_underflow_to_index']: validated.add('natural_underflow_to_index')
if neg['standalone_none']=='אין': validated.add('standalone_none')
validated.update({'label_equality','source_identifier_equality','implicit_place_deref'})
if not neg['implicit_result_deref'].startswith(('המספר ','השם ','מספר השנה ','הספר ')): validated.add('implicit_result_deref')
validated.update({'succ_on_natural','cross_domain_symbol_equality'})
check('negative_semantic_witness_coverage',validated==required_negative,repr(required_negative-validated),'negative')
for item in fx['negative_surface']:
    check('negative_surface_nonempty',bool(normalize(item['source'])),item['id'],'negative')

status='PASS' if not failures else 'FAIL'
result={
 'schema':'marak-a16-test-results-v1',
 'status':status,
 'baseline_b14':'3c2c1d1ea4afda7365e912b161735112d63e9ac3',
 'checks':{
   'total':counts['total'],
   'positive':counts['positive'],
   'negative':counts['negative'],
   'groups':{k[6:]:v for k,v in sorted(counts.items()) if k.startswith('group:')}
 },
 'compositional_programs':['A_symbol_flow','B_index_flow','C_collection_flow'],
 'failures':failures
}
RESULT_PATH.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(0 if status=='PASS' else 1)
