# C5.2 Surface Pipeline

C5.2 lands the accepted post-M2 surface in the same production path used by Core: normalization -> lex -> Earley parse -> exact resolver -> static validation -> typed HAST -> canonical IR -> artifact serialization/verification -> reference/backend execution -> language observation.

The construction registry is `c5.2-a15-a16.1`. The public language-edition string intentionally remains `core-0.1-integration-candidate-a13-b12` until Master assigns a post-M2 edition identifier. This explicitly separates accepted language design from the compiler-registry implementation candidate.

The parser gained a counted-label terminal because the A15 Symbol label boundary is value-dependent. That terminal implements the normative count boundary directly; it is not precedence, greedy recovery, or Text syntax. Negative counted-label failures now produce stable parse expectations rather than leaking a host `AttributeError`.

The resolver creates explicit Symbol domain/member identities and exact static domains for typed places/roles/results. No runtime source-name lookup is used. Existing named role association was generalized to carry independently typed values while preserving named, non-positional association semantics.

No C5.2 production implements Collection operations, Program Input source grammar, general dynamic counted recurrence, or Megillah-specific syntax. The existing frozen A13 recurrence forms remain inherited unchanged.
