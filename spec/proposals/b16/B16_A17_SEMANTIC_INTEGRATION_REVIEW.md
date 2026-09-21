# B16 — A17 Semantic Integration Review

## Baseline identity

- canonical main: `0f269e53ea55b185628e1bc12e2be85426144a1f`;
- A17 reviewed HEAD: `50155cbf86c1cdc1111dde45464e7a9a1605f9df`;
- compiler package version: `0.5.5a1`;
- `pyproject.toml` Git blob: `c16ccd59c924ec90d74b3b79a55cd122f9c84ed0`;
- construction registry version: `c5.5-a15-b13.1`;
- registry Git blob: `c4a174b1cb3bc265773f3d0bdc1a99037749d5d8`;
- registry source snapshot: `C5.4+A15 Program Input Roles+B13 external binding+B15 domain-flow production integration`.

The B16 branch was created directly from the exact baseline commit. There is therefore no local
working-tree delta in the baseline establishment.

## Semantic verdict

A17 is coherent with B13/B15 without any new domain.

Both the year profile and the A17 general `מעלה` profile resolve to the same
`BidirectionalIndex` semantic values. Surface-profile identity is syntactic provenance only.
It may be retained in source/HAST tooling metadata, but it is not part of the runtime Value,
domain contract, invocation contract, state identity, output provenance, or semantic artifact identity.

Cross-profile flow is therefore admitted whenever the resolved expression and carrier both have
the exact domain `BidirectionalIndex`. A restriction based on year/general provenance would be a
new unit/refinement system and is neither required by B13 nor justified by A17 evidence.

## Operation boundary

Accepted as language-level exposure of existing B13 structure:
- generic Index literal/origin construction;
- strict Index order;
- total one-step `succ` and `pred`;
- generic typed carriers for program input, state, roles, output and immediate result.

Not accepted as new source primitives:
- direct `distance(i,j)`;
- Index equality;
- Natural→Index or Index→Natural conversion;
- signed arithmetic closure;
- arbitrary user-defined profile/unit nouns.

No contradiction or missing B13 semantic law was found.
