from __future__ import annotations

from dataclasses import replace

from compiler.parse.a12_registry import A12_REGISTRY
from compiler.parse.grammar import (
    ConstructionDeclaration,
    ConstructionKind,
    ConstructionRegistry,
    Nonterminal,
    Production,
    SpecStatus,
    WordTerminal,
)

A13_B12_LANGUAGE_EDITION = "core-0.1-integration-candidate-a13-b12"


def W(text: str) -> WordTerminal:
    return WordTerminal(text)

# A13 changes the whole-program category of initialized place introduction.
# Historical A12 stays immutable; current A13 removes the executable/root
# production and introduces it only as a PreparatoryUnit.
_BASE_PRODUCTIONS = tuple(
    replace(p, root=False)
    for p in A12_REGISTRY.productions
    if p.production_id != "A10.PLACE.INTRODUCE"
)

_DECLARATIONS = A12_REGISTRY.declarations + (
    ConstructionDeclaration(
        "A13.CORE_PROGRAM",
        ConstructionKind.POSITIVE,
        SpecStatus.NORMATIVE,
        ("A-CORE-005", "A-CORE-006"),
        "A Core program is preparatory discourse followed by exactly one top-level ועתה transition and one explicit executable sequence.",
    ),
    ConstructionDeclaration(
        "A13.PREPARATION",
        ConstructionKind.POSITIVE,
        SpecStatus.NORMATIVE,
        ("A-CORE-005", "A-STATE-002", "A-ACT-001", "A-ROLE-001", "A-BODY-001"),
        "Initialized place introduction, act introduction, role declaration and act body definition are preparatory units, not top-level executable actions.",
    ),
    ConstructionDeclaration(
        "A13.PRINCIPAL_EXECUTION",
        ConstructionKind.POSITIVE,
        SpecStatus.NORMATIVE,
        ("A-CORE-005", "A-SEQ-001"),
        "ועתה explicitly transitions from preparation to the principal execution; it is not a magic main act.",
    ),
    ConstructionDeclaration(
        "A13.VISIBILITY_LIFETIME",
        ConstructionKind.CONSTRAINT,
        SpecStatus.NORMATIVE,
        ("A-CORE-007", "A-CORE-008", "A-NAME-004", "A-NAME-005", "A-ACT-003", "A-ROLE-004"),
        "Core uses source discourse introduction-before-use with typed identities, no hoisting, and occurrence-local role values.",
    ),
    ConstructionDeclaration(
        "A13.NATURAL_SUBTRACTION_DOMAIN",
        ConstructionKind.CONSTRAINT,
        SpecStatus.NORMATIVE,
        ("A-CALC-002", "A-CALC-003"),
        "Core subtraction B-A is defined only for A<=B; B12 maps failure to ARITHMETIC_DOMAIN_ERROR rather than a signed value.",
    ),
    ConstructionDeclaration(
        "A13.NO_HALT_PRIMITIVE",
        ConstructionKind.NEGATIVE,
        SpecStatus.NORMATIVE,
        ("A-ACT-004", "A-ACT-005"),
        "Normal exhaustion is completion; no Core HALT/exit/main-return construction exists.",
    ),
)

# Reuse the exact A12 surface phrases, but place them into A13 whole-program
# categories.  Source order inside Preparation is discourse dependency order,
# not executable sequencing.
_place_intro_rhs = next(p.rhs for p in A12_REGISTRY.productions if p.production_id == "A10.PLACE.INTRODUCE")

_PRODUCTIONS = _BASE_PRODUCTIONS + (
    Production(
        "A13.PREP.PLACE.INTRODUCE", "A13.PREPARATION", "PreparatoryUnit",
        _place_intro_rhs, "A13.PREP_PLACE_INTRODUCTION",
    ),
    Production(
        "A13.PREP.ACT.INTRODUCE", "A13.PREPARATION", "PreparatoryUnit",
        (Nonterminal("NamedActIdentity"),), "A13.PREP_ACT_INTRODUCTION",
    ),
    Production(
        "A13.PREP.ROLE.DECLARE", "A13.PREPARATION", "PreparatoryUnit",
        (Nonterminal("RoleDeclaration"),), "A13.PREP_ROLE_DECLARATION",
    ),
    Production(
        "A13.PREP.BODY.DEFINE", "A13.PREPARATION", "PreparatoryUnit",
        (Nonterminal("ActBodyDefinition"),), "A13.PREP_BODY_DEFINITION",
    ),
    Production(
        "A13.PREPARATION.ONE", "A13.PREPARATION", "Preparation",
        (Nonterminal("PreparatoryUnit"),), "A13.PREPARATION",
    ),
    Production(
        "A13.PREPARATION.MORE", "A13.PREPARATION", "Preparation",
        (Nonterminal("Preparation"), Nonterminal("PreparatoryUnit")), "A13.PREPARATION",
    ),
    Production(
        "A13.EXEC.UNIT.ATOMIC", "A13.PRINCIPAL_EXECUTION", "ExecutableUnit",
        (Nonterminal("AtomicAction"),), "A13.EXECUTABLE_UNIT",
    ),
    Production(
        "A13.EXEC.UNIT.CONDITIONAL", "A13.PRINCIPAL_EXECUTION", "ExecutableUnit",
        (Nonterminal("ConditionalConsequence"),), "A13.EXECUTABLE_UNIT",
    ),
    Production(
        "A13.EXEC.UNIT.COUNTED", "A13.PRINCIPAL_EXECUTION", "ExecutableUnit",
        (Nonterminal("CountedConsequence"),), "A13.EXECUTABLE_UNIT",
    ),
    Production(
        "A13.EXEC.UNIT.RECURRENCE", "A13.PRINCIPAL_EXECUTION", "ExecutableUnit",
        (Nonterminal("AfterGatedRecurrence"),), "A13.EXECUTABLE_UNIT",
    ),
    Production(
        "A13.EXEC.SEQUENCE.ONE", "A13.PRINCIPAL_EXECUTION", "ExecutableSequence",
        (Nonterminal("ExecutableUnit"),), "A13.EXECUTABLE_SEQUENCE",
    ),
    Production(
        "A13.EXEC.SEQUENCE.MORE", "A13.PRINCIPAL_EXECUTION", "ExecutableSequence",
        (Nonterminal("ExecutableSequence"), W("ואחרי"), W("כן"), Nonterminal("ExecutableUnit")),
        "A13.EXECUTABLE_SEQUENCE",
    ),
    Production(
        "A13.PRINCIPAL", "A13.PRINCIPAL_EXECUTION", "PrincipalExecution",
        (W("ועתה"), Nonterminal("ExecutableSequence")), "A13.PRINCIPAL_EXECUTION",
    ),
    Production(
        "A13.PROGRAM.NO_PREP", "A13.CORE_PROGRAM", "CoreProgram",
        (Nonterminal("PrincipalExecution"),), "A13.CORE_PROGRAM", root=True,
    ),
    Production(
        "A13.PROGRAM.WITH_PREP", "A13.CORE_PROGRAM", "CoreProgram",
        (Nonterminal("Preparation"), Nonterminal("PrincipalExecution")),
        "A13.CORE_PROGRAM", root=True,
    ),
)

A13_B12_REGISTRY = ConstructionRegistry(
    language_edition=A13_B12_LANGUAGE_EDITION,
    registry_version="a13-b12.1",
    source_snapshot="A13_A_Core_v0.1_Integration_Frozen_Candidate+B12_A13_SEMANTIC_INTEGRATION",
    declarations=_DECLARATIONS,
    productions=_PRODUCTIONS,
    semantic_gates=A12_REGISTRY.semantic_gates,
)

__all__ = ["A13_B12_LANGUAGE_EDITION", "A13_B12_REGISTRY"]
