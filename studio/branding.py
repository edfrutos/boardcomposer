"""Application branding assets for BoardComposer Studio."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from PySide6.QtGui import QIcon

_ASSETS_DIR = Path(__file__).resolve().parent / "assets"
APP_ICON_ICNS_PATH = _ASSETS_DIR / "AppIcon.icns"
APP_ICON_PATH = _ASSETS_DIR / "app_icon.jpg"


@lru_cache(maxsize=1)
def app_icon() -> QIcon:
    """Return the BoardComposer Studio application icon."""
    if APP_ICON_ICNS_PATH.is_file():
        icon = QIcon(str(APP_ICON_ICNS_PATH))
        if not icon.isNull():
            return icon
    if not APP_ICON_PATH.is_file():
        return QIcon()
    return QIcon(str(APP_ICON_PATH))
