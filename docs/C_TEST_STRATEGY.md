# C Test Strategy

M4.2 retains all M4.1 regressions and A13/B12 conformance, then adds resource-boundary and bootstrap-metadata coverage.

Execution coverage includes deep finite recursion across the old quota boundary, low Python recursion-limit independence, no-fuel infinite recursion under external subprocess timeout, optional explicit caller budget behavior, high sequential performance counts, activation cleanup and three-way HAST/IR-reference/backend differential agreement. Resource controls are never treated as language semantics.

Existing coverage remains for exact whitespace/U+200B, source maps, ambiguity, whole-program structure, visibility/no-hoisting, typed identities, Natural arithmetic/underflow, effect boundaries, conditionals, recurrence, named role correspondence, occurrence locality, outputs/provenance, artifacts, CLI and relocation.

Bootstrap tests require Marak/MIT/`marak` metadata, prohibit stale source-root handoff ledgers and generated payload directories, and reject absolute workspace dependencies.
