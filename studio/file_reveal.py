"""Open or reveal local files in the system file manager."""

from __future__ import annotations

from pathlib import Path


def open_local_path(path: Path | str) -> bool:
    """Open a file or folder with the OS default application."""
    from PySide6.QtCore import QUrl
    from PySide6.QtGui import QDesktopServices

    target = Path(path).expanduser().resolve()
    if not target.exists():
        return False
    return QDesktopServices.openUrl(QUrl.fromLocalFile(str(target)))


def reveal_in_file_manager(path: Path | str) -> bool:
    """Reveal ``path`` by opening its parent folder in the file manager."""
    target = Path(path).expanduser().resolve()
    folder = target if target.is_dir() else target.parent
    if not folder.is_dir():
        return False
    return open_local_path(folder)
