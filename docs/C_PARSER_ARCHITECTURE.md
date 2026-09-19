# C Parser Architecture

Status: current through A13/B12.

The parser is an exact Earley-style chart parser over versioned construction registries. It preserves all legal alternatives and has no score, confidence, probabilistic ranking, nearest-match rule or semantic pruning.

`CURRENT_REGISTRY` is `a13-b12.1`. Historical A0/A3/A8/A9/A10/A11/A12 registries remain immutable snapshots.

A13 adds the real whole-program root:

`CoreProgram := PreparatoryUnit* PrincipalExecution`

`PrincipalExecution := ועתה ExecutableSequence`

`ExecutableSequence := ExecutableUnit (ואחרי כן ExecutableUnit)*`

Preparation and principal execution are distinct grammatical/semantic categories. Top-level executable adjacency is not sequence. `ועתה` is an overt transition, not a magic `main` symbol.

The exact multi-word numeral terminal preserves all licensed boundaries rather than greedy longest-match behavior. Ambiguity remains fatal until a spec-grounded equivalence proof exists.

Tiny RM measurement: 238 tokens, 823 state keys/derivations, 69 completed nodes, one unique whole-program alternative. Timing is tooling evidence only.
