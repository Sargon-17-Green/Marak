# A13_PROGRAM_COMPOSITION.md

Status: NORMATIVE Core v0.1 integration closure

## Need and alternatives
A program must introduce names/acts and then request one unambiguous top-level computation.

Rejected: execute every top-level form by textual order. Rejected: magic first/last/`main` act.
Chosen: Hebrew preparatory discourse followed by an explicit `ועתה` transition into execution.

Biblical `ועתה` naturally transitions from prior discourse to a present instruction (e.g. Joshua 9:25;
2 Kings 10:19). The language does not infer `main()` from this.

## Abstract grammar

    CoreProgram := PreparatoryUnit* PrincipalExecution
    PrincipalExecution := ועתה ExecutableSequence
    ExecutableSequence := ExecutableUnit (ואחרי כן ExecutableUnit)*

PreparatoryUnit:
- initialized place introduction;
- act introduction;
- role declaration;
- act body definition.

These establish referents/contracts/initial facts and are not executed merely by occurrence.

Exactly one top-level `ועתה` is required. No preparatory unit follows it. Two top-level actions require
explicit `ואחרי כן`; newline/punctuation/adjacency never provides order.

## Normal completion
The program completes when the principal sequence and acts it explicitly performs exhaust normally and
no continuation remains. A13 defines no HALT/exit/main-return or exit code.
