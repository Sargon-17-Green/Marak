# Computational Core Requirements

Marak Core must be sufficient to express arbitrary computation.

The constructive proof vehicle is a deterministic Register Machine with unbounded natural-number registers and three instruction forms: increment-and-jump, decrement-or-zero-branch, and halt.

The Register Machine is proof machinery, not source-language architecture. A correct translation must preserve machine state and termination while using only admitted Marak constructions.

Core therefore needs semantic capability equivalent to:
- unbounded natural numbers;
- persistent state and explicit replacement;
- exact increment/decrement within the natural-number domain;
- zero testing and branching;
- unbounded recurrence;
- reusable named computation;
- finite normal completion.

Register-Machine `HALT` maps to ordinary Marak completion; it does not justify a dedicated HALT primitive.

The independent E v0.8.2 review confirmed the current A13/B12/C M4.2 Core against the Register-Machine witness.
