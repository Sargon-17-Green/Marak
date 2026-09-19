from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OriginalPoint:
    file: str
    char_offset: int
    byte_offset: int
    line: int
    column: int


@dataclass(frozen=True, slots=True)
class OriginalSpan:
    start: OriginalPoint
    end: OriginalPoint


@dataclass(frozen=True, slots=True)
class MapUnit:
    normalized_offset: int
    normalized_char: str
    original: OriginalSpan


@dataclass(frozen=True, slots=True)
class SourceMap:
    file: str
    raw_text: str
    normalized_text: str
    units: tuple[MapUnit, ...]

    def __post_init__(self) -> None:
        if len(self.normalized_text) != len(self.units):
            raise ValueError("one source-map unit is required per normalized code point")
        for i, unit in enumerate(self.units):
            if unit.normalized_offset != i or unit.normalized_char != self.normalized_text[i]:
                raise ValueError("source-map units are not canonical")

    def point(self, normalized_offset: int) -> OriginalPoint:
        """Map a normalized boundary/character offset to an original source point."""
        if not 0 <= normalized_offset <= len(self.units):
            raise IndexError("normalized offset outside source map")
        points = _point_table(self.raw_text, self.file)
        if not self.units:
            return points[0] if normalized_offset == 0 and not self.raw_text else points[-1]
        if normalized_offset == len(self.units):
            # A zero-width diagnostic at normalized EOF points at physical EOF,
            # even when the source ends in transparent decoration. Non-empty
            # spans still end at the last normalized unit's provenance.
            return points[-1]
        return self.units[normalized_offset].original.start

    def span(self, normalized_start: int, normalized_end: int) -> OriginalSpan:
        if not 0 <= normalized_start <= normalized_end <= len(self.units):
            raise IndexError("normalized span outside source map")
        if normalized_start == normalized_end:
            p = self.point(normalized_start)
            return OriginalSpan(p, p)
        return OriginalSpan(
            self.units[normalized_start].original.start,
            self.units[normalized_end - 1].original.end,
        )


def _point_table(text: str, file: str) -> tuple[OriginalPoint, ...]:
    """Return source positions for every code-point boundary, CRLF counted once."""
    points: list[OriginalPoint] = []
    byte = 0
    line = 1
    col = 1
    previous_cr = False
    for i, ch in enumerate(text):
        points.append(OriginalPoint(file, i, byte, line, col))
        byte += len(ch.encode("utf-8"))
        if ch == "\r":
            line += 1
            col = 1
            previous_cr = True
        elif ch == "\n":
            if not previous_cr:
                line += 1
                col = 1
            previous_cr = False
        else:
            col += 1
            previous_cr = False
    points.append(OriginalPoint(file, len(text), byte, line, col))
    return tuple(points)


__all__ = ["OriginalPoint", "OriginalSpan", "MapUnit", "SourceMap", "_point_table"]
