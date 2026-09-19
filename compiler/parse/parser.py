from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Mapping, Sequence

from compiler.lex.words import WordToken
from compiler.morphology.api import MorphAnalysis
from compiler.parse.forest import ParseAlternative, ParseElement, ParseForest, ParseLeaf, ParseNode
from compiler.parse.grammar import (
    ConstructionRegistry,
    MorphTerminal,
    NameTerminal,
    NumeralTerminal,
    Nonterminal,
    Production,
    WordTerminal,
)
from compiler.source.source_map import OriginalSpan, SourceMap
from compiler.parse.numeral_lexicons import match_numeral_lexicon


@dataclass(frozen=True, slots=True)
class ParserMetrics:
    token_count: int
    chart_positions: int
    state_keys: int
    derivations: int
    completed_nodes: int
    alternatives: int
    peak_state_keys_at_position: int


@dataclass(frozen=True, slots=True)
class ParseFailure:
    furthest_token: int
    expected: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ParseResult:
    forest: ParseForest
    metrics: ParserMetrics
    failure: ParseFailure | None
    grammar_available: bool


@dataclass(frozen=True, slots=True)
class _StateKey:
    production_id: str
    dot: int
    origin: int


class Parser:
    """Deterministic ambiguity-preserving Earley-style chart parser.

    The engine consumes only NORMATIVE productions from ConstructionRegistry.
    It has no ranking, confidence, nearest-match, recovery, or pruning path.
    Multiple derivations are preserved as distinct parse alternatives.
    """

    def __init__(self, registry: ConstructionRegistry) -> None:
        self.registry = registry
        self._productions = registry.admitted_productions
        self._by_id = {p.production_id: p for p in self._productions}
        by_lhs: dict[str, list[Production]] = {}
        for p in self._productions:
            by_lhs.setdefault(p.lhs, []).append(p)
        self._by_lhs = {k: tuple(sorted(v, key=lambda p: p.production_id)) for k, v in by_lhs.items()}

    def parse(
        self,
        tokens: Sequence[WordToken],
        morphology: Mapping[int, tuple[MorphAnalysis, ...]],
        *,
        source_map: SourceMap | None = None,
        start_lhs: str | None = None,
    ) -> ParseResult:
        n = len(tokens)
        token_words = tuple(t.text for t in tokens)
        start_productions = (
            self.registry.admitted_root_productions
            if start_lhs is None
            else self.registry.productions_for(start_lhs)
        )
        if not start_productions:
            metrics = ParserMetrics(n, n + 1, 0, 0, 0, 0, 0)
            return ParseResult(ParseForest(()), metrics, None, False)

        # chart[position][state-key] = set of partial child tuples.
        chart: list[dict[_StateKey, set[tuple[ParseElement, ...]]]] = [dict() for _ in range(n + 1)]
        agendas: list[deque[tuple[_StateKey, tuple[ParseElement, ...]]]] = [deque() for _ in range(n + 1)]
        completed_nodes: set[ParseNode] = set()

        def add(pos: int, key: _StateKey, derivation: tuple[ParseElement, ...]) -> None:
            bucket = chart[pos].setdefault(key, set())
            if derivation not in bucket:
                bucket.add(derivation)
                agendas[pos].append((key, derivation))

        for p in start_productions:
            add(0, _StateKey(p.production_id, 0, 0), ())

        for pos in range(n + 1):
            while agendas[pos]:
                key, derivation = agendas[pos].popleft()
                prod = self._by_id[key.production_id]
                if key.dot == len(prod.rhs):
                    node = self._make_node(prod, key.origin, pos, derivation, tokens, source_map)
                    completed_nodes.add(node)
                    # Complete every state that was waiting for this lhs at origin.
                    for waiting_key, waiting_derivations in list(chart[key.origin].items()):
                        waiting_prod = self._by_id[waiting_key.production_id]
                        if waiting_key.dot >= len(waiting_prod.rhs):
                            continue
                        symbol = waiting_prod.rhs[waiting_key.dot]
                        if isinstance(symbol, Nonterminal) and symbol.name == prod.lhs:
                            for wd in tuple(waiting_derivations):
                                add(pos, _StateKey(waiting_key.production_id, waiting_key.dot + 1, waiting_key.origin), wd + (node,))
                    continue

                symbol = prod.rhs[key.dot]
                if isinstance(symbol, Nonterminal):
                    # Predict exact admitted productions for this nonterminal.
                    for predicted in self._by_lhs.get(symbol.name, ()):
                        add(pos, _StateKey(predicted.production_id, 0, pos), ())
                    # If a completion is already present at this chart position,
                    # consume it as well. This makes processing order irrelevant.
                    for completed_key, completed_derivations in list(chart[pos].items()):
                        completed_prod = self._by_id[completed_key.production_id]
                        if completed_key.dot != len(completed_prod.rhs) or completed_key.origin != pos:
                            continue
                        if completed_prod.lhs != symbol.name:
                            continue
                        for cd in tuple(completed_derivations):
                            node = self._make_node(completed_prod, pos, pos, cd, tokens, source_map)
                            completed_nodes.add(node)
                            add(pos, _StateKey(prod.production_id, key.dot + 1, key.origin), derivation + (node,))
                    continue

                if pos >= n:
                    continue
                for end_pos, leaf in self._match_terminal(symbol, pos, tokens, token_words, morphology):
                    add(end_pos, _StateKey(prod.production_id, key.dot + 1, key.origin), derivation + (leaf,))

        alternatives: set[ParseAlternative] = set()
        for p in start_productions:
            key = _StateKey(p.production_id, len(p.rhs), 0)
            for derivation in chart[n].get(key, ()):
                root = self._make_node(p, 0, n, derivation, tokens, source_map)
                alternatives.add(ParseAlternative(root=root, semantic_id=p.semantic_id))

        ordered = tuple(sorted(alternatives, key=_alternative_sort_key))
        forest = ParseForest(ordered)
        failure = None if ordered else self._failure(chart, tokens)
        state_keys = sum(len(c) for c in chart)
        derivations = sum(sum(len(ds) for ds in c.values()) for c in chart)
        metrics = ParserMetrics(
            token_count=n,
            chart_positions=n + 1,
            state_keys=state_keys,
            derivations=derivations,
            completed_nodes=len(completed_nodes),
            alternatives=len(ordered),
            peak_state_keys_at_position=max((len(c) for c in chart), default=0),
        )
        return ParseResult(forest, metrics, failure, True)

    def _match_terminal(
        self,
        symbol: WordTerminal | NameTerminal | MorphTerminal | NumeralTerminal,
        pos: int,
        tokens: Sequence[WordToken],
        token_words: tuple[str, ...],
        morphology: Mapping[int, tuple[MorphAnalysis, ...]],
    ) -> tuple[tuple[int, ParseLeaf], ...]:
        token = tokens[pos]
        analyses = morphology.get(token.index, ())
        if isinstance(symbol, WordTerminal):
            if token.text != symbol.text:
                return ()
            return ((pos + 1, ParseLeaf(
                token.index, token.text, token.normalized_start, token.normalized_end, token.original
            )),)

        if isinstance(symbol, NameTerminal):
            # Namehood comes solely from this explicit grammatical slot.
            return ((pos + 1, ParseLeaf(
                token.index, token.text, token.normalized_start, token.normalized_end, token.original,
                terminal_role=symbol.role,
            )),)

        if isinstance(symbol, NumeralTerminal):
            out: list[tuple[int, ParseLeaf]] = []
            for end_pos, value, text in match_numeral_lexicon(symbol.lexicon_id, token_words, pos):
                first = tokens[pos]
                last = tokens[end_pos - 1]
                out.append((end_pos, ParseLeaf(
                    first.index,
                    text,
                    first.normalized_start,
                    last.normalized_end,
                    OriginalSpan(first.original.start, last.original.end),
                    terminal_role=f"Numeral:{symbol.lexicon_id}",
                    numeric_value=value,
                )))
            return tuple(out)

        out: list[tuple[int, ParseLeaf]] = []
        required_features = dict(symbol.features)
        allowed_rules = set(symbol.rule_ids)
        for analysis in analyses:
            if symbol.lemma is not None and analysis.lemma != symbol.lemma:
                continue
            if allowed_rules and analysis.rule_id not in allowed_rules:
                continue
            actual_features = dict(analysis.features)
            if any(actual_features.get(k) != v for k, v in required_features.items()):
                continue
            out.append((pos + 1, ParseLeaf(
                token.index,
                token.text,
                token.normalized_start,
                token.normalized_end,
                token.original,
                morphology_rule_id=analysis.rule_id,
                lemma=analysis.lemma,
                features=analysis.features,
            )))
        return tuple(sorted(out, key=lambda x: (x[1].morphology_rule_id or "", x[1].lemma or "", x[1].features)))

    def _make_node(
        self,
        prod: Production,
        start: int,
        end: int,
        children: tuple[ParseElement, ...],
        tokens: Sequence[WordToken],
        source_map: SourceMap | None,
    ) -> ParseNode:
        normalized_start, normalized_end, original = _span_for_token_range(tokens, start, end, source_map)
        return ParseNode(
            production_id=prod.production_id,
            construction_id=prod.construction_id,
            symbol=prod.lhs,
            token_start=start,
            token_end=end,
            normalized_start=normalized_start,
            normalized_end=normalized_end,
            original=original,
            children=children,
        )

    def _failure(self, chart: Sequence[Mapping[_StateKey, set[tuple[ParseElement, ...]]]], tokens: Sequence[WordToken]) -> ParseFailure:
        furthest = 0
        for i, states in enumerate(chart):
            if states:
                furthest = i
        expected: set[str] = set()
        for key in chart[furthest]:
            prod = self._by_id[key.production_id]
            if key.dot >= len(prod.rhs):
                continue
            symbol = prod.rhs[key.dot]
            if isinstance(symbol, WordTerminal):
                expected.add(f"word:{symbol.text}")
            elif isinstance(symbol, NameTerminal):
                expected.add(f"name:{symbol.role}")
            elif isinstance(symbol, MorphTerminal):
                bits = []
                if symbol.lemma is not None:
                    bits.append(f"lemma={symbol.lemma}")
                bits.extend(f"{k}={v}" for k, v in symbol.features)
                bits.extend(f"rule={r}" for r in symbol.rule_ids)
                expected.add("morph:" + ",".join(bits))
            elif isinstance(symbol, NumeralTerminal):
                expected.add(f"numeral:{symbol.lexicon_id}")
            else:
                expected.add(f"nonterminal:{symbol.name}")
        return ParseFailure(furthest, tuple(sorted(expected)))


def _span_for_token_range(
    tokens: Sequence[WordToken],
    start: int,
    end: int,
    source_map: SourceMap | None,
) -> tuple[int | None, int | None, OriginalSpan | None]:
    if start < end and start < len(tokens):
        first = tokens[start]
        last = tokens[end - 1]
        return first.normalized_start, last.normalized_end, OriginalSpan(first.original.start, last.original.end)
    if not tokens:
        if source_map is not None:
            return 0, 0, source_map.span(0, 0)
        return None, None, None
    if start < len(tokens):
        p = tokens[start].original.start
        return tokens[start].normalized_start, tokens[start].normalized_start, OriginalSpan(p, p)
    p = tokens[-1].original.end
    return tokens[-1].normalized_end, tokens[-1].normalized_end, OriginalSpan(p, p)


def _element_key(x: ParseElement):
    if isinstance(x, ParseLeaf):
        return (
            "leaf", x.token_index, x.text, x.morphology_rule_id or "", x.lemma or "", x.features, x.terminal_role or "", x.numeric_value
        )
    return (
        "node", x.production_id, x.construction_id, x.symbol, x.token_start, x.token_end,
        tuple(_element_key(c) for c in x.children),
    )


def _alternative_sort_key(a: ParseAlternative):
    return (a.semantic_id, _element_key(a.root))


__all__ = ["ParserMetrics", "ParseFailure", "ParseResult", "Parser"]
