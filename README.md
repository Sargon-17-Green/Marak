# Marak — מרק

**Marak** is an esoteric programming language whose source language is controlled Biblical Hebrew.

Current status: **M2 complete — Core v0.1 integration candidate**. Compiler baseline: **0.5.3-alpha.1**. The repository contains the normative Core surface and semantics, a working compiler pipeline, conformance evidence, and the original Megillah that motivated the project.

Public CLI: `marak`. Planned distribution: `marak`, with `marak-lang` reserved only as a fallback if the primary distribution name is unavailable.

The compiler pipeline is:

```text
source → normalization → parse → resolve → validate → canonical HAST
       → validated IR → artifact verification → execution
```

Key Core rules include: punctuation/layout are nonsemantic outside strings; propositions are not Boolean values; `הוצא` is not `return`; role association is not positional; `ועתה` is not `main`; and no hidden execution order is inferred from source layout.

## Quick start

```text
python -m pip install -e .
python -m pytest -q
marak version
```

Normative specification: `spec/`. Compiler implementation: `compiler/`. Independent verification evidence: `conformance/`. Original Megillah: `megillah/original/`.

Marak began as a deliberately whimsical experiment around a Pastafarian calendar Megillah; the project history is documented in `docs/history/ORIGIN.md`.

License: MIT.
