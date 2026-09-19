# Marak CLI Specification

Commands:

- `marak check FILE [--json]`: normalize, parse whole program, resolve and validate; does not execute.
- `marak compile FILE [-o ARTIFACT]`: produce verified canonical artifact.
- `marak run FILE [--json]`: compile/verify and execute the portable backend.
- `marak explain FILE [--normalization|--parse|--resolve|--semantic|--all]`: structured JSON explanation.
- `marak version`: separate compiler, language, registry, HAST, IR, IR-reference, artifact and backend versions.

`explain --all` includes normalized source, tokens/source spans, parse forest/metrics, Preparation/Principal division, typed identities, visibility, role/body ownership, immediate-result provenance, HAST and validated IR. It contains no ranking/confidence.

CLI execution uses the default runtime contract: no artificial performance-depth quota. The CLI currently exposes no quota flag. CLI process exit codes are tooling conventions only; they are not Marak values or program results. Public CLI failures are exception-firewalled and do not print Python tracebacks by default.
