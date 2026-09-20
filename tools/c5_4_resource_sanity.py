from __future__ import annotations

import json
import time
import tracemalloc

from compiler.api import compile_source
from compiler.backend.portable import execute_ir
from compiler.parse.a15_numerals import format_feminine_count, format_natural
from compiler.runtime.observables import backend_observable


def num(n: int) -> str:
    return f"המספר אשר הוא {format_natural(n)}"


def current(place: str) -> str:
    return f"המספר אשר במקום אשר שמו {place}"


def place_nat(place: str, n: int) -> str:
    return f"יהי מקום ושמו {place} ובמקום אשר שמו {place} יהי {num(n)} לבדו"


def replace_nat(place: str, value: str) -> str:
    return f"שים במקום אשר שמו {place} את {value} תחת {current(place)}"


def source(n: int) -> str:
    increment=replace_nat("מונה",f"המספר הנחשב בהוסיף את {num(1)} על {current('מונה')}")
    return " ".join([place_nat("מונה",1),f"ועתה {format_feminine_count(n)} פעמים {increment}"])


def run(n: int, *, traced: bool=False) -> dict[str, object]:
    s=source(n)
    t0=time.perf_counter()
    c=compile_source(s)
    t1=time.perf_counter()
    if not c.valid or c.ir is None:
        raise RuntimeError([d.to_dict() for d in c.diagnostics])
    out=execute_ir(c.ir)
    t2=time.perf_counter()
    obs=backend_observable(out)
    if dict(obs["facts"])["מונה"] != n+1:
        raise RuntimeError(f"RepeatExactly mismatch at {n}")
    return {
        "iterations":n,
        "source_bytes":len(s.encode("utf-8")),
        "compile_ms":round((t1-t0)*1000,3),
        "execute_ms":round((t2-t1)*1000,3),
    }


def traced_peak(n: int) -> int:
    tracemalloc.start()
    try:
        run(n,traced=True)
        return tracemalloc.get_traced_memory()[1]
    finally:
        tracemalloc.stop()


def main() -> int:
    rows=[run(n) for n in (64,256,1024,4096)]
    report={
        "c5_4_resource_sanity":{
            "timings":rows,
            "traced_peak_bytes_at_4096":traced_peak(4096),
            "semantic_threshold":None,
            "note":"observational only; RepeatExactly has no semantic finite-count ceiling",
        }
    }
    print(json.dumps(report,ensure_ascii=False,sort_keys=True))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
