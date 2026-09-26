"""Copy visible Inspector text (IDE-0057)."""

from PySide6.QtWidgets import QApplication

from tests.test_copy_selection_id import _window


def test_copy_inspector_shortcut_and_text(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    assert "Ctrl+Alt+I" in window._actions["copy_inspector"].shortcut().toString()
    window.refresh_inspector_for_piece("A")
    clipboard = QApplication.clipboard()
    assert clipboard is not None
    clipboard.clear()
    window._actions["copy_inspector"].trigger()
    copied = clipboard.text()
    assert "A" in copied
    assert "200" in copied
    assert window.statusBar().currentMessage() == window._tr("status.inspector_copied")
    assert window._actions["copy_inspector"].isEnabled()


def test_copy_inspector_disabled_when_empty(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.inspector.setPlainText(" \n ")
    clipboard = QApplication.clipboard()
    assert clipboard is not None
    clipboard.setText("keep-me")
    assert not window._actions["copy_inspector"].isEnabled()
    tip = window._actions["copy_inspector"].statusTip()
    assert "Ctrl+Alt+I" in tip
    assert window._tr("status.nothing_to_copy_inspector") in tip
    window._copy_inspector()
    assert clipboard.text() == "keep-me"
    assert window.statusBar().currentMessage() == window._tr(
        "status.nothing_to_copy_inspector"
    )
