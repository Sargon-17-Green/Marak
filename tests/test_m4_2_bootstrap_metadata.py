from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_canonical_source_root_has_no_stale_handoff_ledgers_or_generated_payload_dirs():
    assert not (ROOT / "HANDOFF_MANIFEST.json").exists()
    assert not (ROOT / "SHA256SUMS.txt").exists()
    for name in ("evidence", "inputs", "dist", "build"):
        assert not (ROOT / name).exists(), name


def test_bootstrap_metadata_uses_marak_name_cli_and_current_version():
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert 'name = "marak"' in pyproject
    assert 'version = "0.4.2a1"' in pyproject
    assert 'marak = "compiler.cli.main:main"' in pyproject
    assert "0.4.2-alpha.1" in readme
    assert "Public CLI: `marak`" in readme
    assert "0.4.0-alpha.2" not in readme
    assert "0.4.1-alpha.1" not in readme


def test_mit_license_present():
    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert license_text.startswith("MIT License")
    assert "Permission is hereby granted, free of charge" in license_text


def test_no_absolute_workspace_path_in_canonical_code_tests_tools_or_current_docs():
    forbidden = ("/" + "mnt" + "/" + "data" + "/" + "compiler-c" + "/", "/" + "home" + "/" + "oai" + "/")
    roots = [ROOT / "compiler", ROOT / "tests", ROOT / "tools"]
    roots += [p for p in (ROOT / "docs").glob("*.md")]
    for base in roots:
        files = [base] if base.is_file() else list(base.rglob("*.py")) + list(base.rglob("*.md"))
        for path in files:
            text = path.read_text(encoding="utf-8")
            for needle in forbidden:
                # The static-audit tests may name a forbidden string only by constructing it,
                # not by embedding the complete environment path literally.
                assert needle not in text, (path.relative_to(ROOT), needle)


def test_historical_milestone_material_is_explicitly_archived():
    archive = ROOT / "docs/archive/milestones"
    assert archive.is_dir()
    assert (archive / "M4").is_dir()
    assert (archive / "M4_1").is_dir()
