# B16 — A17 Semantic Integration & Megillah Anti-Imitation Review

Status: **B16 A17 SEMANTIC INTEGRATION READY FOR MASTER REVIEW**

Canonical baseline: `0f269e53ea55b185628e1bc12e2be85426144a1f`
A17 reviewed HEAD: `50155cbf86c1cdc1111dde45464e7a9a1605f9df`
Branch: `workstream-b/b16-a17-semantic-integration`

B16 reviews A17 as a semantic integration proposal only. It does not modify A17, production
compiler/runtime, registry, HAST/IR, artifact format, Megillah, or D4.

Core result:
- semantic domain remains exactly `BidirectionalIndex`;
- new semantic domains: **NONE**;
- year/general profiles are source-level linguistic profiles only;
- cross-profile value flow is admitted;
- strict Index order is accepted;
- generic succ/pred are accepted;
- direct Index distance remains algorithmic and has no source primitive;
- Index equality surface is not required;
- Natural↔Index source conversions remain absent;
- signed arithmetic widening: **NONE**.
