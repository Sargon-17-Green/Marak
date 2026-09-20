# B13 External Input Binding Model

## B-INVOKE-001 — Program Input Roles (PROPOSED)
A resolved program may declare named Program Input Roles. One program invocation supplies exactly one immutable value for each required role by semantic identity.

This is not stdin, argv, HTTP, positional arguments, environment variables, or an externally writable place.

## Why this model
Named external places conflate transport input with mutable state and create overwrite questions. Positional arguments have no independent linguistic basis. Program-level roles reuse B12's proven identity-based association model without pretending the whole program is a conventional function.

## Static contract
Each `ProgramInputId` has an owning Program identity, its own resolved role identity, and one declared value domain. D2 presently needs two Natural roles: calculation day and target day. The representation can admit future declared domains without requiring generic polymorphism now.

## Invocation lifecycle
1. parse/resolve/validate source into a program contract;
2. caller supplies associations `ProgramInputId ↦ Value`;
3. validate exact required identities and value domains;
4. establish immutable invocation associations;
5. B12 Preparation begins and may read those associations;
6. Principal follows only after successful Preparation.

Binding order is not executable source order.

## Lifetime/mutability
Associations are immutable throughout one invocation, including Preparation and Principal. Preparation cannot overwrite them because they are not state-bearing places. If mutable working state is needed, Preparation explicitly establishes a place from an input value.

## Invalid invocation
A valid program with bad caller associations fails before Preparation as `InvalidInvocation`:
- `MISSING_INPUT_BINDING`;
- `EXTRA_INPUT_BINDING`;
- `DUPLICATE_INPUT_BINDING`;
- `INPUT_DOMAIN_MISMATCH`.

This is distinct from malformed source and from RuntimeError.

Transport is entirely a C/tooling concern.
