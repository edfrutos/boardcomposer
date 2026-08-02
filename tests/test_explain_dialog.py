"""Tests for Ayuda → Explicar candidata dialog (IDE-0007)."""

from PySide6.QtWidgets import QApplication, QDialogButtonBox, QPushButton

from studio.dialogs.help_dialogs import ExplainSolutionDialog


def test_explain_solution_dialog_copy_writes_clipboard(qapp):
    del qapp
    text = "Fortalezas\n+ compacta"
    dialog = ExplainSolutionDialog(text, language="es")
    box = dialog.findChild(QDialogButtonBox)
    assert box is not None
    copy = next(
        (
            button
            for button in box.buttons()
            if isinstance(button, QPushButton) and button.text() == "Copiar"
        ),
        None,
    )
    assert copy is not None
    copy.click()
    assert QApplication.clipboard().text() == text


def test_explain_solution_dialog_marks_ok_primary(qapp):
    del qapp
    dialog = ExplainSolutionDialog("notes", language="en")
    box = dialog.findChild(QDialogButtonBox)
    assert box is not None
    ok = box.button(QDialogButtonBox.StandardButton.Ok)
    assert ok is not None
    assert ok.objectName() == "primaryButton"
