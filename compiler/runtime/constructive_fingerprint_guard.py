"""Fail-closed, whole-program authorization for opt-in T21 arithmetic fast paths.

An intrinsic's spelling / roles / scratch places are not a proof of its body.
Only the two explicitly audited, complete, exact T21 production programs may
use the shortcut. The digest covers every node in the compiled program,
including act/helper bodies, role bindings, global state and principal steps.

If the program is different, incomplete, unknown or structurally unhashable,
the runtime must execute it normally.  No matching by name is sufficient.
"""
from __future__ import annotations

from dataclasses import fields, is_dataclass
from enum import Enum
from hashlib import sha256


# SHA-256 fingerprints are produced by tools/d4_t21_intrinsic_fingerprints.py
# from the immutable SHA-pinned T21 source and reviewed in a follow-up commit.
# Until the exact fingerprints are pinned, all intrinsics fail closed.
APPROVED_WHOLE_PROGRAM_SHA256: dict[str, frozenset[str]] = {
    "hast": frozenset(),
    "ir": frozenset(),
}


def structural_program_sha256(program: object) -> str:
    """Canonical, non-recursive structural digest of an entire compiled AST/IR.

    Dataclass class identity, all field names and values, container kind/order,
    symbol IDs, source spans, definitions and principal are covered.  Unlike
    repr() or pickle, this does not rely on hash seed or recursion depth.
    Unsupported objects raise TypeError, resulting in a safe slow fallback.
    """
    digest = sha256(b"marak-full-program-intrinsic-guard-v1\0")
    stack: list[object] = [program]

    def atom(kind: bytes, raw: bytes) -> None:
        digest.update(kind)
        digest.update(len(raw).to_bytes(8, "big"))
        digest.update(raw)

    while stack:
        value = stack.pop()
        if value is None:
            atom(b"n", b"")
        elif type(value) is bool:
            atom(b"b", b"1" if value else b"0")
        elif type(value) is int:
            atom(b"i", str(value).encode("ascii"))
        elif type(value) is str:
            atom(b"s", value.encode("utf-8"))
        elif type(value) is bytes:
            atom(b"y", value)
        elif isinstance(value, Enum):
            atom(b"e", (type(value).__module__ + "." + type(value).__qualname__ + ":" + value.name).encode("utf-8"))
        elif is_dataclass(value) and not isinstance(value, type):
            cls = type(value)
            sequence = fields(value)
            atom(b"d", (cls.__module__ + "." + cls.__qualname__).encode("utf-8"))
            atom(b"#", str(len(sequence)).encode("ascii"))
            for f in reversed(sequence):
                stack.append(getattr(value, f.name))
                stack.append(f.name)
        elif type(value) in (tuple, list):
            atom(b"t" if type(value) is tuple else b"l", str(len(value)).encode("ascii"))
            stack.extend(reversed(value))
        elif type(value) is dict:
            # The trusted AST currently has no mapping-valued structural
            # fields. Reject unknown mapping layouts rather than risk
            # order-dependent/ambiguous authorization.
            raise TypeError("mapping-valued compiled program cannot be authorized")
        else:
            raise TypeError(f"unhandled structural node {type(value)!r}")
    return digest.hexdigest()


def approved_canonical_program(program: object, kind: str) -> bool:
    if kind not in APPROVED_WHOLE_PROGRAM_SHA256:
        return False
    allowed = APPROVED_WHOLE_PROGRAM_SHA256[kind]
    if not allowed:
        return False
    try:
        return structural_program_sha256(program) in allowed
    except (TypeError, ValueError, OverflowError, RecursionError, AttributeError):
        return False


__all__ = ["APPROVED_WHOLE_PROGRAM_SHA256", "approved_canonical_program", "structural_program_sha256"]
