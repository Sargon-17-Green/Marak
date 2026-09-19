# C M4.2 Metadata Cleanup

E-FIND-027 identified stale M4 handoff metadata embedded inside the M4.1 source tree.

The canonical source root now:

- identifies the language/project as **Marak**;
- uses compiler version `0.4.2-alpha.1`;
- uses distribution name `marak` and CLI command `marak`;
- carries an MIT `LICENSE`;
- contains no `HANDOFF_MANIFEST.json` or `SHA256SUMS.txt` generated for an older handoff;
- contains no embedded handoff `inputs/` or `evidence/`, old wheel, or build directory; committed canonical example artifacts remain because they are verified regression fixtures;
- contains no absolute workspace-specific dependency in canonical code/tests/current docs;
- places historical milestone documentation under `docs/archive/milestones/` rather than presenting it as current metadata.

Final handoff manifests/checksums are generated outside the canonical `source/` tree.
