# Marak — Core compiler implementation

Marak is a programming language whose Core v0.1 candidate surface is controlled Biblical Hebrew. This tree is the canonical Workstream C implementation after C M4.2 remediation.

The implemented pipeline is:

```text
source → normalization → parse → resolve → validate → canonical HAST
       → validated IR → artifact verification → reference/backend execution
```

Current implementation versions:

- compiler: `0.4.2-alpha.1`
- language: `Marak`
- language edition: `core-0.1-integration-candidate-a13-b12`
- construction registry: `a13-b12.1`
- HAST: `core-hast-0.1-candidate-1`
- IR: `core-ir-0.1-candidate-1`
- artifact: `core-artifact-0.1-candidate-1`
- IR reference evaluator: `core-ir-reference-0.1-candidate-3`
- portable backend: `portable-ir-vm-0.1-candidate-3`

Execution uses explicit implementation activations; they are not language-visible stack frames. By default there is **no artificial semantic depth/performance-count ceiling**. An optional `max_active_performances=N` argument exists only as a caller/harness resource control. Actual host allocation failure is mapped to an implementation-resource failure, not to a Marak language error.

Public CLI: `marak`. Planned distribution name: `marak` (fallback only if unavailable at publication time: `marak-lang`).

License: MIT.

Run tests:

```text
python -m pytest -q
```

Historical milestone handoff documents are retained under `docs/archive/milestones/`; generated handoff manifests and checksum ledgers are intentionally not part of the canonical source root.
