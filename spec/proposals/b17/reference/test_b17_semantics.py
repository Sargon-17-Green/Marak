#!/usr/bin/env python3
from __future__ import annotations

import unittest

from spec.proposals.b17.reference.b17_reference_model import *


class B17SemanticTests(unittest.TestCase):
    def test_01_simple_name_preserves_one_word_spelling(self):
        self.assertEqual(simple_name("ראובן").spelling, "ראובן")

    def test_02_counted_name_joins_with_single_space(self):
        n = counted_name(3, ("מספר", "טיפה", "גלויה"))
        self.assertEqual(n.spelling, "מספר טיפה גלויה")

    def test_03_count_and_frame_are_not_identity_material(self):
        a = counted_name(3, ("מספר", "טיפה", "גלויה"))
        b = CanonicalSourceName(("מספר", "טיפה", "גלויה"))
        self.assertEqual(a, b)

    def test_04_count_one_is_not_an_alias_for_simple_name(self):
        with self.assertRaisesRegex(ValueError, "COUNTED_SOURCE_NAME_COUNT"):
            counted_name(1, ("ראובן",))

    def test_05_wrong_count_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "COUNTED_SOURCE_NAME_ARITY"):
            counted_name(2, ("א", "ב", "ג"))

    def test_06_welded_and_spaced_are_distinct(self):
        self.assertNotEqual(
            simple_name("מספרטיפהגלויה"),
            counted_name(3, ("מספר", "טיפה", "גלויה")),
        )

    def test_07_prefix_names_are_distinct_without_longest_match(self):
        a = counted_name(2, ("א", "ב"))
        b = counted_name(3, ("א", "ב", "ג"))
        self.assertNotEqual(a, b)

    def test_08_ten_word_name_has_no_special_case(self):
        words = ("שנת", "חמשת", "אלפים", "מיום", "ברוא", "מפלצת", "הספגטי", "המעופפת", "שמים", "וארץ")
        self.assertEqual(counted_name(10, words).words, words)

    def test_09_construction_words_are_ordinary_payload(self):
        words = ("מעשה", "מקום", "אשר", "שמו")
        self.assertEqual(counted_name(4, words).spelling, "מעשה מקום אשר שמו")

    def test_10_cross_kind_same_spelling_is_distinct(self):
        n = counted_name(2, ("שם", "אחד"))
        self.assertNotEqual(
            SourceIdentityKey(NameKind.ACT, None, n),
            SourceIdentityKey(NameKind.PLACE, None, n),
        )

    def test_11_role_owner_is_part_of_scope(self):
        n = counted_name(2, ("מספר", "ראשון"))
        self.assertNotEqual(
            SourceIdentityKey(NameKind.ROLE, "act-1", n),
            SourceIdentityKey(NameKind.ROLE, "act-2", n),
        )

    def test_12_symbol_member_domain_is_part_of_scope(self):
        n = counted_name(2, ("חודש", "ראשון"))
        self.assertNotEqual(
            SourceIdentityKey(NameKind.SYMBOL_MEMBER, "domain-1", n),
            SourceIdentityKey(NameKind.SYMBOL_MEMBER, "domain-2", n),
        )

    def test_13_program_input_owner_is_part_of_scope(self):
        n = counted_name(3, ("היום", "אשר", "נשאל"))
        self.assertNotEqual(
            SourceIdentityKey(NameKind.PROGRAM_INPUT, "program-A", n),
            SourceIdentityKey(NameKind.PROGRAM_INPUT, "program-B", n),
        )

    def test_14_repeated_name_corefers_after_declaration(self):
        env = StaticNameEnvironment()
        key = SourceIdentityKey(NameKind.ACT, None, counted_name(2, ("חשב", "מספר")))
        declared = env.declare(key)
        self.assertIs(env.resolve(key), declared)

    def test_15_reference_before_declaration_remains_illegal(self):
        env = StaticNameEnvironment()
        key = SourceIdentityKey(NameKind.PLACE, None, counted_name(2, ("אות", "החסר")))
        with self.assertRaisesRegex(ValueError, "REFERENCE_BEFORE_DECLARATION"):
            env.resolve(key)

    def test_16_duplicate_act_name_remains_illegal(self):
        env = StaticNameEnvironment()
        key = SourceIdentityKey(NameKind.ACT, None, counted_name(2, ("חשב", "מספר")))
        env.declare(key)
        with self.assertRaisesRegex(ValueError, "DUPLICATE_SOURCE_NAME"):
            env.declare(key)

    def test_17_same_role_name_under_two_owners_is_legal(self):
        env = StaticNameEnvironment()
        n = counted_name(2, ("מספר", "ראשון"))
        a = env.declare(SourceIdentityKey(NameKind.ROLE, "act-1", n))
        b = env.declare(SourceIdentityKey(NameKind.ROLE, "act-2", n))
        self.assertNotEqual(a, b)

    def test_18_program_input_material_uses_canonical_spelling(self):
        n = counted_name(3, ("היום", "אשר", "נשאל"))
        self.assertEqual(
            program_input_semantic_material("contract", n),
            ("ProgramInputId", "contract", "היום אשר נשאל"),
        )

    def test_19_program_input_material_distinguishes_welded(self):
        a = program_input_semantic_material("contract", simple_name("היוםאשרנשאל"))
        b = program_input_semantic_material("contract", counted_name(3, ("היום", "אשר", "נשאל")))
        self.assertNotEqual(a, b)

    def test_20_symbol_source_material_has_no_visible_label(self):
        n = counted_name(2, ("חודש", "ראשון"))
        material = symbol_source_material("months", n)
        self.assertEqual(material, ("SymbolMemberId", "months", "חודש ראשון"))
        self.assertNotIn("visible", repr(material).lower())

    def test_21_owner_is_required_only_for_existing_owner_qualified_families(self):
        n = simple_name("א")
        for kind in (NameKind.ROLE, NameKind.PROGRAM_INPUT, NameKind.SYMBOL_MEMBER):
            with self.assertRaisesRegex(ValueError, "SOURCE_NAME_OWNER_REQUIRED"):
                SourceIdentityKey(kind, None, n)

    def test_22_top_level_identity_does_not_gain_owner_scope(self):
        n = simple_name("א")
        for kind in (NameKind.ACT, NameKind.PLACE, NameKind.SYMBOL_DOMAIN):
            with self.assertRaisesRegex(ValueError, "SOURCE_NAME_UNEXPECTED_OWNER"):
                SourceIdentityKey(kind, "invented", n)

    def test_23_no_resolution_policy_depends_on_prefix_or_type(self):
        self.assertEqual(FORBIDDEN_RESOLUTION_POLICIES, {
            "longest-match", "expected-type-rescue", "declaration-known-tokenization",
            "nearest-declaration", "welded-spaced-alias", "visible-label-alias",
            "runtime-name-lookup",
        })

    def test_24_no_runtime_name_object_is_needed(self):
        key = SourceIdentityKey(NameKind.PLACE, None, counted_name(2, ("ספר", "החלקים")))
        resolved = StaticNameEnvironment().declare(key)
        self.assertEqual(resolved.key.name.spelling, "ספר החלקים")
        self.assertFalse(hasattr(resolved, "runtime_name"))

    def test_25_serial_is_allocation_not_source_boundary(self):
        env = StaticNameEnvironment()
        a = env.declare(SourceIdentityKey(NameKind.ACT, None, simple_name("א")))
        b = env.declare(SourceIdentityKey(NameKind.ACT, None, simple_name("ב")))
        self.assertNotEqual(a.serial, b.serial)
        self.assertEqual(a.key.kind, b.key.kind)


if __name__ == "__main__":
    unittest.main(verbosity=2)
