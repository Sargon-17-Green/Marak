from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, TypeAlias

from compiler.source.unicode_policy import HEBREW_LETTER_SET


class SpecStatus(str, Enum):
    NORMATIVE = "normative"
    PROPOSED = "proposed"
    OPEN = "open"
    REJECTED = "rejected"


class ConstructionKind(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    CONSTRAINT = "constraint"


@dataclass(frozen=True, slots=True)
class WordTerminal:
    """Exact normalized orthographic word.

    This is deliberately exact. No prefix stripping, edit distance, regex, or
    probabilistic matching is performed by the parser.
    """

    text: str

    def __post_init__(self) -> None:
        if not self.text or " " in self.text:
            raise ValueError("WordTerminal requires exactly one normalized word")
        if any(ch not in HEBREW_LETTER_SET for ch in self.text):
            raise ValueError("WordTerminal must contain only the 27 admitted Hebrew letters")


@dataclass(frozen=True, slots=True)
class NameTerminal:
    """One-word open-class name licensed only by an explicit grammatical name slot.

    A bare word never becomes an identifier merely because this terminal exists.
    Reserved-word filtering is intentionally absent: A8 reopened that convention.
    """

    role: str = "CoreName"

    def __post_init__(self) -> None:
        if not self.role:
            raise ValueError("NameTerminal role must be non-empty")


@dataclass(frozen=True, slots=True)
class MorphTerminal:
    """A terminal licensed by an admitted morphology analysis."""

    lemma: str | None = None
    features: tuple[tuple[str, str], ...] = ()
    rule_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.lemma is None and not self.features and not self.rule_ids:
            raise ValueError("MorphTerminal must constrain lemma, features, or rule_ids")
        feature_keys = [k for k, _ in self.features]
        if len(feature_keys) != len(set(feature_keys)):
            raise ValueError("duplicate morphology feature key")
        if len(self.rule_ids) != len(set(self.rule_ids)):
            raise ValueError("duplicate morphology rule id")




@dataclass(frozen=True, slots=True)
class NumeralTerminal:
    """Versioned multi-word canonical numeral lexicon terminal.

    The parser preserves every lexical boundary licensed by the named lexicon;
    it never commits to a longest match merely because one exists.
    """

    lexicon_id: str

    def __post_init__(self) -> None:
        if not self.lexicon_id:
            raise ValueError("NumeralTerminal lexicon_id must be non-empty")


@dataclass(frozen=True, slots=True)
class CountedLabelTerminal:
    """A15 finite-Symbol visible-label metadata field.

    Starting at the count, this consumes one admitted direct Natural, the
    exact words והמלים הן, and exactly that many normalized Hebrew words.
    It creates declaration metadata only; it never creates a Text Value.
    """

    lexicon_id: str

    def __post_init__(self) -> None:
        if not self.lexicon_id:
            raise ValueError("CountedLabelTerminal lexicon_id must be non-empty")


@dataclass(frozen=True, slots=True)
class Nonterminal:
    name: str

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("nonterminal name must be non-empty")


GrammarSymbol: TypeAlias = WordTerminal | NameTerminal | MorphTerminal | NumeralTerminal | CountedLabelTerminal | Nonterminal


@dataclass(frozen=True, slots=True)
class ConstructionDeclaration:
    construction_id: str
    kind: ConstructionKind
    status: SpecStatus
    spec_ids: tuple[str, ...]
    summary: str

    def __post_init__(self) -> None:
        if not self.construction_id:
            raise ValueError("construction id must be non-empty")
        if not self.spec_ids:
            raise ValueError("construction declaration requires at least one spec id")
        if len(self.spec_ids) != len(set(self.spec_ids)):
            raise ValueError("duplicate spec id in construction declaration")


@dataclass(frozen=True, slots=True)
class Production:
    production_id: str
    construction_id: str
    lhs: str
    rhs: tuple[GrammarSymbol, ...]
    semantic_id: str
    root: bool = False

    def __post_init__(self) -> None:
        if not self.production_id or not self.construction_id or not self.lhs or not self.semantic_id:
            raise ValueError("production identifiers and lhs must be non-empty")


class SemanticReadiness(str, Enum):
    READY = "ready"
    BLOCKED_ON_SPEC = "blocked_on_spec"


@dataclass(frozen=True, slots=True)
class ConstructionSemanticGate:
    construction_id: str
    status: SemanticReadiness
    reason: str
    dependencies: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.construction_id or not self.reason:
            raise ValueError("semantic gate requires construction_id and reason")


@dataclass(frozen=True, slots=True)
class ConstructionRegistry:
    language_edition: str
    registry_version: str
    declarations: tuple[ConstructionDeclaration, ...] = ()
    productions: tuple[Production, ...] = ()
    source_snapshot: str | None = None
    semantic_gates: tuple[ConstructionSemanticGate, ...] = ()

    def __post_init__(self) -> None:
        decl_ids = [d.construction_id for d in self.declarations]
        if len(decl_ids) != len(set(decl_ids)):
            raise ValueError("construction IDs must be unique")
        prod_ids = [p.production_id for p in self.productions]
        if len(prod_ids) != len(set(prod_ids)):
            raise ValueError("production IDs must be unique")
        known = set(decl_ids)
        gate_ids = [g.construction_id for g in self.semantic_gates]
        if len(gate_ids) != len(set(gate_ids)):
            raise ValueError("semantic gate construction IDs must be unique")
        unknown_gates = set(gate_ids) - known
        if unknown_gates:
            raise ValueError(f"semantic gates reference undeclared constructions: {sorted(unknown_gates)}")
        for p in self.productions:
            if p.construction_id not in known:
                raise ValueError(f"production {p.production_id} references undeclared construction")
            decl = self.declaration(p.construction_id)
            if decl.kind is not ConstructionKind.POSITIVE:
                raise ValueError(f"production {p.production_id} belongs to non-positive construction")
        roots = [p for p in self.admitted_productions if p.root]
        for p in roots:
            if not p.rhs and p.lhs == "":
                raise ValueError("invalid root production")

    def declaration(self, construction_id: str) -> ConstructionDeclaration:
        for d in self.declarations:
            if d.construction_id == construction_id:
                return d
        raise KeyError(construction_id)

    @property
    def admitted_productions(self) -> tuple[Production, ...]:
        """Only NORMATIVE positive constructions can reach the production parser."""
        admitted = [
            p for p in self.productions
            if self.declaration(p.construction_id).status is SpecStatus.NORMATIVE
        ]
        return tuple(sorted(admitted, key=lambda p: p.production_id))

    @property
    def admitted_root_productions(self) -> tuple[Production, ...]:
        return tuple(p for p in self.admitted_productions if p.root)

    def productions_for(self, lhs: str) -> tuple[Production, ...]:
        return tuple(p for p in self.admitted_productions if p.lhs == lhs)

    def semantic_gate(self, construction_id: str) -> ConstructionSemanticGate | None:
        for gate in self.semantic_gates:
            if gate.construction_id == construction_id:
                return gate
        return None

    def to_dict(self) -> dict[str, object]:
        def symbol(s: GrammarSymbol) -> dict[str, object]:
            if isinstance(s, WordTerminal):
                return {"kind": "word", "text": s.text}
            if isinstance(s, NameTerminal):
                return {"kind": "name", "role": s.role}
            if isinstance(s, MorphTerminal):
                return {
                    "kind": "morph",
                    "lemma": s.lemma,
                    "features": dict(s.features),
                    "rule_ids": list(s.rule_ids),
                }
            if isinstance(s, NumeralTerminal):
                return {"kind": "numeral", "lexicon_id": s.lexicon_id}
            if isinstance(s, CountedLabelTerminal):
                return {"kind": "counted_label", "lexicon_id": s.lexicon_id}
            return {"kind": "nonterminal", "name": s.name}

        out: dict[str, object] = {
            "registry_version": self.registry_version,
            "language_edition": self.language_edition,
            "source_snapshot": self.source_snapshot,
            "declarations": [
                {
                    "construction_id": d.construction_id,
                    "kind": d.kind.value,
                    "status": d.status.value,
                    "spec_ids": list(d.spec_ids),
                    "summary": d.summary,
                }
                for d in sorted(self.declarations, key=lambda d: d.construction_id)
            ],
            "productions": [
                {
                    "production_id": p.production_id,
                    "construction_id": p.construction_id,
                    "lhs": p.lhs,
                    "rhs": [symbol(s) for s in p.rhs],
                    "semantic_id": p.semantic_id,
                    "root": p.root,
                    "admitted": p in self.admitted_productions,
                }
                for p in sorted(self.productions, key=lambda p: p.production_id)
            ],
        }
        if self.semantic_gates:
            out["semantic_gates"] = [
                {
                    "construction_id": g.construction_id,
                    "status": g.status.value,
                    "reason": g.reason,
                    "dependencies": list(g.dependencies),
                }
                for g in sorted(self.semantic_gates, key=lambda g: g.construction_id)
            ]
        return out


def registry_from_parts(
    *,
    language_edition: str,
    registry_version: str,
    declarations: Iterable[ConstructionDeclaration],
    productions: Iterable[Production],
    source_snapshot: str | None = None,
    semantic_gates: Iterable[ConstructionSemanticGate] = (),
) -> ConstructionRegistry:
    """Small explicit builder used by tests/tooling; it performs no inference."""
    return ConstructionRegistry(
        language_edition=language_edition,
        registry_version=registry_version,
        declarations=tuple(declarations),
        productions=tuple(productions),
        source_snapshot=source_snapshot,
        semantic_gates=tuple(semantic_gates),
    )


__all__ = [
    "SpecStatus",
    "ConstructionKind",
    "WordTerminal",
    "NameTerminal",
    "MorphTerminal",
    "NumeralTerminal",
    "CountedLabelTerminal",
    "Nonterminal",
    "GrammarSymbol",
    "ConstructionDeclaration",
    "Production",
    "ConstructionRegistry",
    "SemanticReadiness",
    "ConstructionSemanticGate",
    "registry_from_parts",
]
