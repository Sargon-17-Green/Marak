# D4 Repair Metrics

D4 makes no candidate-source edit while the first frontier is blocked.

## Inherited D3 candidate metrics

- original normalized tokens: **9,227**
- candidate normalized tokens: **9,039**
- D3 normalized-token delta: **-188**
- matched original tokens in sequence: **8,940**
- D3 lexical match: **96.8896%**
- documentary/example words explicitly externalized: **238**
- blocked interface words retained separately: **38**
- inherited approved local source spans changed: **6**
- inherited structural repairs: **1**

## D4 delta

- new candidate spans changed: **0**
- words inserted into candidate: **0**
- words removed from candidate: **0**
- new documentary spans externalized: **0**
- new structural repairs: **0**
- new algorithm-changing repairs: **0**
- structural moves: **0**
- starting candidate SHA-256: `afc6eda11a8d7f4b6499cf643d2ef5b36581bcad61b5fce761a7709274d2d643`
- final candidate SHA-256: `afc6eda11a8d7f4b6499cf643d2ef5b36581bcad61b5fce761a7709274d2d643` — **confirmed unchanged by CI**
- historical original SHA-256: `7b834f4a444e021bb65164282b851af960a6dbc0be3d458c2412181773b9db7b` — **confirmed unchanged by CI**
- provenance: **100% inherited D3 coverage; no D4 orphan source introduced**

## Verification

Executable/evidence head `6a2bffcce5d390c47c524c7d06ce5429500a4a4c`:
- GitHub Actions run `35570493493`: **15/15 jobs PASS**
- D3 + D4 targeted: **29 passed**
- full pytest: **478 passed, 126 subtests passed**
- Ubuntu D4: **PASS**
- Windows D4: **PASS**

Preservation metrics are not algorithm-equivalence proof.
