from __future__ import annotations

import ast
from pathlib import Path

from compiler.parse.c5_2_registry import C5_2_REGISTRY
from compiler.parse.c5_3_registry import C5_3_REGISTRY

ROOT=Path(__file__).resolve().parents[1]


def _new_productions():
    old={p.production_id for p in C5_2_REGISTRY.productions}
    return [p for p in C5_3_REGISTRY.productions if p.production_id not in old]


def test_c53_only_adds_collection_tranche_productions():
    new=_new_productions()
    assert new
    assert all(p.production_id.startswith("C53.") for p in new)
    allowed_lhs={
        "CollectionKind","CollectionValue","NumberValue","IndexValue","SymbolValue",
        "Proposition","PreparatoryUnit","AtomicAction","AssociationValue","BodyAtomicAction",
    }
    assert {p.lhs for p in new} <= allowed_lhs


def test_c53_does_not_add_counted_recurrence_program_input_or_megillah_surface():
    blob="\n".join(repr(p) for p in _new_productions()).lower()
    forbidden=(
        "repeatexactly","repeatcount","programinput","program input",
        "megillah","pastafari","cutlet","calendar",
        "iterator","cursor","comparator","booleanvalue","generic integer",
    )
    for needle in forbidden:
        assert needle not in blob


def test_c53_append_is_value_construction_not_mutating_action():
    append=[p for p in _new_productions() if ".APPEND." in p.production_id]
    assert len(append)==6
    assert all(p.lhs=="CollectionValue" for p in append)
    assert all(p.semantic_id=="C53.APPEND" for p in append)
    assert all(p.lhs not in {"AtomicAction","BodyAtomicAction"} for p in append)


def test_c53_has_exactly_six_book_kind_productions_and_no_generic_kind():
    kinds=[p for p in _new_productions() if p.lhs=="CollectionKind"]
    assert {p.production_id for p in kinds}=={
        "C53.KIND.NATURAL","C53.KIND.INDEX","C53.KIND.SYMBOL",
        "C53.KIND.NESTED.NATURAL","C53.KIND.NESTED.INDEX","C53.KIND.NESTED.SYMBOL",
    }
    assert all("Generic" not in repr(p) and "<" not in repr(p) for p in kinds)


def test_c53_canonical_layers_add_no_repeat_exactly_iterator_or_mutable_collection_nodes():
    paths=[
        ROOT/"compiler"/"models"/"hast.py",
        ROOT/"compiler"/"models"/"ir.py",
        ROOT/"compiler"/"resolve"/"a13_program.py",
        ROOT/"compiler"/"runtime"/"reference.py",
        ROOT/"compiler"/"runtime"/"ir_reference.py",
        ROOT/"compiler"/"backend"/"portable.py",
    ]
    class_names=set()
    function_names=set()
    for path in paths:
        tree=ast.parse(path.read_text(encoding="utf-8"),filename=str(path))
        class_names.update(n.name for n in ast.walk(tree) if isinstance(n,ast.ClassDef))
        function_names.update(n.name for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)))
    forbidden={"RepeatExactly","Iterator","CollectionIterator","MutableCollection","AppendInPlace","ComparatorAct"}
    assert not (class_names & forbidden)
    assert not (function_names & {"append_in_place","next_item","make_iterator","compare_with_act"})


def test_language_edition_stays_frozen_while_registry_advances():
    assert C5_3_REGISTRY.language_edition=="core-0.1-integration-candidate-a13-b12"
    assert C5_3_REGISTRY.registry_version=="c5.3-a15-a16.1"


def test_c53_append_runtime_avoids_repeated_prefix_tuple_copy():
    runtime_paths=[
        ROOT/"compiler"/"runtime"/"reference.py",
        ROOT/"compiler"/"runtime"/"ir_reference.py",
        ROOT/"compiler"/"backend"/"portable.py",
    ]
    for path in runtime_paths:
        text=path.read_text(encoding="utf-8").replace(" ","")
        assert ".items+(item,)" not in text
        assert "whileisinstance(current," in text
        assert "items=list(collection.items)" in text
