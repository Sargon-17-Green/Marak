from __future__ import annotations

from tests.test_c5_6_general_index_surface import three
from tests.test_d4_t21_luach17 import (
    _call,
    _index,
    _nat,
    _oracle,
    _preparation,
    _probe_gate_decl,
    _probe_query_decl,
)


def _run_full_production_first_gate(side: str):
    assert side in {"after", "before"}

    # No oracle gap or selected value enters the production source. The real
    # T21 builder advances the ordinal query day, executes חשב רווח שער
    # end-to-end (drops/bowls -> T19 -> T20 -> +41), and advances the gate.
    extra = _probe_query_decl() + " " + _probe_gate_decl()
    builder = "בנה שערים אחרי" if side == "after" else "בנה שערים לפני"
    principal = " ואחרי כן ".join([
        _call("חשב המספר הגדול"),
        _call("אתחל שערים"),
        _call(builder, [("מנין", _nat(1))]),
        "עשה את המעשה אשר שמו צלם",
        "עשה את המעשה אשר שמו ראי",
    ])

    # three(...) executes the same compiled source through HAST/reference,
    # IR/reference, and the portable backend and requires exact equality.
    return three(_preparation(extra) + " ועתה " + principal)[1]


def _assert_full_production_side(side: str, expected_gap: int):
    want = _oracle(side, 1)
    assert want["gap"] == expected_gap

    obs = _run_full_production_first_gate(side)
    assert obs["outcome"] == "Normal"

    gaps = [v for act, v in obs["products"] if act == "חשב רווח שער"]
    assert gaps == [expected_gap]

    selections = [v for act, v in obs["products"] if act == "בחירה"]
    assert selections[-1:] == [want["selected"]]
    assert want["selected"] + 41 == expected_gap

    firsts = [v for act, v in obs["products"] if act == "חשב מענה ראשון"]
    assert firsts[-1:] == [want["first"]]
    directions = [v for act, v in obs["products"] if act == "חשב כיוון המענה"]
    assert directions[-1:] == [want["direction"]]

    query_snapshots = [v for act, v in obs["products"] if act == "צלם"]
    assert query_snapshots == [_index(side, 1)]

    gate_snapshots = [v for act, v in obs["products"] if act == "ראי"]
    assert gate_snapshots == [_index(side, expected_gap)]

    gate_act = "השער הבא אחרי" if side == "after" else "השער הבא לפני"
    gate_steps = [v for act, v in obs["products"] if act == gate_act]
    assert gate_steps == [_index(side, expected_gap)]

    facts = dict(obs["facts"])
    assert facts["השער התיכון"] == _index("after", 0)
    assert facts["יום שאלת השער"] == _index(side, 1)
    assert facts["השער הנוכחי"] == _index(side, expected_gap)
    assert facts["מונה השערים"] == 1
    assert facts["מלא הקערות"] == want["fills"]
    assert facts["מערכת הטיפה האחרונה"] == want["last_arr"]


def test_d4_t21_end_to_end_first_gate_after_three_runtimes():
    _assert_full_production_side("after", 377)


def test_d4_t21_end_to_end_first_gate_before_three_runtimes():
    _assert_full_production_side("before", 762)
