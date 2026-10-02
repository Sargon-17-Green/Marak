#!/usr/bin/env python3
from __future__ import annotations

import dataclasses
import unittest

from compiler.artifact.format import _decode, _encode
from compiler.models.domains import ProgramInputId, SymbolDomainId, SymbolMemberId
from compiler.models.hast import HastActIntroduction, HastSymbolMemberDeclaration
from compiler.models.ir import IRSymbol
from compiler.models.program_contract import ir_program_contract_id, reowner_program_inputs
from compiler.models.symbols import ActId, PlaceId, RoleId
from compiler.models.values import NaturalValue
from compiler.runtime.invocation import InputBinding
from compiler.source.source_map import OriginalPoint, OriginalSpan
from compiler.version import ARTIFACT_FORMAT_VERSION, HAST_VERSION, IR_VERSION


@dataclasses.dataclass(frozen=True)
class DummyContractMaterial:
    input_id: ProgramInputId


def span() -> OriginalSpan:
    p = OriginalPoint("b17", 0, 0, 1, 1)
    return OriginalSpan(p, p)


class B17ProductionCompatibilityTests(unittest.TestCase):
    def test_01_existing_identity_dataclasses_accept_multiword_spelling(self):
        act = ActId(1, "חשב מספר")
        place = PlaceId(2, "מספר טיפה גלויה")
        role = RoleId(3, act, "מספר ראשון")
        self.assertEqual((act.spelling, place.spelling, role.spelling),
                         ("חשב מספר", "מספר טיפה גלויה", "מספר ראשון"))

    def test_02_program_and_symbol_ids_accept_multiword_spelling(self):
        inp = ProgramInputId(1, "היום אשר נשאל", "program")
        dom = SymbolDomainId(2, "חדשי השנה")
        mem = SymbolMemberId(3, "חודש ראשון")
        self.assertEqual((inp.spelling, dom.spelling, mem.spelling),
                         ("היום אשר נשאל", "חדשי השנה", "חודש ראשון"))

    def test_03_spaced_and_welded_metadata_are_not_equal(self):
        self.assertNotEqual(PlaceId(1, "מספר טיפה גלויה"), PlaceId(1, "מספרטיפהגלויה"))

    def test_04_role_owner_contract_is_unchanged(self):
        owner = ActId(1, "חשב מספר")
        a = RoleId(2, owner, "מספר ראשון")
        b = RoleId(3, owner, "מספר ראשון")
        self.assertEqual(a.owner, b.owner)
        self.assertEqual(a.spelling, b.spelling)
        self.assertNotEqual(a.serial, b.serial)

    def test_05_program_contract_fingerprint_includes_canonical_spelling(self):
        a = DummyContractMaterial(ProgramInputId(1, "היום אשר נשאל", "ignored-owner"))
        b = DummyContractMaterial(ProgramInputId(1, "היוםאשרנשאל", "ignored-owner"))
        self.assertNotEqual(ir_program_contract_id(a), ir_program_contract_id(b))

    def test_06_program_contract_fingerprint_excludes_owner_field_and_has_no_count_field(self):
        a = DummyContractMaterial(ProgramInputId(1, "היום אשר נשאל", "owner-a"))
        b = DummyContractMaterial(ProgramInputId(1, "היום אשר נשאל", "owner-b"))
        self.assertEqual(ir_program_contract_id(a), ir_program_contract_id(b))
        material = _encode(a.input_id)
        self.assertNotIn("count", material)
        self.assertNotIn("words", material)

    def test_07_reowner_preserves_multiword_spelling(self):
        x = DummyContractMaterial(ProgramInputId(1, "היום אשר נשאל", "old"))
        y = reowner_program_inputs(x, "new")
        self.assertEqual(y.input_id.spelling, "היום אשר נשאל")
        self.assertEqual(y.input_id.program_contract, "new")

    def test_08_ir_symbol_existing_spelling_field_carries_spaces(self):
        x = IRSymbol(span(), "place", 1, "מספר טיפה גלויה", None)
        self.assertEqual(x.spelling, "מספר טיפה גלויה")
        self.assertNotIn("multiword", {f.name for f in dataclasses.fields(x)})

    def test_09_hast_identity_existing_field_carries_spaces(self):
        x = HastActIntroduction(span(), ActId(1, "חשב מספר"))
        self.assertEqual(x.act.spelling, "חשב מספר")

    def test_10_artifact_tagged_encoding_roundtrips_program_input_with_spaces(self):
        x = ProgramInputId(7, "היום אשר נשאל", "program")
        self.assertEqual(_decode(_encode(x)), x)

    def test_11_artifact_encoding_uses_existing_spelling_string_only(self):
        x = _encode(SymbolMemberId(9, "חודש ראשון"))
        self.assertEqual(x["tag"], "SymbolMemberId")
        self.assertEqual(x["spelling"], "חודש ראשון")
        self.assertEqual(set(x), {"tag", "serial", "spelling"})

    def test_12_symbol_visible_label_remains_separate_field(self):
        names = {f.name for f in dataclasses.fields(HastSymbolMemberDeclaration)}
        self.assertIn("member_id", names)
        self.assertIn("external_label", names)
        self.assertNotIn("external_label", {f.name for f in dataclasses.fields(SymbolMemberId)})

    def test_13_runtime_binding_rejects_raw_source_string_identity(self):
        with self.assertRaisesRegex(TypeError, "resolved ProgramInputId"):
            InputBinding("היום אשר נשאל", NaturalValue(1))

    def test_14_runtime_binding_accepts_resolved_multiword_program_input_id(self):
        x = InputBinding(ProgramInputId(1, "היום אשר נשאל", "program"), NaturalValue(1))
        self.assertEqual(x.input_id.spelling, "היום אשר נשאל")

    def test_15_no_schema_bump_is_needed_to_represent_spaces(self):
        self.assertEqual(HAST_VERSION, "core-hast-0.7-candidate-1")
        self.assertEqual(IR_VERSION, "core-ir-0.7-candidate-1")
        self.assertEqual(ARTIFACT_FORMAT_VERSION, "core-artifact-0.7-candidate-1")


if __name__ == "__main__":
    unittest.main(verbosity=2)
