from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True, order=True)
class SymbolId:
    """Legacy implementation identity retained for historical C tests."""
    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("SymbolId must be non-negative")


@dataclass(frozen=True, slots=True, order=True)
class PlaceId:
    serial: int
    spelling: str

    def __post_init__(self) -> None:
        if self.serial <= 0 or not self.spelling:
            raise ValueError("PlaceId requires positive serial and spelling")


@dataclass(frozen=True, slots=True, order=True)
class ActId:
    serial: int
    spelling: str

    def __post_init__(self) -> None:
        if self.serial <= 0 or not self.spelling:
            raise ValueError("ActId requires positive serial and spelling")


@dataclass(frozen=True, slots=True, order=True)
class RoleId:
    serial: int
    owner: ActId
    spelling: str

    def __post_init__(self) -> None:
        if self.serial <= 0 or not self.spelling:
            raise ValueError("RoleId requires positive serial, owner and spelling")


@dataclass(frozen=True, slots=True, order=True)
class OccurrenceId:
    serial: int

    def __post_init__(self) -> None:
        if self.serial <= 0:
            raise ValueError("OccurrenceId must be positive")


__all__ = ["SymbolId", "PlaceId", "ActId", "RoleId", "OccurrenceId"]
