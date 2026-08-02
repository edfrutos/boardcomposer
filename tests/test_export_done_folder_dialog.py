"""Export-done dialog uses folder-aware copy when the path is a directory."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QMessageBox

from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


class _FakeBox:
    """Minimal QMessageBox stand-in that records labels and auto-closes."""

    instances: list["_FakeBox"] = []
    Icon = QMessageBox.Icon
    StandardButton = QMessageBox.StandardButton
    ButtonRole = QMessageBox.ButtonRole

    def __init__(self, parent=None):
        del parent
        self._texts: list[str] = []
        self._buttons: list[object] = []
        self._clicked: object | None = None
        type(self).instances.append(self)

    def setIcon(self, icon) -> None:
        del icon

    def setWindowTitle(self, title: str) -> None:
        del title

    def setText(self, text: str) -> None:
        self._texts.append(text)

    def addButton(self, *args, **kwargs):
        del kwargs
        label = args[0] if args else ""
        button = object()
        if isinstance(label, QMessageBox.StandardButton):
            return button
        self._buttons.append(str(label))
        if self._clicked is None:
            self._clicked = button
        return button

    def exec(self) -> int:
        return 0

    def clickedButton(self):
        return self._clicked


def _window(tmp_path) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    return MainWindow(services)


def test_offer_open_exported_path_folder_copy(qapp, tmp_path, monkeypatch):
    del qapp
    window = _window(tmp_path)
    folder = tmp_path / "backup-stamp"
    folder.mkdir()
    opened: list[Path] = []

    _FakeBox.instances.clear()
    monkeypatch.setattr("studio.main_window.QMessageBox", _FakeBox)
    monkeypatch.setattr(
        "studio.file_reveal.open_local_path",
        lambda path: opened.append(Path(path)) or True,
    )

    window._offer_open_exported_path(folder)

    assert len(_FakeBox.instances) == 1
    box = _FakeBox.instances[0]
    assert any("Carpeta creada" in text for text in box._texts)
    assert "Abrir carpeta" in box._buttons
    assert "Mostrar en carpeta" not in box._buttons
    assert opened == [folder]


def test_offer_open_exported_path_file_keeps_reveal(qapp, tmp_path, monkeypatch):
    del qapp
    window = _window(tmp_path)
    target = tmp_path / "out.svg"
    target.write_text("<svg/>", encoding="utf-8")

    _FakeBox.instances.clear()
    monkeypatch.setattr("studio.main_window.QMessageBox", _FakeBox)

    window._offer_open_exported_path(target)

    assert len(_FakeBox.instances) == 1
    box = _FakeBox.instances[0]
    assert any("Archivo guardado" in text for text in box._texts)
    assert "Abrir archivo" in box._buttons
    assert "Mostrar en carpeta" in box._buttons
