from __future__ import annotations
import ast
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def _method_self_calls(path:str, cls_name:str, method_name:str)->int:
    tree=ast.parse((ROOT/path).read_text(encoding='utf-8'))
    for node in tree.body:
        if isinstance(node,ast.ClassDef) and node.name==cls_name:
            for fn in node.body:
                if isinstance(fn,(ast.FunctionDef,ast.AsyncFunctionDef)) and fn.name==method_name:
                    return sum(1 for x in ast.walk(fn) if isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute) and isinstance(x.func.value,ast.Name) and x.func.value.id=='self' and x.func.attr==method_name)
    raise AssertionError((path,cls_name,method_name))

def test_language_recursion_is_not_host_method_recursion():
    assert _method_self_calls('compiler/runtime/reference.py','ReferenceEvaluator','execute')==0
    assert _method_self_calls('compiler/runtime/ir_reference.py','IRReferenceEvaluator','action')==0
    assert _method_self_calls('compiler/backend/portable.py','PortableVM','action')==0

def test_artifact_verifier_invokes_shared_canonical_ir_validator():
    text=(ROOT/'compiler/artifact/format.py').read_text(encoding='utf-8')
    assert 'validate_canonical_ir(program)' in text

def test_backend_does_not_encode_role_correspondence_by_zip_position():
    text=(ROOT/'compiler/backend/portable.py').read_text(encoding='utf-8')
    assert 'zip(self.acts' not in text
    assert 'z.role: self.value(z.value' in text

def test_public_observable_module_has_explicit_debug_serial_api():
    text=(ROOT/'compiler/runtime/observables.py').read_text(encoding='utf-8')
    assert 'backend_debug_internal_state' in text
    assert 'Source-semantic identity' in text or 'source-semantic identity' in text
