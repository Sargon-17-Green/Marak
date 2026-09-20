# B15 Typed Output Semantics

## Static output contract

For act a, inspect all syntactic `הוצא` sites after independent expression-domain resolution:

- zero sites: `ActOutputDomain(a)=None`;
- one or more sites, all exact D: `ActOutputDomain(a)=D`;
- sites with differing domains: InvalidProgram(`MIXED_OUTPUT_DOMAINS`);
- unresolved output expression domain: InvalidProgram.

The result domain is not inferred from caller use and A16 introduces no return-type declaration.

Mutually exclusive output sites are one output position, not several. They are legal only when all
sites have the same D.

## Runtime occurrence

Every occurrence begins with an empty product slot.
Reached `הוצא v`:
1. requires v's statically resolved domain to equal the act output domain;
2. stores `Some(v)` if the slot is empty;
3. execution continues normally after production.

Thus output is not return. A later body action still executes.

A second reached production in the same occurrence violates the existing zero/one cardinality.
Separate repeated act performances each have independent product slots and may each emit an ordinary
output event. No Collection of repeated outputs is synthesized.

## Observation

B13 observation remains:
- Symbol: member identity presented through canonical visible label metadata;
- BidirectionalIndex: Before/Zero/After and exact magnitude;
- Collection: finite order/length plus recursively observable members.

No stdout, transport, exit status, or return convention is introduced.
