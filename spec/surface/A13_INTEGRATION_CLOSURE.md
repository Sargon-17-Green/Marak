# A13_INTEGRATION_CLOSURE.md

Snapshot: **A-Core v0.1 A13 Integration-Frozen Candidate**

A13 is a closure revision of A12, not Language 0.2.

Closed Master-review blockers:
1. exact closed Unicode whitespace table;
2. Natural-only subtraction domain;
3. no HALT surface primitive;
4. whole-program composition;
5. discourse visibility/lifetime;
6. normal completion.

Preserved A12 invariants:
- propositions are not Boolean Values;
- `הוצא` is not abrupt return;
- role binding is name-addressed, not positional;
- no implicit dereference;
- execution order comes from explicit language, chiefly `ואחרי כן`;
- punctuation/layout do not establish syntax;
- Register Machine organization remains proof-only.

A13 is ready to be handed to B12, C M4 and E v0.8 for downstream integration. A13 does not declare M2.
