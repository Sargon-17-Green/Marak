from __future__ import annotations

from dataclasses import dataclass

from compiler.normalize.code import NormalizationResult
from compiler.source.source_map import OriginalSpan


@dataclass(frozen=True, slots=True)
class WordToken:
    index: int
    text: str
    normalized_start: int
    normalized_end: int
    original: OriginalSpan


def lex_words(normalized: NormalizationResult) -> tuple[WordToken, ...]:
    """Return orthographic word spans; a word is not assumed to be a semantic token."""
    text = normalized.text
    out: list[WordToken] = []
    i = 0
    while i < len(text):
        if text[i] == " ":
            i += 1
            continue
        start = i
        while i < len(text) and text[i] != " ":
            i += 1
        end = i
        out.append(WordToken(
            index=len(out),
            text=text[start:end],
            normalized_start=start,
            normalized_end=end,
            original=normalized.source_map.span(start, end),
        ))
    return tuple(out)
