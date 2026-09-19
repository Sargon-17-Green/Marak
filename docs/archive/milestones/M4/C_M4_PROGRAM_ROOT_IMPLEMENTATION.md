# C M4 — Program Root Implementation

A13 whole-program grammar is implemented as:

- zero or more `PreparatoryUnit` items;
- exactly one top-level `ועתה` transition;
- one `ExecutableSequence` after the transition;
- additional principal actions only through explicit `ואחרי כן`.

Preparation includes initialized place introductions, act introductions, role declarations and act-body definitions. Preparation is processed in source/discourse order for visibility and dependency, but it is not lowered to an executable statement list.

Principal execution is represented separately. No symbol called `main` is created and no act name receives entry semantics.

Stable program diagnostics include:

- `PROG0001`: no principal transition;
- `PROG0002`: multiple top-level principal transitions;
- `PROG0003`: preparatory material after principal transition;
- `PROG0004`: unsequenced principal executable material.

Newlines, headings and punctuation do not define the program boundary.
