# B-Core v0.1 State and Effects — A13

## Place identity

A place is a source-resolved state-bearing referent.

Identity is not:
- current numeric value;
- memory address;
- pointer;
- runtime string.

## Current fact

\[
Current_S(p)=n,\quad n\in\mathbb N.
\]

## Preparatory establishment

A13 initialized-place introduction establishes the first current fact during Preparation.

The place becomes source-visible only after the complete introduction.

This is not executable replacement.

## Replacement

Executable replacement:
1. evaluate pure Natural RHS;
2. if successful, replace current fact;
3. if RHS errors, perform no replacement.

Earlier completed actions remain committed.

## No local mutable state
Performance-local mutable places are not Core v0.1.

Internal activation storage remains implementation-only.
