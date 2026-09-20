# B14 Program Input Integration

A15 Program Input declarations map exactly to B13 Program Input Roles.

The declaration belongs to the resolved program invocation contract. It is not an executable
assignment, not a Preparation action, and not a parameter list of an implicit main function.

Lifecycle:
1. resolve ProgramInputIds and declared domains;
2. caller supplies identity-keyed associations;
3. validate exact required identities/domains;
4. establish immutable invocation associations;
5. begin A13/B12 Preparation;
6. begin Principal only at the unique `ועתה`.

Bad association sets are InvalidInvocation: MISSING_INPUT_BINDING, EXTRA_INPUT_BINDING,
DUPLICATE_INPUT_BINDING, INPUT_DOMAIN_MISMATCH. No Preparation effect occurs.

Binding is by semantic ProgramInputId, never declaration order, ordinal position, or spelling alone.

For request 007, B13 needs two Natural day roles. Natural input references can initialize frozen A13
Natural places during Preparation, so input→mutable-working-state flow exists for these two inputs.
The same copy pattern is absent for Symbol/Index/Collection only because typed places are missing.
