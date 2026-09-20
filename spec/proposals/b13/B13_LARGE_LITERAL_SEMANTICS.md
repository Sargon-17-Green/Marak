# B13 Large Literal Semantics

## B-LIT-001 (PROPOSED)
REQUEST-005 requires no new B value domain or arithmetic operation.

Whenever A admits a direct numeral construction and resolves it to mathematical magnitude n:

`LiteralNat(source) ⇓ Natural(n)` exactly.

There is no semantic maximum such as 9,999, 32-bit, 64-bit, or 256-bit.

## A dependency
A14 must define a productive Biblical numeral grammar beyond the A13 frozen range and map every admitted form unambiguously to a Natural. B does not select wording.

## C consequence
Parsing/validation must preserve arbitrary mathematical magnitude and cannot use a machine-word ceiling as language validity. Actual inability to process an enormous literal is implementation resource exhaustion, not a different value and not a normative maximum.

## Status
B semantics are already sufficient; request status is **AWAITING_A**.
