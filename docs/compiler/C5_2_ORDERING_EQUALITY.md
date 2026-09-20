# C5.2 Ordering and Equality

C5.2 adds only the accepted typed propositions and metadata. It does not create generic equality or generic comparison.

Natural strict ordering is represented by `NaturalGT` over two independently Natural operands, uses exact arbitrary-size integer comparison, and remains a proposition rather than a Boolean Value. No less-than, LE, GE, mixed Natural/Index comparison, or alternate alias was added. The inverse operand order expresses the opposite strict relation.

Symbol equality is domain-specific and identity-based. Both operands must independently resolve to the same declared Symbol domain; cross-domain comparison is an InvalidProgram. Same visible labels do not imply equality.

Symbol order is declarative adjacency metadata validated as a complete chain. No order is inferred from declaration order, source names, external labels, or numeric serials. The compiler preserves the relation through HAST/IR/artifact metadata for later consumers such as C5.3 without implementing Collection sorting/traversal in this tranche.
