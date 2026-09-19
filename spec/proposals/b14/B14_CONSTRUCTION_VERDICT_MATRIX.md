# B14 Construction Verdict Matrix

| A15 construction | Verdict | B13/B12 target | Note |
|---|---|---|---|
| A15.SYM.DOMAIN | EXACT_SEMANTIC_MATCH | finite Symbol domain | declaration only; no Text |
| A15.SYM.MEMBER | SEMANTIC_CLARIFICATION | Symbol member + label metadata | label is presentation metadata |
| A15.SYM.REF | EXACT_SEMANTIC_MATCH | Symbol value | domain-qualified |
| A15.SYM.ORDER.ADJ | SEMANTIC_CLARIFICATION | strict total Symbol order | chain validation static |
| A15.IDX.ZERO | ACCEPTABLE_SURFACE_NARROWING | ZeroIndex | year profile |
| A15.IDX.BEFORE | ACCEPTABLE_SURFACE_NARROWING | BeforeZero(N) | year profile |
| A15.IDX.AFTER | ACCEPTABLE_SURFACE_NARROWING | AfterZero(N) | year profile |
| A15.COLL.EMPTY | EXACT_SEMANTIC_MATCH | empty Collection<D> | homogeneous |
| A15.COLL.APPEND | EXACT_SEMANTIC_MATCH | append(C,x) | pure |
| A15.COLL.COUNT | EXACT_SEMANTIC_MATCH | count(C)→Natural | exact |
| A15.COLL.MEMBER | EXACT_SEMANTIC_MATCH | membership by equality | proposition |
| A15.COLL.FIRST | EXACT_SEMANTIC_MATCH | select(C,1) | empty errors |
| A15.COLL.LAST | EXACT_SEMANTIC_MATCH | select(C,count(C)) | empty errors |
| A15.COLL.ORDINAL | EXACT_SEMANTIC_MATCH | select(C,k) | 1..count |
| A15.COLL.SUCCESSOR | SEMANTIC_CLARIFICATION | select(C,k+1) | derived, not primitive |
| A15.COLL.ORDER.NAT | EXACT_SEMANTIC_MATCH | order(C,NaturalLT) | pure |
| A15.COLL.ORDER.SYM | EXACT_SEMANTIC_MATCH | order(C,R_domain) | explicit order |
| A15.COLL.ORDER.LEX | EXACT_SEMANTIC_MATCH | order(C,Lex(R)) | structural |
| A15.ORD.GT | EXACT_SEMANTIC_MATCH | GT(A,B) Natural | proposition |
| A15.NUM.DIRECT | EXACT_SEMANTIC_MATCH | exact Natural literal | no semantic ceiling |
| A15.REP.LITERAL | EXACT_SEMANTIC_MATCH | RepeatExactly(N,A) | one action |
| A15.REP.DYNAMIC | EXACT_SEMANTIC_MATCH | RepeatExactly(eval-once N,A) | count once |
| A15.INPUT.DECL | EXACT_SEMANTIC_MATCH | Program Input Role contract | pre-invocation |
| A15.INPUT.REF | EXACT_SEMANTIC_MATCH | immutable input association | identity-based |

Counts: EXACT_SEMANTIC_MATCH **18**; ACCEPTABLE_SURFACE_NARROWING **3**;
SEMANTIC_CLARIFICATION **3**; SEMANTIC_MISMATCH **0**; NEEDS_MASTER_CLARIFICATION **0**.

Five missing construction families are recorded separately as SURFACE_GAP findings.
