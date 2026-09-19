from __future__ import annotations

from dataclasses import dataclass

from compiler.source.source_map import MapUnit, OriginalSpan, SourceMap, _point_table
from compiler.source.text import SourceText
from compiler.source.unicode_policy import (
    DEFAULT_WHITESPACE_POLICY,
    HEBREW_LETTER_SET,
    WhitespacePolicy,
    is_code_whitespace,
)


@dataclass(frozen=True, slots=True)
class DiscardedSpan:
    original: OriginalSpan
    text: str


@dataclass(frozen=True, slots=True)
class NormalizationResult:
    text: str
    source_map: SourceMap
    discarded: tuple[DiscardedSpan, ...]
    whitespace_policy_id: str


def normalize_code(
    source: SourceText | str,
    *,
    file: str = "<memory>",
    whitespace_policy: WhitespacePolicy = DEFAULT_WHITESPACE_POLICY,
) -> NormalizationResult:
    """Normalize CODE mode only.

    No string delimiter is recognized. Core v0.1 has no strings (A-LEX-003), and
    future STRING mode is deliberately not guessed here.
    """
    if isinstance(source, str):
        source = SourceText(source, file)
    raw = source.text
    points = _point_table(raw, source.file)
    out: list[str] = []
    units: list[MapUnit] = []
    discarded: list[DiscardedSpan] = []

    pending_space_start: int | None = None
    pending_space_end: int | None = None
    discard_start: int | None = None

    def flush_discard(end_index: int) -> None:
        nonlocal discard_start
        if discard_start is None:
            return
        discarded.append(DiscardedSpan(
            OriginalSpan(points[discard_start], points[end_index]),
            raw[discard_start:end_index],
        ))
        discard_start = None

    def emit_space() -> None:
        nonlocal pending_space_start, pending_space_end
        if pending_space_start is None or pending_space_end is None:
            return
        # Adjacent normalized whitespace never duplicates: transparent characters
        # cannot split a semantic whitespace run.
        if out and out[-1] == " ":
            prev = units[-1]
            units[-1] = MapUnit(
                prev.normalized_offset,
                " ",
                OriginalSpan(prev.original.start, points[pending_space_end]),
            )
        else:
            idx = len(out)
            out.append(" ")
            units.append(MapUnit(
                idx,
                " ",
                OriginalSpan(points[pending_space_start], points[pending_space_end]),
            ))
        pending_space_start = None
        pending_space_end = None

    for i, ch in enumerate(raw):
        if ch in HEBREW_LETTER_SET:
            flush_discard(i)
            emit_space()
            idx = len(out)
            out.append(ch)
            units.append(MapUnit(idx, ch, OriginalSpan(points[i], points[i + 1])))
            continue
        if is_code_whitespace(ch, whitespace_policy):
            flush_discard(i)
            if pending_space_start is None:
                pending_space_start = i
            pending_space_end = i + 1
            continue
        # Transparent characters disappear. If whitespace is pending, keep the
        # gap attached to that run for useful provenance; otherwise record it.
        if pending_space_start is not None:
            pending_space_end = i + 1
        elif discard_start is None:
            discard_start = i

    flush_discard(len(raw))
    emit_space()
    normalized = "".join(out)
    smap = SourceMap(source.file, raw, normalized, tuple(units))
    return NormalizationResult(normalized, smap, tuple(discarded), whitespace_policy.policy_id)
