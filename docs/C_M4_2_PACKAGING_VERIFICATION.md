# C M4.2 Packaging Verification

Final relocation was performed at an arbitrary directory while the original canonical source path was renamed out of existence.

Results:

- relocated full suite: **256/256 pytest + 126 subtests PASS**;
- relocated targeted resource/bootstrap suite: **14/14 PASS**;
- two fixed-epoch independent wheel builds: byte-identical;
- wheel: `marak-0.4.2a1-py3-none-any.whl`;
- wheel SHA-256: `46baf626f9e48878d3b37bc3e54937e98f0599c815fbf84facf2c5bbca6fb812`;
- clean virtual-environment installation: PASS;
- installed CLI `marak version/check/compile/run/explain`: PASS;
- installed tiny RM execution: Normal, facts `גד=0`, `עזר=0`;
- wheel contains MIT LICENSE and console entry point metadata.

The canonical source root contains no stale inner handoff manifest/checksum ledger, old wheel, embedded handoff input/evidence payloads, build directory or environment-specific absolute path dependency. Canonical example artifacts remain intentionally because tests verify them byte-for-byte.
