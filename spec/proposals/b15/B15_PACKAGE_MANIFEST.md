# B15 Package Manifest

Baseline:
- A16 HEAD: `bb7b5da71e34eeaab4dfe2a735f1025ae87c1ec0`
- B14 ancestor: `3c2c1d1ea4afda7365e912b161735112d63e9ac3`
- B13 ancestor: `3c47a57debd381c2b4e41d00d12c792ae43debe8`
- A15 ancestor: `2ae820803250b0753834eff7275c9409426bd0ad`
- canonical main at opening: `621a656c25b7667640cc61a1d1a6ddef95db474d`

Branch:
`workstream-b/b15-a16-semantic-remediation`

Scope:
Only `spec/proposals/b15/` is changed by B15.
A16 was restored byte-identical after its own test runner rewrote its generated result file.

Required review outputs are present, together with:
- independent B15 semantic reference model;
- 29-test independent B15 suite;
- unchanged regression logs;
- conceptual C implementation requirements because all B15 semantic gates are green.

No production compiler/parser, frozen A13/B12 file, or Megillah candidate is modified.

Draft PR: https://github.com/Sargon-17-Green/Marak/pull/9
