# C5.2 BidirectionalIndex

C5.2 implements the accepted A15/A16 BidirectionalIndex source family as a semantic domain separate from Natural. The admitted literal family contains the zero origin, one/two year before/after forms, and productive N>=3 year-count forms using the accepted feminine count morphology. Historical year notation is not introduced as an alias.

Index places, named roles, outputs, and immediate-result reads are statically typed as `BidirectionalIndex`. There is no expected-type rescue and no Natural-to-Index conversion. A Natural expression inside an Index successor/predecessor form is not admitted.

Successor and predecessor are total domain operations. The crossing laws are tested explicitly: `pred(AfterZero(1))=Zero`, `pred(Zero)=BeforeZero(1)`, `succ(BeforeZero(1))=Zero`, and `succ(Zero)=AfterZero(1)`, plus farther magnitudes. Internal arithmetic is implementation detail; no signed Integer or `++` surface exists.

The HAST, canonical IR, artifact validator, HAST reference evaluator, IR reference evaluator, and portable backend all represent/execute the same Index semantics. Malformed internal Index states and non-Index operation operands are rejected at the artifact trust boundary before execution.
