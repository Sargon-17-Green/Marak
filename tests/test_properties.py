import random
import string
import unittest

from compiler.normalize.code import normalize_code


class PropertyTests(unittest.TestCase):
    def test_punctuation_latin_digit_emoji_injection_is_transparent(self):
        rnd = random.Random(20260919)
        base = "אב גד הו זח"
        junk = list(".,;:!?[]{}#*_-/0123456789ABCxyz😀🚀")
        for _ in range(200):
            chars = []
            for ch in base:
                chars.extend(rnd.choice(junk) for _ in range(rnd.randrange(0, 4)))
                chars.append(ch)
                chars.extend(rnd.choice(junk) for _ in range(rnd.randrange(0, 4)))
            self.assertEqual(normalize_code("".join(chars)).text, base)

    def test_whitespace_variants_are_equivalent(self):
        variants = [" ", "\t", "\n", "\r\n", "\u00a0", "\u2003", "\u3000"]
        expected = normalize_code("אב גד").text
        for ws in variants:
            self.assertEqual(normalize_code(f"אב{ws}גד").text, expected)

    def test_normalization_is_idempotent(self):
        samples = ["אב גד", "#אב😀\tגד", "אָב גד", " אב  גד "]
        for s in samples:
            n = normalize_code(s).text
            self.assertEqual(normalize_code(n).text, n)


if __name__ == "__main__":
    unittest.main()
