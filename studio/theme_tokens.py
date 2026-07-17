"""Design tokens for BoardComposer Studio (Industrial madera)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class ThemeTokens:
    """Color and typography tokens for one appearance mode."""

    window: str
    base: str
    alternate: str
    panel: str
    text: str
    muted: str
    border: str
    accent: str
    accent_hover: str
    accent_text: str
    danger: str
    tooltip: str
    scroll: str
    scroll_handle: str
    font_ui: str
    font_brand: str


LIGHT = ThemeTokens(
    # Warm oak / parchment neutrals (tinted, never pure gray/white/black)
    window="#f3ebe1",
    base="#faf6f0",
    alternate="#ebe1d4",
    panel="#e8ddd0",
    text="#2c241c",
    muted="#6b5c4d",
    border="#c9b8a4",
    # Tool amber accent ≤10% of chrome
    accent="#c47a1a",
    accent_hover="#a86512",
    accent_text="#fff8f0",
    danger="#b42318",
    tooltip="#2c241c",
    scroll="#e8ddd0",
    scroll_handle="#b59f88",
    font_ui="Source Sans 3",
    # Bundled Archivo static TTF reports this family name to Qt.
    font_brand="Archivo SemiBold",
)

DARK = ThemeTokens(
    # Night workshop: warm slate / charcoal with wood undertone
    window="#1f1b17",
    base="#2a241f",
    alternate="#342c25",
    panel="#342c25",
    text="#ebe1d4",
    muted="#a89480",
    border="#4a3f34",
    accent="#d4922a",
    accent_hover="#e0a44a",
    accent_text="#1a1410",
    danger="#f04438",
    tooltip="#ebe1d4",
    scroll="#2a241f",
    scroll_handle="#6b5c4d",
    font_ui="Source Sans 3",
    font_brand="Archivo SemiBold",
)

TOKENS_BY_NAME: Mapping[str, ThemeTokens] = {
    "light": LIGHT,
    "dark": DARK,
}


def tokens_for(theme: str) -> ThemeTokens | None:
    """Return tokens for `light`/`dark`, or None for `system`/unknown."""
    return TOKENS_BY_NAME.get(theme)
