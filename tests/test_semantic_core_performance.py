import unittest

from compiler.semantic_core.performance import (
    CompletedPerformance,
    DescribedActId,
    PerformanceIssue,
    PerformanceOccurrenceId,
    RoleAssociation,
    RoleId,
    begin_performance,
    complete_performance,
    denote_immediate_result,
    produce_number,
    with_successor_snapshot,
)
from compiler.semantic_core.state import NUMBER_ASPECT, SemanticSnapshot, StateReferentId


class SemanticCorePerformanceTests(unittest.TestCase):
    def setUp(self):
        self.act = DescribedActId("ראובן")
        self.x = RoleId(self.act, "שמעון")
        self.y = RoleId(self.act, "לוי")
        self.s0 = SemanticSnapshot().establish(StateReferentId("גד"), NUMBER_ASPECT, 3)

    def start(self, associations=None, occurrence="o1"):
        if associations is None:
            associations = (RoleAssociation(self.x, 7), RoleAssociation(self.y, 9))
        return begin_performance(
            PerformanceOccurrenceId(occurrence), self.act,
            required_roles=(self.x, self.y), associations=associations,
            incoming_snapshot=self.s0,
        )

    def test_role_matching_is_identity_based_and_permutation_invariant(self):
        a = self.start((RoleAssociation(self.x, 7), RoleAssociation(self.y, 9)))
        b = self.start((RoleAssociation(self.y, 9), RoleAssociation(self.x, 7)))
        self.assertEqual(a, b)
        self.assertEqual(a.value_for_role(self.x), 7)
        self.assertEqual(a.value_for_role(self.y), 9)

    def test_missing_duplicate_and_undeclared_associations_are_not_positional_fallbacks(self):
        missing = self.start((RoleAssociation(self.x, 7),))
        duplicate = self.start((RoleAssociation(self.x, 7), RoleAssociation(self.x, 8)))
        other_act = DescribedActId("יהודה")
        undeclared = self.start((RoleAssociation(self.x, 7), RoleAssociation(RoleId(other_act, "לוי"), 9)))
        self.assertEqual(missing.code, "MISSING_ROLE_ASSOCIATION")
        self.assertEqual(duplicate.code, "DUPLICATE_ROLE_ASSOCIATION")
        self.assertEqual(undeclared.code, "UNDECLARED_ROLE_ASSOCIATION")

    def test_output_does_not_complete_performance(self):
        occurrence = self.start()
        produced = produce_number(occurrence, 42)
        self.assertNotIsInstance(produced, CompletedPerformance)
        self.assertEqual(produced.produced_number, 42)
        # A later committed state transition remains possible after output.
        s1 = self.s0.replace(StateReferentId("גד"), NUMBER_ASPECT, 4)
        later = with_successor_snapshot(produced, s1)
        self.assertEqual(later.produced_number, 42)
        self.assertEqual(later.current_snapshot.current_of(StateReferentId("גד"), NUMBER_ASPECT).value, 4)

    def test_second_output_is_outside_a12_core(self):
        occurrence = produce_number(self.start(), 1)
        second = produce_number(occurrence, 2)
        self.assertIsInstance(second, PerformanceIssue)
        self.assertEqual(second.code, "SECOND_OUTPUT_OUTSIDE_A12_CORE")

    def test_completion_carries_optional_output_without_unit_or_return_value(self):
        without = complete_performance(self.start())
        with_one = complete_performance(produce_number(self.start(occurrence="o2"), -3))
        self.assertIsNone(without.produced_number)
        self.assertEqual(with_one.produced_number, -3)
        self.assertEqual(with_one.snapshot, self.s0)

    def test_immediate_result_requires_explicit_completed_performance_object(self):
        no_output = denote_immediate_result(complete_performance(self.start()))
        with_output = denote_immediate_result(complete_performance(produce_number(self.start(occurrence="o2"), 12)))
        self.assertIsInstance(no_output, PerformanceIssue)
        self.assertEqual(no_output.code, "NO_NUMERIC_OUTPUT")
        self.assertEqual(with_output, 12)

    def test_recursive_reentrant_occurrences_have_distinct_semantic_identity(self):
        outer = self.start(occurrence="outer")
        inner = self.start(occurrence="inner")
        self.assertNotEqual(outer.identity, inner.identity)
        self.assertEqual(outer.act, inner.act)
        self.assertEqual(outer.associations, inner.associations)

    def test_host_bool_is_not_numeric_role_or_output_value(self):
        with self.assertRaises(TypeError):
            RoleAssociation(self.x, True)
        with self.assertRaises(TypeError):
            produce_number(self.start(), False)


if __name__ == "__main__":
    unittest.main()
