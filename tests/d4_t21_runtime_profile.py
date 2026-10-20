from __future__ import annotations

from collections import Counter
from pathlib import Path
import os
import signal
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from compiler.api import compile_source
from compiler.runtime.reference import ReferenceEvaluator
from tests.d4_t21_end_to_end_evidence import _production_source


PROFILE_SECONDS = 120


def _dump(evaluator: ReferenceEvaluator, label: str) -> None:
    print(
        f"PROFILE {label} products={len(evaluator.products)} "
        f"next_occurrence={evaluator.next_occurrence}",
        flush=True,
    )
    print("PROFILE top-action-nodes", flush=True)
    for (act, node), count in sorted(
        evaluator.profile_action_counts.items(),
        key=lambda item: (-item[1], item[0]),
    )[:60]:
        print(f"{count:12d}  {act}  {node}", flush=True)

    print("PROFILE top-perform-calls", flush=True)
    for act, count in Counter(evaluator.profile_call_counts).most_common(60):
        print(f"{count:12d}  {act}", flush=True)

    print("PROFILE last-products", flush=True)
    for product in evaluator.products[-30:]:
        print(
            f"{product.occurrence.serial:12d}  "
            f"{product.act.spelling}  {product.value!r}",
            flush=True,
        )


def main() -> None:
    source = _production_source("after")
    print(
        f"PROFILE compile source_chars={len(source)} "
        f"wall_seconds={PROFILE_SECONDS} intrinsics=on",
        flush=True,
    )
    compiled = compile_source(source)
    assert compiled.valid, [d.to_dict() for d in compiled.diagnostics]

    evaluator = ReferenceEvaluator(
        compiled.hast,
        profile_actions=True,
        constructive_intrinsics=True,
    )

    def timeout_handler(signum, frame):
        _dump(evaluator, "timeout")
        os._exit(0)

    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(PROFILE_SECONDS)
    outcome = evaluator.run()
    signal.alarm(0)

    print(f"PROFILE completed outcome={type(outcome).__name__}", flush=True)
    _dump(evaluator, "completed")


if __name__ == "__main__":
    main()
