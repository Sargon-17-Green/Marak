"""D4 T22 independent finite gate/year oracle; NOT runtime production evidence."""
from __future__ import annotations

from bisect import bisect_left
from dataclasses import dataclass
from random import Random

MIN_GAP, MAX_GAP = 42, 963
MIN_DURATION, MAX_DURATION = 252, 5781
MIN_STEPS = 6


@dataclass(frozen=True)
class YearPair:
    opening: int
    closing: int
    gate_steps: int

    @property
    def duration(self) -> int:
        return self.closing - self.opening


def _ordered_gates(gates: tuple[int, ...]) -> None:
    assert len(gates) >= 2
    assert all(MIN_GAP <= b - a <= MAX_GAP for a, b in zip(gates, gates[1:]))


def all_pairs_oracle(gates: tuple[int, ...], c: int) -> tuple[YearPair, ...]:
    """Exhaustive independent finite reference, without horizon pruning."""
    _ordered_gates(gates)
    pairs = []
    for i, start in enumerate(gates):
        for j in range(i + 1, len(gates)):
            end = gates[j]
            if start < c <= end and j - i >= MIN_STEPS and MIN_DURATION <= end - start <= MAX_DURATION:
                pairs.append(YearPair(start, end, j - i))
    return tuple(sorted(pairs, key=lambda p: (p.duration, p.opening)))


def finite_relevant_pairs(gates: tuple[int, ...], c: int) -> tuple[YearPair, ...]:
    """Logical corridor: c-5781 <= S < c <= E <= c+5780."""
    _ordered_gates(gates)
    starts = [(i, s) for i, s in enumerate(gates) if c - MAX_DURATION <= s < c]
    ends = [(j, e) for j, e in enumerate(gates) if c <= e <= c + MAX_DURATION - 1]
    pairs = [
        YearPair(s, e, j - i)
        for i, s in starts for j, e in ends
        if j - i >= MIN_STEPS and MIN_DURATION <= e - s <= MAX_DURATION
    ]
    return tuple(sorted(pairs, key=lambda p: (p.duration, p.opening)))


def six_step_existence_witness(gates: tuple[int, ...], c: int) -> YearPair:
    """Source 1289–1297, tested only with sufficient finite model neighbors."""
    _ordered_gates(gates)
    at = bisect_left(gates, c)
    if at < len(gates) and gates[at] == c:
        i, j = at - 6, at
    else:
        i, j = at - 1, at + 5
    assert i >= 0 and j < len(gates), "finite model must contain six neighboring steps"
    out = YearPair(gates[i], gates[j], j - i)
    assert out.opening < c <= out.closing and out.gate_steps == 6
    assert 252 <= out.duration <= 5778 <= MAX_DURATION
    return out


def _axis(gaps: tuple[int, ...], start: int = -13000) -> tuple[int, ...]:
    days = [start]
    for gap in gaps:
        days.append(days[-1] + gap)
    return tuple(days)


def test_gate_day_is_closing_endpoint_not_opening():
    gates = tuple(range(-1200, 1300, 100))
    pairs = finite_relevant_pairs(gates, 0)
    assert pairs and any(p.closing == 0 for p in pairs)
    assert all(p.opening < 0 <= p.closing for p in pairs)
    assert pairs == all_pairs_oracle(gates, 0)


def test_non_gate_day_immediate_predecessor():
    gates = tuple(range(-1200, 1300, 100))
    for c in (1, 37, 99):
        p = six_step_existence_witness(gates, c)
        assert (p.opening, p.closing) == (0, 600)
        assert p in finite_relevant_pairs(gates, c)
        assert finite_relevant_pairs(gates, c) == all_pairs_oracle(gates, c)


def test_six_or_more_gate_steps_not_exactly_six():
    pairs = finite_relevant_pairs(tuple(range(-1200, 1300, 100)), 0)
    assert any(p.gate_steps == 6 for p in pairs)
    assert any(p.gate_steps > 6 for p in pairs)
    assert all(p.gate_steps >= 6 and p.duration == p.closing - p.opening for p in pairs)


def test_five_steps_rejected_even_if_length_is_eligible():
    p = finite_relevant_pairs(tuple(range(-1100, 1200, 100)), 0)
    assert YearPair(-500, 0, 5) not in p
    assert YearPair(-600, 0, 6) in p


def test_duration_252_and_5781_inclusive_but_5782_rejected():
    low = _axis((42,) * 25, -420)
    assert YearPair(-252, 0, 6) in finite_relevant_pairs(low, 0)
    high = _axis((825,) * 6 + (831,) + (825,) * 10, -4950)
    assert YearPair(-4950, 831, 7) in finite_relevant_pairs(high, 1)
    above = _axis((826,) * 16, -4956)
    assert YearPair(-4956, 826, 7) not in finite_relevant_pairs(above, 1)


def test_sort_duration_then_earlier_opening_not_discovery_order():
    pairs = finite_relevant_pairs(tuple(range(-1400, 1500, 100)), 0)
    ties = [p for p in pairs if p.duration == 600]
    assert len(ties) >= 2
    assert [p.opening for p in ties] == sorted(p.opening for p in ties)
    assert pairs == tuple(sorted(pairs, key=lambda p: (p.duration, p.opening)))


def test_existence_witness_at_minimum_and_maximum_gap():
    for gap in (42, 963):
        gates = tuple(range(-12 * gap, 13 * gap, gap))
        for c in (0, 1, gap - 1):
            witness = six_step_existence_witness(gates, c)
            assert witness.duration == 6 * gap
            assert witness in finite_relevant_pairs(gates, c)


def test_finite_corridor_matches_complete_pair_oracle():
    rng = Random(20261021)
    cases = [
        (42,) * 36,
        (963,) * 36,
        (42, 963, 83, 407, 61, 788) * 7,
        tuple(rng.randint(42, 963) for _ in range(48)),
    ]
    for gaps in cases:
        gates = _axis(tuple(gaps))
        for i in (8, 15, 25, min(33, len(gates) - 8)):
            for c in (gates[i], gates[i] + 1):
                assert finite_relevant_pairs(gates, c) == all_pairs_oracle(gates, c)
                assert six_step_existence_witness(gates, c) in finite_relevant_pairs(gates, c)


def test_all_distinct_years_not_merely_six_step_witness():
    candidates = finite_relevant_pairs(tuple(range(-1200, 1300, 100)), 0)
    assert len(candidates) > 6
    assert len({(p.opening, p.closing) for p in candidates}) == len(candidates)
    assert candidates == all_pairs_oracle(tuple(range(-1200, 1300, 100)), 0)


def test_proved_corridor_contains_every_eligible_pair():
    gates = tuple(range(-10000, 10001, 100))
    for c in (-1, 0, 1, 50, 100):
        for p in all_pairs_oracle(gates, c):
            assert c - MAX_DURATION <= p.opening < c <= p.closing <= c + MAX_DURATION - 1
