# C5.1 Test Evidence

Windows implementation checkout at baseline descendant `6888bd538a73f9dc76bf87cdf87640b7b4b93d9e`:

- production pytest: 280 passed + 126 subtests (pre-final-doc run; final rerun required before PR)
- B15 independent: 29/29 PASS
- A16 surface/reference: 2,548/2,548 PASS
- B14 integration: 22/22 PASS
- B13 reference: 28/28 PASS
- A15 surface/reference: 335,280 checks PASS
- A13 frozen selftest: 289 PASS
- B12 frozen `run_all.py`: PASS

C5.1 adversarial coverage includes Symbol into Natural place, Collection into Symbol role, mixed output domains, wrong immediate-result typed head, unknown domain tags, heterogeneous collection metadata, duplicate/conflicting Program Input contracts, expected-type rescue rejection, old artifact-version rejection, and Symbol internal-ID renumbering invariance.

Non-Natural carrier chains cross HAST -> IR -> artifact serialization -> artifact verification -> HAST reference evaluator / IR reference evaluator / portable backend, and compare semantic observations.

Performance smoke on the A13 tiny RM (10 measured runs after warm-up, Windows): baseline compile median 0.0662374 s / run median 0.0731869 s; C5.1 compile median 0.05157575 s / run median 0.05886465 s. This run shows no catastrophic Natural-only regression; it is not a benchmark guarantee.

Machine-readable evidence is under `docs/compiler/evidence/`.
