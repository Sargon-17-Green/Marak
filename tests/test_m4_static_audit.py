from __future__ import annotations
import ast
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CANONICAL=[
    ROOT/'compiler/models/hast.py', ROOT/'compiler/models/ir.py', ROOT/'compiler/ir_lower.py',
    ROOT/'compiler/resolve/a13_program.py', ROOT/'compiler/validate/a13_b12_rules.py',
    ROOT/'compiler/runtime/reference.py', ROOT/'compiler/runtime/ir_reference.py', ROOT/'compiler/backend/portable.py', ROOT/'compiler/artifact/format.py',
]
HISTORICAL=['A0','A3','A8','A9','A10','A11','A12']

class M4StaticAuditTests(unittest.TestCase):
    def test_no_conventional_ontology_class_names_in_canonical_layers(self):
        forbidden={'Function','Parameter','Return','Frame','While','BooleanValue','Statement'}
        for path in CANONICAL:
            tree=ast.parse(path.read_text(encoding='utf-8'),filename=str(path))
            names={n.name for n in ast.walk(tree) if isinstance(n,(ast.ClassDef,ast.FunctionDef))}
            with self.subTest(path=path.name): self.assertFalse(names & forbidden,names & forbidden)

    def test_reference_model_firewall(self):
        for path in CANONICAL:
            text=path.read_text(encoding='utf-8')
            self.assertNotIn('compiler.reference_models',text,path)

    def test_no_megillah_or_calendar_special_case_in_canonical_path(self):
        pattern=re.compile(r'(?i)megillah|pastafari|cutlet|calendar')
        for path in CANONICAL:
            self.assertIsNone(pattern.search(path.read_text(encoding='utf-8')),path)

    def test_normalizer_does_not_use_host_whitespace_classification(self):
        text=(ROOT/'compiler/source/unicode_policy.py').read_text(encoding='utf-8')+(ROOT/'compiler/normalize/code.py').read_text(encoding='utf-8')
        self.assertNotIn('.isspace(',text)
        self.assertNotRegex(text,r're\.compile\([^\n]*\\s')

    def test_no_dynamic_source_loading_pickle_or_eval_in_canonical_compiler(self):
        blob='\n'.join(p.read_text(encoding='utf-8') for p in (ROOT/'compiler').rglob('*.py') if 'reference_models' not in p.parts)
        for needle in ('spec_from_file_location','SourceFileLoader','exec_module','pickle.loads','eval('):
            self.assertNotIn(needle,blob)

    def test_no_absolute_environment_path_in_tests_or_compiler(self):
        bad=re.compile(r'/mnt/data|/home/oai|[A-Za-z]:\\\\')
        for base in (ROOT/'compiler',ROOT/'tests',ROOT/'tools'):
            for p in base.rglob('*.py'):
                if p.resolve() == Path(__file__).resolve():
                    continue  # this audit file names forbidden prefixes; it does not depend on them
                self.assertIsNone(bad.search(p.read_text(encoding='utf-8')),p)

    def test_historical_registry_snapshots_are_distinct_from_new_current_snapshot(self):
        current=(ROOT/'spec/CURRENT_CONSTRUCTION_REGISTRY.json').read_bytes()
        a13=(ROOT/'spec/A13_B12_CONSTRUCTION_REGISTRY.json').read_bytes()
        self.assertEqual(current,a13)
        hashes=[]
        for name in HISTORICAL:
            p=ROOT/f'spec/{name}_CONSTRUCTION_REGISTRY.json'
            self.assertTrue(p.is_file(),p)
            hashes.append(hashlib.sha256(p.read_bytes()).hexdigest())
        self.assertEqual(len(hashes),len(set(hashes)))
        self.assertNotIn(hashlib.sha256(current).hexdigest(),hashes)

if __name__=='__main__': unittest.main()
