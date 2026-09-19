# C M4 — Relocation Verification

The repository was copied to a fresh arbitrary directory and the original source path was temporarily moved away so it did not exist during the verification run.

The relocated copy successfully ran:

- the full pytest suite;
- source-tree CLI `version`, `check`, `compile`, `run`, `explain` on the A13 tiny RM;
- wheel build without network/build isolation;
- clean virtual-environment installation;
- installed CLI `version`, `check`, `compile`, `run`, `explain`.

The initial M3 hard-coded fixture path defect was removed before M4 work by moving the fixture into repository-relative `tests/fixtures` lookup. Static audit rejects `/mnt/data`, `/home/oai` and Windows-drive literals in compiler/tests/tools source, except the audit pattern itself.

A final relocation rerun is recorded in `evidence/C_M4_RELOCATION_VERIFICATION_FINAL.log`.

## Final signed run

After the final M4 code/tests/examples/version state, relocation was repeated with the original working-tree path absent. The relocated tree passed **230 tests + 126 subtests**, built the same wheel hash as the source tree, installed into a clean virtual environment, and passed installed `version/check/compile/run/explain` on the A13 tiny RM.

Final wheel SHA-256: `266189bb6e478baec313c320b3fefd32e98c78b3f686556effe89905833dd320`.

The static absolute-path scan reports one literal `/home/oai` occurrence only inside `tests/test_m4_static_audit.py`, where that literal is itself the forbidden pattern being searched for. It is not dereferenced or used as a fixture/source location.
