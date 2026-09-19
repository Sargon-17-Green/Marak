# Contributing to Marak

Marak is still pre-1.0. Changes to implementation are welcome, but language changes require stronger justification than ordinary compiler changes.

For a proposed language feature, state:
1. the computational or semantic need;
2. the Biblical-Hebrew expression proposed;
3. ambiguity risks;
4. whether the design was independently derived or borrowed from a familiar programming-language convention;
5. positive and negative conformance cases.

Do not treat current compiler behavior as automatically normative. The authority order is: Language Charter → normative specification → conformance requirements → implementation → examples/guides.

Pull requests must keep the Core test suite green and should add tests for every normative change.
