from __future__ import annotations

from collections import Counter

from compiler.api import compile_source
from compiler.runtime.reference import ReferenceEvaluator
from tests.d4_t21_end_to_end_evidence import _production_source


FUEL = 500_000


def main() -> None:
    source = _production_source("after")
    print(f"PROFILE compile source_chars={len(source)} fuel={FUEL}", flush=True)
    compiled = compile_source(source)
    assert compiled.valid, [d.to_dict() for d in compiled.diagnostics]

    evaluator = ReferenceEvaluator(
        compiled.hast,
        fuel=FUEL,
        profile_actions=True,
    )
    outcome = evaluator.run()

    print(
        f"PROFILE outcome={type(outcome).__name__} "
        f"fuel_remaining={evaluator.fuel} products={len(evaluator.products)}",
        flush=True,
    )
    print("PROFILE top-action-nodes", flush=True)
    for (act, node), count in sorted(
        evaluator.profile_action_counts.items(),
        key=lambda item: (-item[1], item[0]),
    )[:40]:
        print(f"{count:12d}  {act}  {node}", flush=True)

    print("PROFILE top-perform-calls", flush=True)
    for act, count in Counter(evaluator.profile_call_counts).most_common(40):
        print(f"{count:12d}  {act}", flush=True)


if __name__ == "__main__":
    main()
