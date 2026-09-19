from __future__ import annotations

from compiler.parse.forest import ParseNode
from compiler.resolve.a10_constraints import find_a10_constraint_issues
from compiler.resolve.a11_constraints import find_a11_constraint_issues
from compiler.resolve.a12_constraints import find_a12_constraint_issues


def find_current_constraint_issues(root: ParseNode):
    """Aggregate only spec-grounded resolver constraints for the current frontier."""
    return find_a10_constraint_issues(root) + find_a11_constraint_issues(root) + find_a12_constraint_issues(root)


__all__ = ["find_current_constraint_issues"]
