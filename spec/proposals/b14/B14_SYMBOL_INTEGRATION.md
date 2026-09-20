# B14 Symbol Integration

A15 domain/member/reference forms map uniquely to B13 `Symbol(DomainId,MemberId)`. The value is atomic.
Source identity is not a runtime value and the visible label is not Text.

The canonical external label is the normalized counted Hebrew-word sequence. Raw punctuation, maqaf,
Markdown, niqqud, layout, and erased characters are not observable. Label metadata cannot be indexed,
concatenated, or inspected by a Marak program.

Symbol equality remains DomainId+MemberId equality, never label equality. A presentation label is not
a serialization key.

Validation:
- zero label-word count: InvalidProgram;
- too few words or malformed counted declaration: InvalidProgram;
- duplicate member identity: InvalidProgram;
- repeated visible label does not merge values;
- same visible label in another domain is legal and distinct.

A Symbol-domain order is usable only when adjacency facts form one acyclic nonforking chain containing
every member once. Its transitive closure is the admitted strict total relation. Declaration and
spelling order are irrelevant; no comparator Value exists.

Integration remains blocked because A15 lacks Symbol state/roles/output/immediate-result forms.
The Megillah also explicitly compares selected names in book traversal (original around 1493–1502
and 1782–1796), while A13 equality is numeric-only. Membership is not a standalone Symbol-equality
proposition.
