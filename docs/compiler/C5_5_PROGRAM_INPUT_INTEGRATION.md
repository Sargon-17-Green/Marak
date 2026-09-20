# C5.5 — Program Input Source & Binding Integration

Status: implementation candidate on `workstream-c/c5-5-program-input-binding`.

## Scope

C5.5 integrates the frozen A15/B13/B15 Program Input contract into the production compiler/runtime pipeline:

`source -> resolution -> HAST -> IR -> artifact -> validated invocation -> Preparation -> Principal`.

C5.1's existing `ProgramInputId`, Program Input domain contracts, `InputBinding`, `ValidatedInvocation`, `validate_invocation()`, and the four frozen invocation error categories are reused rather than replaced.

C5.5 does not add transport semantics, optional/default parameters, positional arguments, mutable Program Inputs, generic parameters, I/O, modules, new loops, Megillah-specific behavior, or Megillah edits.

## Canonical source declaration

A required Program Input Role is top-level Preparation metadata, not executable action syntax:

```text
יהי למלאכה הזאת דבר ושמו ROLE
ובטרם תחל המלאכה הזאת
יעמד DOMAIN_HEAD
תחת הדבר אשר למלאכה הזאת שמו ROLE
```

The two ROLE occurrences must match. The declaration is admitted only as a `PreparatoryUnit`; it is not admitted inside an act body or after the principal `ועתה` transition.

Supported declaration domains are the already-frozen production domains:

- Natural: `מספר`
- Symbol(D): `שם ממשפחת השמות אשר שמה DOMAIN`
- BidirectionalIndex: `מספר שנה`
- Collection: one of the exact C5.3 admitted `CollectionKind` book heads, including admitted nested books

No generic type syntax is introduced. Symbol domains must already be visible under the existing introduced-before-use rule. Collection domains retain their exact recursive element domain.

## Canonical reads

Natural:

```text
המספר אשר עומד תחת הדבר אשר למלאכה הזאת שמו ROLE
```

Symbol:

```text
השם אשר במשפחת השמות אשר שמה DOMAIN
עומד תחת הדבר אשר למלאכה הזאת שמו ROLE
```

BidirectionalIndex:

```text
מספר השנה אשר עומד תחת הדבר אשר למלאכה הזאת שמו ROLE
```

Collection:

```text
הספר אשר עומד תחת הדבר אשר למלאכה הזאת שמו ROLE
```

The Collection read does not carry a guessed consumer type. Its exact recursive Collection domain comes from the resolved Program Input declaration. Symbol reads independently name the Symbol domain and must equal the declared Program Input domain.

## Source identity and visibility

Program Input Roles are source-resolved semantic identities.

- introduced-before-use is preserved;
- no hoisting is added;
- undeclared reads are rejected;
- duplicate Program Input Role declarations are rejected;
- declaration-role mismatch is rejected;
- raw role spelling is not an invocation identity;
- Program Input declarations are Preparation-only.

The resolver snapshots visible Program Inputs when named act bodies are defined, so an act body can read a Program Input declared before that body definition but cannot acquire a later declaration by hoisting.

## Program ownership

A `ProgramInputId` contains:

- resolved serial;
- source spelling metadata;
- a reusable program-contract owner.

The owner is not host object identity and is not a raw spelling key.

For compiled programs, the owner is a SHA-256 fingerprint over source-independent canonical IR semantics. Source spans are excluded, and the owner field itself is excluded from the fingerprint to avoid circular hashing. This gives two properties simultaneously:

1. charter-equivalent source variants retain the same program-contract identity;
2. artifact verification can recompute the owner from the decoded IR and reject a consistently forged owner even when the artifact digest was recomputed.

Canonical IR requires every Program Input identity in one program to carry the same recomputed owner. It also rejects source-unrepresentable identity collisions: Program Input serials are unique within the program contract, and Program Input role spellings are unique within that same owner.

Two different programs with colliding input serial/spelling metadata therefore do not automatically share Program Input identities; forged same-program serial or role-spelling collisions are rejected before execution.

## HAST and IR representation

C5.5 adds only the missing immutable read nodes.

HAST:

- `HastProgramInputNumber(input_id)`
- `HastProgramInputValue(input_id, domain)`

IR:

- `IRReadProgramInputNumber(input_id)`
- `IRReadProgramInputValue(input_id, domain)`

Natural reads are Natural expressions. Typed reads carry their exact static domain. There is no generic untyped runtime “input object”.

The Program Input contract remains explicit in `HastProgramInputDomain` / `IRProgramInputDomain`.

## Domain validation

Static-first validation covers:

- numeric read requires a Natural Program Input contract;
- typed read requires exact declared domain equality;
- Symbol(D) must equal the exact declared Symbol(D);
- BidirectionalIndex heads require BidirectionalIndex;
- Collection reads preserve exact recursive CollectionDomain;
- undeclared ProgramInputId reads are rejected;
- duplicate/conflicting contracts are rejected;
- cross-owner contracts are rejected;
- Symbol domains referenced by canonical input contracts must be declared;
- consumer context cannot rescue a malformed read.

The canonical IR validator repeats these checks independently of source resolution.

## Artifact contract

C5.5 advances the serialized contracts coherently:

- compiler: `0.5.5-alpha.1`
- Python package: `0.5.5a1`
- HAST: `core-hast-0.6-candidate-1`
- IR: `core-ir-0.6-candidate-1`
- artifact: `core-artifact-0.6-candidate-1`
- portable backend: `portable-ir-vm-0.6-candidate-1`
- IR reference: `core-ir-reference-0.6-candidate-1`
- construction registry: `c5.5-a15-b13.1`
- language edition: unchanged, `core-0.1-integration-candidate-a13-b12`

Artifact 0.5 is rejected rather than silently reinterpreted as 0.6.

Reusable artifacts contain Program Input identities, owning contract metadata, and declared domains. Invocation values are never serialized into the reusable artifact.

## Invocation lifecycle

The production execution contract is:

1. source compiles to a program plus required Program Input contract;
2. caller supplies `InputBinding` values using resolved `ProgramInputId` identities and Marak semantic Values;
3. all bindings are validated as a set;
4. only a valid binding set becomes `ValidatedInvocation`;
5. only then may Preparation begin;
6. Principal follows Preparation under the ordinary frozen semantics.

An invalid binding set produces `InvalidInvocation`, not `RuntimeError`, `InvalidProgram`, or a generic host exception.

The preserved categories are exactly:

- `MISSING_INPUT_BINDING`
- `EXTRA_INPUT_BINDING`
- `DUPLICATE_INPUT_BINDING`
- `INPUT_DOMAIN_MISMATCH`

Validation is set/identity based. Caller binding order is semantically irrelevant.

## ValidatedInvocation safety

`ValidatedInvocation` is not a transferable bearer token.

Every execution path revalidates its immutable bindings against the target program. Reusing an invocation validated for Program A against Program B therefore fails with the ordinary invocation issues if the Program Input identities do not belong to B.

This is enforced in the HAST reference runtime, IR reference runtime, and portable backend.

## Preparation boundary

All three runtimes perform invocation validation before evaluator/VM execution and before any Place initializer is evaluated.

Consequences:

- missing/extra/duplicate/wrong-domain bindings cannot cause partial Preparation;
- a Preparation runtime error cannot precede an invocation error;
- no initializer effect occurs for invalid invocation;
- a Program Input read in a valid Place initializer sees the immutable bound Value.

## Runtime representation

The invocation boundary uses Marak semantic Values.

In particular, Natural input is supplied as `NaturalValue(n)`, not arbitrary host integers. The existing evaluator internals continue to use Python exact integers for Natural evaluation; conversion occurs only after successful invocation validation.

Symbol, BidirectionalIndex, and Collection values remain their existing semantic Value representations. Collection values retain their recursive element-domain metadata.

No semantic size ceiling is introduced.

## Production execution APIs

Program Input bindings are available through production paths, not test-only helpers.

- `run_source(..., bindings=...)`
- `run_reference(..., bindings=...)`
- `execute_ir(..., bindings=...)`
- `execute_ir_reference(..., bindings=...)`
- `execute_reference(..., bindings=...)`

Programs without Program Inputs continue to execute with the existing zero-argument/default binding behavior.

## Runtime agreement

The HAST reference runtime, canonical-IR reference runtime, and portable backend all:

- validate bindings before Preparation;
- read the same immutable invocation association;
- preserve existing state/effect/output/provenance semantics;
- return distinct InvalidInvocation behavior before language runtime execution.

C5.5 tests compare language observations across all three engines for Natural, Symbol, Index, Collection, nested Collection, invalid invocation, and cross-program ownership cases.

## Exact Natural and resources

Program Input Natural remains an unbounded Natural. Tests include a value far beyond fixed host-width integer ranges.

Resource observations are implementation evidence only. No semantic threshold, truncation, coercion, or new input-size limit is introduced.

## Scope exclusions

C5.5 intentionally excludes:

- Megillah-specific behavior or edits;
- stdin, argv, environment variables, files, HTTP, JSON protocol, GUI/network input;
- CLI parameter mapping;
- source-spelling host dictionaries;
- positional arguments;
- optional/default parameters;
- mutable Program Inputs;
- generic function parameters;
- generic Integer or Boolean Value;
- new Collection capabilities;
- iterator/cursor/loop-index Values;
- generic while/for;
- modules or I/O.

Workstream D remains separate.
