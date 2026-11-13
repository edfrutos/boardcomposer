"""Single package version for Studio UI (Welcome / About).

Source of truth is ``pyproject.toml`` at the repo root (or the bundled macOS
``Contents/Info.plist`` ``CFBundleShortVersionString`` when running inside a
frozen ``.app`` bundle). Installed package metadata is only a fallback when
the TOML file is missing.
"""

from __future__ import annotations

import plistlib
import re
import sys
import tomllib
from importlib import metadata
from pathlib import Path


def _default_root() -> Path:
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        return Path(meipass)
    return Path(__file__).resolve().parents[1]


_REPO_ROOT = _default_root()
_VERSION_RE = re.compile(
    r'^version\s*=\s*["\']([^"\']+)["\']\s*$',
    re.MULTILINE,
)


def _read_bundle_info_plist_version() -> str | None:
    if not getattr(sys, "frozen", False):
        return None
    candidates: list[Path] = []
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        candidates.append(Path(meipass).parent / "Info.plist")
    executable = getattr(sys, "executable", None)
    if executable:
        candidates.append(Path(executable).resolve().parents[1] / "Info.plist")
    for info_plist in candidates:
        if not info_plist.is_file():
            continue
        try:
            data = plistlib.loads(info_plist.read_bytes())
        except Exception:
            continue
        short = data.get("CFBundleShortVersionString")
        if isinstance(short, str) and short.strip():
            return short.strip()
    return None


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
    if pyproject_path is None:
        bundle_version = _read_bundle_info_plist_version()
        if bundle_version is not None:
            return bundle_version
    path = (
        pyproject_path if pyproject_path is not None else _REPO_ROOT / "pyproject.toml"
    )
    return _read_pyproject_version(path) or _read_installed_version() or "0.0.0+unknown"


# Resolved once at import for Welcome / About.
STUDIO_VERSION = read_package_version()
