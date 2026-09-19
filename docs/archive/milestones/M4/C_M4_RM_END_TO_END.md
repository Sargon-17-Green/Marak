# C M4 — A13 Tiny Register Machine End-to-End

Fixture: `tests/fixtures/a13/a13_tiny_machine.he.txt`.

The witness passes:

- normalization;
- whole-program parse;
- typed resolution;
- validation;
- canonical HAST;
- canonical IR;
- deterministic artifact serialization;
- artifact verification;
- HAST reference execution;
- IR reference execution;
- portable backend execution.

Observed final state is Normal with Place serials 1 and 2 both holding `0`; the fixture produces no act products.

Parser measurement over 25 runs records 238 tokens, 823 state keys, 823 derivations, 69 completed nodes, one parse alternative and unique ambiguity status. Timing is tooling evidence only and is not semantic.

The external RM HALT state is represented by ordinary Core body/program exhaustion. There is no language-level HALT opcode. DECJZ translation guards zero before decrement; B12 underflow-guard regression covers 65 cases.
