from __future__ import annotations
import unittest
from compiler.api import check, normalize, parse
from compiler.source.unicode_policy import A13_NORMATIVE_WHITESPACE_CODEPOINTS
from tests.m4_support import a13_json, tiny_source

EXPECTED_WS = set(range(0x0009,0x000E)) | {0x0020,0x0085,0x00A0,0x1680,0x2028,0x2029,0x202F,0x205F,0x3000} | set(range(0x2000,0x200B))

class M4WhitespaceTests(unittest.TestCase):
    def test_exact_normative_whitespace_table(self):
        self.assertEqual(set(A13_NORMATIVE_WHITESPACE_CODEPOINTS), EXPECTED_WS)

    def test_every_normative_whitespace_is_one_canonical_space(self):
        for cp in sorted(EXPECTED_WS):
            with self.subTest(cp=f"U+{cp:04X}"):
                self.assertEqual(normalize("א"+chr(cp)+"ב").text, "א ב")
                self.assertEqual(normalize("א"+chr(cp)*3+"ב").text, "א ב")

    def test_u200b_is_transparent_not_separator(self):
        self.assertEqual(normalize("א\u200bב").text, "אב")
        self.assertEqual(normalize("אב").text, normalize("א\u200bב").text)

    def test_non_normative_host_whitespace_does_not_become_separator(self):
        # MONGOLIAN VOWEL SEPARATOR historically had whitespace-like treatment in some hosts.
        self.assertEqual(normalize("א\u180eב").text, "אב")

    def test_whitespace_substitution_preserves_full_program_semantics(self):
        src=tiny_source().strip()
        canonical=normalize(src).text
        for cp in sorted(EXPECTED_WS):
            mutated=src.replace(" ",chr(cp))
            with self.subTest(cp=f"U+{cp:04X}"):
                self.assertEqual(normalize(mutated).text,canonical)
                self.assertTrue(check(mutated).valid)

class M4WholeProgramTests(unittest.TestCase):
    def test_all_a13_positive_program_fixtures_check(self):
        data=a13_json("a13_program_conformance.json")
        for x in data["positive"]:
            with self.subTest(x=x["id"]):
                r=check(x["source"],file=x["id"])
                self.assertTrue(r.valid,[d.code for d in r.diagnostics])

    def test_all_a13_negative_program_fixtures_reject(self):
        data=a13_json("a13_program_conformance.json")
        for x in data["negative"]:
            with self.subTest(x=x["id"]):
                self.assertFalse(check(x["source"],file=x["id"]).valid)

    def test_tiny_rm_has_one_whole_program_parse(self):
        r=parse(tiny_source())
        self.assertEqual(len(r.forest.alternatives),1)
        self.assertEqual(r.forest.ambiguity_status.value,"unique")
        self.assertEqual(r.parse_result.metrics.token_count,238)
        self.assertLess(r.parse_result.metrics.state_keys,2000)

    def test_source_order_trap_adjacent_actions_do_not_sequence(self):
        src=("יהי מקום ושמו גד ובמקום אשר שמו גד יהי המספר אשר הוא שנים לבדו "
             "ועתה שים במקום אשר שמו גד את המספר אשר הוא שלשה תחת המספר אשר במקום אשר שמו גד "
             "שים במקום אשר שמו גד את המספר אשר הוא ארבע תחת המספר אשר במקום אשר שמו גד")
        r=check(src)
        self.assertFalse(r.valid)
        self.assertIn("PROG0004",[d.code for d in r.diagnostics])

    def test_preparation_and_principal_are_distinct_in_hast(self):
        r=check(a13_json("a13_program_conformance.json")["positive"][0]["source"])
        self.assertTrue(r.valid)
        self.assertTrue(r.hast.preparation)
        self.assertIsNotNone(r.hast.principal)
        self.assertNotEqual(type(r.hast.preparation[0]).__name__, type(r.hast.principal).__name__)

if __name__ == '__main__': unittest.main()
