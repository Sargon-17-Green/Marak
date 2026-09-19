# B Formal Semantics Core v0.1 — A13 / B12

## 1. Domains

\[
n\in\mathbb N.
\]

Typed semantic identities:

\[
p\in PlaceId,\quad a\in ActId,\quad \rho\in RoleId.
\]

State:

\[
S:PlaceId\rightharpoonup\mathbb N.
\]

No source-visible Location object is implied.

## 2. Outcome

\[
Outcome ::= Normal(S,O)\mid Error(S,E)\mid Divergence.
\]

## 3. Program

\[
Program(Prep,Principal).
\]

### Preparation success

\[
\langle Prep,S_\emptyset\rangle\Downarrow_{prep} S_0
\]

followed by:

\[
\langle Principal,S_0\rangle\Downarrow Normal(S_f,O)
\]

gives:

\[
Program\Downarrow Normal(S_f,O).
\]

### Preparation error

If:

\[
\langle Prep,S_\emptyset\rangle\Downarrow_{prep} Error(S_p,E),
\]

then:

\[
Program\Downarrow Error(S_p,E)
\]

and Principal is not evaluated.

## 4. Initial place establishment

For resolved place \(p\) whose initializer \(N\) successfully denotes \(n\):

\[
\frac{\langle N,S\rangle\Downarrow n}
{\langle EstablishInitial(p,N),S\rangle_{prep}\Downarrow S[p\mapsto n]}.
\]

If N errors, no fact for p is established by that unit.

## 5. Addition

\[
\frac{\langle A,S\rangle\Downarrow a\quad\langle B,S\rangle\Downarrow b}
{\langle Add(A,B),S\rangle\Downarrow a+b}.
\]

## 6. Natural subtraction

Success:

\[
\frac{\langle A,S\rangle\Downarrow a\quad\langle B,S\rangle\Downarrow b\quad a\le b}
{\langle SubFrom(A,B),S\rangle\Downarrow b-a}.
\]

Failure:

\[
\frac{\langle A,S\rangle\Downarrow a\quad\langle B,S\rangle\Downarrow b\quad a>b}
{\langle SubFrom(A,B),S\rangle\Downarrow Error(ARITHMETIC\_DOMAIN\_ERROR)}.
\]

If this inequality is proved during validation, the resolved executable program is not produced:
`InvalidProgram(ARITHMETIC_DOMAIN_ERROR)`.

## 7. Replacement

Success:

\[
\frac{\langle N,S\rangle\Downarrow n}
{\langle Replace(p,N),S\rangle\Downarrow Normal(S[p\mapsto n])}.
\]

RHS failure:

\[
\frac{\langle N,S\rangle\Downarrow Error(E)}
{\langle Replace(p,N),S\rangle\Downarrow Error(S,E)}.
\]

No replacement write occurs in the second rule.

## 8. Equality proposition

\[
S\models Equal(A,B)
\]

iff both numeric descriptions denote the same Natural.

No `true` Value is created.

## 9. Conditional

\[
\frac{S\models P\quad\langle A,S\rangle\Downarrow K}
{\langle If(P,A,B),S\rangle\Downarrow K}
\]

and analogously for \(S\not\models P\) using B.

Only the selected action executes.

## 10. Explicit sequence

\[
\frac{\langle A,S\rangle\Downarrow Normal(S')\quad\langle B,S'\rangle\Downarrow K}
{\langle A\ then\ B,S\rangle\Downarrow K}.
\]

If A errors/diverges, B has no evaluation premise and does not begin.

## 11. Post-action recurrence

First:

\[
\langle A,S\rangle\Downarrow Normal(S_1).
\]

If:

\[
S_1\models P,
\]

recurrence completes normally.

Otherwise repeat A from \(S_1\).

An infinite chain is Divergence.

## 12. Performance occurrence

Performing act a creates occurrence o with one fixed association per declared role:

\[
Associated(o,\rho,n).
\]

The association relation is occurrence-specific.

## 13. Output

Occurrence output slot initially empty.

Explicit production of n changes the occurrence's product from empty to `Some(n)` and execution
continues.

A second production is outside A13 Core validity.

## 14. Immediate provenance

A direct successful `Perform(a,...)` establishes ephemeral context:

\[
Recent(o,a,product).
\]

It is available only to the immediately following executable unit.

Any intervening executable unit clears it.

No successful provenance exists when the performance errors/diverges.

## 15. Normal completion

Body exhaustion:

\[
Body_a\Downarrow Completed(o,S,product).
\]

Principal exhaustion:

\[
Principal\Downarrow Normal(S,O).
\]

Neither creates HALT, Unit, return value, or exit status.

## 16. Runtime error propagation

Fatal Core error propagates outward through current control/performance/program context.

Earlier completed state/output effects remain.
No later explicit sequence continuation starts.

## 17. Trace

An internal trace may accompany an implementation derivation but is erased by the observation
projection and cannot be read by Core source.
