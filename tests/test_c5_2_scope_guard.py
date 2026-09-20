from __future__ import annotations

from pathlib import Path

from compiler.parse.c5_2_registry import C5_2_REGISTRY

ROOT=Path(__file__).resolve().parents[1]


def test_c52_new_productions_do_not_implement_deferred_surface_families():
    new=[p for p in C5_2_REGISTRY.productions if p.production_id.startswith("C52.")]
    assert new
    blob="\n".join(repr(p) for p in new)
    assert "Collection" not in blob
    assert "ProgramInput" not in blob
    assert "פעמים" not in blob
    assert "RepeatCount" not in blob


def test_c52_registry_has_no_megillah_special_case():
    text=(ROOT/"compiler"/"parse"/"c5_2_registry.py").read_text(encoding="utf-8")
    lowered=text.lower()
    assert "megillah" not in lowered
    assert "pastafari" not in lowered
    assert "cutlet" not in lowered


def test_language_edition_stays_frozen_while_registry_advances():
    assert C5_2_REGISTRY.language_edition=="core-0.1-integration-candidate-a13-b12"
    assert C5_2_REGISTRY.registry_version=="c5.2-a15-a16.1"
