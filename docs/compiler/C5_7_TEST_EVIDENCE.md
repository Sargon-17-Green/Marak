# C5.7 — Test Evidence

Canonical baseline:
`5679fbe861bc2d30aba479e32fd042bf196295ca`

Local verification was performed on the fresh C5.7 branch created from that
baseline.

## C5.7 targeted production suite

`python -m pytest -q tests/test_c5_7_multiword_source_names.py`

Result: **18 passed**.

Coverage includes:
- exact 115-site / 11-role registry migration;
- explicit counted multi-word production-positive coverage for all 11 name roles;
- counted SourceName semantic text = payload while token/normalized/original provenance spans the complete construction;
- counted-name diagnostic span covers the complete occurrence;
- explicit ResultActionName immediate-result execution through all three runtime paths;
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

Result: **561 passed, 126 subtests passed**.

Affected current-version/portability subset after registry/compiler bump:
**52 passed**.

B17 semantic + production compatibility:
- semantic: **25 passed**;
- production compatibility: **15 passed**;
- total B17 reference: **40 passed**.

## Master remediation rerun

PASS:
- C5.7 targeted production suite: **18 tests**;
- A18 remediation checks: covered directly by the C5.7 counted-surface/span tests; A18 has no standalone executable runner in the repository;
- B17 semantic + production compatibility: **40 tests**;
- B13 reference: **28 tests**;
- B15 reference/integration: **29 tests**;
- C5.6/B16 semantic regressions: **28 tests**;
- B16 required regressions: **4 tests**;
- A17 surface: **4,415 checks**;
- Program Input remediation set: **26 tests**;
- Symbol production pipeline: **18 tests**;
- D3/D4 frozen Megillah regressions: **29 tests**;
- full pytest: **561 tests + 126 subtests**;
- current-version/portability subset: **52 tests**.

The remediation did not require or perform any A18/B17 proposal mutation.

## Canonical-byte evidence

Current construction registry SHA-256:
`3c8e6f179d9259c2f84be34f80b215925d72d6d07fc9bcb7d8e5d4279dd1da17`

The current registry was regenerated twice and remained byte-stable at the SHA above.
Canonical artifacts were regenerated twice with the current compiler and produced
no committed artifact delta; artifact format remains 0.7.

Additional hygiene:
- `python -m py_compile` on changed compiler modules: PASS;
- `git diff --check`: PASS;
- proposal test-result side effects from A16/A17 runners were reverted;
- no Megillah file was edited.
