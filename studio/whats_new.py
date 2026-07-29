"""Helpers for Studio documentation links and changelog “what's new”."""

from __future__ import annotations

from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]


def repo_root() -> Path:
    """Return the BoardComposer repository root (parent of `studio/`)."""
    return _REPO_ROOT


def documentation_paths() -> dict[str, Path]:
    """Known local documentation entry points."""
    root = repo_root()
    return {
        "user_guide": root / "docs" / "user" / "GUIA-RAPIDA.md",
        "docs_index": root / "docs" / "README.md",
        "readme": root / "README.md",
        "masterplan": root / "docs" / "masterplan" / "INDEX.md",
        "changelog": root / "CHANGELOG.md",
        "design": root / "docs" / "DESIGN.md",
    }


def load_whats_new(
    *,
    changelog_path: Path | None = None,
    max_items: int = 12,
) -> tuple[str, list[str]]:
    """Return `(section_title, bullet_lines)` from CHANGELOG Unreleased.

    Falls back to a short built-in note if the file is missing or empty.
    """
    path = changelog_path or documentation_paths()["changelog"]
    if not path.is_file():
        return ("BoardComposer Studio", ["No hay notas de versión disponibles."])

    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return ("BoardComposer Studio", ["No se pudo leer CHANGELOG.md."])

    lines = text.splitlines()
    title = "Unreleased"
    bullets: list[str] = []
    in_unreleased = False
    in_added = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## "):
            heading = stripped[3:].strip()
            if in_unreleased:
                break
            if heading.lower().startswith("unreleased"):
                title = heading
                in_unreleased = True
                in_added = False
            continue
        if not in_unreleased:
            continue
        if stripped.startswith("### "):
            in_added = stripped.lower().startswith(
                "### añadido"
            ) or stripped.lower().startswith("### added")
            continue
        if in_added and stripped.startswith("- "):
            bullets.append(stripped[2:].strip())
            if len(bullets) >= max_items:
                break

    if not bullets:
        bullets = ["Consulta CHANGELOG.md para el detalle completo de la versión."]
    return title, bullets
