# C5.7 — Test Evidence

Canonical baseline:
`5679fbe861bc2d30aba479e32fd042bf196295ca`

Local verification was performed on the fresh C5.7 branch created from that
baseline.

## C5.7 targeted production suite

`python -m pytest -q tests/test_c5_7_multiword_source_names.py`

Result: **14 passed**.

Coverage includes:
- exact 115-site / 11-role registry migration;
- historical C5.6 NameTerminal freeze;
- canonical multi-word Place identity and artifact spelling;
- ten-word and construction-word payloads;
- prefix-related names without longest match;
- count-one, short-payload, and extra-payload rejection;
- declaration/reference mismatch;
- Program Input identity and resolved binding;
- act/role/Symbol domain/member identity;
- forward-reference preservation;
- duplicate rejection in all six existing duplicate scopes;
- required version disposition.

## Full production regression

`python -m pytest -q`

Result: **557 passed, 126 subtests passed**.

Affected current-version/portability subset after registry/compiler bump:
**52 passed**.

B17 semantic + production compatibility:
- semantic: **25 passed**;
- production compatibility: **15 passed**;
- total B17 reference: **40 passed**.

## Inherited gates

PASS:
- A13 self-test: **289 checks**;
- B12 semantic/run-all;
- A15 surface: **335,280 case checks**;
- B13 reference: **28 tests**;
- B14 integration: **22 tests**;
- A16: **2,548 checks**;
- A17: **4,415 checks**;
- B15: **29 tests**;
- C5.6/B16 semantic regressions: **28 tests**;
- B16 required regressions: **4 passed**;
- D3/D4 frozen Megillah regressions: **29 passed**.

## Canonical-byte evidence

Current construction registry SHA-256:
`3c8e6f179d9259c2f84be34f80b215925d72d6d07fc9bcb7d8e5d4279dd1da17`

Canonical artifacts were regenerated with the current compiler and produced
no committed artifact delta; artifact format remains 0.7.

Additional hygiene:
- `python -m py_compile` on changed compiler modules: PASS;
- `git diff --check`: PASS;
- proposal test-result side effects from A16/A17 runners were reverted;
- no Megillah file was edited.
