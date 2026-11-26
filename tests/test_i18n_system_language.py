"""First-run UI language follows the system preferred languages (MAS 4.3)."""

from __future__ import annotations

import pytest

from studio.i18n import (
    FALLBACK_SYSTEM_LANGUAGE,
    VALID_LANGUAGES,
    system_default_language,
)


@pytest.mark.parametrize(
    ("ui_languages", "expected"),
    [
        (["es-ES"], "es"),
        (["es_419"], "es"),
        (["en-US", "es-ES"], "en"),
        (["fr-FR", "es-ES"], "es"),
        (["fr-FR", "de-DE"], FALLBACK_SYSTEM_LANGUAGE),
        (["EN-gb"], "en"),
        ([], FALLBACK_SYSTEM_LANGUAGE),
    ],
)
def test_system_default_language_uses_first_supported_tag(
    ui_languages: list[str], expected: str
) -> None:
    assert system_default_language(ui_languages) == expected


def test_fallback_is_english() -> None:
    assert FALLBACK_SYSTEM_LANGUAGE == "en"


def test_system_default_language_reads_qt_locale() -> None:
    pytest.importorskip("PySide6.QtCore")
    assert system_default_language() in VALID_LANGUAGES
