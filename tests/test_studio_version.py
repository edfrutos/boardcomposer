"""Tests for the single Studio / package version source."""

from pathlib import Path

import tomllib

from studio.version import STUDIO_VERSION, read_package_version
from studio.welcome_screen import STUDIO_VERSION as WELCOME_STUDIO_VERSION
from studio.whats_new import repo_root


def test_studio_version_matches_pyproject():
    pyproject = repo_root() / "pyproject.toml"
    data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    assert data["project"]["version"] == STUDIO_VERSION
    assert WELCOME_STUDIO_VERSION == STUDIO_VERSION


def test_read_package_version_from_explicit_pyproject(tmp_path: Path):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        '[project]\nname = "boardcomposer"\nversion = "9.9.9.dev1"\n',
        encoding="utf-8",
    )
    assert read_package_version(pyproject) == "9.9.9.dev1"


def test_read_package_version_falls_back_when_pyproject_missing(tmp_path: Path):
    missing = tmp_path / "no-pyproject.toml"
    version = read_package_version(missing)
    assert isinstance(version, str)
    assert version  # installed metadata or unknown sentinel
    assert version != "9.9.9.dev1"
