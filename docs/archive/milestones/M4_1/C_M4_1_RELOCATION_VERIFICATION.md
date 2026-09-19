# C M4.1 — Relocation / Packaging Verification

The repository was copied to `/mnt/data/marak-c-m4_1-relocated-final-20260919`, then the original C path was renamed away so it did not exist during verification.

Results:
- full pytest: 242/242 + 126 subtests PASS;
- two fixed-epoch wheels: byte-identical;
- SHA-256: `29f82d91ccdb19a15a354cce71f364b1c870f6fed6522647e6d497ed80de2623`;
- clean venv install: PASS;
- installed `version`, `check`, `compile`, `run`, `explain`: PASS;
- tiny RM: Normal, facts `גד=0`, `עזר=0`.
