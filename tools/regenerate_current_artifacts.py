#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from compiler.api import compile_source

ROOT=Path(__file__).resolve().parents[1]
NAMES=(
    "basic_update","immediate_result","natural_subtraction","normal_completion",
    "output_not_return","post_action_countdown","recursive_countdown",
    "role_association","tiny_rm",
)


def main() -> int:
    for name in NAMES:
        source_rel=Path("examples")/"m4"/f"{name}.he.txt"
        source_path=ROOT/source_rel
        artifact_path=ROOT/"artifacts"/f"{name}.he.cbh-artifact.json"
        result=compile_source(source_path.read_text(encoding="utf-8"),file=source_rel.as_posix())
        if not result.valid or result.artifact is None:
            raise SystemExit(f"compile failed for {source_rel}: {[d.code for d in result.diagnostics]}")
        artifact_path.write_bytes(result.artifact)
        print(artifact_path.relative_to(ROOT).as_posix())
    return 0


if __name__=="__main__":
    raise SystemExit(main())
