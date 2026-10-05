from __future__ import annotations

import argparse
import json
from pathlib import Path

from compiler.api import compile_source
from compiler.backend.portable import execute_ir
from compiler.runtime.ir_reference import execute_reference_ir
from compiler.runtime.observables import (
    backend_observable,
    ir_reference_observable,
    reference_observable,
)
from compiler.runtime.reference import execute_reference
from tests.test_d4_t21_luach17 import (
    _call,
    _index,
    _nat,
    _oracle,
    _preparation,
    _probe_gate_decl,
    _probe_query_decl,
)


def _production_source(side: str) -> str:
    assert side in {"after", "before"}
    builder = "בנה שערים אחרי" if side == "after" else "בנה שערים לפני"
    extra = _probe_query_decl() + " " + _probe_gate_decl()
    principal = " ואחרי כן ".join([
        _call("חשב המספר הגדול"),
        _call("אתחל שערים"),
        _call(builder, [("מנין", _nat(1))]),
        "עשה את המעשה אשר שמו צלם",
        "עשה את המעשה אשר שמו ראי",
    ])
    return _preparation(extra) + " ועתה " + principal


def _execute_one(source: str, runtime: str):
    compiled = compile_source(source)
    assert compiled.valid, [d.to_dict() for d in compiled.diagnostics]

    if runtime == "hast":
        return reference_observable(execute_reference(compiled.hast))
    if runtime == "ir":
        return ir_reference_observable(execute_reference_ir(compiled.ir))
    if runtime == "portable":
        return backend_observable(execute_ir(compiled.ir))
    raise AssertionError(runtime)


def _assert_production_observable(obs, side: str) -> None:
    want = _oracle(side, 1)
    expected_gap = 377 if side == "after" else 762

    # Oracle values are comparison targets only.  Neither expected gap nor
    # selected value is supplied to the production source.
    assert want["gap"] == expected_gap
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


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--side", choices=("after", "before"), required=True)
    ap.add_argument("--runtime", choices=("hast", "ir", "portable"), required=True)
    ap.add_argument("--output", type=Path, required=True)
    ns = ap.parse_args()

    source = _production_source(ns.side)
    obs = _execute_one(source, ns.runtime)
    _assert_production_observable(obs, ns.side)

    ns.output.parent.mkdir(parents=True, exist_ok=True)
    ns.output.write_text(
        json.dumps(obs, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    print(f"PASS side={ns.side} runtime={ns.runtime} output={ns.output}")


if __name__ == "__main__":
    main()
