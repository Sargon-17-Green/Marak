from __future__ import annotations
import hashlib, inspect, json, os, re, subprocess, sys, tempfile, unittest
from pathlib import Path
C=Path(os.environ['E_V082_C_ROOT']); H=Path(os.environ['E_V082_C_HANDOFF_ROOT']); E08=Path(os.environ['E_V082_E08_ROOT']); A=Path(os.environ['E_V082_A13_ROOT'])
sys.path[:0]=[str(C),str(E08/'tools')]
from v08_common import *
from compiler.api import compile_source
from compiler.runtime.reference import execute_reference,ReferenceEvaluator,NormalOutcome,ResourceExhaustionOutcome,DEFAULT_MAX_ACTIVE_PERFORMANCES as HD
from compiler.runtime.ir_reference import execute_reference_ir,IRReferenceEvaluator,IRReferenceNormal,IRReferenceResourceExhaustion,DEFAULT_MAX_ACTIVE_PERFORMANCES as ID
from compiler.backend.portable import execute_ir,PortableVM,VMNormal,VMResourceExhaustion,DEFAULT_MAX_ACTIVE_PERFORMANCES as BD
from compiler.runtime.observables import reference_observable,ir_reference_observable,backend_observable
from compiler.version import LANGUAGE_NAME,COMPILER_VERSION

def expr(n):
    if n<=9999:return literal(n)
    parts=[]
    while n>9999:parts.append(9999);n-=9999
    parts.append(n);s=literal(parts[-1])
    for x in reversed(parts[:-1]):s=add(literal(x),s)
    return s

def deep(n):
    return ' '.join([place_intro('גד',expr(n)),act_intro('ראובן'),act_intro('שמעון'),act_intro('יהודה'),body('ראובן',f'אם {eq(current("גד"),ZERO)} {perform("יהודה")} ואם לא {perform("שמעון")}'),body('שמעון',replace_place('גד',sub(literal(1),current('גד')))+' ואחרי כן '+perform('ראובן')),body('יהודה',replace_place('גד',current('גד'))),'ועתה '+perform('ראובן')])
def seq(n):
    return ' '.join([place_intro('גד',expr(n)),act_intro('ראובן'),body('ראובן',replace_place('גד',sub(literal(1),current('גד')))),'ועתה '+perform('ראובן')+' וכן תעשה עד אשר '+eq(current('גד'),ZERO)])
def three(src,**kw):
    c=compile_source(src);assert c.valid,[d.to_dict() for d in c.diagnostics]
    h=execute_reference(c.hast,**kw);i=execute_reference_ir(c.ir,**kw);b=execute_ir(c.ir,**kw);return c,h,i,b

class ResourceClosure(unittest.TestCase):
    def test_defaults_none_all_layers(self):
        self.assertIsNone(HD);self.assertIsNone(ID);self.assertIsNone(BD)
        self.assertIsNone(inspect.signature(execute_reference).parameters['max_active_performances'].default)
        self.assertIsNone(inspect.signature(execute_reference_ir).parameters['max_active_performances'].default)
        self.assertIsNone(inspect.signature(execute_ir).parameters['max_active_performances'].default)
    def test_runtime_sources_have_no_finite_default_assignment(self):
        for rel in ('compiler/runtime/reference.py','compiler/runtime/ir_reference.py','compiler/backend/portable.py'):
            s=(C/rel).read_text(encoding='utf8')
            self.assertRegex(s,r'DEFAULT_MAX_ACTIVE_PERFORMANCES\s*=\s*None')
            self.assertNotRegex(s,r'DEFAULT_MAX_ACTIVE_PERFORMANCES\s*=\s*[0-9]')
    def test_finite_depths_cross_old_and_claimed_boundaries(self):
        for n in (4999,5000,10001,20000,25000):
            with self.subTest(n=n):
                c,h,i,b=three(deep(n));self.assertIsInstance(h,NormalOutcome);self.assertIsInstance(i,IRReferenceNormal);self.assertIsInstance(b,VMNormal);self.assertEqual(reference_observable(h),ir_reference_observable(i));self.assertEqual(reference_observable(h),backend_observable(b));self.assertEqual(dict(backend_observable(b)['facts'])['גד'],0)
    def test_sequential_20001_no_cumulative_quota(self):
        c,h,i,b=three(seq(20001));self.assertIsInstance(b,VMNormal);self.assertEqual(dict(backend_observable(b)['facts'])['גד'],0)
    def test_explicit_budget_is_caller_tooling_only(self):
        c=compile_source(deep(300));self.assertTrue(c.valid)
        for fn,arg,rc,norm in ((execute_reference,c.hast,ResourceExhaustionOutcome,NormalOutcome),(execute_reference_ir,c.ir,IRReferenceResourceExhaustion,IRReferenceNormal),(execute_ir,c.ir,VMResourceExhaustion,VMNormal)):
            o=fn(arg,max_active_performances=100);self.assertIsInstance(o,rc);self.assertIn('caller-imposed',o.detail);self.assertIsInstance(fn(arg),norm)
    def test_activation_cleanup_after_deep_runs(self):
        c=compile_source(deep(5000));self.assertTrue(c.valid)
        for Cls,arg in ((ReferenceEvaluator,c.hast),(IRReferenceEvaluator,c.ir),(PortableVM,c.ir)):
            for _ in range(3):
                e=Cls(arg);e.run();self.assertEqual(e.active_performances,0)
    def test_python_recursion_limit_independent(self):
        helper=Path(__file__).with_name('low_limit_probe.py')
        p=subprocess.run([sys.executable,str(helper)],env={**os.environ,'E_V082_C_ROOT':str(C),'E_V082_E08_ROOT':str(E08)},text=True,capture_output=True,timeout=20)
        self.assertEqual(p.returncode,0,(p.stdout,p.stderr));self.assertIn('NormalOutcome IRReferenceNormal VMNormal',p.stdout)
    def test_no_fuel_infinite_survives_external_timeout_all_layers(self):
        fx=json.loads((A/'fixtures/a13_program_conformance.json').read_text(encoding='utf8'));s=next(x['source'] for x in fx['positive'] if x['id']=='P-SELFREC-001')
        fd,path=tempfile.mkstemp();os.close(fd);Path(path).write_text(s,encoding='utf8')
        try:
            for layer in ('hast','ir','backend'):
                pth=Path(__file__).with_name('infinite_probe.py')
                try: subprocess.run([sys.executable,str(pth),layer,path],env={**os.environ,'E_V082_C_ROOT':str(C)},text=True,capture_output=True,timeout=.8)
                except subprocess.TimeoutExpired: continue
                self.fail(layer+' terminated before external timeout')
        finally:Path(path).unlink(missing_ok=True)

class MetadataClosure(unittest.TestCase):
    def test_source_root_clean_and_current(self):
        names={p.name for p in C.iterdir() if p.is_file()};self.assertNotIn('HANDOFF_MANIFEST.json',names);self.assertNotIn('SHA256SUMS.txt',names)
        self.assertEqual(LANGUAGE_NAME,'Marak');self.assertEqual(COMPILER_VERSION,'0.4.2-alpha.1')
        py=(C/'pyproject.toml').read_text();self.assertIn('name = "marak"',py);self.assertIn('marak = "compiler.cli.main:main"',py)
        self.assertTrue((C/'LICENSE').read_text().startswith('MIT License'))
        nonarchive='\n'.join(p.read_text(encoding='utf8',errors='ignore') for p in [C/'README.md',C/'pyproject.toml',C/'compiler/version.py'])
        self.assertNotIn('marak-0.4.1',nonarchive)
    def test_outer_manifest_values(self):
        m=json.loads((H/'HANDOFF_MANIFEST.json').read_text());self.assertEqual(m['project'],'Marak');self.assertEqual(m['distribution'],'marak');self.assertEqual(m['cli'],'marak');self.assertEqual(m['license'],'MIT');self.assertEqual(m['compiler_version'],'0.4.2-alpha.1')
    def test_outer_checksum_ledger_all_entries(self):
        lines=(H/'SHA256SUMS.txt').read_text().splitlines();self.assertEqual(len(lines),257)
        for line in lines:
            sha,rel=line.split(None,1);p=H/rel.strip();self.assertTrue(p.is_file(),rel);self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),sha,rel)

class RMSmoke(unittest.TestCase):
    def test_tiny_rm_three_layers(self):
        s=(C/'examples/m4/tiny_rm.he.txt').read_text(encoding='utf8');c,h,i,b=three(s);self.assertEqual(reference_observable(h),ir_reference_observable(i));self.assertEqual(reference_observable(h),backend_observable(b))

if __name__=='__main__':unittest.main(verbosity=2)
