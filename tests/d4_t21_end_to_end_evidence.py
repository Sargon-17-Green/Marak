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


def _run_full_production_first_gate_each_side():
    # This intentionally uses the real T21 gate builders.  No oracle gap is
    # injected into the production computation.  three(...) compiles once and
    # executes the identical source through HAST/reference, IR/reference, and
    # the portable backend, asserting exact observable agreement.
    extra = _probe_query_decl() + " " + _probe_gate_decl()
    principal = " ואחרי כן ".join([
        _call("חשב המספר הגדול"),
        _call("אתחל שערים"),
        _call("בנה שערים אחרי", [("מנין", _nat(1))]),
        "עשה את המעשה אשר שמו צלם",
        "עשה את המעשה אשר שמו ראי",
        _call("בנה שערים לפני", [("מנין", _nat(1))]),
        "עשה את המעשה אשר שמו צלם",
        "עשה את המעשה אשר שמו ראי",
    ])
    return three(_preparation(extra) + " ועתה " + principal)[1]


def test_d4_t21_end_to_end_first_gate_after_and_before_three_runtimes():
    after = _oracle("after", 1)
    before = _oracle("before", 1)

    # Oracle values are comparison targets only.  The production source below
    # receives neither 377 nor 762 (nor either selected 1..922 value).
    assert after["gap"] == 377
    assert before["gap"] == 762

    obs = _run_full_production_first_gate_each_side()
    assert obs["outcome"] == "Normal"

    # Actual T21 production gap: query-day setup -> drops/bowls -> T19 -> T20
    # -> +41.  Both representative sides must match the independent oracle.
    gaps = [v for act, v in obs["products"] if act == "חשב רווח שער"]
    assert gaps == [377, 762]

    # Prove that the actual T20 selector, fed by the actual T19 computation,
    # is what produced the gap inputs (gap = selected + 41).
    selections = [v for act, v in obs["products"] if act == "בחירה"]
    assert selections[-2:] == [after["selected"], before["selected"]]
    assert selections[-2:] == [336, 721]

    firsts = [v for act, v in obs["products"] if act == "חשב מענה ראשון"]
    assert firsts[-2:] == [after["first"], before["first"]]
    directions = [v for act, v in obs["products"] if act == "חשב כיוון המענה"]
    assert directions[-2:] == [after["direction"], before["direction"]]

    # Query day is the ordinal +/-1 day; resulting gate is independently
    # accumulated by the real T21 gate recurrence.
    query_snapshots = [v for act, v in obs["products"] if act == "צלם"]
    assert query_snapshots == [_index("after", 1), _index("before", 1)]

    gate_snapshots = [v for act, v in obs["products"] if act == "ראי"]
    assert gate_snapshots == [_index("after", 377), _index("before", 762)]

    after_steps = [v for act, v in obs["products"] if act == "השער הבא אחרי"]
    before_steps = [v for act, v in obs["products"] if act == "השער הבא לפני"]
    assert after_steps == [_index("after", 377)]
    assert before_steps == [_index("before", 762)]

    # Final state belongs to the negative representative query and proves that
    # the full bowl pipeline actually ran, not merely the lightweight gate
    # stepping fixture retained in test_d4_t21_luach17.py.
    facts = dict(obs["facts"])
    assert facts["השער התיכון"] == _index("after", 0)
    assert facts["יום שאלת השער"] == _index("before", 1)
    assert facts["השער הנוכחי"] == _index("before", 762)
    assert facts["מספר המעשה"] == 1
    assert facts["מספר השאלה"] == 2
    assert facts["מספר המרחק"] == 2
    assert facts["מספר החיבור"] == 3
    assert facts["מספר הדרך"] == 1
    assert facts["מלא הקערות"] == before["fills"]
    assert facts["מערכת הטיפה האחרונה"] == before["last_arr"]
