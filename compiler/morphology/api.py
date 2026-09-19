from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Mapping, Protocol

from compiler.lex.words import WordToken


@dataclass(frozen=True, slots=True)
class MorphAnalysis:
    rule_id: str
    lemma: str
    features: tuple[tuple[str, str], ...] = ()


class MorphologyRule(Protocol):
    rule_id: str
    def analyze(self, token: WordToken) -> Iterable[MorphAnalysis]: ...


class MorphologyEngine:
    """Spec-driven candidate enumerator. It never ranks or chooses a winner."""
    def __init__(self, rules: Iterable[MorphologyRule] = ()) -> None:
        self._rules = tuple(rules)

    def analyze(self, tokens: Iterable[WordToken]) -> Mapping[int, tuple[MorphAnalysis, ...]]:
        result: dict[int, tuple[MorphAnalysis, ...]] = {}
        for token in tokens:
            candidates: list[MorphAnalysis] = []
            seen: set[MorphAnalysis] = set()
            for rule in self._rules:
                for candidate in rule.analyze(token):
                    if candidate.rule_id != rule.rule_id:
                        raise ValueError("morphology rule emitted an analysis with a different rule_id")
                    if candidate not in seen:
                        seen.add(candidate)
                        candidates.append(candidate)
            result[token.index] = tuple(candidates)
        return result
