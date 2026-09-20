from __future__ import annotations

import ast
from pathlib import Path

from compiler.parse.c5_3_registry import C5_3_REGISTRY
from compiler.parse.c5_4_registry import C5_4_REGISTRY

ROOT=Path(__file__).resolve().parents[1]


def new_productions():
    old={p.production_id for p in C5_3_REGISTRY.productions}
    return [p for p in C5_4_REGISTRY.productions if p.production_id not in old]


def test_c54_surface_is_exact_recurrence_tranche_only():
    new=new_productions()
    recurrence={p.production_id for p in new if p.lhs=="CountedConsequence"}
    assert recurrence=={
        "C54.REPEAT.ONE","C54.REPEAT.TWO","C54.REPEAT.MANY","C54.REPEAT.DYNAMIC",
    }
    assert {p.lhs for p in new}<={"CountedConsequence","CountAsNumber"}
    assert all(p.production_id.startswith("C54.") for p in new)


def test_dynamic_count_is_prefix_form_and_not_a_second_numeric_value_category():
    dynamic=next(p for p in C5_4_REGISTRY.productions if p.production_id=="C54.REPEAT.DYNAMIC")
    assert dynamic.lhs=="CountedConsequence"
    assert "CountAsNumber" in repr(dynamic.rhs)
    assert "NumberValue" not in repr(dynamic.rhs)
    count_as=[p for p in new_productions() if p.lhs=="CountAsNumber"]
    assert count_as
    assert all("כמספר" in repr(p.rhs[0]) for p in count_as)


def test_language_edition_frozen_and_registry_advances_only():
    assert C5_4_REGISTRY.language_edition=="core-0.1-integration-candidate-a13-b12"
    assert C5_4_REGISTRY.registry_version=="c5.4-a15-b13.1"


def test_c54_adds_no_out_of_scope_language_or_transport_surface():
    blob="\n".join(repr(p) for p in new_productions()).lower()
    forbidden=(
        "programinput","program input","megillah","pastafari","calendar",
        "iterator","cursor","loop index","booleanvalue","mutablecollection",
        "while","generic integer","transport",
    )
    for needle in forbidden:
        assert needle not in blob


def test_repeat_exactly_runtime_has_no_semantic_iteration_cap_or_host_recursion():
    paths=[
        ROOT/"compiler"/"runtime"/"reference.py",
        ROOT/"compiler"/"runtime"/"ir_reference.py",
        ROOT/"compiler"/"backend"/"portable.py",
    ]
    blob="\n".join(p.read_text(encoding="utf-8") for p in paths)
    lower=blob.lower()
    for needle in ("max_repeat","max_iterations","repeat_limit","repeat_cap"):
        assert needle not in lower
    for path in paths:
        tree=ast.parse(path.read_text(encoding="utf-8"),filename=str(path))
        recursive_calls=[]
        for fn in (n for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name in {"execute","action"}):
            for call in ast.walk(fn):
                if (
                    isinstance(call,ast.Call) and isinstance(call.func,ast.Attribute)
                    and isinstance(call.func.value,ast.Name) and call.func.value.id=="self"
                    and call.func.attr==fn.name
                ):
                    recursive_calls.append((fn.name,call.lineno))
        # Value-expression recursion is unrelated to the recurrence cardinality.
        # C5.4's finite N must not consume Python stack through execute/action.
        assert not recursive_calls


def test_repeat_exactly_contract_does_not_add_iterator_or_hidden_counter_value_classes():
    names=set()
    for p in [ROOT/"compiler"/"models"/"hast.py",ROOT/"compiler"/"models"/"ir.py"]:
        tree=ast.parse(p.read_text(encoding="utf-8"),filename=str(p))
        names.update(n.name for n in ast.walk(tree) if isinstance(n,ast.ClassDef))
    forbidden={"Iterator","LoopIndex","IRIterator","IRLoopIndex","HastIterator","HastLoopIndex"}
    assert not names & forbidden
