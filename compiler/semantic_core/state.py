from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True, order=True)
class StateReferentId:
    """Opaque identity of a source-resolved state-bearing referent.

    This is not a memory address, variable slot, frame coordinate, or current
    value.  Resolver policy decides when two source uses denote the same ID.
    """

    key: str

    def __post_init__(self) -> None:
        if not self.key:
            raise ValueError("state referent id must be non-empty")


@dataclass(frozen=True, slots=True, order=True)
class StateAspect:
    """Named semantic aspect whose current fact can be singular."""

    key: str

    def __post_init__(self) -> None:
        if not self.key:
            raise ValueError("state aspect must be non-empty")


NUMBER_ASPECT = StateAspect("number")


@dataclass(frozen=True, slots=True)
class CurrentObservation:
    referent: StateReferentId
    aspect: StateAspect
    value: int

    def __post_init__(self) -> None:
        _require_exact_integer(self.value)


@dataclass(frozen=True, slots=True)
class MissingCurrentFact:
    referent: StateReferentId
    aspect: StateAspect


CurrentQueryResult = CurrentObservation | MissingCurrentFact


@dataclass(frozen=True, slots=True)
class _Fact:
    referent: StateReferentId
    aspect: StateAspect
    value: int

    def __post_init__(self) -> None:
        _require_exact_integer(self.value)


@dataclass(frozen=True, slots=True)
class SemanticSnapshot:
    """Immutable observational model of B7 current facts.

    The tuple representation is an implementation choice.  Its order and any
    physical sharing are deliberately unobservable.
    """

    _facts: tuple[_Fact, ...] = ()

    def __post_init__(self) -> None:
        seen: set[tuple[StateReferentId, StateAspect]] = set()
        for fact in self._facts:
            key = (fact.referent, fact.aspect)
            if key in seen:
                raise ValueError("duplicate singular-current fact")
            seen.add(key)
        canonical = tuple(sorted(self._facts, key=lambda f: (f.referent.key, f.aspect.key)))
        if canonical != self._facts:
            object.__setattr__(self, "_facts", canonical)

    def current_of(self, referent: StateReferentId, aspect: StateAspect) -> CurrentQueryResult:
        for fact in self._facts:
            if fact.referent == referent and fact.aspect == aspect:
                return CurrentObservation(referent, aspect, fact.value)
        return MissingCurrentFact(referent, aspect)

    def establish(self, referent: StateReferentId, aspect: StateAspect, value: int) -> "SemanticSnapshot":
        """Establish a previously absent current fact.

        Re-establishing an already-current singular aspect is rejected by this
        model API so that callers must choose deliberately between establish and
        replace.  This ValueError is an implementation contract, not a language
        exception or observable runtime semantics.
        """
        _require_exact_integer(value)
        if isinstance(self.current_of(referent, aspect), CurrentObservation):
            raise ValueError("current fact already established; use replace")
        return SemanticSnapshot(self._facts + (_Fact(referent, aspect, value),))

    def replace(self, referent: StateReferentId, aspect: StateAspect, value: int) -> "SemanticSnapshot":
        """Replace exactly one current fact while preserving all unrelated facts."""
        _require_exact_integer(value)
        found = False
        out: list[_Fact] = []
        for fact in self._facts:
            if fact.referent == referent and fact.aspect == aspect:
                out.append(_Fact(referent, aspect, value))
                found = True
            else:
                out.append(fact)
        if not found:
            raise ValueError("cannot replace an absent current fact")
        return SemanticSnapshot(tuple(out))

    def observable_facts(self) -> tuple[CurrentObservation, ...]:
        return tuple(CurrentObservation(f.referent, f.aspect, f.value) for f in self._facts)


def _require_exact_integer(value: int) -> None:
    # bool is a subclass of int in Python; accepting it would accidentally
    # collapse B8's proposition/data distinction into a host-language quirk.
    if type(value) is not int:
        raise TypeError("current numeric facts require exact integers; bool is not an integer datum here")


__all__ = [
    "StateReferentId", "StateAspect", "NUMBER_ASPECT", "CurrentObservation",
    "MissingCurrentFact", "CurrentQueryResult", "SemanticSnapshot",
]
