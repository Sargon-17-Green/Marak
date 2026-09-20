from __future__ import annotations

import json
import time
import tracemalloc

from compiler.api import compile_source
from compiler.backend.portable import execute_ir
from compiler.parse.a15_numerals import format_natural
from compiler.runtime.observables import backend_observable


def number(n: int) -> str:
    return f"המספר אשר הוא {format_natural(n)}"


def nat_book(size: int) -> str:
    book="ספר מספרים אשר אין בו מספר"
    for n in range(1,size+1):
        book=f"ספר מספרים אשר בו כל אשר ב {book} כסדרו ואחר כלם {number(n)}"
    return book


def program(size: int) -> str:
    book=nat_book(size)
    return " ".join([
        f"יהי מקום ושמו ספר ובמקום אשר שמו ספר יהי {book} לבדו",
        "יהי מקום ושמו מנה ובמקום אשר שמו מנה יהי המספר אשר הוא אחד לבדו",
        "ועתה שים במקום אשר שמו מנה את "
        "מספר הדברים אשר בתוך הספר אשר במקום אשר שמו ספר "
        "תחת המספר אשר במקום אשר שמו מנה",
    ])


def checked_compile_and_run(source: str, size: int):
    compiled=compile_source(source)
    if not compiled.valid or compiled.ir is None:
        raise RuntimeError([d.to_dict() for d in compiled.diagnostics])
    outcome=execute_ir(compiled.ir)
    observed=backend_observable(outcome)
    if dict(observed["facts"])["מנה"] != size:
        raise RuntimeError(f"count mismatch for {size}")
    return compiled


def timed(size: int) -> dict[str, object]:
    source=program(size)
    t0=time.perf_counter()
    compiled=compile_source(source)
    t1=time.perf_counter()
    if not compiled.valid or compiled.ir is None:
        raise RuntimeError([d.to_dict() for d in compiled.diagnostics])
    outcome=execute_ir(compiled.ir)
    t2=time.perf_counter()
    observed=backend_observable(outcome)
    if dict(observed["facts"])["מנה"] != size:
        raise RuntimeError(f"count mismatch for {size}")
    return {
        "items":size,
        "source_bytes":len(source.encode("utf-8")),
        "compile_ms_untraced":round((t1-t0)*1000,3),
        "backend_ms_untraced":round((t2-t1)*1000,3),
    }


def traced_peak(size: int) -> int:
    source=program(size)
    tracemalloc.start()
    try:
        checked_compile_and_run(source,size)
        _,peak=tracemalloc.get_traced_memory()
        return peak
    finally:
        tracemalloc.stop()


def main() -> int:
    rows=[timed(n) for n in (16,32,64,128)]
    evidence={
        "timings":rows,
        "traced_peak_bytes_at_128":traced_peak(128),
        "timing_note":"wall timings are collected with tracemalloc disabled; peak is a separate traced run",
    }
    print(json.dumps({"c5_3_resource_sanity":evidence},ensure_ascii=False,sort_keys=True))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
