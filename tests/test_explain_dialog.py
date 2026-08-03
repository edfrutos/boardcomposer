"""Tests for Ayuda → Explicar candidata dialog (IDE-0007)."""

from PySide6.QtWidgets import QApplication, QDialogButtonBox, QMainWindow, QPushButton

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


def test_explain_solution_dialog_copy_updates_status_bar(qapp):
    del qapp
    window = QMainWindow()
    dialog = ExplainSolutionDialog("body", language="es", parent=window)
    box = dialog.findChild(QDialogButtonBox)
    assert box is not None
    copy = next(button for button in box.buttons() if button.text() == "Copiar")
    copy.click()
    assert "portapapeles" in window.statusBar().currentMessage().lower()


def test_explain_solution_dialog_marks_ok_primary(qapp):
    del qapp
    dialog = ExplainSolutionDialog("notes", language="en")
    box = dialog.findChild(QDialogButtonBox)
    assert box is not None
    ok = box.button(QDialogButtonBox.StandardButton.Ok)
    assert ok is not None
    assert ok.objectName() == "primaryButton"


def test_explain_solution_dialog_copy_has_tip(qapp):
    del qapp
    dialog = ExplainSolutionDialog("body", language="es")
    box = dialog.findChild(QDialogButtonBox)
    assert box is not None
    copy = next(button for button in box.buttons() if button.text() == "Copiar")
    tip = (copy.toolTip() or "").lower()
    assert "portapapeles" in tip
    assert copy.statusTip() == copy.toolTip()
    assert copy.minimumHeight() >= 36


def test_explain_solution_dialog_custom_heading(qapp):
    from PySide6.QtWidgets import QLabel

    del qapp
    dialog = ExplainSolutionDialog(
        "body",
        language="es",
        heading="Soluciones desactualizadas: aviso",
    )
    label = dialog.findChild(QLabel, "explainSolutionHeading")
    assert label is not None
    assert "desactualizadas" in label.text().lower()
