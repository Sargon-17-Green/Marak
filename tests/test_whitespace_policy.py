import unittest

from compiler.api import normalize
from compiler.source.unicode_policy import WhitespacePolicy


class WhitespacePolicyTests(unittest.TestCase):
    def test_policy_is_explicit_and_injectable(self):
        ascii_only = WhitespacePolicy("test-ascii-space-only", frozenset({" "}))
        default_result = normalize("אב\u00a0גד")
        strict_result = normalize("אב\u00a0גד", whitespace_policy=ascii_only)
        self.assertEqual(default_result.text, "אב גד")
        self.assertEqual(strict_result.text, "אבגד")
        self.assertEqual(strict_result.whitespace_policy_id, "test-ascii-space-only")

    def test_policy_does_not_use_host_isspace(self):
        none = WhitespacePolicy("test-no-space", frozenset())
        self.assertEqual(normalize("אב\tגד", whitespace_policy=none).text, "אבגד")


if __name__ == "__main__":
    unittest.main()
