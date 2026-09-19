import unittest

from compiler.semantic_core.state import (
    NUMBER_ASPECT, CurrentObservation, MissingCurrentFact, SemanticSnapshot,
    StateAspect, StateReferentId,
)


class StateSemanticCoreTests(unittest.TestCase):
    def test_equal_contents_do_not_merge_referents(self):
        a, b = StateReferentId("a"), StateReferentId("b")
        s = SemanticSnapshot().establish(a, NUMBER_ASPECT, 7).establish(b, NUMBER_ASPECT, 7)
        s2 = s.replace(a, NUMBER_ASPECT, 8)
        self.assertEqual(s2.current_of(a, NUMBER_ASPECT).value, 8)
        self.assertEqual(s2.current_of(b, NUMBER_ASPECT).value, 7)

    def test_same_resolved_referent_observes_replacement(self):
        r = StateReferentId("same-source-referent")
        s = SemanticSnapshot().establish(r, NUMBER_ASPECT, 1)
        s2 = s.replace(r, NUMBER_ASPECT, 2)
        self.assertEqual(s2.current_of(r, NUMBER_ASPECT).value, 2)
        self.assertEqual(s.current_of(r, NUMBER_ASPECT).value, 1)

    def test_replacement_preserves_unrelated_facts_and_aspects(self):
        a, b = StateReferentId("a"), StateReferentId("b")
        mark = StateAspect("mark")
        s = SemanticSnapshot().establish(a, NUMBER_ASPECT, 3).establish(a, mark, 9).establish(b, NUMBER_ASPECT, 4)
        s2 = s.replace(a, NUMBER_ASPECT, 5)
        self.assertEqual(s2.current_of(a, mark).value, 9)
        self.assertEqual(s2.current_of(b, NUMBER_ASPECT).value, 4)

    def test_query_does_not_implicitly_turn_referent_into_value(self):
        r = StateReferentId("r")
        self.assertNotEqual(r, 5)
        missing = SemanticSnapshot().current_of(r, NUMBER_ASPECT)
        self.assertIsInstance(missing, MissingCurrentFact)
        s = SemanticSnapshot().establish(r, NUMBER_ASPECT, 5)
        self.assertIsInstance(s.current_of(r, NUMBER_ASPECT), CurrentObservation)

    def test_host_bool_is_not_numeric_data(self):
        with self.assertRaises(TypeError):
            SemanticSnapshot().establish(StateReferentId("r"), NUMBER_ASPECT, True)

    def test_physical_order_is_canonical_and_unobservable(self):
        a, b = StateReferentId("a"), StateReferentId("b")
        s1 = SemanticSnapshot().establish(b, NUMBER_ASPECT, 2).establish(a, NUMBER_ASPECT, 1)
        s2 = SemanticSnapshot().establish(a, NUMBER_ASPECT, 1).establish(b, NUMBER_ASPECT, 2)
        self.assertEqual(s1.observable_facts(), s2.observable_facts())


if __name__ == "__main__":
    unittest.main()
