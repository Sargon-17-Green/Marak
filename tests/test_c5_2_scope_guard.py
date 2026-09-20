from __future__ import annotations

import ast
import re
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


C52_RESOLUTION_DIAGNOSTICS = {
    "Symbol current-place head names a domain different from the place's static domain.": "REF0203",
    "A current role value is available only in an occurrence of its owning act.": "REF0110",
    "Symbol current-role head names a domain different from the role's static domain.": "REF0204",
    "Immediate result reference has no structurally immediate preceding performance.": "REF0112",
    "Immediate result reference names a different act from the directly preceding performance.": "REF0113",
    "Index current-place reference requires a BidirectionalIndex place.": "REF0210",
    "Index current-role reference requires a BidirectionalIndex role.": "REF0211",
    "Symbol equality operands must independently resolve to the same declared Symbol domain.": "SEM0301",
    "Typed replacement destination and displaced current-value description must name the same place.": "REF0001",
    "Typed replacement value domain does not equal the place's fixed domain.": "SEM0302",
    "Displaced Symbol-place head names the wrong Symbol domain.": "SEM0303",
    "Role association explicitly names a different owning act.": "REF0111",
    "A role is associated more than once in one performance.": "REF0111",
    "Role association value domain does not equal the role's static domain.": "SEM0304",
    "Performance role associations must match the described act's required roles exactly.": "REF0111",
    "Result production is licensed only within the current act performance.": "REF0114",
    "Duplicate Symbol domain name.": "REF0205",
    "Symbol member declaration must explicitly co-refer to one domain/member and one counted label.": "REF0001",
    "Duplicate Symbol member source name within one domain.": "REF0206",
    "Symbol order adjacency operands must belong to the explicitly named domain.": "SEM0305",
    "Initialized typed place introduction must repeat the same place name.": "REF0001",
    "Duplicate place name.": "REF0102",
    "Typed role declaration repeated descriptions must co-refer explicitly.": "REF0001",
    "Role owner act has not been introduced.": "REF0107",
    "Role declaration appears after its owner's body definition.": "REF0108",
    "Duplicate role name within one act.": "REF0104",
    "One act has result-production sites with different semantic domains.": "SEM0306",
}

_MOJIBAKE_MARKERS = ("\\u00c3", "\\u00c2", "\\u00e2\\u20ac", "\\u00ef\\u00bf\\u00bd")


def _replacement_corruption(text: str) -> bool:
    return bool(
        re.search(r"\\?{3,}",text)
        or "\\ufffd" in text
        or any(marker in text for marker in _MOJIBAKE_MARKERS)
        or text.count("\\u00d7")>=2
    )


def _literal_issue_calls() -> list[tuple[str, str, str]]:
    source=(ROOT/"compiler"/"resolve"/"a13_program.py").read_text(encoding="utf-8")
    tree=ast.parse(source)
    found=[]
    for node in ast.walk(tree):
        if not isinstance(node,ast.Call) or not isinstance(node.func,ast.Name) or node.func.id!="_issue":
            continue
        if len(node.args)<3:
            continue
        first=node.args[:3]
        if not all(isinstance(arg,ast.Constant) and isinstance(arg.value,str) for arg in first):
            continue
        found.append((first[0].value,first[1].value,first[2].value))
    return found


def test_c52_compiler_sources_have_no_replacement_text_corruption():
    bad=[]
    for source_path in sorted((ROOT/"compiler").rglob("*.py")):
        text=source_path.read_text(encoding="utf-8")
        for line_no,line in enumerate(text.splitlines(),start=1):
            if _replacement_corruption(line):
                bad.append(f"{source_path.relative_to(ROOT)}:{line_no}: {line}")
    assert bad==[]


def test_c52_resolution_diagnostic_hebrew_literals_are_intact_and_codes_stable():
    relevant={}
    for code,message_en,message_he in _literal_issue_calls():
        if message_en in C52_RESOLUTION_DIAGNOSTICS:
            relevant.setdefault(message_en,[]).append((code,message_he))
    assert set(relevant)==set(C52_RESOLUTION_DIAGNOSTICS)
    for message_en,expected_code in C52_RESOLUTION_DIAGNOSTICS.items():
        instances=relevant[message_en]
        assert instances
        for code,message_he in instances:
            assert code==expected_code
            assert message_he.strip()
            assert re.search(r"[\u0590-\u05ff]",message_he)
            assert not _replacement_corruption(message_he)
