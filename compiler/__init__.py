"""Compiler implementation package. Language semantics live in the spec, not here."""
from .api import check, explain, lex, normalize, parse
from .version import ARTIFACT_FORMAT_VERSION, COMPILER_VERSION, IR_REFERENCE_VERSION, IR_VERSION, LANGUAGE_EDITION

__all__ = [
    "normalize", "lex", "parse", "check", "explain",
    "COMPILER_VERSION", "LANGUAGE_EDITION", "IR_VERSION", "IR_REFERENCE_VERSION", "ARTIFACT_FORMAT_VERSION",
]
