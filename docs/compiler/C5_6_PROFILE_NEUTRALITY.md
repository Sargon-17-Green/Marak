# C5.6 — BidirectionalIndex Profile Neutrality

## Semantic identity

C5.6 preserves B16's decision that year/general profile is non-semantic.

No profile metadata is stored in:

- `BidirectionalIndexValue`;
- `BidirectionalIndexDomain`;
- `ProgramInputId`;
- HAST Index Value semantic fields;
- IR Index Value semantic fields;
- program-contract fingerprint identity;
- artifact semantic identity;
- runtime observations.

The existing Index value remains only side + magnitude.

## Flow rule

Once a legal source expression independently resolves to `BIDIRECTIONAL_INDEX`, its source profile does not restrict later flow.

The production tests cover:

- year literal vs general literal identity;
- year-initialized place read/replaced by general head;
- general-initialized place read/replaced by year head;
- year-declared role receiving/reading general Index;
- general-declared role receiving/reading year Index;
- year Program Input declaration read by general head;
- general Program Input declaration read by year head;
- all four output/immediate-result source-profile combinations;
- mixed source-profile operands under general successor/predecessor;
- general Index values flowing into existing year-oriented Collection<BidirectionalIndex> operations.

## Program Input identity

C5.6 reuses C5.5 ownership and canonicality protections unchanged.

`ProgramInputId` fields remain:

- serial;
- spelling metadata;
- owning reusable program contract.

There is no profile field.

Binding remains named, owner-bound, immutable, non-positional, transport-independent, and validated before Preparation.

## State and role contracts

Places remain:

`PlaceId -> BIDIRECTIONAL_INDEX`.

Roles remain:

`RoleId -> BIDIRECTIONAL_INDEX`.

Act result contracts remain only `BIDIRECTIONAL_INDEX`.

No profile metadata participates in validation.

## Runtime observability

The HAST reference runtime, IR reference runtime, and portable backend observe only semantic BidirectionalIndex Values.

Source profile is not emitted in facts, products, errors, artifact value identity, or invocation identity.

## No generic type widening

Profile neutrality does not create:

- a generic unit system;
- runtime refinement types;
- arbitrary source-profile nouns;
- a second Index type;
- generic Index collections;
- signed arithmetic.

It is only the accepted equivalence of two source-level linguistic profiles over the same B13 semantic domain.
