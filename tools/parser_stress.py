from __future__ import annotations

import argparse
import json

from compiler.api import normalize
from compiler.lex.words import lex_words
from compiler.parse.grammar import (
    ConstructionDeclaration,
    ConstructionKind,
    Nonterminal,
    Production,
    SpecStatus,
    WordTerminal,
    registry_from_parts,
)
from compiler.parse.parser import Parser


def main() -> None:
    ap = argparse.ArgumentParser(description="Synthetic ambiguity probe; not language syntax")
    ap.add_argument("words", type=int, nargs="?", default=5)
    args = ap.parse_args()
    if args.words < 1:
        raise SystemExit("words must be >= 1")

    declaration = ConstructionDeclaration(
        "SYNTHETIC.AMBIG",
        ConstructionKind.POSITIVE,
        SpecStatus.NORMATIVE,
        ("SYNTHETIC-ONLY",),
        "Synthetic left-recursive ambiguity stress grammar; never a language rule.",
    )
    registry = registry_from_parts(
        language_edition="synthetic",
        registry_version="synthetic.1",
        source_snapshot="tools/parser_stress.py",
        declarations=(declaration,),
        productions=(
            Production("SYN.P0", declaration.construction_id, "Program", (Nonterminal("X"),), "PROGRAM", root=True),
            Production("SYN.P1", declaration.construction_id, "X", (Nonterminal("X"), Nonterminal("X")), "PAIR"),
            Production("SYN.P2", declaration.construction_id, "X", (WordTerminal("אב"),), "ATOM"),
        ),
    )
    source = " ".join(["אב"] * args.words)
    normalized = normalize(source)
    tokens = lex_words(normalized)
    result = Parser(registry).parse(tokens, {}, source_map=normalized.source_map)
    print(json.dumps({
        "synthetic_only": True,
        "words": args.words,
        "ambiguity_status": result.forest.ambiguity_status.value,
        "metrics": {
            "token_count": result.metrics.token_count,
            "chart_positions": result.metrics.chart_positions,
            "state_keys": result.metrics.state_keys,
            "derivations": result.metrics.derivations,
            "completed_nodes": result.metrics.completed_nodes,
            "alternatives": result.metrics.alternatives,
            "peak_state_keys_at_position": result.metrics.peak_state_keys_at_position,
        },
    }, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
