# A15 — B13 Semantic Mapping

Every admitted A15 construction below has an explicit B13 target. There is no syntax-only row.

| Surface ID | Exact form/profile | B13 semantic object/operation | Errors / invalidity | Observable result |
|---|---|---|---|---|
| A15.SYM.DOMAIN | `תהי משפחת שמות ושמה DOMAIN` | finite Symbol domain declaration | duplicate/unresolved source identity | domain/member identities become resolvable; no runtime Text |
| A15.SYM.MEMBER | `יהי ... שם ושמו MEMBER ... מספר המלים ... LABEL_WORD_COUNT והמלים הן LABEL_WORDS` | declare `Symbol(DomainId,MemberId)` + canonical label metadata | bad count, unknown domain, malformed label metadata | atomic Symbol has declared canonical external label |
| A15.SYM.REF | `השם אשר במשפחת השמות אשר שמה DOMAIN שמו MEMBER` | Symbol Value reference | unknown/ambiguous domain/member | exact atomic Symbol Value |
| A15.SYM.ORDER.ADJ | `במשפט משפחת ... יהיה SYMBOL_A מיד לפני SYMBOL_B` | source declaration of admitted strict total Symbol relation | incomplete/cyclic/forked relation invalid | order relation metadata, no comparator Value |
| A15.IDX.ZERO | `שנת אין` | `ZeroIndex` | outside typed year/index slot invalid | origin index Value |
| A15.IDX.BEFORE | `N שנים לפני שנת אין` with one/two special agreement | `BeforeZero(N)` | N not positive / malformed count | before-origin index Value |
| A15.IDX.AFTER | `N שנים אחרי שנת אין` with one/two special agreement | `AfterZero(N)` | N not positive / malformed count | after-origin index Value |
| A15.COLL.EMPTY | typed `ספר ... אשר אין בו ELEMENT_HEAD` | empty `Collection<D>` | unsupported/ambiguous kind | immutable empty collection |
| A15.COLL.APPEND | `BOOK_KIND אשר בו כל אשר ב BOOK_VALUE כסדרו ואחר כלם ITEM_VALUE` | `append(C,x)` | domain mismatch | new immutable collection; old C unchanged |
| A15.COLL.COUNT | `מספר הדברים אשר בתוך BOOK_VALUE` | `count(C)` | non-collection operand | Natural count |
| A15.COLL.MEMBER | `ITEM_VALUE כתוב בתוך BOOK_VALUE` | equality membership | domain mismatch | proposition, not Boolean Value |
| A15.COLL.FIRST | `ELEMENT_HEAD אשר בראש BOOK_VALUE` | `select(C,1)` | empty -> `COLLECTION_POSITION_ERROR` | first element |
| A15.COLL.LAST | `ELEMENT_HEAD האחרון אשר בתוך BOOK_VALUE` | `select(C,count(C))` | empty -> `COLLECTION_POSITION_ERROR` | last element |
| A15.COLL.ORDINAL | `ELEMENT_HEAD אשר מספרו בסדר BOOK_VALUE הוא POSITION_VALUE` | `select(C,k)` | k outside 1..count -> `COLLECTION_POSITION_ERROR` | kth ordered element |
| A15.COLL.SUCCESSOR | ordinal selection at `k+1` | `select(C,k+1)` | last/outside -> `COLLECTION_POSITION_ERROR` | following occurrence, not following equal Value |
| A15.COLL.ORDER.NAT | `הספר הערוך מן BOOK_VALUE מן המעט אל הרב` | `order(C,NaturalLT)` | wrong element domain | pure sorted permutation |
| A15.COLL.ORDER.SYM | `הספר הערוך ... כמשפט משפחת ...` | `order(C,R_domain)` | missing/invalid strict total relation | pure sorted permutation |
| A15.COLL.ORDER.LEX | `... מראש כל ספר ועד אחריתו ...` | `order(C,Lex(R))` | wrong nested kind/relation | pure lexicographic permutation |
| A15.ORD.GT | `NUMBER_VALUE_A רב מן NUMBER_VALUE_B` | `GT(A,B)` | non-Natural operands invalid | strict proposition |
| A15.NUM.DIRECT | admitted productive numeral phrase | `LiteralNat(source) -> Natural(n)` | malformed/noncanonical phrase | exact Natural n |
| A15.REP.LITERAL | `פעם אחת A`; `שתי פעמים A`; `REPEAT_COUNT פעמים A` | `RepeatExactly(N,A)` | count morphology/body invalid | A performed exact N times subject to B13 outcomes |
| A15.REP.DYNAMIC | `פעמים COUNT_AS_NUMBER ATOMIC_ACTION`, where initial `המספר` is inflected as `כמספר` | `RepeatExactly(eval-once N,A)` | malformed/double numeric head or count domain/error follows B13 | eval count once, then exact recurrence |
| A15.INPUT.DECL | `יהי למלאכה הזאת דבר ושמו ROLE ... יעמד DOMAIN_HEAD תחת ...` | Program Input Role declaration | duplicate role/domain declaration invalid | invocation contract metadata |
| A15.INPUT.REF | typed `... אשר עומד תחת הדבר אשר למלאכה הזאת שמו ROLE` | immutable Program Input association lookup | missing/extra/duplicate/domain mismatch invalid invocation | exact bound Value by semantic role identity |

## Derived/non-surfaced B13 relations

B13 LE/GE remain meta-semantic derived relations; A15 adds no direct surface. B13 generic BidirectionalIndex remains broader than A15's year-specific source family. B13 arbitrary comparator acts remain absent. B13 deeper nested collections remain semantically possible but do not receive new A15 syntax beyond the one nested level justified by the Megillah.
