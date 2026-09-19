import json
import unittest

from compiler.normalize.code import normalize_code
from compiler.source.text import SourceText
from compiler.source.unicode_policy import HEBREW_LETTER_SET


class NormalizationTests(unittest.TestCase):
    def test_exact_27_letters(self):
        self.assertEqual(len(HEBREW_LETTER_SET), 27)
        s = "אבגדהוזחטיכךלמםנןסעפףצץקרשת"
        self.assertEqual(normalize_code(s).text, s)

    def test_transparent_characters_delete_without_creating_space(self):
        self.assertEqual(normalize_code("אב,./😀ABC123גד").text, "אבגד")

    def test_niqqud_and_cantillation_are_transparent_not_normalized(self):
        self.assertEqual(normalize_code("אָֽב").text, "אב")

    def test_presentation_form_does_not_become_letter_via_nfkc(self):
        # U+FB2A HEBREW LETTER SHIN WITH SHIN DOT is not one of the 27 code points.
        self.assertEqual(normalize_code("אשׁב").text, "אב")

    def test_whitespace_collapses_across_transparent_gap(self):
        self.assertEqual(normalize_code("אב \t,😀 \n גד").text, "אב גד")

    def test_leading_and_trailing_whitespace_runs_are_preserved_as_one_space(self):
        self.assertEqual(normalize_code("\t אב  גד\n").text, " אב גד ")

    def test_arabic_digits_and_latin_are_transparent(self):
        self.assertEqual(normalize_code("אב 123 XYZ גד").text, "אב גד")
        # Whitespace separated only by transparent text is one semantic run after
        # the transparent characters are removed.

    def test_equivalent_decoration_normalizes_identically(self):
        base = normalize_code("אב גד").text
        decorated = normalize_code("#**אב**😀 גד!!!").text
        self.assertEqual(base, decorated)


if __name__ == "__main__":
    unittest.main()
