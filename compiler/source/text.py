from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class SourceText:
    text: str
    file: str = "<memory>"

    @classmethod
    def from_file(cls, path: str | Path) -> "SourceText":
        p = Path(path)
        data = p.read_bytes()
        text = data.decode("utf-8", errors="strict")
        return cls(text=text, file=str(p))
