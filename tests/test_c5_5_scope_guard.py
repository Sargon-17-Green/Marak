from __future__ import annotations

from compiler.parse.c5_4_registry import C5_4_REGISTRY
from compiler.parse.c5_5_registry import C5_5_REGISTRY
from compiler.version import LANGUAGE_EDITION


def test_c55_adds_only_program_input_declaration_and_reference_productions():
    old={p.production_id for p in C5_4_REGISTRY.productions}
    new=[p for p in C5_5_REGISTRY.productions if p.production_id not in old]
    assert new
    assert all(p.production_id.startswith("C55.INPUT.") for p in new)
    assert {p.lhs for p in new} <= {"PreparatoryUnit","NumberValue","SymbolValue","IndexValue","CollectionValue","CountAsNumber"}
    assert not any(p.lhs in {"AtomicAction","BodyAtomicAction","ExecutableUnit","PrincipalExecution"} for p in new)


def test_c55_surface_contains_no_transport_positional_optional_main_or_replacement_construction():
    old={p.production_id for p in C5_4_REGISTRY.productions}
    new=[p for p in C5_5_REGISTRY.productions if p.production_id not in old]
    terminals={
        getattr(symbol,"text",None)
        for production in new
        for symbol in production.rhs
        if getattr(symbol,"text",None) is not None
    }
    forbidden={"stdin","argv","HTTP","JSON","environment","optional","default","main","הארגומנט","הקלט"}
    assert terminals.isdisjoint(forbidden)
    assert LANGUAGE_EDITION=="core-0.1-integration-candidate-a13-b12"
    assert C5_5_REGISTRY.language_edition==C5_4_REGISTRY.language_edition
