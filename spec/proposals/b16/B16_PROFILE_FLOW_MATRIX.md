# B16 Profile Flow Matrix

All rows below have semantic domain `BidirectionalIndex`.

| Producer profile | Consumer carrier profile | Verdict | Semantic result |
|---|---|---|---|
| year literal/input | year carrier | ADMITTED | unchanged Index Value |
| general literal/input | general carrier | ADMITTED | unchanged Index Value |
| year | general Program Input read/state carrier | ADMITTED | unchanged Index Value |
| general | year state carrier | ADMITTED | unchanged Index Value |
| year | general named-act role | ADMITTED | occurrence association to same Value |
| general | year named-act role | ADMITTED | occurrence association to same Value |
| year | general output/immediate-result head | ADMITTED | same output Value/provenance |
| general | year output/immediate-result head | ADMITTED | same output Value/provenance |

## Coherence rule

Source expressions must be internally well-formed in one admitted construction family. Mixed literal
phrases such as year noun + general origin remain InvalidProgram at parse/resolution.

After a complete source expression independently resolves to `BidirectionalIndex`, its profile does
not constrain later carriers. Carrier heads establish/confirm the semantic domain, not a hidden unit.

No expected-type rescue is permitted.

## Program input

The generic head changes no invocation semantics. ProgramInputId identity, named association,
immutability, binding-order irrelevance, pre-Preparation validation, error categories, and transport
independence remain exactly B13/C5.5.
