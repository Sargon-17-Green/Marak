from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping

from compiler.source.source_map import OriginalSpan


class Severity(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass(frozen=True, slots=True)
class Diagnostic:
    code: str
    severity: Severity
    phase: str
    message_en: str
    message_he: str
    source_span: OriginalSpan | None = None
    normalized_span: tuple[int, int] | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        def point(p):
            return {"file": p.file, "char_offset": p.char_offset, "byte_offset": p.byte_offset,
                    "line": p.line, "column": p.column}
        span = None
        if self.source_span is not None:
            span = {"start": point(self.source_span.start), "end": point(self.source_span.end)}
        return {
            "code": self.code,
            "severity": self.severity.value,
            "phase": self.phase,
            "message_en": self.message_en,
            "message_he": self.message_he,
            "source_span": span,
            "normalized_span": list(self.normalized_span) if self.normalized_span else None,
            "metadata": dict(self.metadata),
        }
