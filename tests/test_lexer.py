import unittest

from compiler.lex.words import lex_words
from compiler.normalize.code import normalize_code


class LexerTests(unittest.TestCase):
    def test_words_are_orthographic_not_semantic(self):
        n = normalize_code(" אב גד הו ")
        tokens = lex_words(n)
        self.assertEqual([t.text for t in tokens], ["אב", "גד", "הו"])
        self.assertEqual([(t.normalized_start, t.normalized_end) for t in tokens], [(1,3),(4,6),(7,9)])


if __name__ == "__main__":
    unittest.main()
