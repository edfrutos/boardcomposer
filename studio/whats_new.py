"""Helpers for Studio documentation links and changelog “what's new”."""

from __future__ import annotations

from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
_GENERIC_FALLBACK = ["Consulta CHANGELOG.md para el detalle completo de la versión."]


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


def _is_placeholder_bullet(text: str) -> bool:
    """True for empty-cycle markers like ``_(ciclo post-… — vacío al corte)_``."""
    stripped = text.strip()
    if not stripped:
        return True
    if "vacío al corte" in stripped.lower() or "vacio al corte" in stripped.lower():
        return True
    return stripped.startswith("_(") and stripped.endswith(")_")


def _is_added_heading(stripped: str) -> bool:
    lower = stripped.lower()
    return lower.startswith("### añadido") or lower.startswith("### added")


def _is_changed_heading(stripped: str) -> bool:
    lower = stripped.lower()
    return lower.startswith("### cambiado") or lower.startswith("### changed")


def _collect_section_bullets(
    lines: list[str],
    *,
    heading_match,
    include_changed: bool,
    max_items: int,
) -> tuple[str, list[str]]:
    """Collect bullets under the first matching ``##`` section."""
    title = ""
    bullets: list[str] = []
    in_section = False
    in_wanted = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## "):
            heading = stripped[3:].strip()
            if in_section:
                break
            if heading_match(heading):
                title = heading
                in_section = True
                in_wanted = False
            continue
        if not in_section:
            continue
        if stripped.startswith("### "):
            if _is_added_heading(stripped):
                in_wanted = True
            elif include_changed and _is_changed_heading(stripped):
                in_wanted = True
            else:
                in_wanted = False
            continue
        if in_wanted and stripped.startswith("- "):
            item = stripped[2:].strip()
            if _is_placeholder_bullet(item):
                continue
            bullets.append(item)
            if len(bullets) >= max_items:
                break

    return title, bullets


def load_whats_new(
    *,
    changelog_path: Path | None = None,
    max_items: int = 12,
) -> tuple[str, list[str]]:
    """Return ``(section_title, bullet_lines)`` for Ayuda → Novedades.

    Prefers Unreleased **Añadido** (ignoring empty-cycle placeholders). When
    Unreleased has nothing useful, falls back to the latest released section
    (Añadido, then Cambiado) so the dialog stays useful mid-cycle.
    """
    path = changelog_path or documentation_paths()["changelog"]
    if not path.is_file():
        return ("BoardComposer Studio", ["No hay notas de versión disponibles."])

    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return ("BoardComposer Studio", ["No se pudo leer CHANGELOG.md."])

    lines = text.splitlines()

    title, bullets = _collect_section_bullets(
        lines,
        heading_match=lambda h: h.lower().startswith("unreleased"),
        include_changed=False,
        max_items=max_items,
    )
    if bullets:
        return title or "Unreleased", bullets

    title, bullets = _collect_section_bullets(
        lines,
        heading_match=lambda h: not h.lower().startswith("unreleased"),
        include_changed=True,
        max_items=max_items,
    )
    if bullets:
        return title or "BoardComposer Studio", bullets

    return title or "Unreleased", list(_GENERIC_FALLBACK)
