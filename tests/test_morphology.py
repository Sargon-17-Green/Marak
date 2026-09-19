import unittest

from compiler.lex.words import lex_words
from compiler.morphology.api import MorphAnalysis, MorphologyEngine
from compiler.normalize.code import normalize_code


class ExactRule:
    rule_id = "A-TEST-EXACT"
    def analyze(self, token):
        if token.text == "עשה":
            yield MorphAnalysis(self.rule_id, "עשה", (("form", "imperative"),))


class MorphologyTests(unittest.TestCase):
    def test_no_dictionary_means_no_guesses(self):
        tokens = lex_words(normalize_code("עשה רבוע"))
        result = MorphologyEngine().analyze(tokens)
        self.assertEqual(result[0], ())
        self.assertEqual(result[1], ())

    def test_candidates_not_winner(self):
        tokens = lex_words(normalize_code("עשה"))
        result = MorphologyEngine((ExactRule(),)).analyze(tokens)
        self.assertEqual(len(result[0]), 1)
        self.assertEqual(result[0][0].rule_id, "A-TEST-EXACT")


if __name__ == "__main__":
    unittest.main()
