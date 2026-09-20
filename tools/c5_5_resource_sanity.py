from __future__ import annotations

import json
import time
import tracemalloc

from compiler.api import compile_source
from compiler.backend.portable import execute_ir
from compiler.models.values import NaturalValue
from compiler.runtime.invocation import InputBinding
from compiler.runtime.observables import backend_observable


def source() -> str:
    inp="מנין"; target="מונה"
    input_decl=(
        f"יהי למלאכה הזאת דבר ושמו {inp} "
        f"ובטרם תחל המלאכה הזאת יעמד מספר "
        f"תחת הדבר אשר למלאכה הזאת שמו {inp}"
    )
    one="המספר אשר הוא אחד"
    current=f"המספר אשר במקום אשר שמו {target}"
    add=f"המספר הנחשב בהוסיף את {one} על {current}"
    replace=f"שים במקום אשר שמו {target} את {add} תחת {current}"
    return " ".join([
        input_decl,
        f"יהי מקום ושמו {target} ובמקום אשר שמו {target} יהי {one} לבדו",
        f"ועתה פעמים כמספר אשר עומד תחת הדבר אשר למלאכה הזאת שמו {inp} {replace}",
    ])


def main() -> None:
    t0=time.perf_counter()
    c=compile_source(source())
    compile_ms=(time.perf_counter()-t0)*1000
    if not c.valid or c.ir is None:
        raise SystemExit("C5.5 resource sanity source failed to compile")
    pid=c.ir.program_input_domains[0].input_id
    timings=[]
    peak=0
    for n in (64,256,1024,4096):
        binding=(InputBinding(pid,NaturalValue(n)),)
        if n==4096:
            tracemalloc.start()
        t1=time.perf_counter()
        out=execute_ir(c.ir,bindings=binding)
        elapsed=(time.perf_counter()-t1)*1000
        if n==4096:
            _,peak=tracemalloc.get_traced_memory()
            tracemalloc.stop()
        obs=backend_observable(out)
        if obs.get("outcome")!="Normal" or dict(obs["facts"])["מונה"]!=n+1:
            raise SystemExit("C5.5 resource sanity observation mismatch")
        timings.append({"iterations":n,"execute_ms":round(elapsed,3)})
    print(json.dumps({
        "c5_5_resource_sanity":{
            "note":"observational only; Program Input Natural remains unbounded and no semantic size threshold is introduced",
            "semantic_threshold":None,
            "compile_ms":round(compile_ms,3),
            "timings":timings,
            "traced_peak_bytes_at_4096":peak,
        }
    },ensure_ascii=False,sort_keys=True))


if __name__=="__main__":
    main()
