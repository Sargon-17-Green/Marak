from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from compiler import api
from compiler.parse.current_registry import CURRENT_REGISTRY
from compiler.runtime.observables import backend_observable
from compiler.source.text import SourceText
from compiler.version import (
    ARTIFACT_FORMAT_VERSION,
    COMPILER_VERSION,
    LANGUAGE_NAME,
    CONSTRUCTION_REGISTRY_VERSION,
    HAST_VERSION,
    IR_VERSION,
    IR_REFERENCE_VERSION,
    LANGUAGE_EDITION,
    RUNTIME_BACKEND_VERSION,
)


def _read_source(path: str) -> SourceText:
    if path == "-":
        return SourceText(sys.stdin.read(), "<stdin>")
    return SourceText.from_file(path)


def _print_diagnostics(result, as_json: bool) -> None:
    if as_json:
        if result.diagnostics:
            print(json.dumps([d.to_dict() for d in result.diagnostics], ensure_ascii=False, indent=2, sort_keys=True))
        return
    for d in result.diagnostics:
        p = d.source_span.start if d.source_span else None
        loc = f"{p.file}:{p.line}:{p.column}: " if p else ""
        print(f"{loc}{d.severity.value} {d.code}: {d.message_en}", file=sys.stderr)


def _default_artifact_path(source_path: str) -> str | None:
    if source_path == "-":
        return None
    return source_path + ".cbh-artifact.json"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="marak")
    sub = p.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check")
    check.add_argument("file")
    check.add_argument("--json", action="store_true")

    compile_p = sub.add_parser("compile")
    compile_p.add_argument("file")
    compile_p.add_argument("-o", "--output")
    compile_p.add_argument("--json", action="store_true")

    run = sub.add_parser("run")
    run.add_argument("file")
    run.add_argument("--json", action="store_true")

    explain = sub.add_parser("explain")
    explain.add_argument("file")
    levels = explain.add_mutually_exclusive_group()
    levels.add_argument("--normalization", action="store_true")
    levels.add_argument("--parse", action="store_true")
    levels.add_argument("--resolve", action="store_true")
    levels.add_argument("--semantic", action="store_true")
    levels.add_argument("--all", action="store_true")
    explain.add_argument("--json", action="store_true", help="accepted for CLI symmetry; explain is JSON")

    sub.add_parser("version")
    return p


def _explain_level(args: argparse.Namespace) -> str:
    for level in ("normalization", "parse", "resolve", "semantic", "all"):
        if getattr(args, level, False):
            return level
    return "all"


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "version":
        print(json.dumps({
            "language_name": LANGUAGE_NAME,
            "compiler_version": COMPILER_VERSION,
            "language_edition": LANGUAGE_EDITION,
            "construction_registry_version": CONSTRUCTION_REGISTRY_VERSION,
            "hast_contract_version": HAST_VERSION,
            "ir_version": IR_VERSION,
            "artifact_format_version": ARTIFACT_FORMAT_VERSION,
            "ir_reference_version": IR_REFERENCE_VERSION,
            "runtime_backend_version": RUNTIME_BACKEND_VERSION,
        }, ensure_ascii=False, sort_keys=True))
        return 0

    source = _read_source(args.file)
    if args.command == "explain":
        obj = api.explain(source, level=_explain_level(args))
        print(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if not obj["diagnostics"] else 1

    if args.command == "check":
        result = api.check(source)
        _print_diagnostics(result, args.json)
        if args.json and result.valid:
            print(json.dumps({"valid": True}, ensure_ascii=False, sort_keys=True))
        return 0 if result.valid else 1

    if args.command == "compile":
        result = api.compile_source(source)
        _print_diagnostics(result, args.json)
        if not result.valid or result.artifact is None:
            return 1
        target = args.output or _default_artifact_path(args.file)
        if target is None:
            # stdin compilation has no implicit filesystem destination; emit canonical artifact bytes.
            sys.stdout.buffer.write(result.artifact)
            if not result.artifact.endswith(b"\n"):
                sys.stdout.buffer.write(b"\n")
        else:
            out = Path(target)
            out.write_bytes(result.artifact)
            summary = {"valid": True, "artifact": str(out), "bytes": len(result.artifact)}
            print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
        return 0

    if args.command == "run":
        result = api.run_source(source)
        _print_diagnostics(result.compilation, args.json)
        if not result.compilation.valid or result.outcome is None:
            return 1
        observable = backend_observable(result.outcome)
        print(json.dumps(observable, ensure_ascii=False, indent=2 if args.json else None, sort_keys=True))
        if observable.get("tooling_status") in {"ResourceExhausted", "InternalFailure"}:
            # Tooling/runtime infrastructure status, not a Marak language Error.
            return 70
        if observable["outcome"] == "Normal":
            return 0
        if observable["outcome"] == "Error":
            # Tooling exit code only; the Core language has no process-exit value.
            return 2
        return 3

    raise AssertionError(args.command)


_main_impl = main
def main(argv: list[str] | None = None) -> int:
    """Public CLI exception firewall.

    Tracebacks are developer diagnostics, never Marak language semantics.  The
    public CLI therefore emits a stable tooling classification for unexpected
    host failures.
    """
    try:
        return _main_impl(argv)
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as exc:
        payload = {
            "tooling_status": "InternalFailure",
            "code": "TOOL_INTERNAL_FAILURE",
            "host_exception_type": type(exc).__name__,
        }
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True), file=sys.stderr)
        return 70


if __name__ == "__main__":
    raise SystemExit(main())
