# C Windows Tooling Portability

## Finding

D-C-FIND-001 reproduced two Windows-only failures in registry dumping:
1. the test compared a native path as text and assumed forward slashes;
2. `Path.write_text()` used host newline translation, producing CRLF instead of canonical LF.

## Fix

Path output remains a native filesystem path. Tests parse it as `pathlib.Path` and compare resolved path identities rather than separator spelling.

Canonical generated registry snapshots are serialized as JSON text ending in one LF, encoded as UTF-8, and written with `Path.write_bytes()`. This avoids host text-mode newline conversion. The same policy is applied to both current-registry and A0 snapshot generators.

## Canonical policy

Generated registry files are byte-canonical UTF-8 + LF on every supported host. Byte equality against the tracked snapshot remains mandatory; semantic JSON equality is an additional check, not a replacement.

## Scope audit

The repository's canonical registry generators are `tools/dump_current_registry.py` and `tools/dump_construction_registry.py`; both previously used `write_text()` and both now use explicit canonical bytes. `tools/parser_stress.py` does not generate tracked canonical artifacts.

## Verification

The targeted portability test reruns both generators, verifies the reported target using path semantics, verifies exact before/after bytes, rejects CRLF, and confirms the parsed registry model.

CI runs the lightweight portability test on `ubuntu-latest` and `windows-latest`, reports the generated current-registry SHA-256, and requires zero diff for both canonical snapshot files.

The compiler surface, parser, semantics, IR, artifact format, and runtime are unchanged.
