"""Minimal UI language catalog for Studio (SCR-006)."""

from __future__ import annotations

VALID_LANGUAGES = ("es", "en")
DEFAULT_LANGUAGE = "es"

_STRINGS: dict[str, dict[str, str]] = {
    "es": {
        "language.es": "Español",
        "language.en": "English",
        "units.mm": "Milímetros (mm)",
        "units.cm": "Centímetros (cm)",
        "units.in": "Pulgadas (in)",
        "prefs.title": "Preferencias",
        "prefs.general": "General",
        "prefs.workspace": "Workspace",
        "prefs.algorithms": "Algoritmos",
        "prefs.export": "Exportación",
        "prefs.language": "Idioma:",
        "prefs.theme": "Tema:",
        "prefs.units": "Unidades:",
        "prefs.show_grid": "Mostrar cuadrícula",
        "prefs.grid_size": "Tamaño de cuadrícula:",
        "prefs.strategy": "Estrategia:",
        "prefs.export_format": "Formato por defecto:",
        "welcome.tagline": (
            "Optimiza el corte de tableros. Crea un proyecto, abre uno reciente "
            "o importa piezas para empezar."
        ),
        "welcome.recent": "Proyectos recientes",
        "welcome.new": "Nuevo proyecto",
        "welcome.open": "Abrir proyecto…",
        "welcome.import": "Importar piezas (CSV/Excel)…",
        "welcome.demo": "Proyecto de ejemplo",
        "welcome.preferences": "Preferencias…",
        "welcome.empty_recent": "Sin proyectos recientes",
    },
    "en": {
        "language.es": "Spanish",
        "language.en": "English",
        "units.mm": "Millimetres (mm)",
        "units.cm": "Centimetres (cm)",
        "units.in": "Inches (in)",
        "prefs.title": "Preferences",
        "prefs.general": "General",
        "prefs.workspace": "Workspace",
        "prefs.algorithms": "Algorithms",
        "prefs.export": "Export",
        "prefs.language": "Language:",
        "prefs.theme": "Theme:",
        "prefs.units": "Units:",
        "prefs.show_grid": "Show grid",
        "prefs.grid_size": "Grid size:",
        "prefs.strategy": "Strategy:",
        "prefs.export_format": "Default format:",
        "welcome.tagline": (
            "Optimise panel cutting. Create a project, open a recent one, "
            "or import pieces to get started."
        ),
        "welcome.recent": "Recent projects",
        "welcome.new": "New project",
        "welcome.open": "Open project…",
        "welcome.import": "Import pieces (CSV/Excel)…",
        "welcome.demo": "Sample project",
        "welcome.preferences": "Preferences…",
        "welcome.empty_recent": "No recent projects",
    },
}


def normalize_language(language: str) -> str:
    return language if language in VALID_LANGUAGES else DEFAULT_LANGUAGE


def tr(key: str, language: str = DEFAULT_LANGUAGE) -> str:
    """Translate `key` for the selected language, falling back to Spanish."""
    lang = normalize_language(language)
    return _STRINGS.get(lang, _STRINGS[DEFAULT_LANGUAGE]).get(
        key, _STRINGS[DEFAULT_LANGUAGE].get(key, key)
    )
