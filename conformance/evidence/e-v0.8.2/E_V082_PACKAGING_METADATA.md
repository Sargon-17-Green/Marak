# Packaging and Metadata Smoke

- C M4.2 relocation: original source path hidden; full 256 pytest + 126 subtests PASS.
- Clean wheel-only virtual environment: installed local `marak-0.4.2a1` wheel.
- Installed CLI: `marak version`, `check`, `compile`, `run`, `explain` PASS.
- Two independent `pip wheel --no-deps --no-build-isolation` builds under fixed `SOURCE_DATE_EPOCH=1700000000`: byte-identical SHA-256 `31d6e63555586af635ef4dfe507d84a944624da445e410473e5b39a4e1d3a118`.
- Wheel metadata: Name `marak`, Version `0.4.2a1`, console script `marak`.
- Canonical source license: MIT.
