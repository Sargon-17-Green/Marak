import unittest

from compiler.semantic_core.recurrence import OccurrenceDue, RecurrenceComplete, begin_after_gated, checkpoint_until
from compiler.semantic_core.state import NUMBER_ASPECT, SemanticSnapshot, StateReferentId
from compiler.semantic_core.truth import CurrentNumber, EqualNumberProposition, IntegerNumber


class RecurrenceSemanticCoreTests(unittest.TestCase):
    def test_initial_occurrence_is_due_even_if_endpoint_already_holds(self):
        r = StateReferentId("r")
        s = SemanticSnapshot().establish(r, NUMBER_ASPECT, 3)
        p = EqualNumberProposition(CurrentNumber(r), IntegerNumber(3))
        start = begin_after_gated(s)
        self.assertIsInstance(start, OccurrenceDue)
        # The gate is intentionally not consulted by begin_after_gated.
        s_after = s.replace(r, NUMBER_ASPECT, 4)
        self.assertIsInstance(checkpoint_until(p, s_after), OccurrenceDue)

    def test_start_zero_increment_until_three_requires_three_external_occurrences(self):
        r = StateReferentId("r")
        s = SemanticSnapshot().establish(r, NUMBER_ASPECT, 0)
        p = EqualNumberProposition(CurrentNumber(r), IntegerNumber(3))
        phase = begin_after_gated(s)
        observed = []
        while isinstance(phase, OccurrenceDue):
            current = phase.snapshot.current_of(r, NUMBER_ASPECT).value
            observed.append(current)
            successor = phase.snapshot.replace(r, NUMBER_ASPECT, current + 1)
            phase = checkpoint_until(p, successor)
        self.assertIsInstance(phase, RecurrenceComplete)
        self.assertEqual(observed, [0, 1, 2])
        self.assertEqual(phase.snapshot.current_of(r, NUMBER_ASPECT).value, 3)

    def test_no_hidden_recurrence_counter_in_semantic_phase(self):
        fields = set(OccurrenceDue.__dataclass_fields__)
        self.assertEqual(fields, {"snapshot"})


if __name__ == "__main__":
    unittest.main()
