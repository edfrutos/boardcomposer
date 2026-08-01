"""Single package version for Studio UI (Welcome / About).

Source of truth is ``pyproject.toml`` at the repo root. Installed package
metadata is only a fallback when the TOML file is missing (e.g. frozen
install without the source tree).
"""

from __future__ import annotations

import re
import tomllib
from importlib import metadata
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
_VERSION_RE = re.compile(
    r'^version\s*=\s*["\']([^"\']+)["\']\s*$',
    re.MULTILINE,
)


def _read_pyproject_version(path: Path) -> str | None:
    if not path.is_file():
        return None
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        data = tomllib.loads(raw)
    except tomllib.TOMLDecodeError:
        match = _VERSION_RE.search(raw)
        return match.group(1).strip() if match else None
    version = data.get("project", {}).get("version")
    if isinstance(version, str) and version.strip():
        return version.strip()
    return None


def _read_installed_version() -> str | None:
    try:
        return metadata.version("boardcomposer")
    except metadata.PackageNotFoundError:
        return None


def read_package_version(pyproject_path: Path | None = None) -> str:
    """Return BoardComposer version string for UI and docs surfaces."""
    path = (
        pyproject_path if pyproject_path is not None else _REPO_ROOT / "pyproject.toml"
    )
    return _read_pyproject_version(path) or _read_installed_version() or "0.0.0+unknown"


# Resolved once at import for Welcome / About.
STUDIO_VERSION = read_package_version()
