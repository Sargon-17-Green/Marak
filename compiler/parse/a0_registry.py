from __future__ import annotations

from compiler.parse.grammar import (
    ConstructionDeclaration,
    ConstructionKind,
    ConstructionRegistry,
    SpecStatus,
)
# Historical A0 snapshot: its edition string must not follow the current compiler frontier.
A0_LANGUAGE_EDITION = "core-0.1-draft-a0"


# This is a faithful implementation snapshot of A0 statuses, not a grammar guess.
# In particular, A-CLAUSE-001 and A-SEQ-002 are PROPOSED, so they deliberately
# have no productions that the production parser can admit.
A0_REGISTRY = ConstructionRegistry(
    language_edition=A0_LANGUAGE_EDITION,
    registry_version="a0.1",
    source_snapshot="A0_Surface_Language_Handoff",
    declarations=(
        ConstructionDeclaration(
            "A0.ATOMIC_IMPERATIVE_CANDIDATE",
            ConstructionKind.POSITIVE,
            SpecStatus.PROPOSED,
            ("A-CLAUSE-001",),
            "Controlled imperative atomic-action shape; exact admitted morphology/valency remains open.",
        ),
        ConstructionDeclaration(
            "A0.NO_CONSONANTAL_VERB_GUESS",
            ConstructionKind.CONSTRAINT,
            SpecStatus.NORMATIVE,
            ("A-CLAUSE-002",),
            "Consonantal resemblance alone never licenses a verbal parse.",
        ),
        ConstructionDeclaration(
            "A0.BARE_WAW_NOT_SEQUENCE",
            ConstructionKind.NEGATIVE,
            SpecStatus.NORMATIVE,
            ("A-SEQ-001", "NG-A0-002"),
            "Bare prefixed waw is insufficient as a general sequencing/action-boundary operator.",
        ),
        ConstructionDeclaration(
            "A0.EXPLICIT_SEQUENCE_CANDIDATE",
            ConstructionKind.POSITIVE,
            SpecStatus.PROPOSED,
            ("A-SEQ-002",),
            "The surface form ואחרי כן is a sequencing candidate, not yet admitted syntax.",
        ),
        ConstructionDeclaration(
            "A0.MARKDOWN_NOT_COMMENT",
            ConstructionKind.NEGATIVE,
            SpecStatus.NORMATIVE,
            ("NG-A0-004",),
            "Transparent Markdown punctuation cannot create comment semantics.",
        ),
    ),
    productions=(),
)


__all__ = ["A0_REGISTRY"]
