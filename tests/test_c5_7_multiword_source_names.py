from __future__ import annotations

import json

import pytest

from compiler.api import compile_source, parse
from compiler.models.values import NaturalValue
from compiler.parse.a15_numerals import format_natural
from compiler.parse.c5_6_registry import C5_6_REGISTRY
from compiler.parse.current_registry import CURRENT_REGISTRY
from compiler.parse.forest import ParseLeaf
from compiler.parse.grammar import NameTerminal, SourceNameTerminal
from compiler.runtime.invocation import InputBinding
from compiler.version import (
    ARTIFACT_FORMAT_VERSION,
    COMPILER_VERSION,
    HAST_VERSION,
    IR_VERSION,
)
from tests.test_c5_2_surface_pipeline import (
    act, body, member, num, output, perform, perform_one, place_nat, place_typed,
    replace_nat, role_idx, symbol_domain,
)
from tests.test_c5_5_program_inputs import (
    input_id, input_nat, input_nat_ref, place_nat_value, three,
)
from tests.test_c5_6_general_index_surface import (
    general_index, general_recent, general_role, general_role_decl,
    replace_general, three as three_index,
)


def counted(*words: str) -> str:
    assert len(words) >= 2
    return (
        "שם אשר מספר המלים אשר בו הוא "
        f"{format_natural(len(words))} והמלים הן {' '.join(words)}"
    )


def _codes(source: str) -> list[str]:
    compiled = compile_source(source)
    assert not compiled.valid
    return [d.code for d in compiled.diagnostics]


def _role_rows(root):
    rows = []

    def walk(node):
        for child in node.children:
            if isinstance(child, ParseLeaf):
                if child.terminal_role:
                    rows.append((child.terminal_role, node.production_id, child))
            else:
                walk(child)

    walk(root)
    return rows


def _first_role_leaf(source: str, role: str):
    pipeline = parse(source)
    assert len(pipeline.forest.alternatives) == 1
    rows = _role_rows(pipeline.forest.alternatives[0].root)
    return pipeline, next(leaf for found_role, _, leaf in rows if found_role == role)


def _all_roles_fixture() -> str:
    domain = counted("חדשי", "השנה")
    member_name = counted("חודש", "ראשון")
    input_role = counted("היום", "הנשאל")
    place = counted("מקום", "היעד")
    actor = counted("חשב", "מספר")
    role = counted("מספר", "ראשון")
    return " ".join([
        symbol_domain(domain),
        member(domain, member_name, 2, "חודש ראשון"),
        input_nat(input_role),
        place_typed(place, general_index(0)),
        act(actor),
        general_role_decl(actor, role),
        body(actor, output(general_role(actor, role))),
        "ועתה " + perform_one(actor, role, general_index(1)) +
        " ואחרי כן " + replace_general(place, general_recent(actor)),
    ])


def test_current_registry_migrates_all_a18_name_sites_without_rewriting_c56():
    current = [
        s for p in CURRENT_REGISTRY.productions for s in p.rhs
        if isinstance(s, SourceNameTerminal)
    ]
    assert len(current) == 115
    assert sum(
        any(isinstance(s, SourceNameTerminal) for s in p.rhs)
        for p in CURRENT_REGISTRY.productions
    ) == 61
    assert {s.role for s in current} == {
        "ActionName", "PlaceName", "RoleOwnerActionName",
        "AssociatedRoleName", "DeclaredRoleName", "BodyActionName",
        "ResultActionName", "PerformedActionName", "SymbolDomainName",
        "SymbolMemberName", "ProgramInputRoleName",
    }
    assert not any(
        isinstance(s, NameTerminal)
        for p in CURRENT_REGISTRY.productions for s in p.rhs
    )
    assert sum(
        isinstance(s, NameTerminal)
        for p in C5_6_REGISTRY.productions for s in p.rhs
    ) == 115


def test_counted_leaf_text_is_payload_but_provenance_covers_complete_construction():
    name = counted("מספר", "טיפה", "גלויה")
    source = place_nat(name, 1) + " ועתה " + replace_nat(name, num(2))
    pipeline, leaf = _first_role_leaf(source, "PlaceName")

    assert leaf.text == "מספר טיפה גלויה"
    assert source[leaf.original.start.char_offset:leaf.original.end.char_offset] == name
    assert pipeline.normalized.text[leaf.normalized_start:leaf.normalized_end] == name

    start_token = next(token for token in pipeline.tokens if token.index == leaf.token_index)
    assert start_token.text == "שם"
    assert start_token.normalized_start == leaf.normalized_start

    compiled = compile_source(source)
    assert compiled.valid, [d.to_dict() for d in compiled.diagnostics]
    assert compiled.hast.places[0].spelling == "מספר טיפה גלויה"


def test_multiword_place_roundtrips_to_canonical_spelling_and_artifact():
    name = counted("מספר", "טיפה", "גלויה")
    source = place_nat(name, 1) + " ועתה " + replace_nat(name, num(2))
    compiled = compile_source(source)
    assert compiled.valid, [d.to_dict() for d in compiled.diagnostics]
    assert compiled.hast.places[0].spelling == "מספר טיפה גלויה"

    artifact = json.loads(compiled.artifact.decode("utf-8"))
    symbols = artifact["program"]["symbols"]
    place_symbols = [x for x in symbols if x["kind"] == "place"]
    assert any(x["spelling"] == "מספר טיפה גלויה" for x in place_symbols)
    assert all("multiword" not in x and "count" not in x for x in place_symbols)


def test_ten_word_and_construction_word_payloads_are_ordinary_source_names():
    words = (
        "שנת", "חמשת", "אלפים", "מיום", "ברוא",
        "מפלצת", "הספגטי", "המעופפת", "שמים", "וארץ",
    )
    name = counted(*words)
    compiled = compile_source(place_nat(name, 1) + " ועתה " + replace_nat(name, num(2)))
    assert compiled.valid, [d.to_dict() for d in compiled.diagnostics]
    assert compiled.hast.places[0].spelling == " ".join(words)

def test_whitespace_and_maqaf_normalize_identity_without_losing_full_provenance():
    name = (
        "שם\tאשר\nמספר המלים אשר בו הוא שנים "
        "והמלים הן א־ב\tג"
    )
    source = place_nat(name, 1) + " ועתה " + replace_nat(name, num(2))
    pipeline, leaf = _first_role_leaf(source, "PlaceName")

    assert leaf.text == "אב ג"
    assert source[leaf.original.start.char_offset:leaf.original.end.char_offset] == name
    assert pipeline.normalized.text[leaf.normalized_start:leaf.normalized_end] == (
        "שם אשר מספר המלים אשר בו הוא שנים והמלים הן אב ג"
    )
    start_token = next(token for token in pipeline.tokens if token.index == leaf.token_index)
    assert start_token.text == "שם"
    assert start_token.normalized_start == leaf.normalized_start

    compiled = compile_source(source)
    assert compiled.valid, [d.to_dict() for d in compiled.diagnostics]
    assert compiled.hast.places[0].spelling == "אב ג"


def test_prefix_related_names_are_distinct_without_longest_match():
    short = counted("א", "ב")
    long = counted("א", "ב", "ג")
    source = " ".join([
        place_nat(short, 1),
        place_nat(long, 2),
        "ועתה " + replace_nat(short, num(3)) +
        " ואחרי כן " + replace_nat(long, num(4)),
    ])
    compiled = compile_source(source)
    assert compiled.valid, [d.to_dict() for d in compiled.diagnostics]
    assert {p.spelling for p in compiled.hast.places} == {"א ב", "א ב ג"}


@pytest.mark.parametrize("bad_name", [
    "שם אשר מספר המלים אשר בו הוא אחד והמלים הן א",
    "שם אשר מספר המלים אשר בו הוא שלשה והמלים הן א ב",
    "שם אשר מספר המלים אשר בו הוא שנים והמלים הן א ב ג",
])
def test_count_one_short_payload_and_unconsumable_extra_payload_are_rejected(bad_name):
    source = place_nat(bad_name, 1) + " ועתה " + replace_nat("יעד", num(2))
    _codes(source)


def test_declaration_reference_payload_mismatch_is_not_rescued():
    declared = counted("א", "ב")
    other = counted("א", "ג")
    source = place_nat(declared, 1) + " ועתה " + replace_nat(other, num(2))
    codes = _codes(source)
    assert any(code.startswith("REF") for code in codes)


def test_counted_name_diagnostic_span_covers_complete_occurrence():
    name = counted("מקום", "אחד")
    source = " ".join([
        place_nat(name, 1),
        place_nat(name, 2),
        "ועתה " + replace_nat(name, num(3)),
    ])
    compiled = compile_source(source)
    assert not compiled.valid
    diagnostic = next(d for d in compiled.diagnostics if d.code == "REF0102")
    assert diagnostic.source_span is not None
    actual = source[
        diagnostic.source_span.start.char_offset:
        diagnostic.source_span.end.char_offset
    ]
    assert actual == name


def test_all_11_name_roles_have_counted_multiword_positive_production_paths():
    source = _all_roles_fixture()
    compiled = compile_source(source)
    assert compiled.valid, [d.to_dict() for d in compiled.diagnostics]
    assert len(compiled.check_result.forest.alternatives) == 1

    expected = {
        "ActionName": "A10.ACT.IDENTITY",
        "PlaceName": "C52.PREP.PLACE.INDEX",
        "RoleOwnerActionName": "C56.ROLE.DECLARE.INDEX",
        "AssociatedRoleName": "C56.INDEX.GENERAL.CURRENT.ROLE",
        "DeclaredRoleName": "C56.ROLE.DECLARE.INDEX",
        "BodyActionName": "A12.BODY.DEFINITION",
        "ResultActionName": "C56.INDEX.GENERAL.IMMEDIATE",
        "PerformedActionName": "C52.ACT.PERFORM.ROLES",
        "SymbolDomainName": "C52.SYMBOL.DOMAIN",
        "SymbolMemberName": "C52.SYMBOL.MEMBER",
        "ProgramInputRoleName": "C55.INPUT.DECLARE.NATURAL",
    }
    actual = {}
    for role, production_id, leaf in _role_rows(
        compiled.check_result.forest.alternatives[0].root
    ):
        if role not in expected:
            continue
        occurrence = source[
            leaf.original.start.char_offset:leaf.original.end.char_offset
        ]
        assert occurrence.startswith("שם אשר מספר המלים אשר בו הוא ")
        assert " " in leaf.text
        actual.setdefault(role, set()).add(production_id)

    assert set(actual) == set(expected)
    for role, production_id in expected.items():
        assert production_id in actual[role], (role, actual[role])


def test_counted_result_action_name_resolves_and_executes_immediate_result():
    actor = counted("חשב", "תוצאה")
    role = counted("מעלה", "ראשונה")
    place = counted("מקום", "פלט")
    source = " ".join([
        place_typed(place, general_index(0)),
        act(actor),
        general_role_decl(actor, role),
        body(actor, output(general_role(actor, role))),
        "ועתה " + perform_one(actor, role, general_index(4)) +
        " ואחרי כן " + replace_general(place, general_recent(actor)),
    ])
    compiled, observed = three_index(source)
    assert dict(observed["facts"])["מקום פלט"] == {
        "index": "AfterZero",
        "magnitude": 4,
    }
    result_rows = [
        leaf
        for found_role, production_id, leaf in _role_rows(
            compiled.check_result.forest.alternatives[0].root
        )
        if found_role == "ResultActionName"
        and production_id == "C56.INDEX.GENERAL.IMMEDIATE"
    ]
    assert len(result_rows) == 1
    assert result_rows[0].text == "חשב תוצאה"


def test_multiword_program_input_binds_only_by_resolved_program_input_id():
    role = counted("היום", "אשר", "נשאל")
    source = " ".join([
        input_nat(role),
        place_nat_value("יעד", input_nat_ref(role)),
        "ועתה " + replace_nat("יעד", num(9)),
    ])
    compiled = compile_source(source)
    assert compiled.valid, [d.to_dict() for d in compiled.diagnostics]
    pid = input_id(compiled, "היום אשר נשאל")
    observed = three(compiled, (InputBinding(pid, NaturalValue(7)),))
    assert dict(observed["facts"])["יעד"] == 9
    assert pid.spelling == "היום אשר נשאל"

def test_multiword_act_role_symbol_domain_and_member_use_existing_ids():
    actor = counted("חשב", "מספר")
    role = counted("מספר", "ראשון")
    domain = counted("חדשי", "השנה")
    member_name = counted("חודש", "ראשון")
    source = " ".join([
        symbol_domain(domain),
        member(domain, member_name, 2, "חודש ראשון"),
        place_nat("דגל", 1),
        act(actor),
        role_idx(actor, role),
        body(actor, replace_nat("דגל", num(2))),
        "ועתה " + perform_one(actor, role, "שנת אין"),
    ])
    compiled = compile_source(source)
    assert compiled.valid, [d.to_dict() for d in compiled.diagnostics]
    assert {x.spelling for x in compiled.hast.acts} == {"חשב מספר"}
    assert {x.spelling for x in compiled.hast.roles} == {"מספר ראשון"}
    assert compiled.ir.symbol_domains[0].domain_id.spelling == "חדשי השנה"
    assert compiled.ir.symbol_members[0].member_id.spelling == "חודש ראשון"
    assert compiled.ir.symbol_members[0].external_label == "חודש ראשון"


def test_multiword_program_input_reference_before_declaration_remains_illegal():
    role = counted("היום", "אשר", "נשאל")
    source = " ".join([
        place_nat_value("יעד", input_nat_ref(role)),
        input_nat(role),
        "ועתה " + replace_nat("יעד", num(1)),
    ])
    assert "REF0501" in _codes(source)


def test_duplicate_canonical_name_rejected_in_all_existing_duplicate_scopes():
    place = counted("מקום", "אחד")
    actor = counted("מעשה", "אחד")
    role = counted("תפקיד", "אחד")
    inp = counted("קלט", "אחד")
    domain = counted("משפחה", "אחת")
    member_name = counted("שם", "אחד")
    flag = place_nat("דגל", 1)
    principal = "ועתה " + replace_nat("דגל", num(2))

    cases = [
        " ".join([place_nat(place, 1), place_nat(place, 2), principal]),
        " ".join([flag, act(actor), act(actor), principal]),
        " ".join([flag, act(actor), role_idx(actor, role), role_idx(actor, role), principal]),
        " ".join([input_nat(inp), input_nat(inp), flag, principal]),
        " ".join([symbol_domain(domain), symbol_domain(domain), flag, principal]),
        " ".join([
            symbol_domain(domain),
            member(domain, member_name, 1, "א"),
            member(domain, member_name, 1, "ב"),
            flag, principal,
        ]),
    ]
    for source in cases:
        codes = _codes(source)
        assert any(code.startswith("REF") for code in codes), codes

def test_versions_follow_b17_contract():
    assert CURRENT_REGISTRY.registry_version == "c5.7-a18-b17.1"
    assert COMPILER_VERSION == "0.5.7-alpha.1"
    assert HAST_VERSION == "core-hast-0.7-candidate-1"
    assert IR_VERSION == "core-ir-0.7-candidate-1"
    assert ARTIFACT_FORMAT_VERSION == "core-artifact-0.7-candidate-1"
